from http import HTTPStatus

import pytest

from tests.settings import test_settings
from tests.utils import encode_user


pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize(
    'user, query_data, expected_response',
    [
        (
            {'role': 'admin', 'user_id': 1},
            {'film_id': 1},
            {
                'status': HTTPStatus.CREATED,
                'body': {
                    'user_id': 1,
                    'film_id': 1,
                }
            }
        )
    ]
)
async def test_post_reviews(make_get_request, make_post_request, user, query_data, expected_response):
    cookies = {'Authorization': f'Bearer {encode_user(user)}'}
    response = await make_post_request('/api/v1/reviews/', query_data, cookies)
    body = await response.json()

    assert response.status == expected_response['status']
    assert body['user_id'] == expected_response['body']['user_id']
    assert body['film_id'] == expected_response['body']['film_id']

@pytest.mark.parametrize(
    'user, query_data, expected_response',
    [
        (
            {'role': 'admin', 'user_id': 1},
            {'film_id': 1},
            {
                'status': HTTPStatus.CREATED,
                'body': {
                    'user_id': 1,
                    'film_id': 1,
                }
            }
        )
    ]
)
async def test_get_reviews(make_get_request, make_post_request, user, query_data, expected_response):
    cookies = {'Authorization': f'Bearer {encode_user(user)}'}
    response = await make_get_request('/api/v1/reviews/', query_data, cookies)
    body = await response.json()

    assert response.status == expected_response['status']

    assert len(body) == 1
    assert body[0]['user_id'] == expected_response['body']['user_id']
    assert body[0]['film_id'] == expected_response['body']['film_id']