from logging import Logger
from typing import Iterator, Any, List, Optional

from confluent_kafka import Consumer
from utils.offset_registry import BaseOffsetRegistry
from utils.backoff import backoff


class BaseMessageBroker:
    def extract(self, batch_size: int) -> Optional[Iterator[Any]]:
        return None


class KafkaBroker(BaseMessageBroker):
    def __init__(
        self, consumer: Consumer,
        offset_registry: BaseOffsetRegistry,
        logger: Logger
    ) -> None:
        self.consumer = consumer
        self.offset_registry = offset_registry
        self.logger = logger

    @backoff()
    def extract(self, batch_size: int = 10000) -> Optional[Iterator[Any]]:
        batch: List = []
        for _ in range(batch_size):
            msg = self.consumer.poll(1.0)
            if msg is None:
                self.logger.error('[Kafka]: No messages.')
                self.logger.info(f'[Kafka]: Consumed a batch of {len(batch)}')
                yield batch
            elif msg.error():
                self.logger.error(
                    f'[Kafka]: Error while consuming messages: {msg.error()}'
                )
                self.logger.info(f'[Kafka]: Consumed a batch of {len(batch)}')
                yield batch
            else:
                self.offset_registry.update(
                    partition=msg.partition(),
                    topic=msg.topic(),
                    offset=msg.offset()
                )
                batch.append(msg.value())

        self.logger.info(f'[Kafka]: Consumed a batch of {len(batch)}')
        yield batch
