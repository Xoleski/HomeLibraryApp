from datetime import datetime
from pydantic import PositiveInt, Field, conlist
from typing import Optional

from .base import DTO
from .tag import TagDTO

__all__ = (
    "BookPrivateDTO",
    "BookPrivateCreateDTO",
    "BookPrivateExtendedDTO",
    "BookPrivateListDTO",
    "BookPrivateUpdateDTO",
    "TagExtendedBookPrivateDTO",
)


class BookPrivateCreateDTO(DTO):
    title: str = Field(min_length=2, max_length=128)
    slug: str | None = None
    author: str = Field(min_length=2, max_length=128)
    category_id: PositiveInt
    general_book_id: Optional[PositiveInt] = None
    tags: Optional[conlist(int)] = None  # Список ID тегов


# class BookPrivateToCreateDTO(BookPrivateCreateDTO):
#     tags: Optional[conlist(int)] = None  # Список ID тегов


class BookPrivateUpdateDTO(BookPrivateCreateDTO):
    picture: Optional[str] = Field(default=None)
    is_published: bool


class BookPrivateDTO(BookPrivateUpdateDTO):
    id: PositiveInt
    created_at: datetime
    user_email: str = Field(min_length=2, max_length=128)


class BookPrivateExtendedDTO(DTO):
    books_private: list[BookPrivateDTO]


class BookPrivateListDTO(BookPrivateDTO):
    tags_private: list[TagDTO] = None


class TagExtendedBookPrivateDTO(TagDTO):
    books_private: list[BookPrivateDTO]




