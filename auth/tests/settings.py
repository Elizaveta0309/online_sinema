from pydantic import BaseSettings


class TestSettings(BaseSettings):
    api_url: str = 'http://localhost:5000/api/v1'


test_settings = TestSettings()
