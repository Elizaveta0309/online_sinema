from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis

from src.core.config import CACHE_EXPIRE_IN_SECONDS
from src.models.film import Model


class BaseService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.model = None
        self.index = None

    async def get_list(self):
        ...

    async def get_by_id(self, object_id: str) -> Optional[Model]:
        obj = await self._get_object_from_cache(object_id)
        if not obj:
            obj = await self._get_object_from_elastic(object_id)
            if not obj:
                return None
            await self._put_object_to_cache(obj)

        return obj

    async def _get_object_from_elastic(self, object_id: str) -> Optional[Model]:
        try:
            doc = await self.elastic.get(self.index, object_id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])

    async def _get_object_from_cache(self, object_id: str) -> Optional[Model]:
        data = await self.redis.get(object_id)
        return self.model.parse_raw(data) if data else None

    async def _put_object_to_cache(self, obj: Model):
        await self.redis.set(obj.id, obj.json(), CACHE_EXPIRE_IN_SECONDS)
