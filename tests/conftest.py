import json
from typing import List

import pytest
from elasticsearch import AsyncElasticsearch, BadRequestError

from tests.settings import test_settings
from tests.testdata.es_mapping import mapping


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host)
    yield client
    await client.close()


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: List[dict]):
        bulk_query = []
        for row in data:
            bulk_query.extend([
                json.dumps({'index': {'_index': test_settings.es_index, '_id': row[test_settings.es_id_field]}}),
                json.dumps(row)
            ])

        str_query = '\n'.join(bulk_query) + '\n'

        es_client = AsyncElasticsearch(hosts=test_settings.es_host)

        try:
            await es_client.indices.create(index='movies', body=mapping)
        except BadRequestError as e:
            if e.error != 'resource_already_exists_exception':
                raise e

        response = await es_client.bulk(operations=str_query, refresh=True)

        await es_client.close()
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest.fixture
def es_delete_index(es_client):
    async def inner(index):
        await es_client.indices.delete(index=index, ignore=[400, 404])
        await es_client.close()

    return inner
