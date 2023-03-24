from functools import lru_cache

from fastapi import Depends

from src.core.config import settings
from src.db.elastic import AsyncElasticsearchStorage, get_elastic
from src.models.person import Person
from src.services.base_service import BaseService


class PersonService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = Person
        self.index = 'persons'


@lru_cache()
def get_person_service(
        elastic: AsyncElasticsearchStorage = Depends(get_elastic),
) -> PersonService:
    return PersonService(elastic, settings.PERSONS_SEARCH_FIELD)
