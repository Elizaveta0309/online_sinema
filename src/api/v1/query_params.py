from fastapi import Query

from src.core.config import settings


class ListQueryParams:
    def __init__(
            self,
            page_number: int = Query(1, description='Page number'),
            page_size: int = Query(settings.PAGE_SIZE, description='Page size'),
            sort: str = Query('uuid', description='Sort field')
    ):
        self.page_number = page_number
        self.page_size = page_size
        self.sort, self.asc = self.get_sorting_field(sort)

    @staticmethod
    def get_sorting_field(sort):
        asc = 'desc' if sort[0] == '-' else 'asc'
        sorting_field = sort.replace('-', '')
        return sorting_field, asc


class SearchQueryParams:
    def __init__(
            self,
            page_number: int = Query(1, description='Page number'),
            page_size: int = Query(settings.PAGE_SIZE, description='Page size'),
            query: str = Query('star', description='Search value')
    ):
        self.page_number = page_number
        self.page_size = page_size
        self.query = query
