from dataclasses import dataclass
from typing import BinaryIO, Protocol


@dataclass(frozen=True)
class ExtractionResult:
    text: str
    page_count: int
    ocr_required: bool


class TextExtractor(Protocol):
    def extract(self, source: BinaryIO) -> ExtractionResult: ...


class PdfTextExtractor:
    def extract(self, source: BinaryIO) -> ExtractionResult:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("Install pypdf to enable PDF extraction.") from exc

        reader = PdfReader(source)
        text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        return ExtractionResult(
            text=text,
            page_count=len(reader.pages),
            ocr_required=not bool(text),
        )
