from datetime import datetime

from pydantic import BaseModel

from app.models.document import DocumentStatus


class DocumentResponse(BaseModel):
    id: int
    original_filename: str
    storage_path: str
    content_type: str
    size_bytes: int
    status: DocumentStatus
    error_message: str | None
    page_count: int | None
    ocr_required: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SearchResult(BaseModel):
    document_id: int
    chunk_id: int
    content: str
    score: float


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


class QuerySource(BaseModel):
    document_id: int
    chunk_id: int
    content: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[QuerySource]
