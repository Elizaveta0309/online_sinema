from fastapi import Query


class NewFilmParams(object):
    def __init__(
            self,
            transport: str = Query(
                default='email'
            ),
            event_type: str = Query(
                default='notification_about_new_film',
                description='Describes type of event',
            ),
            template_id: str = Query(
                description='Template ID'
            ),
            user_id: str = Query(
                description='User ID'
            ),
            film_id: str = Query(
                description='Films ID',
            ),
    ):
        self.transport = transport
        self.event_type = event_type
        self.template_id = template_id
        self.user_id = user_id
        self.film_id = film_id
