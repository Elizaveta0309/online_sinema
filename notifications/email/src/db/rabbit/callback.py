import orjson
from models.notification import NotificationEmail
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from sender.email_sender import send_message


def callback(
    chanel: BlockingChannel,
    method: Basic.Deliver,
    # properties: BasicProperties,
    body: bytes,
) -> None:
    """Processing incoming data to the message sending function."""
    body_json = orjson.loads(body)
    notification = NotificationEmail(**body_json)
    send_message(email=notification.email, content=notification.content)
    chanel.basic_ack(delivery_tag=method.delivery_tag)
