import json
import logging

from elasticsearch import Elasticsearch
from utils.state import ModifiedState
from const import (
    filmwork_schema,
    genres_schema,
    persons_schema
)


INDEX_SCHEMAS = {
    'movies': filmwork_schema.MAPPING,
    'persons': persons_schema.MAPPING,
    'genres': genres_schema.MAPPING
}


class ElasticLoader:
    """Загружает данные в ES

    Attributes:
        state (ModifiedState): Хранилище состояния
        logger (logging.Logger): Логгер
        es_conn: Соединение с ES
    """
    def __init__(
            self,
            state: ModifiedState,
            logger: logging.Logger,
            es_conn: Elasticsearch
            ) -> None:
        self.conn = es_conn
        self.state = state
        self.logger = logger

    def load(self, data: dict):
        """Выгружает батч в нужный индекс ES.

        Принимает на вход словарь вида:
        {
            "index": <название_индекса>,
            "checkpoint": <дата_обновления_последней_записи_батча>,
            "data": <список_с_словарями_данных>
        }

        Args:
            data (dict): Словарь с данными
        """

        # Читаем полученную информацию
        index = data['index']
        checkpoint = data['checkpoint']
        data = data['data']

        # Если батч пустой, пропускаем
        if not data:
            return

        # Получаем настройки целевой схемы
        index_mapping = INDEX_SCHEMAS[index]

        # И создаем ее при необходимости
        self._init_index(
            name=index,
            mapping=index_mapping
        )

        # Преобразуем словари с данными в строку json-формата
        data_to_es = []
        for row in data:
            data_to_es.extend([
                json.dumps({
                    "index": {
                        "_index": index,
                        "_id": str(row.uuid)
                    }
                }),
                row.json()
            ])
        # И записываем в ES
        index_data = '\n'.join(data_to_es) + '\n'
        self.conn.bulk(
            body=index_data,
            index=index
        )

        # Обновляем чекпоинт для индекса
        self.state.set_index_checkpoint(index, checkpoint)

    def _init_index(
        self,
        mapping: dict,
        name: str
    ) -> None:
        """Проверяет наличие схемы и инициализирует, если таковой нет.

        Args:
            settings (dict): Настройки индекса
            mappings (dict): Маппинг индекса
            name (str): Название индекса
        """
        if not self.conn.indices.exists(index=name):
            self.conn.indices.create(
                index=name,
                body=mapping
            )
            self.logger.info('Index schema initialized')
