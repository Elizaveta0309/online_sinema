from core.add_queue import add_queue
from core.config import settings
from core.logger import configure_logging
from core.start_up import start_up
from db.rabbit.callback import callback
from db.rabbit.rabbitmq import get_rabbit

configure_logging()


def main() -> None:
    add_queue()
    rabbit = get_rabbit()
    rabbit.start_consume(callback)


if __name__ == "__main__":
    start_up()
    main()
