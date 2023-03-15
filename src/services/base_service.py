import logging
import math
from typing import Optional

import elasticsearch
from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis

from src.api.v1.query_params import QueryParams
from src.core.config import CACHE_EXPIRE_IN_SECONDS
from src.models.film import Model


class BaseService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.model = None
        self.index = None

    async def get_list(self, params: QueryParams):
        from_ = (params.page_number - 1) * params.page_size

        try:
            data = await self.elastic.search(
                index=self.index,
                body={
                    'from': from_,
                    'size': params.page_size,
                    'query': {
                        'match_all': {}
                    }
                },
                sort=f'{params.sort}:{params.asc}'
            )
        except elasticsearch.exceptions.RequestError as e:
            logging.error(str(e))
            return 'Wrong sort_by field'

        total_pages = math.ceil(data['hits']['total']['value'] / params.page_size)

        return {
            'page_number': params.page_number,
            'total_pages': total_pages,
            'data': data
        }

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
        await self.redis.set(obj.uuid, obj.json(), CACHE_EXPIRE_IN_SECONDS)
