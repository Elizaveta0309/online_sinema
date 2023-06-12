from typing import List

from fastapi import Query


class LikeParams:
    def __init__(
            self,
            transport: str = Query(
                default='email'
            ),
            user_id: str = Query(
                default='user_id_for_example',
                description='User ID',
            ),
            review_id: str = Query(
                default='review_id_for_example',
                description='Review ID',
            ),
            liker_id: str = Query(
                default='liker_id_for_example',
                description='Liker ID',
            )
    ):
        self.transport = transport
        self.user_id = user_id
        self.review_id = review_id
        self.liker_id = liker_id

class NewFilmsParams:
    def __init__(
            self,
            transport: str = Query(
                default='email'
            ),
            users_id: List[str] = Query(
                description='Users IDs',
            ),
            films_id: List[str] = Query(
                description='Films IDs',
            ),
    ):
        self.transport = transport
        self.users_id = users_id
        self.films_id = films_id


class SomeEventParams:
    def __init__(
            self,
            transport: str = Query(
                default='email'
            ),
            user_id: str = Query(
                default='user_id_for_example',
                description='User ID',
            ),
            event_type: str = Query(
                default='personalized subscription offer',
                decsription='Describes type of personalized letter for user'
            ),

    ):
        self.transport = transport
        self.user_id = user_id
        self.event_type = event_type