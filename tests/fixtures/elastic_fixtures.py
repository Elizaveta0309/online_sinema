from typing import List

import pytest
from elasticsearch import AsyncElasticsearch, RequestError
from elasticsearch.helpers import async_bulk

from tests.settings import test_settings


@pytest.fixture()
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host)
    yield client
    await client.close()


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: List[dict], index: str, mapping: dict):
        bulk_query = []
        for row in data:
            bulk_query.append(
                {
                    '_index': index,
                    '_id': row['uuid'],
                    '_source': row
                }
            )

        try:
            await es_client.indices.create(index=index, body=mapping)
        except RequestError as e:
            if e.error != 'resource_already_exists_exception':
                raise e

        await async_bulk(es_client, actions=bulk_query, refresh='wait_for')

    return inner


@pytest.fixture
def es_delete_index(es_client):
    async def inner(index):
        await es_client.indices.delete(index=index, ignore=[400, 404])

    return inner
