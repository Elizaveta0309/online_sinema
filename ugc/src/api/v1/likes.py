from typing import Any, List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.models.like import Like
from src.services import like_service
from src.services.auth_service import Auth

router = APIRouter()
bearer_token = HTTPBearer()
auth = Auth()


@router.get('/{user_id}', response_model=List[Like])
async def get_likes(
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        limit: int = 10,
        offset: int = 0,
) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    return await like_service.get_likes(
        user_id=user_id,
        limit=limit,
        offset=offset)


@router.post('/{user_id}/{film_id}',
             response_model=Like
             )
async def create_like(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    return await like_service.create_like(
        user_id=user_id,
        film_id=film_id
    )


@router.get('/{user_id}/{film_id}', response_model=Like)
async def get_likess(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    return await like_service.get_like(
        user_id=user_id,
        film_id=film_id
    )


@router.delete('/{user_id}/{film_id}',
               response_model=str
               )
async def delete_category(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    await like_service.remove_like(
        user_id=user_id,
        film_id=film_id
    )
    return 'Likes were removed.'
