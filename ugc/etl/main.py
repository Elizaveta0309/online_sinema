from clickhouse_driver import Client
from pre_start import check_kafka_topics, check_clickhouse_inited
from confluent_kafka import Consumer
from etl import ETL

from utils.offset_registry import DictOffsetRegistry
from extractor import KafkaBroker
from models.film_view import FilmView
from transformer import KafkaTransformer
from loader import ClickHouseLoader
from utils.config import (
    ClickHouseSettings,
    KafkaAdminSettings,
    ETLSettings
)
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    clickhouse_config = ClickHouseSettings()
    kafka_config = KafkaAdminSettings()
    etl_config = ETLSettings()

    c = Consumer({
        'bootstrap.servers': kafka_config.bootstrap_servers,
        'group.id': kafka_config.group_id,
        'auto.offset.reset': kafka_config.offset
    })
    c.subscribe(kafka_config.topics.split(','))

    ch = Client(
        host=clickhouse_config.host,
        port=clickhouse_config.port
    )

    check_clickhouse_inited(ch)
    check_kafka_topics(c)
    registry = DictOffsetRegistry()
    extractor = KafkaBroker(c,registry)
    transformer = KafkaTransformer(FilmView)
    loader = ClickHouseLoader(ch)

    etl = ETL(
        extractor=extractor,
        transformer=transformer,
        loader=loader,
        batch_size=etl_config.batch_size
    )

    etl.start()