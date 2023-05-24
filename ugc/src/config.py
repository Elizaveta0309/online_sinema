from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME = 'TimeCodes'
    # KAFKA_BOOTSTRAP_SERVERS=['broker:29092']

    class Config:
        env_file = '.env'


settings = Settings()
