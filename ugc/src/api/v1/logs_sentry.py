import logging
import random
from typing import Any, Optional

from fastapi import APIRouter, Request
from logging_setup import setup_root_logger

log_filename = 'logs/elk.log'
LOGGER = logging.getLogger(__name__)
setup_root_logger(log_filename, LOGGER)
# Get logger for module

LOGGER.info('---Starting App---')
router = APIRouter()


class RequestIdFilter(logging.Filter):
    def __init__(self, request: Optional[Request] = None) -> None:
        super().__init__()
        self.request = request

    def filter(self, record: Any) -> bool:
        if self.request:
            record.request_id = self.request.headers.get('x-request-id')
        return True


@router.get(
    '/',
    summary='Тестирование логирования',
    response_description='Тестирование логирования данных',
)
async def index(request: Request) -> str:
    result = random.randint(1, 50)
    LOGGER.addFilter(RequestIdFilter(request))
    LOGGER.info(f"Пользователю досталось число {result}")
    return f"Ваше число {result}!"


@router.get(
    '/sentry-debug',
    summary='Тестирование sentry',
    response_description='Используется для тестирования sentry',
)
async def trigger_error(request: Request) -> None:
    """
     Sentry testing.
    """
    _ = 1 / 0
