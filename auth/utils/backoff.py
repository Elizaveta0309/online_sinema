import logging
import time
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)


def backoff(
        start_sleep_time: float = 0.1,
        factor: int = 2,
        border_sleep_time: float = 10,
) -> Callable:
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            n = 0

            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(e)
                    if sleep_time >= border_sleep_time:
                        sleep_time = border_sleep_time
                    else:
                        sleep_time = start_sleep_time * factor ** n

                    time.sleep(sleep_time)
                    n += 1
        return inner
    return func_wrapper
