from http import HTTPStatus

import pytest
from aiocache.serializers import PickleSerializer

from tests.settings import test_settings
from tests.testdata.persons_testdata.person_model import Person


pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'page_number': 1, 'page_size': 20},
                {'status': HTTPStatus.OK, 'length': 20}
        ),
        (
                {'page_number': -1, 'page_size': 20},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                {'page_number': 1, 'page_size': -1},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),

    ]
)
async def test_persons(make_get_request, es_write_data, es_delete_index, query_data, expected_answer):
    await es_write_data(test_settings.persons_data, test_settings.persons_index, test_settings.persons_index_mapping)
    response = await make_get_request('/api/v1/persons', query_data)
    body = await response.json()
    assert response.status == expected_answer['status']
    if response.status == HTTPStatus.OK:
        assert len(body['data']) <= expected_answer['length']
    await es_delete_index(test_settings.persons_index)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': test_settings.persons_data[0]['uuid']},
                {'status': HTTPStatus.OK}
        ),
        (
                {'id': 'this_id_doesnt_exists'},
                {'status': HTTPStatus.NOT_FOUND}
        ),
    ]
)
async def test_one_person(make_get_request, es_write_data, es_delete_index, query_data, expected_answer, aioredis_pool):
    await es_write_data(test_settings.persons_data, test_settings.persons_index, test_settings.persons_index_mapping)
    response = await make_get_request('/api/v1/persons/' + query_data['id'], query_data)
    body = await response.json()
    assert response.status == expected_answer['status']
    if response.status == HTTPStatus.OK:
        assert Person(**body)

    await es_delete_index(test_settings.persons_index)


@pytest.mark.parametrize(
    'index, test_data, endpoint, query_data, expected_answer',
    [
        (
                'persons',
                (test_settings.persons_data, test_settings.persons_index, test_settings.persons_index_mapping),
                '/api/v1/persons',
                {'page_number': 1, 'page_size': 20},
                {'status': HTTPStatus.OK, 'cache_key': "main:get_list:persons:1:20:uuid:asc"}
        ),

    ]
)
async def test_person_cache(es_write_data, es_delete_index, make_get_request, aioredis_pool, index, test_data,
                            endpoint, query_data, expected_answer):
    await es_write_data(*test_data)
    response = await make_get_request(endpoint, query_data)
    body = await response.json()

    assert response.status == expected_answer['status']

    cache_data = await aioredis_pool.get(expected_answer['cache_key'])
    cache_dict = PickleSerializer().loads(cache_data)

    assert body['page_number'] == cache_dict['page_number']
    assert body['total_pages'] == cache_dict['total_pages']
    assert len(body['data']) == len(cache_dict['data'])
    assert body['data'] == cache_dict['data']

    await aioredis_pool.flushall()
    await es_delete_index(index)
