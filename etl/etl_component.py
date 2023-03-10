from datetime import datetime
import logging
from typing import Optional
from extractor import BaseExtractor
from transformer import Transformer
from loader import BaseLoader
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
            extractor: BaseExtractor,
            transformer: Transformer,
            loader: BaseLoader,
            state: ModifiedState) -> None:

        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.logger = logger
        self.state = state

    def start(self, checkpoint: Optional[datetime] = None):
        """Совершает ETL-процедуру.

        Args:
            checkpoint (Optional[datetime], optional): Чекпоинт для выгрузки
        """

        # Получаем данные из БД с учетом чекпоинта
        data = self.extractor.extract_data(checkpoint)
        batch_count = 0

        # Содержимое каждого из батчей сериализуем и
        # дополняем инф-ей об индексе и модели
        for extracted in data:
            batch_count += 1
            transformed = self.transformer.transform(
                model=extracted['model'],
                index=extracted['index'],
                data=extracted['rows']
            )
            # И выгружаем в БД
            self.loader.load(transformed)

        # И завершаем процесс, очищая хранилище состояния
        self.logger.info(f'Batches loaded: {batch_count}')
        self.logger.info('Finished loading data. Clearing state...')
        self.state.clear_modified_id_list()
