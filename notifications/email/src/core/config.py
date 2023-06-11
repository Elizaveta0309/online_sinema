from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    RECEIVING_QUEUE: str = Field('rabbit', env='QUEUE_NAME')
    EXCHANGE: str = Field('email', env='EVENTS_EXCHANGE_NAME')
    USER: str = Field('user', env='USER')
    PASSWORD: str = Field('rabbit', env='PASSWORD')
    R_HOST: str = Field('rabbitmq', env='HOST')
    LOG_LEVEL: str = 'INFO'
    R_PORT: int = Field(5672, env='PORT')
    SENDGRID: str = Field(..., env='SENDGRID')
    email_from: str = 'noname@yandex.ru'


settings = Settings()
