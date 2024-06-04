from typing import Optional

from pydantic import Field, PositiveInt

from src.types.base import DTO
from src.types.general_books import GeneralBooksDTO

__all__ = [
    "CategoryDTO",
    "CategoryCreateDTO",
    "CategoryUpdateDTO",
    "CategoryExtendedDTO",
]


class CategoryCreateDTO(DTO):
    name: str = Field(min_length=2,max_length=32)
    slug: Optional[str] = None


class CategoryUpdateDTO(CategoryCreateDTO):
    ...


class CategoryDTO(CategoryCreateDTO):
    id: PositiveInt


class CategoryExtendedDTO(CategoryDTO):
    general_books: list[GeneralBooksDTO]
