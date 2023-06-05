from datetime import datetime
from http import HTTPStatus
from typing import List, Optional

from fastapi import HTTPException

from src.config import settings
from src.db.mongo import Mongo
from src.models.like import Like

mongo = Mongo()


async def get_likes(
        user_id: str,
        limit: int = settings.LIMIT,
        offset: int = settings.OFFSET,
) -> List[Like]:
    data = await mongo.find(
        settings.LIKE,
        {'user_id': user_id},
        limit=limit,
        offset=offset
    )
    return [Like(**item) async for item in data]


async def get_like(user_id: str, film_id: str) -> Optional[Like]:
    data = await mongo.find_one(
        settings.LIKE,
        {'user_id': user_id, 'film_id': film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return Like(**data)


async def create_like(user_id: str, film_id: str) -> Like:
    data = await mongo.find_one(
        settings.LIKE,
        {'user_id': user_id, 'film_id': film_id}
    )
    if data:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    data = Like(user_id=user_id, film_id=film_id, date_time=datetime.now())
    await mongo.replace_one(settings.LIKE, data.dict(), upsert=True)
    return data

async def remove_like(user_id: str, film_id: str) -> None:
    data = await mongo.find_one(
        settings.LIKE,
        {'user_id': user_id, 'film_id': film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    await mongo.delete(settings.LIKE, {'user_id': user_id, 'film_id': film_id})
