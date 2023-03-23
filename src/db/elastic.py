import backoff
from elasticsearch import AsyncElasticsearch, NotFoundError
import elasticsearch
from logging import getLogger
from src.db.storage import Storage
from src.core.config import settings

es: AsyncElasticsearch | None = None

logger = getLogger()

class AsyncElasticsearchStorage(Storage):
    def __init__(self, client: AsyncElasticsearch) -> None:
        super().__init__()
        self.client = client

    @backoff.on_exception(backoff.expo,
                          elasticsearch.ConnectionError,
                          max_time=settings.STORAGE_BACKOFF_MAX_TIME,
                          factor=settings.BACKOFF_FACTOR)
    async def get(self, index: str, id: str):
        try:
            doc = await self.client.get(index=index, id=id)
        except NotFoundError:
            return None

        return doc

    @backoff.on_exception(backoff.expo,
                          elasticsearch.ConnectionError,
                          max_time=settings.STORAGE_BACKOFF_MAX_TIME,
                          factor=settings.BACKOFF_FACTOR)
    async def search(self, index: str, body: dict, sort: str | None = None):
        doc = await self.client.search(
            index=index,
            body=body,
            sort=sort
        )

        return doc


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElasticsearchStorage:
    return AsyncElasticsearchStorage(es)
