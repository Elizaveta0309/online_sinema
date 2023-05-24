from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from aiokafka import AIOKafkaProducer

from src.api.v1 import time_code
from src.config import settings
from src.db import kafka_cluster

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    debug=True
)


@app.on_event('startup')
async def startup():
    kafka_cluster.producer = AIOKafkaProducer(bootstrap_servers=['broker:29092'])
    await kafka_cluster.producer.start()


@app.on_event('shutdown')
async def shutdown():
    await kafka_cluster.producer.stop()


# Подключаем роутер к серверу, указав префикс /v1/time_code
# Теги указываем для удобства навигации по документации
app.include_router(time_code.router, prefix='/api/v1/time_code', tags=['time_code'])
