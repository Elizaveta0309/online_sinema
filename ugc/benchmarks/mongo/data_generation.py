from random import choice, randint
from typing import Callable
from uuid import uuid4

from faker import Faker
from settings import settings

fake = Faker()


def generate_likes(user_id, film_id):
    return {
        'user_id': user_id if user_id else str(uuid4()),
        'film_id': film_id if film_id else str(uuid4()),
        'type': choice([settings.LIKE, settings.DISLIKE]),
        'datetime': fake.date_time_between(
            start_date=settings.START_DATE,
            end_date=settings.END_DATE
        ),
    }


def generate_reviews(user_id, film_id):
    return {
        'user_id': user_id if user_id else str(uuid4()),
        'film_id': film_id if film_id else str(uuid4()),
        'text': 'This film is ...',
        'rating': randint(settings.MIN_RATING, settings.MAX_RATING),
        'datetime': fake.date_time_between(
            start_date=settings.START_DATE,
            end_date=settings.END_DATE
        ),
    }


def generate_bookmarks(user_id, film_id):
    return {
        'user_id': user_id if user_id else str(uuid4()),
        'film_id': film_id if film_id else str(uuid4()),
        'datetime': fake.date_time_between(
            start_date=settings.START_DATE,
            end_date=settings.END_DATE
        ),
    }


def generate_batch(attribute: Callable, users_number: int, batch_size: int):
    users = [str(uuid4()) for _ in range(users_number)]
    return [attribute(user_id=choice(users)) for _ in range(batch_size)]


def generate_users_batch(attribute: Callable, users: list, batch_size: int):
    return [attribute(user_id=choice(users)) for _ in range(batch_size)]
