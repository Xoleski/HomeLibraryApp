from typing import Optional

from pydantic import PositiveInt, Field

from .base import DTO


class TagCreateDTO(DTO):
    name: Optional[str] = None


class TagDTO(TagCreateDTO):
    id: PositiveInt


class TagUpdateDTO(TagCreateDTO):
    ...
