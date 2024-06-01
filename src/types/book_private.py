from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, Field

from .base import DTO


from .tag import TagDTO

__all__ = (
    "BookPrivateDTO",
    "BookPrivateCreateDTO",
    "BookPrivateExtendedDTO",
    "BookPrivateListDTO",
)


class BookPrivateCreateDTO(DTO):
    title: str = Field(min_length=2, max_length=128)
    slug: str | None = None
    author: str = Field(min_length=2, max_length=128)
    category_id: PositiveInt
    general_book_id: Optional[PositiveInt] = None


class BookPrivateDTO(BookPrivateCreateDTO):
    id: PositiveInt
    picture: Optional[str] = Field(default=None)
    created_at: datetime
    is_published: bool
    user_email: str = Field(min_length=2, max_length=128)


class BookPrivateExtendedDTO(DTO):
    books_private: list[BookPrivateDTO]


class BookPrivateListDTO(BookPrivateDTO):
    tags_private: list[TagDTO] = None


class BookPrivateUpdateDTO(BookPrivateCreateDTO):
    ...


