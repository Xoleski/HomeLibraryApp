from datetime import datetime
from pydantic import PositiveInt, Field
from typing import Optional

from src.types.base import DTO
from src.types.tag import TagDTO

__all__ = [
    "BookPrivateDTO",
    "BookPrivateCreateDTO",
    "BookPrivateExtendedDTO",
    "BookPrivateListDTO",
    "BookPrivateUpdateDTO",
    "TagExtendedBookPrivateDTO",
]


class BookPrivateCreateDTO(DTO):
    title: str = Field(min_length=2, max_length=128)  # может быть не уникальным
    slug: Optional[str] = None
    author: str = Field(min_length=2, max_length=128)
    category_id: PositiveInt
    general_book_id: Optional[PositiveInt] = None
    tags: Optional[list[int]] = None  # Список ID тегов (conlist - можно добавить проверку на уникальность)


class BookPrivateUpdateDTO(BookPrivateCreateDTO):
    picture: Optional[str] = Field(default=None)
    is_published: bool


class BookPrivateDTO(BookPrivateUpdateDTO):
    id: PositiveInt
    created_at: datetime
    user_id: Optional[PositiveInt] = None


class BookPrivateExtendedDTO(DTO):
    books_private: list[BookPrivateDTO]


class BookPrivateListDTO(BookPrivateDTO):
    tags_private: Optional[list[TagDTO]] = None


class TagExtendedBookPrivateDTO(TagDTO):
    books_private: list[BookPrivateDTO]




