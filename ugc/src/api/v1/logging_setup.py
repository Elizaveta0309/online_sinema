import logging
from logging.handlers import RotatingFileHandler
from typing import Any

LOG_FORMAT = '{"log_api":"%(asctime)s - %(levelname)s - %(name)s - %(message)s"} {"request_id": "%(request_id)s"}'

old_factory = logging.getLogRecordFactory()


def record_factory(*args, request_id: str = "", **kwargs) -> Any:
    """Adding requist_id."""
    record = old_factory(*args, **kwargs)
    record.request_id = request_id
    return record


def setup_root_logger(log_filename: str, logger: logging.Logger) -> None:
    """Logger configs."""
    formatter = logging.Formatter(LOG_FORMAT)
    file_log = RotatingFileHandler(
        filename=log_filename,
        mode='a',
        maxBytes=15000000,
        backupCount=5
    )
    file_log.setFormatter(formatter)
    logger.addHandler(file_log)
    logging.setLogRecordFactory(record_factory)
    logger.setLevel(logging.INFO)
