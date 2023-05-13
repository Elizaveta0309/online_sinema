from fastapi import Depends
from time import sleep
from src.api.v1.query_params import TimeCodeParams
from src.db.kafka_cluster import get_kafka
from kafka import KafkaProducer


class TimeCodeService:

    def __init__(self, producer: KafkaProducer):
        self.producer = producer

    async def post_time_code(self, params: TimeCodeParams):
        await self.producer.send(params.user_id, params.film_id, params.viewed_frame)
        sleep(1)



def get_time_code_service(kafka: KafkaProducer = Depends(get_kafka)
) -> TimeCodeService:
    return TimeCodeService(kafka)

