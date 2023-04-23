from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5433
    POSTGRES_USER: str = 'postgres-auth'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'postgres'
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: str = 6379
    SECRET: str = '4b54ed6943c2'
    TOKEN_EXP: int = 10
    REFRESH_EXP: int = 43200
    SALT: bytes = b'$2b$12$PuxeYPUtTZ2bvJjWR0ZWVu'

    class Config:
        env_file = '.env'


settings = Settings()
