from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

dsl = 'postgresql://postgres:postgres@localhost/postgres'  # TODO заменить
engine = create_engine(dsl)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # Здесь необходимо импортировать все модули с моделями, которые должны зарегистрироваться в ORM.
    # В противном случае их нужно импортировать до вызова init_db()
    # Это необходимо, чтобы sqlalchemy увидел все таблицы и при необходимости создал их.
    Base.metadata.create_all(bind=engine)
