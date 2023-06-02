from logging import Logger
import time
from extractor import BaseMessageBroker
from transformer import BaseTransformer
from loader import BaseDatabaseLoader


class ETL:
    """
    ETL-процесс, производящий перенос данных.
    """
    def __init__(self,
                 extractor: BaseMessageBroker,
                 transformer: BaseTransformer,
                 loader: BaseDatabaseLoader,
                 logger: Logger,
                 batch_size: int = 1000,
                 refresh_time: int = 5) -> None:
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.batch_size = batch_size
        self.refresh_time = refresh_time
        self.logger = logger

    def start(self, batch_size: int = 1000):
        while True:
            self.logger.info('[ETL]: Started processing batch.')
            start_time = time.time()

            raw_data = self.extractor.extract(batch_size)

            for data in raw_data:
                print(data)
                if len(data):
                    self.logger.info('[ETL]: Finished extractiong batch.')
                    data = self.transformer.transform(data)
                    self.logger.info('[ETL]: Finished transforming batch.')
                    self.loader.load(data)
                    total_time = time.time() - start_time
                    self.logger.info(
                        f'[ETL]: Finished loading batch. Finished in: {total_time:.2f} sec.'
                    )
                else:
                    self.logger.error(
                        '[ETL]: Can\'t comsume messages. Waiting...'
                    )
                    time.sleep(self.refresh_time)
