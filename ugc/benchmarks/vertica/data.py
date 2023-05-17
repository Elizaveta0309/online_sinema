import random
import time
from datetime import datetime
import vertica_python
from tqdm.contrib.concurrent import process_map

dns = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': False,
    'use_prepared_statements': True,
}

user_ids = [str(x) for x in range(10000)]
movie_ids = [str(x) for x in range(10000)]


def database(dns):
    with vertica_python.connect(**dns) as connect:
        cursor = connect.cursor()
        cursor.execute("""
        CREATE TABLE views (
            id IDENTITY,
            user_id VARCHAR(36) NOT NULL,
            movie_id VARCHAR(36) NOT NULL,
            viewed_frame INTEGER NOT NULL,
            event_time DATETIME NOT NULL
        );
        """)


def generate_line() -> tuple:
    line = (random.choice(user_ids), random.choice(movie_ids), random.randint(1, 180), datetime.now())
    return line


def insert_line(x):
    connect = vertica_python.connect(**dns)
    cursor = connect.cursor()
    values = [generate_line() for i in range(1000)]
    start = time.time()
    try:
        cursor.executemany(
            'INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)', values)
    except Exception as e:
        raise e
    cursor.close()
    connect.commit()
    connect.close()
    end = time.time()
    print(end - start)


def generate():
    _max = 10000
    process_map(insert_line, range(0, _max), max_workers=4, chunksize=1)


if __name__ == '__main__':
    generate()
