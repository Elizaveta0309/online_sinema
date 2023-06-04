"""Mongo DB adapter."""
from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorCollection,
                                 AsyncIOMotorCursor)

from src.config import settings


class Mongo:
    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(
            settings.MONGO_HOST,
            settings.MONGO_PORT
        )
        self.db = self.client[settings.MONGO_DB]

    def _get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        return self.db[collection_name]

    async def find(
            self,
            collection_name: str,
            condition: dict,
            limit: int = settings.LIMIT,
            offset: int = settings.OFFSET,
    ) -> AsyncIOMotorCursor:
        collection = self._get_collection(collection_name)
        return collection.find(condition).skip(offset).limit(limit)

    async def insert(
            self,
            collection_name: str,
            data: dict,
    ) -> None:
        collection = self._get_collection(collection_name)
        await collection.insert_one(data)

    async def find_one(
            self,
            collection_name: str,
            condition: dict,
    ) -> dict:
        collection = self._get_collection(collection_name)
        return await collection.find_one(condition)

    async def delete(
            self,
            collection_name: str,
            condition: dict,
    ) -> None:
        collection = self._get_collection(collection_name)
        await collection.delete_many(condition)
