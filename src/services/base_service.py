import logging
import math

import elasticsearch
from aiocache import cached
from elasticsearch import AsyncElasticsearch, NotFoundError

from src.api.v1.query_params import ListQueryParams, SearchQueryParams
from src.core.config import CACHE_EXPIRE_IN_SECONDS
from src.core.utils import get_items_source, build_cache_key
from src.db.redis import get_redis_cache_conf
from src.models.film import Model


class BaseService:
    def __init__(self, elastic: AsyncElasticsearch, search_field: str):
        self.elastic = elastic
        self.search_field = search_field
        self.model = None
        self.index = None

    # @cached(
    #     ttl=CACHE_EXPIRE_IN_SECONDS,
    #     noself=True,
    #     **get_redis_cache_conf(),
    #     key_builder=build_cache_key
    # )
    async def get_list(self, params: ListQueryParams):
        from_ = (params.page_number - 1) * params.page_size
        data = await self.elastic.search(
            index=self.index,
            body={
                'from': from_,
                'size': params.page_size,
                'query': {
                    'match_all': {}
                }
            },
            sort=f'{params.sort}:{params.asc}',
        )


        total_pages = math.ceil(data['hits']['total']['value'] / params.page_size)
        data = get_items_source(data)

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
    async def get_by_id(self, object_id: str) -> Model | None:
        obj = await self._get_object_from_elastic(object_id)
        return obj or None

    async def _get_object_from_elastic(self, object_id: str) -> Model | None:
        try:
            doc = await self.elastic.get(self.index, object_id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])

    @cached(
        ttl=CACHE_EXPIRE_IN_SECONDS,
        noself=True,
        **get_redis_cache_conf(),
        key_builder=build_cache_key
    )
    async def search(self, params: SearchQueryParams):
        from_ = (params.page_number - 1) * params.page_size

        try:
            data = await self.elastic.search(
                index=self.index,
                body={
                    'from': from_,
                    'size': params.page_size,
                    'query': {
                        'match': {
                            self.search_field: {
                                'query': params.query,
                                'fuzziness': 'AUTO',
                                'operator': 'and',
                                'minimum_should_match': '75%'
                            }

                        }
                    },
                }
            )
        except elasticsearch.exceptions.RequestError as e:
            logging.error(str(e))
            return {'error': 'request error'}

        total_pages = math.ceil(data['hits']['total']['value'] / params.page_size)
        data = get_items_source(data)

        return {
            'page_number': params.page_number,
            'total_pages': total_pages,
            'data': data
        }
