from logging import config as logging_config


def configure_logging() -> None:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_default_handlers = [
        "console",
    ]

    logging = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {"format": log_format},
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "": {
                "handlers": log_default_handlers,
                "level": "INFO",
            },
        },
        "root": {
            "level": "DEBUG",
            "formatter": "verbose",
            "handlers": log_default_handlers,
        },
    }
    logging_config.dictConfig(logging)
