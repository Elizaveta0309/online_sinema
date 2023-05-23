from fastapi import Depends
from time import sleep
from src.api.v1.query_params import TimeCodeParams
from src.db.kafka_cluster import get_kafka
from src.db.clickhouse_cluster import get_clickhouse
from kafka import KafkaProducer
from clickhouse_driver import Client


class TimeCodeService:

    def __init__(self, producer: KafkaProducer, client: Client):
        self.producer = producer
        self.client = client

    async def set_time_code(self, params: TimeCodeParams):
        await self.producer.send(params.user_id, params.film_id, params.viewed_frame)
        sleep(1)

    async def get_time_code(self, user_id: str, film_id: str):
        await self.client.get(user_id, film_id)
        sleep(1)


def get_time_code_service(kafka: KafkaProducer = Depends(get_kafka),
                          clickhouse: Client = Depends(get_clickhouse)
                          ) -> TimeCodeService:
    return TimeCodeService(kafka, clickhouse)
