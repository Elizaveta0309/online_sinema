from logging import Logger
from typing import Any, Iterator, List

from pydantic import BaseModel, ValidationError


class BaseTransformer:
    def __init__(self, target_model: BaseModel, logger: Logger) -> None:
        self.target_model = target_model
        self.logger = logger
    def transform(self, data: List[Any]) -> List[Any]:
        pass


class KafkaTransformer(BaseTransformer):
    def transform(self, data: List[Any]) -> List[Any]:
        res = []
        for record in data:
            try:
                res.append(self.target_model.parse_raw(record))
            except ValidationError as e:
                self.logger.error(
                    f'[Transformer]: Error while parsing data to {self.target_model.__repr_name__}: {e}'
                )
        return res