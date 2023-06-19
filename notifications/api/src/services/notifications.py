from fastapi import Depends

from src.db.rabbit import get_rabbit, AsyncRabbitPublisher


class NotificationsService:

    def __init__(self, publisher: AsyncRabbitPublisher):
        self.publisher = publisher

    async def send_notification(self, message):
        await self.publisher.send(message)


def get_notifications_service(rabbit: AsyncRabbitPublisher = Depends(get_rabbit)
                              ) -> NotificationsService:
    return NotificationsService(rabbit)
