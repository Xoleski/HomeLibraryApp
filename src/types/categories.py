from pydantic import Field, PositiveInt

from .articles import ArticleDTO
from .base import DTO
from .general_books import GeneralBooksDTO


class CategoryCreateDTO(DTO):
    name: str = Field(
        min_length=2,
        max_length=64,
    )
    slug: str | None


class CategoryUpdateDTO(CategoryCreateDTO):
    ...


class CategoryDTO(CategoryCreateDTO):
    id: PositiveInt


class CategoryExtendedDTO(CategoryDTO):
    general_books: list[GeneralBooksDTO]
