import orjson
# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class ConfigMixin:
    # Заменяем стандартную работу с json на более быструю
    json_loads = orjson.loads
    json_dumps = orjson_dumps


class Model(BaseModel, ConfigMixin):
    uuid: str = Field(title='uuid', example='1dhe6')
