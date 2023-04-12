from flask import Flask

from db import init_db

app = Flask(__name__)

# noinspection PyUnresolvedReferences
from api.v1.views import *


# TODO убрать
def create_user():
    if not User.query.filter_by(login='admin').first():
        u = User(login='admin', password='admin')
        u.save()


if __name__ == '__main__':
    init_db()
    create_user()  # TODO убрать
    app.run()
