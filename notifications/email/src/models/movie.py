from uuid import UUID

from models.transform import OrjsonModel


class Movie(OrjsonModel):
    """ Модель представления фильма. """
    id: UUID
    title: str
    description: str
    imdb_rating: int
    age_limit: int
