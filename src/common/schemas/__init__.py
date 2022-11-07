import typing
from typing import TypeVar

from src.core.validator.schema import Schema
from pydantic import Field


T = TypeVar('T')


class PaginationQuerySchema(Schema):
    page: int = Field(default=1, ge=1, le=100000)
    limit: int = Field(default=10, ge=1, le=100000)


def pagination_response(list_item: T):
    class PaginationResponse(Schema):
        total: int = Field(ge=0)
        page_count: int = Field(ge=0)
        data: typing.List[list_item]

    return PaginationResponse


def data_list_response(list_item: T):
    class DataListResponse(Schema):
        total: int = Field(ge=0)
        data: typing.List[list_item]

    return DataListResponse


class ValidationErrorSchema(Schema):
    class ValidationChildError(Schema):
        message: str
        location: typing.List[str] = Field(description='Путь к свойству объекта')

    message: str = 'Validation error'
    code: int = 1
    errors: typing.List[ValidationChildError]


