from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import redis
from utils.backoff import backoff


class BaseStorage(ABC):
    @abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass

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

    @classmethod
    @abstractmethod
    def remove(self, list_name: str, id: str) -> None:
        """Удалить значение из списка"""
        pass


# Вопрос: нужно ли использовать backoff и для подключения к Redis?
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

    def save_state(self, state: dict) -> None:
        (key, value), = state.items()

        if not isinstance(key, str):
            raise TypeError()

        if isinstance(value, datetime):
            value = value.isoformat()

        self.r.set(key, value)

    def retrieve_state(self, key: str) -> dict:
        if not isinstance(key, str):
            raise TypeError()
        return {key: self.r.get(key)}

    def add_to_list(self, list_name: str, value) -> None:
        self.r.lpush(list_name, value)

    def clear_list(self, list_name: str) -> None:
        self.r.delete(list_name)

    def get_list(self, list_name: str) -> list[str]:
        return self.r.lrange(list_name, 0, -1)

    def remove(self, list_name: str, value: str) -> None:
        self.r.lrem(list_name, 0, value)


class State:
    """
    Класс для хранения состояния при работе с данными,
    чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение
    на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        state = {key: value}
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        state = self.storage.retrieve_state(key)

        return state[key]


class ModifiedState(State):
    """
    State, адаптированный для:
    1. Хранения последней даты изменения индекса
    2. Хранения списка изменененных filmworks
    """

    def __init__(self, storage: BaseStorage):
        super().__init__(storage)

    def set_index_checkpoint(self, index: str, checkpoint: datetime) -> None:
        key = 'modified:{0}'.format(index)
        self.set_state(key, checkpoint)

    def get_index_checkpoint(self, index: str) -> str:
        key = 'modified:{0}'.format(index)
        return self.get_state(key)

    def push_modified_id(self, id: str) -> None:
        self.storage.add_to_list('modified_ids', id)

    def clear_modified_id_list(self) -> None:
        self.storage.clear_list('modified_ids')

    def del_modified_id(self, id: str) -> None:
        self.storage.remove('modified_ids', id)

    def get_modified_movies_list(self) -> list[str]:
        list = self.storage.get_list('modified_ids')
        if list is None or not list:
            return ["00000000-0000-0000-0000-000000000000"]

        return list
