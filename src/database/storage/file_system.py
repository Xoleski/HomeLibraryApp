from pathlib import Path
from threading import Thread

from .base import AbstractFileStorage

__all__ = (
    "FileSystemStorage",
)


class FileSystemStorage(AbstractFileStorage):
    def __init__(self, upload_to: str) -> None:
        self.upload_to = Path(upload_to)

    def _save(self, filename: str, file: bytes):
        with self.upload_to.joinpath(filename).open(mode="wb") as f:
            f.write(file)

    def save(self, filename: str, file: bytes) -> str:
        thread = Thread(target=self._save, kwargs={"filename": filename, "file": file})
        thread.start()
        return f"{self.upload_to.joinpath(filename)}"

