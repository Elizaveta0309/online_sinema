import json
import pika
import datetime



class AsyncRabbitPublisher:
    def __init__(self):
        self.credentials = pika.PlainCredentials('guest', 'guest')
        self.parameters = pika.URLParameters('rabbitmq',
                                       5672,
                                       '/',
                                       self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = None

        self.EXCHANGE = "email"



    async def send(self, message):
        self.channel.basic_publish(self.EXCHANGE, str(datetime.datetime.now()),
                                    json.dumps(message, ensure_ascii=False))


async def get_rabbit() -> AsyncRabbitPublisher:
    return AsyncRabbitPublisher()

