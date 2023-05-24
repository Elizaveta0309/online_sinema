from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME = 'TimeCodes'
    KAFKA_BOOTSTRAP_SERVERS=['broker:29092']

    class Config:
        env_file = '.env'


settings = Settings()
