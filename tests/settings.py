from tests.testdata.es_mapping import mapping
from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ES_HOST')
    es_index: str = 'movies'
    es_id_field: str = 'uuid'
    es_index_mapping: dict = mapping

    redis_host: str = 'redis:6379'
    service_url: str = 'http://localhost'


test_settings = TestSettings()
