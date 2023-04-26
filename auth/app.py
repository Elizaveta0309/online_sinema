from flask import Flask
from flasgger import Swagger

from middleware import ExceptionHandlerMiddleware

app = Flask(__name__)
swagger = Swagger(app)
app.wsgi_app = ExceptionHandlerMiddleware(app.wsgi_app)


# noinspection PyUnresolvedReferences
from api.v1.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

