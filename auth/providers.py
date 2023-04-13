import flask
import flask_injector
import injector
from config import settings
from utils.storage import Blacklist, RedisStorage


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
