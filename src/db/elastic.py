import logging
from logging import getLogger

import backoff
import elasticsearch
from elasticsearch import AsyncElasticsearch, NotFoundError

from src.core.config import settings
from src.db.storage import Storage

es: AsyncElasticsearch | None = None

logger = getLogger()


class AsyncElasticsearchStorage(Storage):
    @backoff.on_exception(backoff.expo,
                          elasticsearch.ConnectionError,
                          max_time=settings.STORAGE_BACKOFF_MAX_TIME,
                          factor=settings.BACKOFF_FACTOR,
                          raise_on_giveup=True)
    async def get(self, index: str, id_: str):

        try:
            doc = await self.client.get(index=index, id=id_)
        except (NotFoundError, elasticsearch.exceptions.ConnectionError) as e:
            logging.error(str(e))
            return

        return doc

    @backoff.on_exception(backoff.expo,
                          elasticsearch.ConnectionError,
                          max_time=settings.STORAGE_BACKOFF_MAX_TIME,
                          factor=settings.BACKOFF_FACTOR,
                          raise_on_giveup=True)
    async def search(self, index: str, body: dict, sort: str | None = None):
        try:
            return await self.client.search(index=index, body=body, sort=sort)
        except elasticsearch.exceptions.ConnectionError as e:
            logging.error(str(e))
            return


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElasticsearchStorage:
    return AsyncElasticsearchStorage(es)
