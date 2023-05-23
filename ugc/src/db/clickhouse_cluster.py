from clickhouse_driver import Client
from clickhouse_driver.errors import Error
import logging
import time


def connection() -> Client:
    while True:
        try:
            return Client("clickhouse-node1")
        except Error as e:
            logging.error(e)
            logging.info("Connection in progress")
            time.sleep(1)


client = connection()


class AsyncClickhouseClient:
    def __init__(self, client):
        self.client = client

    async def get(self, user_id, film_id):
        last_viewed_second = self.client.execute(
            """
                    SELECT 'viewed_frame' FROM analysis.viewed_progress
                    WHERE user_id=%(user_id)s and film_id=%(film_id)s;
            
            """,
            {'user-id': user_id, 'film_id': film_id})
        return last_viewed_second


async def get_clickhouse() -> AsyncClickhouseClient:
    return AsyncClickhouseClient(client)
