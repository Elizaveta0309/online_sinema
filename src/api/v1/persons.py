from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.models.film import Person
from src.services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/', response_model=Person)
async def persons():
    ...


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return person
