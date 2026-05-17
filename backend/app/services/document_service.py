import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import Document, DocumentStatus
from app.services.exceptions import DocumentTooLargeError, EmptyDocumentError, UnsupportedDocumentTypeError
from app.services.storage import LocalStorage, StorageBackend


def normalize_filename(filename: str | None) -> str:
    safe_name = Path(filename or "document.pdf").name.strip()
    return safe_name or "document.pdf"


def build_storage_path(filename: str) -> str:
    suffix = Path(filename).suffix.lower() or ".bin"
    now = datetime.now(UTC)
    return f"documents/{now:%Y/%m/%d}/{uuid4().hex}{suffix}"


def get_upload_size(upload_file: UploadFile) -> int:
    upload_file.file.seek(0, os.SEEK_END)
    size = upload_file.file.tell()
    upload_file.file.seek(0)
    return size


def validate_upload(upload_file: UploadFile, size_bytes: int) -> None:
    if size_bytes == 0:
        raise EmptyDocumentError("Uploaded file is empty.")
    if upload_file.content_type not in settings.allowed_upload_content_types:
        raise UnsupportedDocumentTypeError("Only configured document types are accepted.")
    if size_bytes > settings.max_upload_size_bytes:
        raise DocumentTooLargeError("Uploaded file exceeds the configured size limit.")


def create_document(
    db: Session,
    upload_file: UploadFile,
    storage: StorageBackend | None = None,
) -> Document:
    original_filename = normalize_filename(upload_file.filename)
    size_bytes = get_upload_size(upload_file)
    validate_upload(upload_file, size_bytes)

    storage_backend = storage or LocalStorage(settings.upload_dir)
    storage_path = storage_backend.save(upload_file.file, build_storage_path(original_filename))
    document = Document(
        original_filename=original_filename,
        storage_path=storage_path,
        content_type=upload_file.content_type or "application/octet-stream",
        size_bytes=size_bytes,
        status=DocumentStatus.UPLOADED.value,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_document(db: Session, document_id: int) -> Document | None:
    return db.query(Document).filter(Document.id == document_id).one_or_none()
