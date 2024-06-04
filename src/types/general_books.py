from datetime import datetime
from pydantic import PositiveInt, Field, conlist
from typing import Optional

from src.types.book_private import BookPrivateListDTO
from src.types.base import DTO
from src.types.tag import TagDTO

__all__ = [
    "GeneralBooksDTO",
    "GeneralBookExtendedDTO",
    "GeneralBookUpdateDTO",
    "GeneralBookCreateDTO",
    "GeneralBooksForPrivateDTO",
]


class GeneralBookCreateDTO(DTO):
    title: str = Field(min_length=2, max_length=128)  # может быть не уникальным
    slug: Optional[str] = None
    author: str = Field(min_length=2, max_length=128)
    category_id: PositiveInt
    tags: Optional[list[int]] = None  # Список ID тегов (conlist - можно добавить проверку на уникальность)


class GeneralBookUpdateDTO(GeneralBookCreateDTO):
    is_published: bool
    picture: Optional[str] = Field(default=None)


class GeneralBooksForPrivateDTO(GeneralBookUpdateDTO):
    id: PositiveInt
    created_at: datetime


class GeneralBooksDTO(GeneralBooksForPrivateDTO):
    tags_general: list[TagDTO]


class GeneralBookExtendedDTO(GeneralBooksForPrivateDTO):
    books_private: list[BookPrivateListDTO]
