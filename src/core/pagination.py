from typing import Generic, TypeVar, Optional, Sequence
from pydantic import BaseModel
from fastapi import Query

T = TypeVar("T")

class Paginator(BaseModel, Generic[T]):
    items: Sequence[T]
    total: int
    page: int
    size: int
    pages: int

    @property
    def has_previous(self) -
