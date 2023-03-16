from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.query_params import ListQueryParams, SearchQueryParams
from src.models.base_model import Model
from src.models.genre import Genre
from src.services.genre import GenreService, get_genre_service
from src.core.config import GENRES_SEARCH_FIELD

router = APIRouter()


@router.get('/')
async def genres(params: ListQueryParams = Depends(), genre_service: GenreService = Depends(get_genre_service)):
    return await genre_service.get_list(params)


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Model:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return genre

@router.get("/search/")
async def search_genres(params: SearchQueryParams = Depends(), genre_service: GenreService = Depends(get_genre_service)):
    return await genre_service.search(params, GENRES_SEARCH_FIELD)

