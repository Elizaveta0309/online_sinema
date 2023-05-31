from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME = 'TimeCodes'
    # KAFKA_BOOTSTRAP_SERVERS=['broker:29092']
    MONGO_HOST: str = Field('127.0.0.1', env = 'MONGO_HOST')
    MONGO_PORT: int = Field(27017, env = 'MONGO_PORT')
    MONGO_DB: str = Field('ugc_db', env = 'MONGO_DB')
    PROJECT_NAME: str = 'ugc_mongo'
    KAFKA_HOST: str = Field('broker', env = 'KAFKA_HOST')
    KAFKA_PORT: str = Field('29092', env = 'KAFKA_PORT')
    SENTRY_DSN = 'https://0051158308b3405aa651a7c8d71f34eb@o4504248096391168.ingest.sentry.io/4505279661277184'
    LIKE = 'likedfilms'
    LIMIT: int = 10
    OFFSET: int = 0
    traces_sample_rate: float = 1.0

    class Config:
        env_file = '.env'


settings = Settings()
