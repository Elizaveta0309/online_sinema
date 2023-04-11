from abc import ABC, abstractmethod

import redis
from utils.backoff import backoff


class BaseStorage(ABC):
    @abstractmethod
    def add_to_list(self, list_name: str, value) -> None:
        """Добавить в список значение. Если список не существует, создать."""
        pass

    @abstractmethod
    def clear_list(self, list_name: str) -> None:
        """Очистить список"""
        pass

    @abstractmethod
    def get_list(self, list_name: str) -> list[str]:
        """Получить содержимое списка"""
        pass

    @abstractmethod
    def remove_from_list(self, list_name: str, id: str) -> None:
        """Удалить значение из списка"""
        pass


class RedisStorage(BaseStorage):
    def __init__(self, host: str, port: int) -> None:
        self.r = redis.Redis(
            host,
            port,
            charset='utf-8',
            decode_responses=True
        )
        self.ping_redis()

    @backoff()
    def ping_redis(self):
        self.r.ping()

    def add_to_list(self, list_name: str, value) -> None:
        self.r.lpush(list_name, value)

    def clear_list(self, list_name: str) -> None:
        self.r.delete(list_name)

    def get_list(self, list_name: str) -> list[str]:
        return self.r.lrange(list_name, 0, -1)

    def remove_from_list(self, list_name: str, value: str) -> None:
        self.r.lrem(list_name, 0, value)


class Blacklist:
    def __init__(
            self,
            token_storage: BaseStorage) -> None:
        self.storage = token_storage

    def is_expired(self, token: str) -> bool:
        tokens = self.storage.get_list("tokens")
        return token in tokens

    def add_to_expired(self, token: str) -> None:
        self.storage.add_to_list("tokens", token)

    def remove_from_expired(self, token: str) -> None:
        self.storage.remove_from_list("tokens", token)

    def clear(self):
        self.storage.clear_list("tokens")
