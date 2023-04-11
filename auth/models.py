import uuid
from datetime import datetime
from datetime import timezone

import jwt
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import DataError, PendingRollbackError

from config import settings
from db import Base, db_session
from utils.utils import encrypt_password


class Role(Base):
    __tablename__ = 'role'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(ForeignKey('role.id'))

    def __init__(self, login, password, role):
        self.login = login
        self.password = encrypt_password(password)
        self.role = role

    def __repr__(self):
        return f'<User {self.login}>'

    def save(self):
        try:
            db_session.add(self)
            db_session.commit()
        except (PendingRollbackError, DataError) as e:
            db_session.rollback()
            raise e

    def generate_tokens(self):
        role = Role.query.filter_by(id=self.role).first().title
        params = [
            {'role': role, 'exp': datetime.now(timezone.utc)},
            settings.SECRET
        ]
        return jwt.encode(*params), jwt.encode(*params)

    def check_password(self, password):
        return encrypt_password(password) == self.password
