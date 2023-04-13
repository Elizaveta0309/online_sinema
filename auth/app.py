from flask import Flask

from db import init_db

app = Flask(__name__)

# noinspection PyUnresolvedReferences
from api.v1.views import *

if __name__ == '__main__':
    init_db()
