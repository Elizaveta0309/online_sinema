from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.db.elastic import get_elastic
from src.models.person import Person
from src.services.base_service import BaseService
from src.core.config import PERSONS_SEARCH_FIELD


class PersonService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = Person
        self.index = 'persons'
        self.search_field = PERSONS_SEARCH_FIELD


@lru_cache()
def get_person_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(elastic)
