from typing import Any, List

from fastapi import APIRouter

from src.models.like import Like
from src.services.like_service import get_likes, create_like, get_like, remove_like

router = APIRouter()


@router.get('/{user_id}', response_model= List[Like])
async def get_likes(
        user_id: str,
        limit: int = 10,
        offset: int = 0,
) -> Any:
    return await get_likes(user_id=user_id, limit=limit, offset=offset)


@router.post('/{user_id}/{film_id}', response_model=Like)
async def create_like(
        user_id: str,
        film_id: str,
) -> Any:
    return await create_like(user_id=user_id, film_id=film_id)


@router.get('/{user_id}/{film_id}', response_model=Like)
async def read_category(
        user_id: str,
        film_id: str,
) -> Any:
    return await get_like(user_id=user_id, film_id=film_id)


@router.delete('/{user_id}/{film_id}', response_model=str)
async def delete_category(
        user_id: str,
        film_id: str,
) -> Any:
    await remove_like(user_id=user_id, film_id=film_id)
    return 'Liles were removed.'
