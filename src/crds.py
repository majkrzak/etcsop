from .const import API_GROUP, API_VERSION
from pykube.objects import NamespacedAPIObject


class ConfigShard(NamespacedAPIObject):
    version = f"{API_GROUP}/{API_VERSION}"
    endpoint = "configshards"
    kind = "ConfigShard"

    @property
    def data(self) -> dict:
        return dict(self.obj["data"])
