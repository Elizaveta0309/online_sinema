from pydantic import Field

from src.models.base_model import Model


class Genre(Model):
    name: str = Field(title='Название', example='Comedy')
