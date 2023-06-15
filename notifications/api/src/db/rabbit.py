import json
import pika
import datetime


class AsyncRabbitPublisher:
    def __init__(self):
        self.parameters = pika.URLParameters("here coonection to rabbit has to be")
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = None

        self.EXCHANGE = "email"



    async def send(self, message):
        self.channel.basic_publish(self.EXCHANGE, str(datetime.datetime.now()),
                                    json.dumps(message, ensure_ascii=False))


async def get_rabbit() -> AsyncRabbitPublisher:
    return AsyncRabbitPublisher()

