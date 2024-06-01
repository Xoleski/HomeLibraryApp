from pydantic import PositiveInt

from .base import DTO


class TagCreateDTO(DTO):
    name: str


class TagDTO(TagCreateDTO):
    id: PositiveInt


class TagUpdateDTO(TagCreateDTO):
    ...
