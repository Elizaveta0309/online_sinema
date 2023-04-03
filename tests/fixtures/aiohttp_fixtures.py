import pytest
from aiohttp import ClientSession

from tests.settings import test_settings


@pytest.fixture()
async def client_session():
    session = ClientSession()
    yield session
    await session.close()


@pytest.fixture()
def make_get_request(client_session):
    async def inner(endpoint: str, query_data: dict = None):
        url = test_settings.service_url + endpoint
        response = await client_session.get(url, params=query_data)
        return response

    return inner
