import aioredis
import pytest

from tests.settings import test_settings


@pytest.fixture()
async def aioredis_pool():
    redis_host = test_settings.redis_host
    pool = await aioredis.from_url(f"redis://{redis_host}")
    yield pool
    await pool.close()
