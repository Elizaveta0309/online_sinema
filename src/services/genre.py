from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.core.config import GENRES_SEARCH_FIELD
from src.db.elastic import get_elastic
from src.models.genre import Genre
from src.services.base_service import BaseService


class GenreService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = Genre
        self.index = 'genres'


@lru_cache()
def get_genre_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic, GENRES_SEARCH_FIELD)
