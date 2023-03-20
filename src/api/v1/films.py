from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.query_params import SearchQueryParams, ListQueryParams
from src.models.base_model import Model
from src.services.film import FilmService, get_film_service
from src.models.film import Film
from .constants import FILM_NOT_FOUND_MESSAGE

router = APIRouter()


@router.get('/', description='Метод позволяет получить список всех фильмов',
            response_description='List of all films')
async def films(params: ListQueryParams = Depends(), film_service: FilmService = Depends(get_film_service)):
    return await film_service.get_list(params)


@router.get('/{film_id}', response_model=Film, description='Метод позволяет получить информацию о фильме по id',
            response_description='Info about the film')
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Model:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND_MESSAGE)

    return film


@router.get("/search/", description='Метод осуществляет поиск фильма по названию',
            response_description='Result of search, sorted by max_score')
async def search_films(params: SearchQueryParams = Depends(), film_service: FilmService = Depends(get_film_service)):
    return await film_service.search(params)
