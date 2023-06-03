import orjson


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ConfigMixin:
    # Заменяем стандартную работу с json на более быструю
    json_loads = orjson.loads
    json_dumps = orjson_dumps
