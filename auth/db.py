from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import settings

dsl = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}' \
      f'@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/postgres'

dsl = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}' \
      f'@localhost:5433/postgres'

engine = create_engine(dsl)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
