from pydantic import BaseModel, Field


class Person(BaseModel):
    uuid: str = Field(title='uuid', example='1dhe6')
    full_name: str = Field(title='Полное имя', example='Julia Roberts')
    film_ids: list[str] = Field(title='ids кинопроизведений', example=[
        '123732dnjn',
        'm23nkfmf'
    ])
