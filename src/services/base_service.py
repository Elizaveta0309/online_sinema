import logging
import math
from typing import Optional

import elasticsearch
from elasticsearch import AsyncElasticsearch, NotFoundError
from aiocache import cached


from src.api.v1.query_params import QueryParams
from src.core.config import CACHE_EXPIRE_IN_SECONDS
from src.models.film import Model
from src.db.redis import get_redis_cache_conf


def build_cache_key(f, args, kwargs) -> str:
    if isinstance(kwargs, QueryParams):
        query = f'{kwargs.page_size}:{kwargs.page_number}:{kwargs.sort}:{kwargs.asc}'
    else:
        query = str(kwargs)

    return (
        f.__name__
        + ':'
        + str(args.index)
        + ':'
        + query
    )


class BaseService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic
        self.model = None
        self.index = None

    @cached(
        ttl=CACHE_EXPIRE_IN_SECONDS,
        noself=True,
        **get_redis_cache_conf(),
        key_builder=build_cache_key
    )
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

    @cached(
        ttl=CACHE_EXPIRE_IN_SECONDS,
        noself=True,
        **get_redis_cache_conf(),
        key_builder=build_cache_key
    )
    async def get_by_id(self, object_id: str) -> Optional[Model]:
        obj = await self._get_object_from_elastic(object_id)
        if not obj:
            return None
        return obj

    async def _get_object_from_elastic(self, object_id: str) -> Optional[Model]:
        try:
            doc = await self.elastic.get(self.index, object_id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])
