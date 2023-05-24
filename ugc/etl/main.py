from clickhouse_driver import Client
from utils.log import setup_logger
from pre_start import check_kafka_topics, check_clickhouse_inited
from confluent_kafka import Consumer
from etl import ETL
import logging

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
    logger = setup_logger(
        name=__name__,
        debug=etl_config.debug
    )
    
    logger.info('[Main]: Initializing...')

    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': kafka_config.group_id,
        'auto.offset.reset': kafka_config.offset
    })
    c.subscribe(kafka_config.topics.split(','))
    logger.info('[Main]: Connected to Kafka')

    ch = Client(
        host=clickhouse_config.host
    )
    logger.info('[Main]: Connected to ClickHouse')

    check_clickhouse_inited(ch, logger)
    #check_kafka_topics(c, logger)
    
    registry = DictOffsetRegistry()
    extractor = KafkaBroker(
        consumer=c,
        logger=logger,
        offset_registry=registry
    )
    transformer = KafkaTransformer(
        target_model=FilmView,
        logger=logger
    )
    loader = ClickHouseLoader(
        client=ch,
        logger=logger
    )

    etl = ETL(
        extractor=extractor,
        transformer=transformer,
        loader=loader,
        batch_size=etl_config.batch_size,
        logger=logger
    )

    etl.start(50)