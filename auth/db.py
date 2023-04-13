import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import settings

dsl = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}' \
      f'@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/postgres'

engine = create_engine(dsl)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def create_default_role():
    from models import Role
    if not Role.query.filter_by(title='user').first():
        r = Role(title='user')
        r.save()


def init_db():
    # Здесь необходимо импортировать все модули с моделями, которые должны зарегистрироваться в ORM.
    # В противном случае их нужно импортировать до вызова init_db()
    # Это необходимо, чтобы sqlalchemy увидел все таблицы и при необходимости создал их.

    # noinspection PyUnresolvedReferences
    from models import RefreshToken, Role, User
    while True:
        try:
            Base.metadata.create_all(bind=engine)
            create_default_role()
            break
        except OperationalError:
            time.sleep(1)
