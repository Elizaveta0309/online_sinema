from flasgger import Swagger
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import settings

from middleware import ExceptionHandlerMiddleware

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
    strategy='fixed-window',
    default_limits=[
        f'{settings.REQUEST_NUM_LIMIT} per {settings.REQUEST_TIME_LIMIT}'
    ]
)

swagger = Swagger(app)
app.wsgi_app = ExceptionHandlerMiddleware(app.wsgi_app)

# noinspection PyUnresolvedReferences
from api.v1.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
