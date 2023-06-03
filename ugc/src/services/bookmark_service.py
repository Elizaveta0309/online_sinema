from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException

from src.core.settings import Settings
from src.db.mongo import Mongo
from src.models.bookmark import Bookmark

mongo = Mongo()

settings = Settings()


async def get_bookmarks_list(
    user_id: str,
    limit: int = settings.LIMIT,
    offset: int = settings.OFFSET,
) -> list[Bookmark]:
    data = await mongo.find(
        settings.MONGO_COLLECTION_BOOKMARK,
        {'user_id': user_id},
        limit=limit,
        offset=offset
    )
    return [Bookmark(**item) async for item in data]


async def get_bookmark(user_id: str, film_id: str) -> Optional[Bookmark]:
    data = await mongo.find_one(
        settings.BOOKMARK, {'user_id': user_id, 'film_id': film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return Bookmark(**data)


async def create_bookmark(user_id: str, film_id: str) -> Bookmark:
    data = await mongo.find_one(
        settings.BOOKMARK, {'user_id': user_id, 'film_id': film_id}
    )
    if data:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    data = Bookmark(user_id=user_id, film_id=film_id, dt=datetime.now())
    await mongo.insert(settings.BOOKMARK, data.dict())
    return data


async def remove_bookmark(user_id: str, film_id: str) -> None:
    data = await mongo.find_one(
        settings.BOOKMARK, {'user_id': user_id, 'film_id': film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    await mongo.delete(
        settings.BOOKMARK, {'user_id': user_id, 'film_id': film_id}
    )
