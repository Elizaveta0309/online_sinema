from typing import Any, Callable, Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(
    obj_to_serialize: Any,
    *,
    default: Optional[Callable[[Any], Any]],
) -> Any:
    return orjson.dumps(obj_to_serialize, default=default).decode()


class OrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumbs = orjson_dumps
