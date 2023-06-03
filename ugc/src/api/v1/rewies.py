from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ugc.src.models.review import Review
from ugc.src.services import review_service
from ugc.src.services.auth_service import Auth

router = APIRouter()
bearer_token = HTTPBearer()
auth = Auth()


@router.get('/',
            response_model=list[Review],
            description='Список рецензий'
            )
async def get_reviews(
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
        limit: int = 10,
        offset: int = 0,
) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    return await review_service.get_reviews(
        user_id=user_id,
        limit=limit,
        offset=offset
    )


@router.post('/{film_id}',
             response_model=Review,
             description='Создать рецензию'
             )
async def create_review(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    return await review_service.create_review(
        user_id=user_id,
        film_id=film_id
    )


@router.get('/{film_id}',
            response_model=Review,
            description='Получить рецензию'
            )
async def read_review(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    return await review_service.get_review(
        user_id=user_id,
        film_id=film_id
    )


@router.delete('/{film_id}',
               response_model=str,
               description='Удалить рецензию'
               )
async def delete_review(
        film_id: str,
        request: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> Any:
    token = request.credentials
    user_id = auth.decode_token(token)
    await review_service.get_review(
        user_id=user_id,
        film_id=film_id
    )
    return "The review was deleted"
