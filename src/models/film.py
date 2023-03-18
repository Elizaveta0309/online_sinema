from datetime import datetime
from typing import List, Union, Dict

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import Field

from src.models.base_model import Model


class Film(Model):
    type: str = Field(title='Тип кинопроизведения', example='movie')
    title: str = Field(title='Название', example='Pretty Woman')
    description: Union[str, None] = Field(title='Описание', example='Very good film!')
    creation_date: datetime | None = Field(None, title='Дата создания', example='1990-01-01')
    imdb_rating: float = Field(title='Рейтинг', example=9.4)
    age_limit: int | None = Field(title='Возрастной ценз', example=18, gt=0, default=0)
    genre: List[Dict] = Field(title='Жанры', example=[
        {"name": "Comedy", "id": "6f822a92"},
        {"name": "Adventure", "id": "00f74939"}
    ])
    actors: List[Dict] = Field(title='Жанры', example=[
        {"full_name": "Julia Roberts", "id": "474hfnvm"},
        {"full_name": "Richard Gir", "id": "47ggfnvm"}
    ])
    writers: List[Dict] = Field(title='Жанры', example=[
        {"full_name": "J.F. Lawton", "id": "0ffdkdmks"}
    ])
    directors: List[Dict] = Field(title='Жанры', example=[
        {"full_name": "Harry Marshall", "id": "343vjmkl"},
    ])
