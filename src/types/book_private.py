from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, Field

from .base import DTO

from .tag import TagDTO

__all__ = (
    "BookPrivateDTO",
    "BookPrivateCreateDTO",
)


class BookPrivateDTO(DTO):
    id: PositiveInt


class BookPrivateCreateDTO(BookPrivateDTO):
    title: str = Field(min_length=2, max_length=128)
    slug: str = Field(min_length=2, max_length=128)
    body: str
    created_at: datetime
    is_published: bool
    tags: list[TagDTO]
    picture: Optional[str] = Field(default=None)