from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.query_params import ListQueryParams, SearchQueryParams
from src.models.base_model import Model
from src.models.person import Person
from src.services.person import PersonService, get_person_service
from .constants import PERSON_NOT_FOUND_MESSAGE

router = APIRouter()


@router.get('/', description='Метод позволяет получить весь список персон',
            response_description='List of all persons')
async def persons(params: ListQueryParams = Depends(), person_service: PersonService = Depends(get_person_service)):
    return await person_service.get_list(params)


@router.get('/{person_id}', response_model=Person, description='Метод позволяет получить информацию о персоне по id',
            response_description='Info about the person')
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Model:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND_MESSAGE)

    return person


@router.get("/search/", description='Метод осуществляет поиск персоны по имени',
            response_description='Result of search, sorted by max_score')
async def search_persons(params: SearchQueryParams = Depends(),
                         person_service: PersonService = Depends(get_person_service)):
    return await person_service.search(params)
