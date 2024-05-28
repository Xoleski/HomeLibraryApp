from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, Field

from .book_private import BookPrivateDTO
from .base import DTO

from .tag import TagDTO

__all__ = (
    "GeneralBooksDTO",
    "GeneralBookExtendedDTO",
    "GeneralBooksIdDTO",
)


class GeneralBooksIdDTO(DTO):
    id: PositiveInt


class GeneralBooksForPrivateDTO(GeneralBooksIdDTO):
    title: str = Field(min_length=2, max_length=128)
    slug: str = Field(min_length=2, max_length=128)
    author: str | None = None
    created_at: datetime
    is_published: bool
    # tags: list[TagDTO] = None
    picture: Optional[str] = Field(default=None)


class GeneralBooksDTO(GeneralBooksIdDTO):
    title: str = Field(min_length=2, max_length=128)
    slug: str = Field(min_length=2, max_length=128)
    author: str | None = None
    created_at: datetime
    is_published: bool
    tags: list[TagDTO] = None
    picture: Optional[str] = Field(default=None)


class GeneralBookExtendedDTO(GeneralBooksForPrivateDTO):
    books_private: list[BookPrivateDTO]

