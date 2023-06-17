import logging
from core.add_queue import add_queue
from core.config import settings
from core.logger import configure_logging
from core.start_up import start_up
from db.rabbit.rabbitmq import get_rabbit

from notifications.email.src.db.psql.postgres import Postgres
from notifications.email.src.models.movie import Movie
from notifications.email.src.models.user import User
from notifications.email.src.services.enricher import ModelEnricher
from notifications.email.src.services.mailer import SendGridMailer
from notifications.email.src.services.templater import PostgresTemplater
from notifications.email.src.services.worker import Worker

# В будущем тут могут появиться review и прочие сущности. Наверное.

MODEL_SCHEMA = {
    'movie': {
        'url': 'http://localhost/api/v1/auth/users',
        'target_model': Movie
    },
    'user': {
        'url': 'http://localhost/api/v1/movies/',
        'target_model': User
    }
}


configure_logging()


def main() -> None:
    add_queue()
    rabbit = get_rabbit()
    logging.info('RabbitMQ connection established.')

    postgres_connection = Postgres()
    logging.info('Postgres connection established.')

    templater = PostgresTemplater(
        postgres_connection
    )
    logging.info('Templater configured.')

    mailer = SendGridMailer(
        email=settings.EMAIL_FROM,
        api_key=settings.SENDGRID
    )
    logging.info('Mailer configured.')

    enrichers = {
        entity: ModelEnricher(**conf)
        for entity, conf in MODEL_SCHEMA.items()
    }

    worker = Worker(
        mailer=mailer,
        templater=templater,
        enrichers=enrichers
    )

    rabbit.start_consume(worker.handle)


if __name__ == "__main__":
    start_up()
    main()
