from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME = 'TimeCodes'

    class Config:
        env_file = '.env'


settings = Settings()
