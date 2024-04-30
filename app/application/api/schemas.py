from typing import (
    Generic,
    TypeVar,
)

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    error: str


IT = TypeVar('IT')


class BaseQueryResponseSchema(BaseModel, Generic[IT]):
    count: int
    offset: int
    limit: int
    items: IT
