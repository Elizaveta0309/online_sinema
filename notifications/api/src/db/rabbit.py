import json
import datetime
from functools import lru_cache


class AsyncRabbitPublisher:
    def __init__(self):
        self.EXCHANGE = "email"
        self.channel = None

    async def send(self, message):
        self.channel.basic_publish(self.EXCHANGE, str(datetime.datetime.now()),
                                   json.dumps(message, ensure_ascii=False))


publisher = AsyncRabbitPublisher()


@lru_cache()
async def get_rabbit() -> AsyncRabbitPublisher:
    return publisher
