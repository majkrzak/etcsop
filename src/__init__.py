import kopf
from kopf import Labels
from .const import API_GROUP, API_VERSION
from .crds import ConfigShard
from .utils import merge
from .renderers import php, json
from pykube import KubeConfig, HTTPClient, ConfigMap

api = HTTPClient(KubeConfig.from_env())


@kopf.on.create(API_GROUP, API_VERSION, ConfigShard.endpoint)
@kopf.on.update(API_GROUP, API_VERSION, ConfigShard.endpoint)
@kopf.on.delete(API_GROUP, API_VERSION, ConfigShard.endpoint)
def config_shard_handler(reason: str, namespace: str, labels: Labels, **_):
    data = merge(
        [
            shard.data
            for shard in ConfigShard.objects(api).filter(namespace, labels)
            if "deletionTimestamp" not in shard.metadata
        ]
    )

    name = labels["app"]

    config_map = ConfigMap(
        api,
        {
            "metadata": {
                "namespace": namespace,
                "name": name,
                "labels": dict(labels),
            },
            "data": {},
        },
    )

    if not data:
        if config_map.exists():
            config_map.delete()
        return

    if not config_map.exists():
        config_map.create()
    else:
        config_map.reload()

    if reason != "delete":
        kopf.append_owner_reference(
            config_map,
            controller=False,
            block_owner_deletion=False,
        )

    config_map.obj["data"] = {
        "env.json": json(data),
        "env.php": php(data),
    }
    config_map.update()
