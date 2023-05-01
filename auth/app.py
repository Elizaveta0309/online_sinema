from authlib.integrations.flask_client import OAuth
from flasgger import Swagger
from flask import Flask

from middleware import ExceptionHandlerMiddleware

app = Flask(__name__)
swagger = Swagger(app)
app.wsgi_app = ExceptionHandlerMiddleware(app.wsgi_app)
app.secret_key = 'asdasd'

oauth = OAuth(app)

# noinspection PyUnresolvedReferences
from api.v1.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
