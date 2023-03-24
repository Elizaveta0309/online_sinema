from tests.testdata.movies_testdata.movies_mapping import MOVIES_MAPPING
from tests.testdata.genres_testdata.genres_mapping import GENRES_MAPPING
from tests.testdata.movies_testdata.movies_index_data import MOVIES_DATA
from tests.testdata.genres_testdata.genres_index_data import GENRES_DATA
from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://localhost:9200')

    es_id_field: str = 'uuid'

    movies_index: str = 'movies'
    movies_index_mapping: dict = MOVIES_MAPPING
    movies_data: list = MOVIES_DATA

    genres_index: str = 'genres'
    genres_index_mapping: dict = GENRES_MAPPING
    genres_data: list = GENRES_DATA

    redis_host: str = 'redis-test:6379'
    service_url: str = 'http://localhost:8000'


test_settings = TestSettings()
