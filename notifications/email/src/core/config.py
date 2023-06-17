from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    RECEIVING_QUEUE: str = Field('rabbit', env='QUEUE_NAME')
    EXCHANGE: str = Field('email', env='EVENTS_EXCHANGE_NAME')
    RABBIT_USER: str = Field('rabbit', env='RABBIT_USER')
    RABBIT_PASSWORD: str = Field('rabbit', env='RABBIT_PASSWORD')
    RABBIT_HOST: str = Field('127.0.0.1', env='HOST')
    LOG_LEVEL: str = 'INFO'
    RABBIT_PORT: int = Field(5672, env='RABBIT_PORT')
    SENDGRID: str = Field('test', env='SENDGRID')
    EMAIL_FROM: str = 'noname@yandex.ru'
    POSTGRES_USER: str = Field('postgres', env='POSTGRES_USER')
    POSTGRES_PORT: int = Field(5432, env='POSTGRES_PORT')
    POSTGRES_HOST: str = Field('postgresql', env='POSTGRES_HOST')
    POSTGRES_PASSWORD: str = Field('postgres', env='POSTGRES_PASSWORD')
    USER_SERVICE_URL: str = Field(
        'http://localhost/api/v1/auth/users',
        env='USER_SERVICE_URL')
    MOVIE_SERVICE_URL: str = Field(
        'http://localhost/api/v1/movies',
        env='MOVIE_SERVICE_URL')
    TEMPLATE_HOST: str = Field('localhost', env='TEMPLATE_HOST')
    TEMPLATE_PORT: int = Field(5432, env='TEMPLATE_PORT')
    TEMPLATE_DB: str = Field('postgres', env='TEMPLATE_DB')


settings = Settings()
