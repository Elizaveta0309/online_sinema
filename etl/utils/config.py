from pydantic import BaseSettings, Field


class PostgresConfig(BaseSettings):
    user: str = Field(..., env='POSTGRES_USER')
    host: str = Field('127.0.0.1', env='POSTGRES_HOST')
    dbname: str = Field(..., env='POSTGRES_DB')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    port: int = Field(5432, env='POSTGRES_PORT')


class ElasticConfig(BaseSettings):
    host: str = Field('127.0.0.1', env='ES_HOST')
    port: int = Field(9200, env='ES_PORT')

    def url(self):
        return f'http://{self.host}:{self.port}'


class RedisConfig(BaseSettings):
    host: str = Field('127.0.0.1', env='REDIS_HOST')
    port: int = Field(6379, env='REDIS_PORT')


class CommonConfig(BaseSettings):
    debug: bool = Field(True, env='ETL_DEBUG')
    sleep_time: int = Field(10, env='ETL_SLEEP_TIME')
