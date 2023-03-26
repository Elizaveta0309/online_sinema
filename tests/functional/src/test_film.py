import pytest
from tests.settings import test_settings
from tests.testdata.movies_testdata.movie_model import Movie


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'page_number': 1, 'page_size': 20},
                {'status': 200, 'length': 20}
        ),
    ]
)
@pytest.mark.asyncio
async def test_films(make_get_request, es_write_data, es_delete_index, query_data, expected_answer):
    await es_write_data(test_settings.movies_data, test_settings.movies_index, test_settings.movies_index_mapping)
    response = await make_get_request('/api/v1/films', query_data)
    body = await response.json()
    assert response.status == expected_answer['status']
    assert len(body['data']) <= expected_answer['length']
    es_delete_index(test_settings.movies_index)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'page_number': 1, 'page_size': 20, 'id': '0044325a-20d9-4925-ad4d-4f1f242c5047'},
                {'status': 200}
        ),

    ]
)
@pytest.mark.asyncio
async def test_one_film(make_get_request, es_write_data, es_delete_index, query_data, expected_answer):
    await es_write_data(test_settings.movies_data, test_settings.movies_index, test_settings.movies_index_mapping)
    response = await make_get_request('/api/v1/films/' + query_data['id'], query_data)
    body = await response.json()
    assert response.status == expected_answer['status']
    assert Movie(**body)
    es_delete_index(test_settings.movies_index)


