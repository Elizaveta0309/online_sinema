from clickhouse_driver import Client
from pre_start import check_kafka_topics, check_clickhouse_inited
from confluent_kafka import Consumer

ch = Client(
    host='localhost'
)

check_clickhouse_inited(ch)