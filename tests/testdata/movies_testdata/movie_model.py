from datetime import datetime
from pydantic import BaseModel


class Movie(BaseModel):
    uuid: str
    type: str
    title: str
    description: str | None
    creation_date: datetime | None
    imdb_rating: float
    age_limit: int | None
    genre: list[dict]
    actors: list[dict]
    writers: list[dict]
    directors: list[dict]
