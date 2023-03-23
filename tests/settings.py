from testdata.es_mapping import mapping
from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://elasticsearch-test:9200')
    es_index: str = 'movies'
    es_id_field: str = 'uuid'
    es_index_mapping: dict = mapping

    redis_host: str = 'redis-test:6379'
    service_url: str = 'http://nginx-test'


test_settings = TestSettings()
