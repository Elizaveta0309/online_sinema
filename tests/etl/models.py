from datetime import date
from uuid import UUID

from pydantic.schema import Optional, List
from pydantic import BaseModel, validator


LIST_FIELDS = [
    'actors',
    'writers',
    'actors_names',
    'writers_names',
    "directors_names",
    'directors',
    'genre'
]

NULLABLES = [
    'description',
    'age_limit'
]


class PersonModel(BaseModel):
    """Модель представления персоны."""
    uuid: UUID
    full_name: str
    film_ids: Optional[List]

    @validator("film_ids")
    def valid_list_field(cls, value):
        if value is None:
            return []
        return value


class GenreModel(BaseModel):
    """Модель представления жанра."""
    uuid: UUID
    name: str


class FilmworkModel(BaseModel):
    """Модель представления кинопроизведения."""
    uuid: UUID
    imdb_rating: Optional[float]
    genre: Optional[List]
    title: str
    description: Optional[str]
    directors: Optional[List]
    actors_names: Optional[List]
    writers_names: Optional[List]
    directors_names: Optional[List]
    actors: Optional[List]
    writers: Optional[List]
    age_limit: Optional[int]
    type: Optional[str]
    creation_date: Optional[str]

    @validator(*NULLABLES)
    def valid_description(cls, value):
        if value is None:
            return ''
        return value

    @validator(*LIST_FIELDS)
    def valid_list_field(cls, value):
        if value is None:
            return []
        return value
