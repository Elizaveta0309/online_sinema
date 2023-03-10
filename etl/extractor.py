import logging
from datetime import datetime
from typing import Generator, Optional


from const.postgres_queries import (
    FILMWORK_QUERY,
    GENRES_QUERY,
    PERSONS_QUERY
)

from models import PersonModel, GenreModel, FilmworkModel
from psycopg2.extras import RealDictCursor
from utils.state import ModifiedState


MODELS = [
    {
        "index": "genres",
        "query": GENRES_QUERY,
        "model": GenreModel
    },
    {
        "index": "persons",
        "query": PERSONS_QUERY,
        "model": PersonModel
    },
    {
        "index": "movies",
        "query": FILMWORK_QUERY,
        "model": FilmworkModel
    }
]


class BaseExtractor:
    """
    Реализует выгрузку данных из БД через пайплайн
    producer -> enricher
    """
    def __init__(
            self,
            state: ModifiedState,
            batch_size: int,
            logger: logging.Logger
            ) -> None:
        self.state = state
        self.batch_size = batch_size
        self.logger = logger

    def extract_data(self, checkpoint: datetime):
        pass

    def _produce(self, checkpoint: datetime):
        pass

    def _enrich(self):
        pass


class PostgresExtractor(BaseExtractor):

    def __init__(
            self,
            state: ModifiedState,
            batch_size: int,
            logger: logging.Logger,
            pg_conn
            ) -> None:
        self.conn = pg_conn
        super().__init__(state, batch_size, logger)

    def _produce(self, checkpoint: Optional[datetime] = None) -> Generator:
        """Извлекает данные из БД батчами.

        Args:
            checkpoint (Optional[datetime], optional): Чекпоинт выгрузки.

        Returns:
            Generator: Генератор батчей
        """
        # Для каждой сущности в БД
        for index in MODELS:
            index, query, model = index.values()

            self.logger.info(f'Extracting data for index {index}')
            # Если чекпойнт не указан явно
            if checkpoint is None:
                # Достаем из хранилища или задаем минимальный (01.01.01)
                checkpoint = self.state.get_index_checkpoint(index)
                if checkpoint is None:
                    checkpoint = datetime(1, 1, 1, tzinfo=None)
                else:
                    checkpoint = datetime.fromisoformat(checkpoint)
            # Забираем из хранилища список id фильмов для модификации
            updated = self.state.get_modified_movies_list()

            self.logger.info(f'Index checkpoint is set to: {checkpoint}')

            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Выполняем запрос к БД
                if index == 'movies':
                    # И получаем список фильмов к обновлению
                    cursor.execute(query, {
                        'checkpoint': checkpoint,
                        'movies_ids': tuple(updated)
                    })
                else:
                    # Или связанные таблицы с id фильмов
                    cursor.execute(query, (checkpoint, ))

                while True:
                    # Считываем batch_size записей из БД
                    rows = [
                        dict(row)
                        for row in cursor.fetchmany(self.batch_size)
                    ]

                    if not rows:
                        break

                    yield self._enrich({
                        'index': index,
                        'rows': rows,
                        'model': model
                    })

    def _enrich(self, data: dict) -> dict:
        """Для связанных таблиц запоминает id фильмов для обновления

        Args:
            data (dict): Батч данных

        Returns:
            dict: Данные
        """
        index = data['index']
        rows = data['rows']

        if index != 'movies':
            # Для всех измененных записей genres и persons
            # запоминаем id фильмов, которые надо обновить
            for row in rows:
                [
                    self.state.push_modified_id(id['fw_id'])
                    for id in row['array_id']
                ]
            # И фиксируем время обновления индекса
            self.state.set_index_checkpoint(index, rows[0]['modified'])

        return data

    def extract_data(self, checkpoint: Optional[datetime] = None) -> Generator:
        """Извлекает данные из БД батчами.

        Args:
            checkpoint (Optional[datetime], optional): Чекпоинт выгрузки.

        Returns:
            Generator: Генератор батчей
        """
        data = self._produce(checkpoint)

        return data
