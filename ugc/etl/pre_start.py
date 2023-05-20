import logging
import time
from confluent_kafka import Consumer
from clickhouse_driver import Client
from utils.config import KafkaAdminSettings, ClickHouseSettings


def check_kafka_topics(c: Consumer):
    """
    Проверка наличия нужных топиков в Kafka.
    """
    print('[Kafka]: Healthcheck started.')
    kafka_topics = ['views']
    while True:
        topic_metadata = c.list_topics()

        if not all(topic_metadata.topics.get(topic) for topic in kafka_topics):
            print('[Kafka]: Couldn\'t find topic.')
            time.sleep(5)
            continue
        break
    
    print('[Kafka]: Healthcheck complete.')
    


def check_clickhouse_inited(c: Client):
    """
    Проверка наличия нужных БД и таблиц в CH.
    """
    print('[ClickHouse]: Healthcheck started.')
    while True:
        databases = c.execute("SHOW DATABASES")
        if 'analysis' not in [db[0] for db in databases]:
            print(
                f"Couldn't find \"analysis\" database."
            )
            continue
        print('[Clickhouse]: Found DB.')

        c.execute(f"USE analysis")

        tables = c.execute("SHOW TABLES")

        if 'viewed_progress' not in [tbl[0] for tbl in tables]:
            print(
                "[ClickHouse]: Couldn't find \"viewed_progress\" table."
            )
            continue
        print('[Clickhouse]: Found table.')
        
        print('[ClickHouse]: Healthcheck complete.')
        c.disconnect()
        break