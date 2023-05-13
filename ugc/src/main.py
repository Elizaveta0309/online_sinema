from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


from src.api.v1 import time_code
from src.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    debug=True
)

# Подключаем роутер к серверу, указав префикс /v1/time_code
# Теги указываем для удобства навигации по документации
app.include_router(time_code.router, prefix='/api/v1/time_code', tags=['time_code'])

