from flasgger import Swagger
from flask import Flask
from authlib.integrations.flask_client import OAuth

from config import settings
from middleware import ExceptionHandlerMiddleware

app = Flask(__name__)
swagger = Swagger(app)
app.wsgi_app = ExceptionHandlerMiddleware(app.wsgi_app)
app.secret_key = 'asdasd'

oauth = OAuth(app)
oauth.register(
    name='vk',
    authorize_url='https://oauth.vk.com/authorize',
    access_token_url='https://oauth.vk.com/access_token',
    client_id='51629723',
    client_secret=settings.VK_ACCESS_TOKEN
)

# noinspection PyUnresolvedReferences
from api.v1.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
