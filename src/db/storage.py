from abc import abstractmethod, ABC


class Storage(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    async def get(self, index: str, id: str):
        pass

    @abstractmethod
    async def search(self, index: str, query: dict):
        pass
