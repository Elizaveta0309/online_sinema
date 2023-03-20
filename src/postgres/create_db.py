import json
from contextlib import closing

import psycopg2

from src.core.config import settings

POSTGRES_CREDENTIALS = {
    'host': settings.POSTGRES_HOST,
    'port': settings.POSTGRES_PORT,
    'user': settings.POSTGRES_USER,
    'password': settings.POSTGRES_PASSWORD,
    'dbname': settings.POSTGRES_DB,
}


def check_bd_exists():
    with closing(psycopg2.connect(**POSTGRES_CREDENTIALS)) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'content';")
            return bool(cursor.fetchall())


def drop_db():
    with closing(psycopg2.connect(**POSTGRES_CREDENTIALS)) as conn:
        with conn.cursor() as cursor:
            cursor.execute('drop schema if exists content cascade')
            cursor.execute('commit')


def create_tables():
    with closing(psycopg2.connect(**POSTGRES_CREDENTIALS)) as conn:
        with conn.cursor() as cursor:
            with open('src/postgres/movies_database.ddl', 'r') as f:
                sql = f.read()
                cursor.execute(sql)
                cursor.execute('commit')


def populate_db():
    with closing(psycopg2.connect(**POSTGRES_CREDENTIALS)) as conn:
        with conn.cursor() as cursor:
            with open('src/postgres/payload.json', 'r') as f:
                payload = json.loads(f.read())

            payload = [entry for entry in payload if entry['model'] in {
                'movies.filmwork',
                'movies.genre',
                'movies.person',
                'movies.personfilmwork',
                'movies.genrefilmwork',
            }]

            tables_mapping = {
                'movies.filmwork': 'film_work',
                'movies.genre': 'genre',
                'movies.person': 'person',
                'movies.personfilmwork': 'person_film_work',
                'movies.genrefilmwork': 'genre_film_work',
            }

            for entry in payload:
                table = tables_mapping[entry['model']]
                id_ = entry['pk']
                fields = tuple(field for field, value in entry['fields'].items() if value)
                values = tuple([id_] + [str(entry['fields'][field]).replace("'", "''") for field in fields])
                values = ', '.join(f"'{value}'" for value in values)
                values = f'({values})'
                sql = f'insert into content.{table} (id,{",".join(fields)}) values {values} on conflict do nothing'
                cursor.execute(sql)
            cursor.execute('commit')


def create_db():
    drop_db()
    create_tables()
    populate_db()
