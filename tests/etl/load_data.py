import time
from etl_component import ETL
from extractor import PostgresExtractor
from loader import ElasticLoader
from transformer import Transformer
from utils.backoff import backoff
from utils.config import (
    ElasticConfig,
    PostgresConfig,
    RedisConfig,
    CommonConfig
)
from utils.state import ModifiedState, RedisStorage
from utils.log import setup_logger
from dotenv import load_dotenv

from utils.connection_manager import (
    pg_connection,
    es_connection
)


load_dotenv()


@backoff()
def connect_to_pg(dsn: dict):
    return pg_connection(dsn)


@backoff()
def connect_to_es(dsn: dict):
    return es_connection(dsn)


if __name__ == '__main__':
    common_conf = CommonConfig()

    logger = setup_logger(
        name=__name__,
        debug=common_conf.debug
    )

    pg_conf = PostgresConfig()
    es_conf = ElasticConfig()
    redis_conf = RedisConfig()

    with connect_to_pg(pg_conf.dict()) as pg_conn, \
         connect_to_es(es_conf.dict()) as es_conn:

        storage = RedisStorage(**redis_conf.dict())
        state = ModifiedState(storage)

        extractor = PostgresExtractor(
            state=state,
            batch_size=100,
            logger=logger,
            pg_conn=pg_conn
        )

        transformer = Transformer(logger)

        loader = ElasticLoader(
            state=state,
            logger=logger,
            es_conn=es_conn,
        )

        etl = ETL(
            logger=logger,
            extractor=extractor,
            transformer=transformer,
            loader=loader,
            state=state
        )

        while True:
            logger.info('Starting process')
            try:
                etl.start()
            except Exception as e:
                logger.error(f'Error in etl process: {e}')
                state.clear_modified_id_list()

            time.sleep(common_conf.sleep_time)
