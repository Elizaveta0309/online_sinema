import backoff
import pika
from core.config import settings
from pika.exceptions import AMQPConnectionError


@backoff.on_exception(backoff.expo, AMQPConnectionError)
def add_queue() -> None:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.R_HOST,
            port=settings.R_PORT,
            credentials=pika.PlainCredentials(
                settings.USER,
                settings.PASSWORD,
            ),
        ),
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=settings.EXCHANGE, durable=True)
    channel.queue_declare(queue=settings.RECEIVING_QUEUE, durable=True)
    channel.queue_bind(
        exchange=settings.EXCHANGE,
        queue=settings.RECEIVING_QUEUE,
    )
    connection.close()
