from pydantic import Field, PositiveInt

from .base import DTO
from .general_books import GeneralBooksDTO


class CategoryCreateDTO(DTO):
    name: str = Field(
        min_length=2,
        max_length=64,
    )
    slug: str | None = None


class CategoryUpdateDTO(CategoryCreateDTO):
    ...


class CategoryDTO(CategoryCreateDTO):
    id: PositiveInt


class CategoryExtendedDTO(CategoryDTO):
    general_books: list[GeneralBooksDTO]
