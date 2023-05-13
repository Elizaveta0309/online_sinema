import logging
import time
from clickhouse_driver import Client
from clickhouse_driver.errors import Error


logging.basicConfig(format='[%(asctime)s]\t[%(levelname)s]\t%(message)s', level=logging.INFO)



def connect() -> Client:
    while True:
        try:
            return Client("clickhouse-node1")
        except Error as e:
            logging.error(e)
            logging.info("Connection in progress.")
            time.sleep(1)


# initialize clickhouse
