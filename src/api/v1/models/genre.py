from pydantic import BaseModel, Field


class Genre(BaseModel):
    uuid: str = Field(title='uuid', example='1dhe6')
    name: str = Field(title='Название', example='Comedy')
