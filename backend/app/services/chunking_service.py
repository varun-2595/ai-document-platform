from dataclasses import dataclass
from typing import Protocol

from app.core.config import settings


@dataclass(frozen=True)
class TextChunk:
    index: int
    content: str
    token_count: int


class Chunker(Protocol):
    def chunk(self, text: str) -> list[TextChunk]: ...


class WordWindowChunker:
    version = "v1"

    def __init__(self, size: int | None = None, overlap: int | None = None) -> None:
        self.size = size or settings.chunk_size_words
        self.overlap = settings.chunk_overlap_words if overlap is None else overlap
        if self.overlap >= self.size:
            raise ValueError("Chunk overlap must be smaller than chunk size.")

    def chunk(self, text: str) -> list[TextChunk]:
        words = text.split()
        chunks: list[TextChunk] = []
        start = 0
        index = 0
        while start < len(words):
            window = words[start : start + self.size]
            chunks.append(TextChunk(index=index, content=" ".join(window), token_count=len(window)))
            if start + self.size >= len(words):
                break
            start += self.size - self.overlap
            index += 1
        return chunks
