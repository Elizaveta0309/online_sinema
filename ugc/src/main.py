from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from aiokafka import AIOKafkaProducer
import sentry_sdk
from ugc.src.api.v1 import time_code
from ugc.src.config import settings
from ugc.src.db import kafka_cluster
from ugc.src.api.v1 import likes


if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=settings.traces_sample_rate,
    )

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    debug=True
)


@app.on_event('startup')
async def startup():
    kafka_cluster.producer = AIOKafkaProducer(
        bootstrap_servers=['broker:29092']
    )
    await kafka_cluster.producer.start()


@app.on_event('shutdown')
async def shutdown():
    await kafka_cluster.producer.stop()


# Подключаем роутер к серверу, указав префикс /v1/time_code
# Теги указываем для удобства навигации по документации
app.include_router(
    time_code.router,
    prefix='/api/v1/time_code',
    tags=['time_code']
)
app.include_router(likes.router, prefix="/api/v1/likes", tags=["likes"])
