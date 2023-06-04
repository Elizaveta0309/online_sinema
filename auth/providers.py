import flask
import flask_injector
import injector
from config import settings
from utils.storage import Blacklist, RedisStorage

from services import LoginRequest


class BlacklistModule(injector.Module):
    def configure(self, binder):
        binder.bind(
            Blacklist,
            to=self.create,
            scope=flask_injector.request
        )

    def create(self):
        storage = RedisStorage(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT
        )

        return Blacklist(storage)


class LoginRequestModule(injector.Module):
    def configure(self, binder):
        binder.bind(
            LoginRequest,
            to=self.create,
            scope=flask_injector.request
        )

    @staticmethod
    def create():
        return LoginRequest()
