from pydantic import PositiveInt

from .base import DTO


class TagDTO(DTO):
    id: PositiveInt
    name: str