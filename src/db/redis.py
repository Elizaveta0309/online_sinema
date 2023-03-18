from functools import lru_cache
from redis.asyncio import Redis
from aiocache import (
    RedisCache,
)
from aiocache.serializers import PickleSerializer
from src.core import config

redis: Redis | None = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return redis


@lru_cache()
def get_redis_cache_conf() -> dict:
    return {
        'cache': RedisCache,
        'serializer': PickleSerializer(),
        'endpoint': config.REDIS_HOST,
        'port': config.REDIS_PORT,
        'namespace': 'main',
        "pool_min_size": 5,
        "pool_max_size": 10,
    }
