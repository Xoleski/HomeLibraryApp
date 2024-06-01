from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, Field

from .book_private import BookPrivateDTO, BookPrivateListDTO
from .base import DTO

from .tag import TagDTO

__all__ = (
    "GeneralBooksDTO",
    "GeneralBookExtendedDTO",
    "GeneralBooksIdDTO",
)


class GeneralBookCreateDTO(DTO):
    title: str = Field(min_length=2, max_length=128)
    slug: str | None = None
    author: str | None = None
    category_id: PositiveInt


class GeneralBooksIdDTO(GeneralBookCreateDTO):
    id: PositiveInt


class GeneralBooksForPrivateDTO(GeneralBooksIdDTO):
    created_at: datetime
    is_published: bool
    # tags: list[TagDTO] = None
    picture: Optional[str] = Field(default=None)


class GeneralBooksDTO(GeneralBooksForPrivateDTO):
    tags: list[TagDTO] = None


class GeneralBookExtendedDTO(GeneralBooksForPrivateDTO):
    books_private: list[BookPrivateListDTO]


class GeneralBookUpdateDTO(GeneralBookCreateDTO):
    ...
