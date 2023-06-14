from pydantic import BaseSettings, Field, Required


class BaseConfig(BaseSettings):
    """_summary_

    Args:
        BaseSettings (_type_): _description_
    """


class ApiConfig(BaseConfig):

    API_HOST: str = Field(Required, env='API_HOST')
    API_PORT: str = Field(Required, env='API_PORT')


class PSQConfig(BaseConfig):
    USER: str = Field('postgres', env='POSTGRES_USER')
    PASSWORD: str = Field('postgres', env='POSTGRES_PASSWORD')
    HOST: str = Field(Required, env='POSTGRES_HOST')
    PORT: int = Field(5432, env='POSTGRES_PORT')
    DB_NAME: str = Field('postgres', env='POSTGRES_DB')


class Config(BaseConfig):
    env_file = '.env'
