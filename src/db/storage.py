from abc import abstractmethod, ABC


class Storage(ABC):
    @abstractmethod
    async def get(self, index: str, id: str):
        pass

    @abstractmethod
    async def search(self, index: str, query: dict):
        pass
