from contextlib import contextmanager

import psycopg2
from elasticsearch import Elasticsearch
from psycopg2.extras import RealDictCursor


@contextmanager
def es_connection(dsn: str):
    host, port = dsn['host'], dsn['port']
    es_conn_string = f'http://{host}:{port}/'

    es_connection = Elasticsearch(es_conn_string)

    try:
        yield es_connection
    finally:
        es_connection.close()


@contextmanager
def pg_connection(dsn: dict):
    pg_conn = psycopg2.connect(**dsn, cursor_factory=RealDictCursor)
    pg_conn.set_session(autocommit=True)

    try:
        yield pg_conn
    finally:
        pg_conn.close()
