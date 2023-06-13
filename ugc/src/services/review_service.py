from datetime import datetime
from http import HTTPStatus
from typing import List, Optional

from fastapi import HTTPException

from src.config import Settings
from src.db.mongo import Mongo
from src.models.review import Review

mongo = Mongo()

settings = Settings()


async def get_reviews(
    user_id: str,
    limit: int = settings.LIMIT,
    offset: int = settings.OFFSET,
) -> List[Review]:
    data = await mongo.find(
        settings.REVIEW, {'user_id': user_id}, limit=limit, offset=offset
    )
    return [Review(**item) async for item in data]


async def get_review(user_id: str, film_id: str) -> Optional[Review]:
    data = await mongo.find_one(
        settings.REVIEW, {'user_id': user_id, 'film_id': film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return Review(**data)


async def create_review(user_id: str, film_id: str) -> Review:
    data = await mongo.find_one(
        settings.REVIEW, {'user_id': user_id, 'film_id': film_id}
    )
    if data:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    data = Review(user_id=user_id, film_id=film_id, dt=datetime.now())
    await mongo.insert(settings.REVIEW, data.dict())
    return data


async def remove_review(user_id: str, film_id: str) -> None:
    data = await mongo.find_one(
        settings.REVIEW, {'user_id': user_id, 'film_id': film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    await mongo.delete(
        settings.REVIEW, {'user_id': user_id, 'film_id': film_id}
    )
