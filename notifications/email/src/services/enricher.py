from abc import ABC, abstractmethod
from typing import Dict, Optional

import backoff as backoff
import orjson
import requests

from notifications.email.src.models.transform import OrjsonModel


class BaseEnricher(ABC):
    def __init__(self, url: str, target_model: OrjsonModel) -> None:
        self.url = url
        self.target_model = target_model
    @abstractmethod
    def get_data(self, id: str):
        pass


class ModelEnricher(BaseEnricher):
    """ Обогащает данными из внешних сервисов via API. """
    @backoff.on_exception(
            backoff.expo,
            requests.exceptions.ConnectionError
    )
    def get_data(
            self,
            id: str,
            params: Dict = None,
            cookies: Dict = None) -> Optional[OrjsonModel]:
        """Запрос модели у сервиса по id."""

        response = requests.get(self.url + id, params=params, cookies=cookies)

        if response.status_code == 404:
            return None

        response.raise_for_status()
        body_json = orjson.loads(response.text)

        return self.target_model(**body_json)


class FakeEnricher(BaseEnricher):
    """ Обогащает данными, взятыми из фикстур. """
    def __init__(self, fixtures: Dict, target_model: OrjsonModel) -> None:
        self.fixtures = fixtures
        self.target_model = target_model

    def get_data(self, id: str) -> Optional[OrjsonModel]:
        """Запрос модели у сервиса по id."""
        try:
            raw_data = self.fixtures[id]
        except KeyError:
            return None

        return self.target_model(**raw_data)
