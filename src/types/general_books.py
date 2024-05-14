from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, Field

# from .articles import ArticleDTO
from .base import DTO

# from .tag import TagDTO

__all__ = (
    "GeneralBooksDTO",
)


class GeneralBooksDTO(DTO):
    id: PositiveInt
    title: str = Field(min_length=2, max_length=128)
    # author: str = Field(min_length=2, max_length=128)
    slug: str = Field(min_length=2, max_length=128)
    body: str
    created_at: datetime
    is_published: bool
    # articles: list[ArticleDTO]
    picture: Optional[str] = Field(default=None)
