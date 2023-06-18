from typing import Any, Dict, List, Optional

import backoff as backoff
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor


class Postgres():
    def __init__(self, dsn: Dict[str, Any]) -> None:
        self.dsn = dsn

    @backoff.on_exception(backoff.expo, psycopg2.OperationalError)
    def exec(
            self,
            template: sql.SQL,
            args: Optional[Dict[str, Any]]) -> Optional[List[Dict[Any, Any]]]:
        """Performs a transaction and returns a response (if any)."""

        with psycopg2.connect(dsn=self.dsn, cursor_factory=DictCursor) \
                as connection:
            with connection.cursor() as cursor:
                cursor.execute(template, args)
                try:
                    results = [dict(item) for item in cursor.fetchall()]
                except psycopg2.ProgrammingError:
                    return None

        return results
