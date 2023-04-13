import flask_injector
from flask import Flask

from db import init_db
from providers import BlacklistModule

INJECTOR_DEFAULT_MODULES = dict(
    blacklist=BlacklistModule()
)

modules = dict(INJECTOR_DEFAULT_MODULES)

app = Flask(__name__)

flask_injector.FlaskInjector(
    app=app,
    modules=modules.values(),
)

# noinspection PyUnresolvedReferences
from api.v1.views import *

if __name__ == '__main__':
    init_db()
