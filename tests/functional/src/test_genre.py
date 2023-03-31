from http import HTTPStatus

import pytest
from aiocache.serializers import PickleSerializer

from tests.settings import test_settings
from tests.testdata.genres_testdata.genre_model import Genre


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
@pytest.mark.asyncio
async def test_genres(make_get_request, es_write_data, es_delete_index, query_data, expected_answer):
    await es_write_data(test_settings.genres_data, test_settings.genres_index, test_settings.genres_index_mapping)
    response = await make_get_request('/api/v1/genres', query_data)
    body = await response.json()
    assert response.status == expected_answer['status']
    if response.status == HTTPStatus.OK:
        assert len(body['data']) <= expected_answer['length']
    await es_delete_index(test_settings.genres_index)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': 'genre_id'},
                {'status': HTTPStatus.OK}
        ),
        (
                {'id': 'this_id_doesnt_exist'},
                {'status': HTTPStatus.NOT_FOUND}
        ),
    ]
)
@pytest.mark.asyncio
async def test_one_genre(make_get_request, es_write_data, es_delete_index, query_data, expected_answer):
    await es_write_data(test_settings.genres_data, test_settings.genres_index, test_settings.genres_index_mapping)
    response = await make_get_request('/api/v1/genres/' + query_data['id'], query_data)
    body = await response.json()
    assert response.status == expected_answer['status']
    if response.status == HTTPStatus.OK:
        assert Genre(**body)

    await es_delete_index(test_settings.genres_index)


@pytest.mark.parametrize(
    'index, test_data, endpoint, query_data, expected_answer',
    [
        (
                'genres',
                (test_settings.genres_data, test_settings.genres_index, test_settings.genres_index_mapping),
                '/api/v1/genres',
                {'page_number': 1, 'page_size': 20},
                {'status': HTTPStatus.OK, 'cache_key': "main:get_list:genres:1:20:uuid:asc"}
        ),

    ]
)
@pytest.mark.asyncio
async def test_genre_cache(es_write_data, es_delete_index, make_get_request, aioredis_pool, index, test_data,
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
