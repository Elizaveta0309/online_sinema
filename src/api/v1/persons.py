from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.query_params import ListQueryParams, SearchQueryParams
from .models.person import Person
from src.services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/')
async def persons(params: ListQueryParams = Depends(), person_service: PersonService = Depends(get_person_service)):
    return await person_service.get_list(params)


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return Person(**dict(person))


@router.get("/search/")
async def search_persons(params: SearchQueryParams = Depends(),
                         person_service: PersonService = Depends(get_person_service)):
    return await person_service.search(params)
