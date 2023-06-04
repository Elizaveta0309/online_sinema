from typing import Optional

from pydantic import BaseSettings, Field


class ClickHouseSettings(BaseSettings):
    port: int = Field(default=8123, env='CLICKHOUSE_PORT')
    user: Optional[str] = Field(..., env='CLICKHOUSE_USER')
    password: Optional[str] = Field(..., env='CLICKHOUSE_PASSWORD')
    database: str = Field(default='default', env='CLICKHOUSE_DB')
    host: str = Field(default='localhost', env='CLICKHOUSE_HOST')


class KafkaAdminSettings(BaseSettings):
    bootstrap_servers: str = Field(
        default='localhost:9092',
        env='KAFKA_BS_SERVERS'
    )
    offset: str = Field(default='earliset', env='KAFKA_AUTO_OFFSET_RESET')
    group_id: str = Field(..., env='KAFKA_GROUP_ID')
    topics: str = Field(..., env='KAFKA_TOPICS')


class ETLSettings(BaseSettings):
    batch_size: int = Field(default=1000, env='ETL_BATCH_SIZE')
    refresh_time: int = Field(default=5, env='ETL_REFRESH_TIME')
    debug: bool = Field(default=True, env='UGC_ETL_DEBUG')
