import uuid
import enum

from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class Role(enum.Enum):
    superadmin = 'superadmin'
    admin = 'admin'
    user = 'user'


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.user, nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return f'<User {self.login}>'
