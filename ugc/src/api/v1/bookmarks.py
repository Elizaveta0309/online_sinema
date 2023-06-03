from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ugc.src.models.bookmark import Bookmark
from ugc.src.services import bookmark_service
from ugc.src.services.auth_service import Auth

router = APIRouter()
bearer_token = HTTPBearer()
auth = Auth()


@router.get('/',
            response_model=list[Bookmark],
            description='Получить список закладок'
            )
async def get_bookmarks(
        limit: int = 10,
        offset: int = 0,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),

) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    return await bookmark_service.get_bookmarks_list(
        user_id=user_id,
        limit=limit,
        offset=offset
    )


@router.post('/{film_id}',
             response_model=Bookmark,
             description='Создать закладку'
             )
async def create_bookmark(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    return await bookmark_service.create_bookmark(
        user_id=user_id,
        film_id=film_id
    )


@router.get('/{film_id}',
            response_model=Bookmark,
            description='Получить закладку'
            )
async def read_bookmark(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    return await bookmark_service.get_bookmark(
        user_id=user_id,
        film_id=film_id
    )


@router.delete('/{film_id}',
               response_model=str,
               description='Удалить закладку'
               )
async def delete_bookmark(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    await bookmark_service.remove_bookmark(
        user_id=user_id,
        film_id=film_id
    )
    return 'The bookmark was deleted'
