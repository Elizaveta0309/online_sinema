import logging
import time
from confluent_kafka import Consumer
from clickhouse_driver import Client
from utils.config import KafkaAdminSettings, ClickHouseSettings


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def check_kafka_topics(c: Consumer):
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
    c.close()
    


def check_clickhouse_inited(c: Client):
    """
    Проверка наличия нужных БД и таблиц в CH.
    """
    logger.info('[ClickHouse]: Healthcheck started.')
    while True:
        databases = c.execute("SHOW DATABASES")

        if 'analysis' not in [db[0] for db in databases]:
            logger.warning(
                f"Couldn't find \"analysis\" database."
            )
            continue

        c.execute(f"USE analysis")

        tables = c.execute("SHOW TABLES")

        if 'viewed_progress_repl' not in [tbl[0] for tbl in tables]:
            logger.warning(
                "[ClickHouse]: Couldn't find \"viewed_progress_repl\" table."
            )
            continue
        
        logger.info('[ClickHouse]: Healthcheck complete.')
        c.disconnect()
        break