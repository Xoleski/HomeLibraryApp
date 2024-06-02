from datetime import datetime
from pydantic import PositiveInt, Field, conlist
from typing import Optional

from .book_private import BookPrivateListDTO
from .base import DTO
from .tag import TagDTO

__all__ = (
    "GeneralBooksDTO",
    "GeneralBookExtendedDTO",
    "GeneralBookUpdateDTO",
    "GeneralBookCreateDTO",
    "GeneralBooksForPrivateDTO",
)


class GeneralBookCreateDTO(DTO):
    title: str = Field(min_length=2, max_length=128)
    slug: str | None = None
    author: str | None = None
    category_id: PositiveInt
    tags: Optional[conlist(int)] = None  # Список ID тегов


class GeneralBookUpdateDTO(GeneralBookCreateDTO):
    is_published: bool
    picture: Optional[str] = Field(default=None)


class GeneralBooksForPrivateDTO(GeneralBookUpdateDTO):
    id: PositiveInt
    created_at: datetime


class GeneralBooksDTO(GeneralBooksForPrivateDTO):
    tags_general: list[TagDTO] = None


class GeneralBookExtendedDTO(GeneralBooksForPrivateDTO):
    books_private: list[BookPrivateListDTO]
