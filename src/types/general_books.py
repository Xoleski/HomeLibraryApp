from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, Field

from .base import DTO

from .tag import TagDTO

__all__ = (
    "GeneralBooksDTO",
)


class GeneralBooksDTO(DTO):
    id: PositiveInt
    title: str = Field(min_length=2, max_length=128)
    # author: str = Field(min_length=2, max_length=128)
    slug: str = Field(min_length=2, max_length=128)
    author: str | None = None
    created_at: datetime
    is_published: bool
    tags: list[TagDTO]
    picture: Optional[str] = Field(default=None)
