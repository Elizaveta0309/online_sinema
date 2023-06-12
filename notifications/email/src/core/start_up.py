import backoff
import pika
from core.config import settings
from db.rabbit import rabbitmq
from pika import BlockingConnection, ConnectionParameters
from pika.exceptions import AMQPConnectionError


@backoff.on_exception(backoff.expo, AMQPConnectionError)
def start_up() -> None:
    rabbitmq.rabbit_connect = BlockingConnection(
        ConnectionParameters(
            host=settings.R_HOST,
            port=settings.R_PORT,
            credentials=pika.PlainCredentials(settings.USER, settings.PASSWORD),
        ),
    )


start_up()
