from typing import Any, Dict

import pytest
from aiohttp import ClientSession, CookieJar

from tests.settings import test_settings


@pytest.fixture()
async def client_session():
    cookie_jar = CookieJar()
    session = ClientSession(cookie_jar=cookie_jar)
    yield session
    await session.close()


@pytest.fixture()
def make_get_request(client_session):
    async def inner(endpoint: str, query_data: Dict[Any, Any], cookies: Dict[Any, Any]):
        url = test_settings.service_url + endpoint
        response = await client_session.get(url, params=query_data, cookies=cookies)
        return response

    return inner

@pytest.fixture()
def make_post_request(client_session):
    async def inner(endpoint: str, query_data: Dict[Any, Any], cookies: Dict[Any, Any]):
        url = test_settings.service_url + endpoint
        response = await client_session.post(url, params=query_data, cookies=cookies)
        return response
    return inner
