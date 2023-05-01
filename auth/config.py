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
    REQUEST_NUM_LIMIT: int = 100
    REQUEST_TIME_LIMIT: str = 'minute'
    VK_AUTHORIZE_URL: str = 'https://oauth.vk.com/authorize'
    VK_ACCESS_TOKEN_URL: str = 'https://oauth.vk.com/access_token'
    VK_ACCESS_TOKEN: str = 'NgRvwx5YoYGauO39VANy'
    VK_CLIENT_ID = '51629723'
    OAUTH_REDIRECT_URI: str = 'http://3a17-46-138-168-89.ngrok-free.app/api/v1/callback'

    class Config:
        env_file = '.env'


settings = Settings()
