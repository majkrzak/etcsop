ETC Shard Operator
==================

About
-----

`etcsop` provides a way to assemble distributed `ConfigShards` into a native `ConfigMap` containing rendered files.
Currently only `json` is supported.

### Input

```yaml
---
apiVersion: etc.s.op/dev
kind: ConfigShard
metadata:
  name: test-shard-1
  labels:
    app: test
data:
  foo:
  - test1
  - test2
  bar:
    bar1: test1
---
apiVersion: etc.s.op/dev
kind: ConfigShard
metadata:
  name: test-shard-2
  labels:
    app: test
data:
  foo:
  - test3
  - test4
  bar:
    bar2: test3
---
apiVersion: etc.s.op/dev
kind: ConfigShard
metadata:
  name: test-shard-3
  labels:
    app: test
data:
  foobar: 123
```

### Output

```
Name:         test
Namespace:    default
Labels:       app=test
Annotations:  <none>

Data
====
env.json:
----
{
  "bar": {
    "bar2": "test3",
    "bar1": "test1"
  },
  "foo": [
    "test3",
    "test4",
    "test1",
    "test2"
  ],
  "foobar": 123
}
```

Installation
------------

```sh
kubectl apply -f https://raw.githubusercontent.com/majkrzak/etcsop/master/etcsop.yaml
```

TODO
---- 

- Implement more sophisticated method of configuring how the shards should be assembled.
- Rewrite Kubernetes integration with something more serious than pykube is.
- Refactor PHP renderer.