import time
import pytest
from aiocache.serializers import PickleSerializer
from tests.settings import test_settings
from http import HTTPStatus


@pytest.mark.parametrize(
        'index, test_data, endpoint, query_data, expected_answer',
        [
            (
                'movies',
                (test_settings.movies_data, test_settings.movies_index, test_settings.movies_index_mapping),
                '/api/v1/films/search/',
                {'query': 'Star'},
                {'status': HTTPStatus.OK, 'ans_len': 20}
            ),
            (
                'genres',
                (test_settings.genres_data, test_settings.genres_index, test_settings.genres_index_mapping),
                '/api/v1/genres/search/',
                {'query': 'Action'},
                {'status': HTTPStatus.OK, 'ans_len': 20}
            ),
            (
                'persons',
                (test_settings.persons_data, test_settings.persons_index, test_settings.persons_index_mapping),
                '/api/v1/persons/search/',
                {'query': 'Jim'},
                {'status': HTTPStatus.OK, 'ans_len': 20}
            ),
            (
                'movies',
                (test_settings.movies_data, test_settings.movies_index, test_settings.movies_index_mapping),
                '/api/v1/films/search/',
                {'query': 'Lorem Ipsum'},
                {'status': HTTPStatus.OK, 'ans_len': 0}
            ),
            (
                'genres',
                (test_settings.genres_data, test_settings.genres_index, test_settings.genres_index_mapping),
                '/api/v1/genres/search/',
                {'query': 'Lorem Ipsum'},
                {'status': HTTPStatus.OK, 'ans_len': 0}
            ),
            (
                'persons',
                (test_settings.persons_data, test_settings.persons_index, test_settings.persons_index_mapping),
                '/api/v1/persons/search/',
                {'query': 'Lorem Ipsum'},
                {'status': HTTPStatus.OK, 'ans_len': 0}
            )
        ]
)
@pytest.mark.asyncio
async def test_search_endpoints(es_write_data, es_delete_index, make_get_request, aioredis_pool, index, test_data, endpoint, query_data, expected_answer):
    await es_write_data(*test_data)
    await aioredis_pool.flushall()

    response = await make_get_request(endpoint, query_data)
    body = await response.json()

    assert response.status == expected_answer['status']
    assert len(body['data']) == expected_answer['ans_len']

    await es_delete_index(index)


@pytest.mark.parametrize(
        'index, test_data, endpoint, query_data, expected_answer',
        [
            (
                'movies',
                (test_settings.movies_data, test_settings.movies_index, test_settings.movies_index_mapping),
                '/api/v1/films/search/',
                {'query': 'Star', 'page_number': 2, 'page_size': 10},
                {'status': HTTPStatus.OK, 'ans_len': 10, 'page_number': 2, 'total_pages': 7}
            ),
            (
                'genres',
                (test_settings.genres_data, test_settings.genres_index, test_settings.genres_index_mapping),
                '/api/v1/genres/search/',
                {'query': 'Action', 'page_number': 2, 'page_size': 10},
                {'status': HTTPStatus.OK, 'ans_len': 10, 'page_number': 2, 'total_pages': 7}
            ),
            (
                'persons',
                (test_settings.persons_data, test_settings.persons_index, test_settings.persons_index_mapping),
                '/api/v1/persons/search/',
                {'query': 'Jim', 'page_number': 2, 'page_size': 10},
                {'status': HTTPStatus.OK, 'ans_len': 10, 'page_number': 2, 'total_pages': 7}
            )
        ]
)
@pytest.mark.asyncio
async def test_search_pagination(es_write_data, es_delete_index, make_get_request, aioredis_pool, index, test_data, endpoint, query_data, expected_answer):
    await es_write_data(*test_data)
    await aioredis_pool.flushall()

    response = await make_get_request(endpoint, query_data)
    body = await response.json()

    assert response.status == expected_answer['status']

    assert body['page_number'] == expected_answer['page_number']
    assert body['total_pages'] == expected_answer['total_pages']
    assert len(body['data']) == expected_answer['ans_len']

    await es_delete_index(index)


@pytest.mark.parametrize(
        'index, test_data, endpoint, query_data, expected_answer',
        [
            (
                'movies',
                (test_settings.movies_data, test_settings.movies_index, test_settings.movies_index_mapping),
                '/api/v1/films/search/',
                {'query': 'Star', 'page_number': 2, 'page_size': 10},
                {'status': HTTPStatus.OK, 'cache_key': "main:search:movies:2:10:Star"}
            ),
            (
                'genres',
                (test_settings.genres_data, test_settings.genres_index, test_settings.genres_index_mapping),
                '/api/v1/genres/search/',
                {'query': 'Action', 'page_number': 2, 'page_size': 10},
                {'status': HTTPStatus.OK, 'cache_key': "main:search:genres:2:10:Action"}
            ),
            (
                'persons',
                (test_settings.persons_data, test_settings.persons_index, test_settings.persons_index_mapping),
                '/api/v1/persons/search/',
                {'query': 'Jim', 'page_number': 2, 'page_size': 10},
                {'status': HTTPStatus.OK, 'cache_key': "main:search:persons:2:10:Jim"}
            )
        ]
)
@pytest.mark.asyncio
async def test_search_cache(es_write_data, es_delete_index, make_get_request, aioredis_pool, index, test_data, endpoint, query_data, expected_answer):
    await es_write_data(*test_data)
    await aioredis_pool.flushall()

    response = await make_get_request(endpoint, query_data)
    body = await response.json()

    assert response.status == expected_answer['status']

    cache_data = await aioredis_pool.get(expected_answer['cache_key'])
    cache_dict = PickleSerializer().loads(cache_data)

    assert body['page_number'] == cache_dict['page_number']
    assert body['total_pages'] == cache_dict['total_pages']
    assert len(body['data']) == len(cache_dict['data'])
    assert body['data'][0] == cache_dict['data'][0]

    await aioredis_pool.flushall()
    await es_delete_index(index)
