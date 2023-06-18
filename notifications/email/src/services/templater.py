from models.template import Template as EmailTemplate
from db.psql.postgres import Postgres
from psycopg2.sql import SQL
from jinja2 import Environment

TEMPLATE_QUERY = """
    SELECT *
    FROM notifications_template
    WHERE event = '%s';
    """


class BaseTemplater:
    """ Базовый сервис работы с шаблонами писем. """
    def get_template(self, name: str) -> EmailTemplate:
        pass

    def render_template(self, template: EmailTemplate, context: dict) -> str:
        pass


class PostgresTemplater(BaseTemplater):
    """ Сервис работы с шаблонами писем, хранящимися в Postgres. """
    def __init__(self, pg_conn: Postgres) -> None:
        self.environment = Environment()
        self.pg_conn = pg_conn

    def get_template(self, name: str) -> EmailTemplate:
        templates = self.pg_conn.exec(
            SQL(TEMPLATE_QUERY).format(name)
        )
        return EmailTemplate(**templates[0])

    def render_template(self, template: str, context: dict) -> str:
        email_template = self.environment.from_string(template)
        return email_template.render(**context)
