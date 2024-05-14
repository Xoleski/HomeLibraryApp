from typing import Optional, Any

from sqlalchemy import VARCHAR, Dialect


from sqlalchemy.types import TypeDecorator


from .storage.base import AbstractFileStorage


class FileType(TypeDecorator):
    impl = VARCHAR
    cache_ok = True

    def __init__(self, storage: AbstractFileStorage = None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.storage = storage

    def process_bind_param(self, value: tuple[str, bytes], dialect: Dialect) -> Any:
        return self.storage.save(filename=value[0], file=value[1])

    def process_result_value(
        self, value: str, dialect: Dialect
    ) -> str:
        return value
