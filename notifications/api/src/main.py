from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.db.rabbit import get_rabbit
from src.config import settings
from contextlib import asynccontextmanager

from notifications.api.src.api.v1 import notifications

rabbit = get_rabbit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbit.channel = rabbit.connection.channel()
    yield
    rabbit.connection.close()

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