import uuid
from contextlib import contextmanager
from datetime import datetime
from typing import Dict, Optional, Any

import backoff
import psycopg2
from psycopg2.extras import DictCursor
from storage.base import MainStorage


class PostgresStorage(MainStorage):

    def __init__(self, connection_p: Dict):
        self.connection_p = connection_p

    @contextmanager
    def conn_context(self):
        conn = psycopg2.connect(
            **self.connection_p,
            cursor_factory=DictCursor,
        )
        yield conn
        conn.commit()
        conn.close()

    @backoff.on_exception(wait_gen=backoff.expo, exception=Exception)
    def get_event(self):
        query = (
            'SELECT ns.id, ns.next_planned_date, ns.frequency, ' +
            'ns.user_group, ns.template_id, nt.subject, nt.channel, ' +
            'ns.priority FROM notifications_schedulemail AS ns ' +
            'JOIN notifications_template AS nt ' +
            'ON ns.template_id = nt.id WHERE next_planned_date <= %s'
        )
        with self.conn_context() as conn:
            with conn.cursor() as curs:
                curs.execute(query, (datetime.now(),))
                while row := curs.fetchone():
                    yield row

    @backoff.on_exception(wait_gen=backoff.expo, exception=Exception)
    def update_event(
        self,
        note_id: Optional[uuid.UUID] = None,
        next_date: Optional[Any] = None,
    ):
        next_date = str(next_date) if next_date else None
        query = (
            'UPDATE notifications_schedulemail ' +
            'SET next_planned_date = %s WHERE id = %s'
        )
        with self.conn_context() as conn:
            with conn.cursor() as curs:
                curs.execute(query, (next_date, str(note_id)))
