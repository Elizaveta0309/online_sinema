from datetime import datetime
from typing import Optional

import orjson as orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseUGCModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Bookmark(BaseUGCModel):

    user_id: str
    film_id: str
    dt: Optional[datetime] = None
