from flask import Flask

from db import init_db

app = Flask(__name__)
init_db()


# noinspection PyUnresolvedReferences
from api.v1.views import *
