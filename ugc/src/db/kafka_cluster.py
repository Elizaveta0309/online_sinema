from kafka import KafkaProducer
import logging
logging.basicConfig(level=logging.INFO)

producer = KafkaProducer(bootstrap_servers=['broker:29092'])


class AsyncKafkaProducer:
    def __init__(self, producer):
        self.producer = producer
    async def send(self, user_id, film_id, viewed_frame):
        self.producer.send(
            topic='views',
            value=str(viewed_frame).encode('utf-8'),
            key=(user_id + "+" + film_id).encode('utf-8')
        )





async def get_kafka() -> AsyncKafkaProducer:
    return AsyncKafkaProducer(producer)
