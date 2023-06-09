import sentry_sdk
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


from src.api.v1 import bookmarks, likes, reviews, time_code
from src.config import settings
from src.db import kafka_cluster
from src.db.mongo import Mongo
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

mongo = Mongo()


# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     docs_url='/api/openapi',
#     openapi_url='/api/openapi.json',
#     default_response_class=ORJSONResponse,
#     debug=True,
# )

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=settings.traces_sample_rate,
    )

# @app.on_event('startup')
# async def startup():
#     kafka_cluster.producer = AIOKafkaProducer(bootstrap_servers=['broker:29092'])
#     await kafka_cluster.producer.start()
#     mongo.client = AsyncIOMotorClient(settings.MONGODB_URL)


# @app.on_event('shutdown')
# async def shutdown():
#     await kafka_cluster.producer.stop()
#     mongo.client.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka_cluster.producer = AIOKafkaProducer(
        bootstrap_servers=['broker:29092']
    )
    await kafka_cluster.producer.start()
    mongo.client = AsyncIOMotorClient(settings.MONGODB_URL)
    yield
    await kafka_cluster.producer.stop()
    mongo.client.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    debug=True,
    lifespan=lifespan
)


app.include_router(
    time_code.router,
    prefix='/api/v1/time_code',
    tags=['time_code']
)
app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])
app.include_router(reviews.router, prefix='/api/v1/review', tags=['review'])
