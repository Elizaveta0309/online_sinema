from aiokafka import AIOKafkaProducer

producer: AIOKafkaProducer | None = None


class AsyncKafkaProducer:
    def __init__(self, producer):
        self.producer = producer

    async def send(self, user_id, film_id, viewed_frame):
        self.producer.send_and_wait(
            topic='views',
            value=str(viewed_frame).encode('utf-8'),
            key=(user_id + "+" + film_id).encode('utf-8')
        )


async def get_kafka() -> AsyncKafkaProducer:
    return AsyncKafkaProducer(producer)
