from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class LikeSettings(BaseSettings):

    MONGO_HOST: str = Field('127.0.0.1', env = 'MONGO_HOST')
    MONGO_PORT: int = Field(27017, env = 'MONGO_PORT')
    MONGO_DB: str = Field('ugc_db', env = 'MONGO_DB')
    LIKE = 'likedfilms'
    LIMIT: int = 10
    OFFSET: int = 0


class Config:
    env_file = '.env'


settings = LikeSettings()
