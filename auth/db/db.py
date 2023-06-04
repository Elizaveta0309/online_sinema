from config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

dsl = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}' \
      f'@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/postgres'

engine = create_engine(dsl)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
