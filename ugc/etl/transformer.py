import logging
from typing import Any, Iterator, List

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BaseTransformer:
    def __init__(self, target_model: BaseModel) -> None:
        self.target_model = target_model
    def transform(self, data: Iterator[Any]) -> List[Any]:
        pass


class KafkaTransformer(BaseTransformer):
    def transform(self, data: Iterator[Any]) -> List[Any]:
        res = []

        for record in data:
            try:
                res.append(self.target_model.parse_raw(record))
            except ValidationError as e:
                logger.error(
                    f'Error while parsing data to {self.target_model.__repr_name__}: {e}'
                )
        print('Transformed')
        return res