from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.query_params import ListQueryParams, SearchQueryParams
from .models.genre import Genre
from src.services.genre import GenreService, get_genre_service
from .constants import GENRE_NOT_FOUND_MESSAGE

router = APIRouter()


@router.get('/', description='Метод позволяет получить список всех жанров',
            response_description='List of all genres')
async def genres(params: ListQueryParams = Depends(), genre_service: GenreService = Depends(get_genre_service)):
    return await genre_service.get_list(params)


@router.get('/{genre_id}', response_model=Genre, description='Метод позволяет получить информацию о жанре по id',
            response_description='Info about the genre')
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND_MESSAGE)

    return Genre(**dict(genre))


@router.get("/search/", description='Метод осуществляет поиск жанра по названию',
            response_description='Result of search, sorted by max_score')
async def search_genres(params: SearchQueryParams = Depends(),
                        genre_service: GenreService = Depends(get_genre_service)):
    return await genre_service.search(params)
