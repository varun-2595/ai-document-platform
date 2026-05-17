from pathlib import Path
from shutil import copyfileobj
from typing import BinaryIO, Protocol


class StorageBackend(Protocol):
    def save(self, source: BinaryIO, destination: str) -> str: ...
    def open(self, path: str, mode: str = "rb") -> BinaryIO: ...


class LocalStorage:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir

    def save(self, source: BinaryIO, destination: str) -> str:
        target = self.root_dir / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        source.seek(0)
        with target.open("wb") as output:
            copyfileobj(source, output)
        return destination

    def open(self, path: str, mode: str = "rb") -> BinaryIO:
        return (self.root_dir / path).open(mode)


class S3Storage:
    """Production storage implementation placeholder; wire credentials through IAM in AWS."""

    def save(self, source: BinaryIO, destination: str) -> str:
        raise NotImplementedError("S3Storage will be enabled during AWS deployment.")

    def open(self, path: str, mode: str = "rb") -> BinaryIO:
        raise NotImplementedError("S3Storage will be enabled during AWS deployment.")
