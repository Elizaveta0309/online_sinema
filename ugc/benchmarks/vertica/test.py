import time
from functools import wraps

import vertica_python

from research.vertica.data import generate_line

dns = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'use_prepared_statements': True,
}


def measure(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.time()
            print(end - start)
            print('\n')

    return inner


@measure
def insert_n_rows(dns, n):
    query = 'INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)'
    print('Lines:', n)
    print(query)
    cursor = dns.cursor()
    values = [generate_line() for i in range(n)]
    try:
        cursor.executemany(query, values)
    except Exception as e:
        raise e
    cursor.close()


@measure
def execute_query(dns, query: str, show_result: bool = True):
    print(query)
    cursor = dns.cursor()
    cursor.execute(query)
    if show_result:
        for line in cursor.iterate():
            print(line)
    cursor.close()


if __name__ == '__main__':
    connection = vertica_python.connect(**dns)

    select_count = 'SELECT COUNT(*) FROM views'
    execute_query(connection, select_count)

    select_unique_movie_id = 'SELECT count(DISTINCT movie_id) FROM views'
    execute_query(connection, select_unique_movie_id)

    select_unique_user_id = 'SELECT count(DISTINCT user_id) FROM views'
    execute_query(connection, select_unique_user_id)

    insert_n_rows(connection, 1000)

    execute_query(connection, select_count)

    connection.commit()
    connection.close()
