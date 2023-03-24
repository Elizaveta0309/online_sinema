import pytest
from tests.settings import test_settings
from tests.testdata.genres_testdata.genre_model import Genre


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
async def test_genres(make_get_request, es_write_data, es_delete_index, query_data, expected_answer):
    await es_write_data(test_settings.genres_data, test_settings.genres_index, test_settings.genres_index_mapping)
    response = await make_get_request('/api/v1/genres', query_data)
    body = await response.json()
    assert response.status == expected_answer['status']
    assert len(body['data']) <= expected_answer['length']
    es_delete_index(test_settings.genres_index)


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'page_number': 1, 'page_size': 20, 'id': '0fe03178-cc0e-4273-a99b-7ea8b0fa16b2'},
                {'status': 200}
        ),

    ]
)
@pytest.mark.asyncio
async def test_one_genre(make_get_request, es_write_data, es_delete_index, query_data, expected_answer):
    await es_write_data(test_settings.genres_data, test_settings.genres_index, test_settings.genres_index_mapping)
    response = await make_get_request('/api/v1/genres/' + query_data['id'], query_data)
    body = await response.json()
    assert response.status == expected_answer['status']
    assert Genre(**body)
    es_delete_index(test_settings.genres_index)
