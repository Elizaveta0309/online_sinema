from flask import Flask

from db import init_db

app = Flask(__name__)
init_db()

# noinspection PyUnresolvedReferences
from api.v1.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
