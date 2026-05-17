from sqlalchemy.orm import Session

from app.models.document import Document, DocumentChunk, DocumentStatus
from app.services.chunking_service import WordWindowChunker
from app.services.embedding_service import OpenAIEmbeddingProvider
from app.services.extraction_service import PdfTextExtractor
from app.services.search_service import OpenSearchIndex
from app.services.storage import LocalStorage
from app.core.config import settings


class DocumentProcessor:
    def __init__(self) -> None:
        self.storage = LocalStorage(settings.upload_dir)
        self.extractor = PdfTextExtractor()
        self.chunker = WordWindowChunker()
        self.embedder = OpenAIEmbeddingProvider()
        self.search_index = OpenSearchIndex()

    def process(self, db: Session, document: Document) -> None:
        document.status = DocumentStatus.PROCESSING.value
        db.commit()

        with self.storage.open(document.storage_path) as source:
            extraction = self.extractor.extract(source)

        document.extracted_text = extraction.text
        document.page_count = extraction.page_count
        document.ocr_required = extraction.ocr_required

        db.query(DocumentChunk).filter(DocumentChunk.document_id == document.id).delete()
        chunks = self.chunker.chunk(extraction.text)
        chunk_models = [
            DocumentChunk(
                document_id=document.id,
                chunk_index=chunk.index,
                content=chunk.content,
                token_count=chunk.token_count,
                chunking_version=self.chunker.version,
            )
            for chunk in chunks
        ]
        db.add_all(chunk_models)
        db.flush()

        embeddings = self.embedder.embed([chunk.content for chunk in chunk_models]) if chunk_models else []
        index_payload = []
        for chunk_model, embedding in zip(chunk_models, embeddings):
            chunk_model.embedding_id = str(chunk_model.id)
            index_payload.append(
                {
                    "chunk_id": chunk_model.id,
                    "document_id": document.id,
                    "content": chunk_model.content,
                    "embedding": embedding,
                    "filename": document.original_filename,
                }
            )
        if index_payload:
            self.search_index.index_chunks(index_payload)

        document.status = DocumentStatus.PROCESSED.value
        document.error_message = None
        db.commit()
