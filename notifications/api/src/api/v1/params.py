from typing import List

from fastapi import Query


class LikeParams:
    def __init__(
            self,
            transport: str = Query(
                default='email'
            ),
            event_type: str = Query(
                default='notification_about_like',
                description='Describes type of event',
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
        self.event_type = event_type
        self.user_id = user_id
        self.review_id = review_id
        self.liker_id = liker_id

class NewFilmsParams:
    def __init__(
            self,
            transport: str = Query(
                default='email'
            ),
            event_type: str = Query(
                default='notification_about_new_films',
                description='Describes type of event',
            ),
            users_id: List[str] = Query(
                description='Users IDs',
            ),
            films_id: List[str] = Query(
                description='Films IDs',
            ),
    ):
        self.transport = transport
        self.event_type = event_type
        self.users_id = users_id
        self.films_id = films_id


class SomeEventParams:
    def __init__(
            self,
            transport: str = Query(
                default='email'
            ),
            event_type: str = Query(
              default='notification_from_admin_panel',
              description='Describes type of event',
            ),
            user_id: str = Query(
                default='user_id_for_example',
                description='User ID',
            ),
            text: str = Query(
                default='some personalized subscription offer',
                decsription='Text of personalized letter for user'
            ),

    ):
        self.transport = transport
        self.event_type = event_type
        self.user_id = user_id
        self.text = text