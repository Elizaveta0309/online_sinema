from typing import List

import aioredis
import pytest
from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch, RequestError
from elasticsearch.helpers import async_bulk

from tests.settings import test_settings


@pytest.fixture()
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host)
    yield client
    await client.close()


@pytest.fixture()
async def client_session():
    session = ClientSession()
    yield session
    await session.close()


@pytest.fixture()
async def aioredis_pool():
    redis_host = test_settings.redis_host
    pool = await aioredis.from_url(f"redis://{redis_host}")
    yield pool
    await pool.close()


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


@pytest.fixture()
def make_get_request(client_session):
    async def inner(endpoint: str, query_data: dict = None):
        url = test_settings.service_url + endpoint
        response = await client_session.get(url, params=query_data)
        return response

    return inner
