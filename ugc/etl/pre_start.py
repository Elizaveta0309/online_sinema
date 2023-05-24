from logging import Logger
import time
from confluent_kafka import Consumer
from clickhouse_driver import Client
from utils.config import KafkaAdminSettings, ClickHouseSettings


def check_kafka_topics(c: Consumer, logger: Logger):
    """
    Проверка наличия нужных топиков в Kafka.
    """
    logger.info('[Kafka]: Healthcheck started.')
    kafka_topics = ['views']
    while True:
        topic_metadata = c.list_topics()
        if not all(topic_metadata.topics.get(topic) for topic in kafka_topics):
            logger.error('[Kafka]: Couldn\'t find topic.')
            time.sleep(5)
            continue
        break
    
    logger.info('[Kafka]: Healthcheck complete.')
    


def check_clickhouse_inited(c: Client, logger: Logger):
    """
    Проверка наличия нужных БД и таблиц в CH.
    """
    logger.info('[ClickHouse]: Healthcheck started.')
    while True:
        databases = c.execute("SHOW DATABASES")
        if 'analysis' not in [db[0] for db in databases]:
            logger.error(
                f"Couldn't find \"analysis\" database."
            )
            continue
        logger.info('[Clickhouse]: Found DB.')

        c.execute(f"USE analysis")

        tables = c.execute("SHOW TABLES")

        if 'viewed_progress' not in [tbl[0] for tbl in tables]:
            logger.error(
                "[ClickHouse]: Couldn't find \"viewed_progress\" table."
            )
            continue
        logger.info('[Clickhouse]: Found table.')
        
        logger.info('[ClickHouse]: Healthcheck complete.')
        c.disconnect()
        break