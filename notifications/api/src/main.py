from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from pika import BlockingConnection, PlainCredentials, URLParameters

from src.db.rabbit import publisher, AsyncRabbitPublisher
from src.config import settings
from contextlib import asynccontextmanager

from notifications.api.src.api.v1 import notifications


@asynccontextmanager
async def lifespan(app: FastAPI):
    credentials = PlainCredentials('guest', 'guest')
    parameters = URLParameters('rabbitmq',
                               5672,
                               '/',
                               credentials)
    rabbit_connect = BlockingConnection(parameters)
    publisher.channel = rabbit_connect.channel()
    yield
    rabbit_connect.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    debug=True,
    lifespan=lifespan
)

app.include_router(
    notifications.router,
    prefix='/api/v1/notifications',
    tags=['notifications']
)
