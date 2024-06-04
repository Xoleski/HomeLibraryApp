from abc import ABC, abstractmethod

__all__ = [
    "AbstractFileStorage"
]


class AbstractFileStorage(ABC):

    @abstractmethod
    def save(self, filename: str, file: bytes) -> str:
        ...
