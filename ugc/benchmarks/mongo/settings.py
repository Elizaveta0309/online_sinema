from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class ResearchSettings(BaseSettings):

    MONGO_HOST: str = Field('127.0.0.1', env='MONGO_HOST')
    MONGO_PORT: int = Field(27017, env='MONGO_PORT')
    MONGO_DB: str = Field('ugc_db', env='MONGO_DB')
    LIKES = 'likedfilms'
    REVIEW = 'reviews'
    BOOKMARK = 'bookmarks'
    ITERATIONS: int = 10
    USERS_IN_BATCH: int = 10
    BATCH_SIZE: int = 200
    RECORDS_SIZE: int = 10000
    LIKE: int = 1
    DISLIKE: int = 0
    START_DATE: str = '-30d'
    END_DATE: str = 'now'
    MIN_RATING: int = 1
    MAX_RATING: int = 10


class Config:
    env_file = '.env'


settings = ResearchSettings()
