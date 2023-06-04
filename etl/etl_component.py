import logging
from datetime import datetime

from extractor import PostgresExtractor
from loader import ElasticLoader
from transformer import Transformer
from utils.exceptions import (ExtractionException, LoadException,
                              TransformException)
from utils.state import ModifiedState


class ETL:
    """Реализует ETL процесс.

    Attributes:
        logger (logging.Logger): Логгер
        extractor (BaseExtractor): Объект `Extractor`, извлекающий данные
        transformer (Transformer): Объект `Transformer`, преобразующий данные
        loader (BaseLoader): Объект `BaseLoader`, загружающий данные
    """
    def __init__(
            self,
            logger: logging.Logger,
            extractor: PostgresExtractor,
            transformer: Transformer,
            loader: ElasticLoader,
            state: ModifiedState) -> None:

        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.logger = logger
        self.state = state

    def start(self, checkpoint: datetime | None = None):
        """Совершает ETL-процедуру.

        Args:
            checkpoint (Optional[datetime], optional): Чекпоинт для выгрузки
        """
        try:
            # Получаем данные из БД с учетом чекпоинта
            data = self.extractor.extract_data(checkpoint)
        except Exception as e:
            raise ExtractionException(
                f"Error while extracting data from Postgres: {e}"
            )
        batch_count = 0

        # Содержимое каждого из батчей сериализуем и
        # дополняем инф-ей об индексе и модели
        for extracted in data:
            batch_count += 1
            try:
                transformed = self.transformer.transform(
                    model=extracted['model'],
                    index=extracted['index'],
                    data=extracted['rows']
                )
            except Exception as e:
                raise TransformException(
                    f"Error while transforming batch: {e}"
                )
            # И выгружаем в БД
            try:
                self.loader.load(transformed)
            except Exception as e:
                raise LoadException(f"Error while loading data: {e}")

        # И завершаем процесс, очищая хранилище состояния
        self.logger.info(f'Batches loaded: {batch_count}')
        self.logger.info('Finished loading data. Clearing state...')
        self.state.clear_modified_id_list()
