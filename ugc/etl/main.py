from clickhouse_driver import Client
from confluent_kafka import Consumer
from dotenv import load_dotenv
from etl_extr import ETL
from extractor import KafkaBroker
from loader import ClickHouseLoader
from pre_start import check_clickhouse_inited
from transformer import KafkaTransformer
from utils.config import ClickHouseSettings, ETLSettings, KafkaAdminSettings
from utils.log import setup_logger
from utils.offset_registry import DictOffsetRegistry

from models.film_view import FilmView

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
        'bootstrap.servers': kafka_config.bootstrap_servers,
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
