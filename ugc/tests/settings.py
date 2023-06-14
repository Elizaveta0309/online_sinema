from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    service_url: str = Field('http://localhost:8001')
    secret_key: str = Field('top_secret')


test_settings = TestSettings()
