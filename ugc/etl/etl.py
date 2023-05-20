from logging import Logger
import time
from extractor import BaseMessageBroker
from transformer import BaseTransformer
from loader import BaseDatabaseLoader
from utils.exceptions import NoMessagesException, ConsumingMessagesException


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
    
    def start(self):
        while True:
            self.logger.info(f'[ETL]: Started processing data.')
            start_time = time.time()
            
            raw_data = self.extractor.extract(self.batch_size)

            if raw_data:
                self.logger.info('[ETL]: Finished extractiong batch.')
                data = self.transformer.transform(raw_data)
                self.logger.info('[ETL]: Finished transforming batch.')
                self.loader.load(data)
                total_time = time.time() - start_time
                self.logger.info(f'[ETL]: Finished loading batch. Finished in: {total_time:.2f} sec.')
            
            time.sleep(self.refresh_time)
