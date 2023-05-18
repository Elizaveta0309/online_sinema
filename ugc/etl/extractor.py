import logging
from typing import Iterator, Any

from confluent_kafka import Consumer
from utils.offset_registry import BaseOffsetRegistry

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BaseMessageBroker:
    def extract(self, batch_size: int) -> Iterator[Any]:
        pass

class KafkaBroker(BaseMessageBroker):
    def __init__(self, consumer: Consumer, offset_registry: BaseOffsetRegistry) -> None:
        self.consumer = consumer
        self.offset_registry = offset_registry
    
    def extract(self, batch_size: int = 10000) -> Iterator[Any]:
        for _ in range(batch_size):
            msg = self.consumer.poll(1.0)
            if msg is None:
                logger.error('[Kafka]: No messages.')
                return
            elif msg.error():
                logger.error(f'[Kafka]: Error while consuming messages: {msg.error()}')
                return
            else:
                self.offset_registry.update(
                    partition=msg.partition(),
                    topic=msg.topic(),
                    offset=msg.offset()
                )
                yield msg.value()
        logger.info('[Kafka]: Consumed a full batch.')