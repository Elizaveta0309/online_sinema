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
            {'user_id': 1, 'film_id': 1, 'viewed_frame': 12},
            {'status': HTTPStatus.CREATED}
        )
    ]
)
async def test_time_code(make_get_request, make_post_request, user, query_data, expected_response):
    cookies = {'Authorization': f'Bearer {encode_user(user)}'}
    response = await make_get_request('/api/v1/time_code/', query_data, cookies)
    await response.json()

    assert response.status == expected_response['status']
