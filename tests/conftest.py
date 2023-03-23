import json
from typing import List

import pytest
from elasticsearch import AsyncElasticsearch, BadRequestError

from settings import test_settings
from testdata.es_mapping import mapping


@pytest.fixture
def es_write_data():
    async def inner(data: List[dict]):
        bulk_query = []
        for row in data:
            bulk_query.extend([
                json.dumps({'index': {'_index': test_settings.es_index, '_id': row[test_settings.es_id_field]}}),
                json.dumps(row)
            ])

        str_query = '\n'.join(bulk_query) + '\n'

        es = AsyncElasticsearch(hosts=test_settings.es_host)

        try:
            await es.indices.create(index='movies', body=mapping)
        except BadRequestError as e:
            if e.error != 'resource_already_exists_exception':
                raise e

        response = await es.bulk(operations=str_query, refresh=True)

        await es.close()
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner
