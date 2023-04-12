import uuid
from datetime import datetime, timedelta
from datetime import timezone

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import DataError, PendingRollbackError

from config import settings
from db import Base, db_session
from utils.utils import encrypt_password, jwt_encode


class Mixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    def save(self):
        try:
            db_session.add(self)
            db_session.commit()
        except (PendingRollbackError, DataError) as e:
            db_session.rollback()
            raise e


class Role(Base, Mixin):
    DEFAULT_ROLE = 'user'
    __tablename__ = 'role'

    title = Column(String, nullable=False)

    def __repr__(self):
        return f'<Role {self.title}>'

    @classmethod
    def get_default_role(cls):
        return cls.query.filter_by(title=cls.DEFAULT_ROLE).first().id


class User(Base, Mixin):
    __tablename__ = 'user'

    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(ForeignKey('role.id'))

    def __init__(self, login, password):
        self.login = login
        self.password = encrypt_password(password)
        self.role = Role.get_default_role()

    def __repr__(self):
        return f'<User {self.login}>'

    def generate_tokens(self):
        role = Role.query.filter_by(id=self.role).first().title
        token_data = {
            'user_id': str(self.id),
            'role': role,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXP)
        }
        refresh_data = {
            'user_id': str(self.id),
            'role': role,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_EXP)
        }
        return jwt_encode(token_data), jwt_encode(refresh_data)

    def check_password(self, password):
        return encrypt_password(password) == self.password


class RefreshToken(Base, Mixin):
    __tablename__ = 'refresh_token'

    token = Column(String, nullable=False, unique=True)
    user = Column(ForeignKey('user.id'))

    def __repr__(self):
        return f'<RefreshToken {self.id}>'
