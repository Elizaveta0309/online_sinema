from fastapi import Query

class TimeCodeParams:
    def __init__(
            self,
            user_id: str = Query(
                default = 'user_id_for_example',
                description='User ID',
            ),
            film_id: str = Query(
                default='film_id_for_example',
                description='Film ID',
            ),
            viewed_frame: int = Query(
                default=1,
                description='Amount viewed seconds of the film',
                ge = 1,
            )
    ):
        self.user_id = user_id
        self.film_id = film_id
        self.viewed_frame = viewed_frame
