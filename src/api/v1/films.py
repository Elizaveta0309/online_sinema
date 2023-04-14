from functools import wraps
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from src.api.v1.query_params import SearchQueryParams, ListQueryParams
from src.core.utils import jwt_decode, is_token_valid, is_token_expired, generate_new_tokens
from src.services.film import FilmService, get_film_service
from .constants import FILM_NOT_FOUND_MESSAGE
from .models.film import Film

router = APIRouter()


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs['request']
        response = kwargs['response']
        token = request.cookies.get('token')
        refresh = request.cookies.get('refresh')

        if not token or not is_token_valid(token):
            return {'error': 'unauthorized'}
        if is_token_expired(token):
            tokens = await generate_new_tokens(refresh)
            token = tokens.get('token')
            refresh = tokens.get('refresh')
            response.set_cookie('token', token)
            response.set_cookie('refresh', refresh)
            return {}

        token_decoded = jwt_decode(token)
        role = token_decoded['role']
        if role != 'admin':
            return {'error': 'роль неоч'}
        return await func(*args, **kwargs)

    return wrapper


@router.get('/', description='Метод позволяет получить список всех фильмов',
            response_description='List of all films')
@login_required
async def films(request: Request, response: Response, params: ListQueryParams = Depends(),
                film_service: FilmService = Depends(get_film_service)):
    return await film_service.get_list(params)


@router.get('/{film_id}', response_model=Film, description='Метод позволяет получить информацию о фильме по id',
            response_description='Info about the film')
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND_MESSAGE)

    return Film(**dict(film))


@router.get("/search/", description='Метод осуществляет поиск фильма по названию',
            response_description='Result of search, sorted by max_score')
async def search_films(params: SearchQueryParams = Depends(), film_service: FilmService = Depends(get_film_service)):
    return await film_service.search(params)
