from uuid import UUID

from pydantic.schema import Optional, List
from pydantic import BaseModel, validator


LIST_FIELDS = [
    'actors',
    'writers',
    'actors_names',
    'writers_names',
    'director',
    'genre'
]

NULLABLES = [
    'description',
]


class PersonModel(BaseModel):
    """Модель представления персоны."""
    id: UUID
    full_name: str
    roles: Optional[List]
    film_ids: Optional[List]

    @validator("roles", "film_ids")
    def valid_list_field(cls, value):
        if value is None:
            return []
        return value


class GenreModel(BaseModel):
    """Модель представления жанра."""
    id: UUID
    name: str


class FilmworkModel(BaseModel):
    """Модель представления кинопроизведения."""
    id: UUID
    imdb_rating: Optional[float]
    genre: Optional[List]
    title: str
    description: Optional[str]
    director: Optional[List]
    actors_names: Optional[List]
    writers_names: Optional[List]
    actors: Optional[List]
    writers: Optional[List]

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
