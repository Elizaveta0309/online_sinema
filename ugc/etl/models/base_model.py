import orjson


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class ConfigMixin:
    # Заменяем стандартную работу с json на более быструю
    json_loads = orjson.loads
    json_dumps = orjson_dumps
