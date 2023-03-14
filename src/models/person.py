from typing import List

from pydantic import Field

from src.models.base_model import Model


class Person(Model):
    full_name: str = Field(title='Полное имя', example='Julia Roberts')
    film_ids: List[str] = Field(title='ids кинопроизведений', example=[
        '123732dnjn',
        'm23nkfmf'
    ])
