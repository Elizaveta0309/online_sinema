from logging import config as logging_config

from pydantic import BaseSettings

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'postgres'
    ES_HOST: str = 'localhost'
    ES_PORT: int = 9200
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    PAGE_SIZE = 20
    CACHE_EXPIRE_IN_SECONDS = 60 * 5
    PROJECT_NAME = 'Movies'
    FILMS_SEARCH_FIELD = 'title'
    PERSONS_SEARCH_FIELD = 'full_name'
    GENRES_SEARCH_FIELD = 'name'
    STORAGE_BACKOFF_MAX_TIME = 5
    BACKOFF_FACTOR = 2
    SECRET = '4b54ed6943c2'
    AUTH_API_URL: str = 'http://auth:5000/api/v1'

    class Config:
        env_file = '.env'


settings = Settings()
