from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, Field

from .base import DTO


from .tag import TagDTO

__all__ = (
    "BookPrivateDTO",
    "BookPrivateCreateDTO",
    "BookPrivateExtendedDTO",
)


class BookPrivateCreateDTO(DTO):
    title: str = Field(min_length=2, max_length=128)
    slug: str = Field(min_length=2, max_length=128)
    author: str = Field(min_length=2, max_length=128)
    created_at: datetime
    is_published: bool
    tags_private: list[TagDTO] = None
    picture: Optional[str] = Field(default=None)
    category_id: PositiveInt


class BookPrivateDTO(BookPrivateCreateDTO):
    id: PositiveInt


class BookPrivateExtendedDTO(DTO):
    books_private: list[BookPrivateDTO]


class BookPrivateListDTO(DTO):
    id: PositiveInt
    title: str = Field(min_length=2, max_length=128)
    slug: str = Field(min_length=2, max_length=128)
    author: str = Field(min_length=2, max_length=128)
    created_at: datetime
    is_published: bool
    # tags_private: list[TagDTO] = None
    picture: Optional[str] = Field(default=None)
