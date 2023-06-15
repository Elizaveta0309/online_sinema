from pydantic import BaseSettings, Field



class Settings(BaseSettings):
    PROJECT_NAME = 'Notifications'


settings = Settings()