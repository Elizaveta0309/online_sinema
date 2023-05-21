class BaseOffsetRegistry():
    def update(self, topic: str, partition: str, offset: str) -> None:
        pass

class DictOffsetRegistry(BaseOffsetRegistry):
    """
    На будущее, если будет выбран брокер без автоматического смещения оффсетов
    или удаления сообщений при чтении.
    """
    def __init__(self) -> None:
        self.__registry = {}
    
    def update(self, topic: str, partition: str, offset: str) -> None:
        if topic not in self.__registry:
            self.__registry[topic] = {}
        self.__registry[topic][partition] = offset
        return
    def __str__(self) -> str:
        return f'Topics: {len(self.__registry)}'
