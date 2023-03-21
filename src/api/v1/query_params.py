from fastapi import Query

from src.core.config import settings


class ListQueryParams:
    def __init__(
            self,
            page_number: int = Query(
                default=1,
                description='Page number',
                ge=1,
                le=1000000
            ),
            page_size: int = Query(
                PAGE_SIZE,
                description='Page size',
                ge=10,
                le=100
            ),
            sort: str = Query(
                default='uuid',
                description='Sort field'
            )
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
            page_number: int = Query(
                default=1,
                description='Page number',
                ge=1,
                le=1000000
            ),
            page_size: int = Query(
                default=PAGE_SIZE,
                description='Page size',
                ge=10,
                le=100
            ),
            query: str = Query(
                default='star',
                description='Search value'
            )
    ):
        self.page_number = page_number
        self.page_size = page_size
        self.query = query
