from functools import lru_cache

from aiocache import (
    RedisCache,
)
from aiocache.serializers import PickleSerializer
from redis.asyncio import Redis

from src.core.config import settings

redis: Redis | None = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return redis


@lru_cache()
def get_redis_cache_conf() -> dict:
    return {
        'cache': RedisCache,
        'serializer': PickleSerializer(),
        'endpoint': settings.REDIS_HOST,
        'port': settings.REDIS_PORT,
        'namespace': 'main',
        "pool_min_size": 5,
        "pool_max_size": 10,
    }
