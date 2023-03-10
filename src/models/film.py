from datetime import datetime
from typing import List, Union, Dict

import orjson

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class ConfigMixin:
    # Заменяем стандартную работу с json на более быструю
    json_loads = orjson.loads
    json_dumps = orjson_dumps


class Person(BaseModel, ConfigMixin):
    id: str = Field(title='id персоны', example='1dhe6')
    full_name: str = Field(title='Полное имя', example='Julia Roberts')
    role: str = Field(title='Роль', example='actor')
    films_ids: List[str] = Field(title='ids кинопроизведений', example=[
        '123732dnjn',
        'm23nkfmf'
    ])


class Genre(BaseModel, ConfigMixin):
    id: str = Field(title='id жанра', example='82dnd')
    name: str = Field(title='Название', example='Comedy')


class Film(BaseModel, ConfigMixin):
    id: str = Field(title='id кинопроизведения', example='3djd8')
    type: str = Field(title='Тип кинопроизведения', example='movie')
    title: str = Field(title='Название', example='Pretty Woman')
    description: Union[str, None] = Field(title='Описание', example='Very good film!')
    creation_date: datetime = Field(title='Дата создания', example='1990-01-01')
    rating: float = Field(title='Рейтинг', example=9.4)
    age_limit: int = Field(title='Возрастной ценз', example=18, gt=0)
    genres: List[Dict] = Field(title='Жанры', example=[
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
