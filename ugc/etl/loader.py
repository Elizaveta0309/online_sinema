from ast import List
import logging
from clickhouse_driver import Client
from clickhouse_driver.errors import Error as ClickHouseError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BaseDatabaseLoader:
    def load(self) -> None:
        pass

class ClickHouseLoader(BaseDatabaseLoader):
    QUERY = "INSERT INTO viewed_progress (user_id, film_id, viewed_frame, created_at) VALUES (%s, %s, %s, %s);"
    def __init__(self, client: Client) -> None:
        self.client = client
    
    def load(self, data) -> None:
        parsed_input = [dict(row) for row in data]
        try:
            print('Started loading')
            self.client.execute(self.QUERY, parsed_input)
            logger.debug(f'[ClickHouse]: Uploaded {len(data)} messages.')
        except ClickHouseError as e:
            logger.exception(f'[ClickHouse]: Error while uploading messages: {e}')
        print('Loaded')
