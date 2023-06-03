from logging import Logger
from typing import List

from clickhouse_driver import Client
from clickhouse_driver.errors import Error as ClickHouseError
from pydantic import BaseModel


class BaseDatabaseLoader:
    def load(self, data: List[BaseModel]) -> None:
        pass


class ClickHouseLoader(BaseDatabaseLoader):
    QUERY = "INSERT INTO analysis.viewed_progress (" \
            "user_id, film_id, viewed_frame, created_at) VALUES"

    def __init__(self, client: Client, logger: Logger) -> None:
        self.client = client
        self.logger = logger

    def load(self, data: List[BaseModel]) -> None:
        parsed_input = [dict(row) for row in data]
        try:
            self.logger.info('[Clickhouse]: Started loading')
            self.client.execute(self.QUERY, parsed_input)
            self.logger.debug(f'[ClickHouse]: Uploaded {len(data)} messages.')
        except ClickHouseError as e:
            self.logger.exception(
                f'[ClickHouse]: Error while uploading messages: {e}'
            )
        self.logger.info('[Clickhouse]: Loaded batch.')
