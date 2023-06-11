from functools import lru_cache
from typing import Callable, Optional

from db.base import BaseQueue
from pika import BlockingConnection

rabbit_connect: Optional[BlockingConnection] = None


@lru_cache
def get_rabbit_con() -> BlockingConnection:
    """Rabbit connection."""
    return rabbit_connect


class Rabbit(BaseQueue):
    """RabbitMQ main class."""

    def __init__(self, connect: BlockingConnection):
        self._con = connect
        self._channel = self._con.channel()

    def start_consume(self, callback: Callable) -> None:
        """Incoming data reading."""
        self._channel.basic_consume(
            queue='email',
            on_message_callback=callback,
            auto_ack=False
        )
        self._channel.start_consuming()


@lru_cache()
def get_rabbit() -> Rabbit:
    return Rabbit(get_rabbit_con())
