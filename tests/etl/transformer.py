import logging

from pydantic import BaseModel


class Transformer:
    """Сериализует модель.

    Attributes:
        logger (logging.Logger): Логгер
    """
    def __init__(
            self,
            logger: logging.Logger) -> None:
        self.logger = logger

    def transform(self, model: BaseModel, data: list, index: str):
        transformed = []

        try:
            for row in data:
                transformed.append(model.parse_obj(row))
        except Exception as e:
            logging.error(
                f"Could not transform to model {model}",
                exc_info=e
            )
        return {
            "index": index,
            "data": transformed,
            "checkpoint": data[0]["modified"]
        }
