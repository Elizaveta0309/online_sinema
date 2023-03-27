import pytest
from tests.settings import test_settings
from tests.testdata.movies_testdata.movie_model import Movie

from http import HTTPStatus


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
async def test_films(make_get_request, es_write_data, es_delete_index, query_data, expected_answer):
    await es_write_data(test_settings.movies_data, test_settings.movies_index, test_settings.movies_index_mapping)
    response = await make_get_request('/api/v1/films', query_data)
    body = await response.json()
    assert response.status == expected_answer['status']
    if response.status == HTTPStatus.OK:
        assert len(body['data']) <= expected_answer['length']
    await es_delete_index(test_settings.movies_index)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'id': 'movie_id'},
                {'status': HTTPStatus.OK}
        ),
        (
                {'id': 'this_id_doesnt_exixts'},
                {'status': HTTPStatus.NOT_FOUND}
        ),
    ]
)
@pytest.mark.asyncio
async def test_one_film(make_get_request, es_write_data, es_delete_index, query_data, expected_answer):
    await es_write_data(test_settings.movies_data, test_settings.movies_index, test_settings.movies_index_mapping)
    response = await make_get_request('/api/v1/films/' + query_data['id'], query_data)
    body = await response.json()
    assert response.status == expected_answer['status']
    if response.status == HTTPStatus.OK:
        assert Movie(**body)
    await es_delete_index(test_settings.movies_index)


