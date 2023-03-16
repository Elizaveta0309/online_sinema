from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.db.elastic import get_elastic
from src.models.film import Film
from src.services.base_service import BaseService
from src.core.config import FILMS_SEARCH_FIELD


class FilmService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = Film
        self.index = 'movies'
        self.search_field = FILMS_SEARCH_FIELD


@lru_cache()
def get_film_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
