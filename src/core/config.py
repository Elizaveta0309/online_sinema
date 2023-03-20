import os
from logging import config as logging_config

from dotenv import load_dotenv

from src.core.logger import LOGGING

load_dotenv()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME')

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))

# Настройки Elasticsearch
ES_HOST = os.getenv('ES_HOST')
ES_PORT = int(os.getenv('ES_PORT'))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

CACHE_EXPIRE_IN_SECONDS = 60 * 5

PAGE_SIZE = 20

FILMS_SEARCH_FIELD = 'title'
PERSONS_SEARCH_FIELD = 'full_name'
GENRES_SEARCH_FIELD = 'name'
