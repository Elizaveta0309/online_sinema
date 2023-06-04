import logging
import sys

fmt = '%(asctime)s - %(levelname)s - %(message)s'


def setup_logger(name: str, debug: bool):
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt=fmt)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.addHandler(handler)

    return logger
