import http
import logging
import time

from dateutil.relativedelta import relativedelta
from delivery_client import DeliveryClient
from storage.postgresql import PostgresStorage

from core.config import ApiConfig, PSQConfig

from .models import AdminNotification, Frequency

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_next_date(date, frequency):
    if frequency == Frequency.once.value:
        return None
    mapping = {
        Frequency.daily.value: 'days',
        Frequency.weekly.value: 'weeks',
        Frequency.monthly.value: 'months',
    }
    kwargs = {mapping[frequency]: 1}
    return date + relativedelta(**kwargs)


storage = PostgresStorage(PSQConfig().dict())
api = DeliveryClient(**ApiConfig().dict())

if __name__ == '__main__':
    logger.info('Scheduler is ready')
    while True:
        admin_events = storage.get_event()

        for event in admin_events:
            admin_event = AdminNotification(**event)
            next_date = get_next_date(
                admin_event.next_planned_date,
                admin_event.frequency.value,
            )

            response = api.send(
                delivery_type=admin_event.channel.value,
                group=admin_event.user_group,
                template_id=admin_event.template_id,
                subject=admin_event.subject,
                priority=admin_event.priority.value,
            )
            if response.status_code == http.HTTPStatus.OK:
                storage.update_event(
                    admin_event.id,
                    next_date,
                )
            time.sleep(1)
