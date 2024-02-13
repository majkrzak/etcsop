from itertools import chain


def merge(objs: []):
    if not objs:
        return None
    if len(objs) == 1:
        return objs[0]
    if all(map(lambda x: isinstance(x, list), objs)):
        return list(chain(*objs))
    if all(map(lambda x: isinstance(x, dict), objs)):
        return {k: merge([obj[k] for obj in objs if k in obj]) for k in chain(*objs)}
    raise ValueError("Unsupported type", objs)
