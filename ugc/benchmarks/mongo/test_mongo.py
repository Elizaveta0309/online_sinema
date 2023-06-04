import time
from typing import Callable
from uuid import uuid4

from data_generation import (generate_batch, generate_bookmarks,
                             generate_likes, generate_reviews,
                             generate_users_batch)
from pymongo import MongoClient
from settings import settings

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT, connect=True)
mongo_db = client[settings.MONGO_DB]


def patch_step(
        faker: Callable,
        collection_name: str,
        batch_size: int,
        iterations: int = settings.ITERATIONS,
) -> None:
    collection = mongo_db.get_collection(collection_name)
    result = []
    for _ in range(iterations):
        batch = generate_batch(faker, settings.USERS_IN_BATCH, batch_size)
        start = time.time()
        collection.insert_many(batch)
        end = time.time()
        result.append(end - start)
    avr_batch = sum(result) / len(result)
    print(
        f"Results {collection_name} "
        f"batch_size={batch_size}: batch={avr_batch} sec."
    )


def test_patch(faker: Callable, collection_name: str) -> None:
    batch_sizes = [200, 1000, 5000]
    for batch_size in batch_sizes:
        patch_step(faker, collection_name, batch_size)


def test_reading(
    faker: Callable,
    collection_name: str,
    users_size: int
) -> None:
    result = []
    collection = mongo_db.get_collection(collection_name)
    users = [str(uuid4()) for _ in range(users_size)]

    for i in range(0, settings.RECORDS_SIZE, settings.BATCH_SIZE):
        print(i)
        batch = generate_users_batch(
            faker,
            users,
            batch_size=settings.BATCH_SIZE
        )
        collection.insert_many(batch)

    for user in users:
        start = time.time()
        _ = list(collection.find({"user_id": user}))
        result.append(time.time() - start)

    avr_batch = sum(result) / len(result)
    print(
        f"Results for{collection_name} "
        f"for ~{int(settings.RECORDS_SIZE/users_size)} records: {avr_batch} sec.",
    )


if __name__ == "__main__":
    test_patch(
        generate_likes,
        settings.LIKES,
    )

    test_patch(
        generate_reviews,
        settings.REVIEW,
    )

    test_patch(
        generate_bookmarks,
        settings.BOOKMARK,
    )
    test_reading(generate_likes, settings.LIKES, 20)
    test_reading(generate_reviews, settings.REVIEW, 20)
    test_reading(generate_bookmarks, settings.BOOKMARK, 20)
