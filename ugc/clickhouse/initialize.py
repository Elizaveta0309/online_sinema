import logging
import time

from clickhouse_driver import Client
from clickhouse_driver.errors import Error

logging.basicConfig(
    format='[%(asctime)s]\t[%(levelname)s]\t%(message)s',
    level=logging.INFO
)


# connect to db
def connection() -> Client:
    while True:
        try:
            return Client("clickhouse-node1")
        except Error as e:
            logging.error(e)
            logging.info("Connection in progress")
            time.sleep(1)


# initialize cluster
def init_cluster(client: Client):
    client.execute(
        "CREATE DATABASE analysis ON CLUSTER 'company_cluster';"
    )
    client.execute(
        """
        CREATE TABLE analysis.viewed_progress_repl ON CLUSTER 'company_cluster' (
            `user_id` String,
            `film_id` String,
            `viewed_frame` UInt64,
            `created_at` DateTime
        ) Engine = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/table', '{replica}')
        PARTITION BY toYYYYMMDD(created_at)
        ORDER BY created_at;
        """
    )
    client.execute(
        """
        CREATE TABLE
            analysis.viewed_progress
        ON CLUSTER 'company_cluster' AS analysis.viewed_progress_repl
        ENGINE = Distributed('company_cluster', analysis, viewed_progress_repl, rand());
        """
    )


if __name__ == '__main__':
    logging.info('Connection in progress.')
    client = connection()
    logging.info('Init cluster - done.')
    init_cluster(client)
    logging.info('Success.')
