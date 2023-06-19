from typing import Any, Dict

from notifications.email.src.services.enricher import BaseEnricher
from notifications.email.src.services.mailer import BaseMailer
from notifications.email.src.services.templater import BaseTemplater

import orjson
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import logging


class EventNotImplementedError(Exception):
    pass


class Worker:
    def __init__(
            self,
            mailer: BaseMailer,
            templater: BaseTemplater,
            enrichers: Dict[str, BaseEnricher],
    ) -> None:
        self.mailer = mailer
        self.templater = templater
        self.enrichers = enrichers

    def handle(
        self,
        channel: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        body_json = orjson.loads(body)
        event_type = body_json['event_type']
        user_id = body_json['user_id']

        try:
            template = self.templater.get_template(event_type)
        except Exception:
            logging.error('Mistake while getting temlate.')
            channel.basic_ack(method.delivery_tag)
            return

        try:
            user_data = self.enrichers['user'].get_data(user_id)
        except Exception:
            logging.error('Mistake while getting users data.')
            channel.basic_ack(method.delivery_tag)
            return

        try:
            context = self._get_context(event_type, body_json)
        except EventNotImplementedError:
            logging.error('Неизвестный тип события.')
            return

        email_content = self.templater.render_template(template, context)
        try:
            self.mailer.send_message(
                email=user_data.email,
                content=email_content,
                subject=template.subject
            )
        except Exception as e:
            logging.error('Mistake while sending letter.', exc_info=e)
            channel.basic_ack(method.delivery_tag)

    def _get_context(self, event_type, message: Dict[str, Any]):
        if event_type == 'notification_about_new_film':
            return self.enrichers['movie'].get_data(message['movie_id'])
        else:
            raise EventNotImplementedError
