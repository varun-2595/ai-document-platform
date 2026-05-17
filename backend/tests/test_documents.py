from io import BytesIO

from fastapi import UploadFile
from starlette.datastructures import Headers

from app.models.document import Document
from app.services.document_service import create_document


def test_upload_pdf_returns_metadata(client):
    response = client.post(
        "/documents/upload",
        files={"file": ("report.pdf", b"%PDF-1.4 sample", "application/pdf")},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["original_filename"] == "report.pdf"
    assert body["status"] == "uploaded"
    assert body["size_bytes"] == 15


def test_upload_rejects_empty_file(client):
    response = client.post(
        "/documents/upload",
        files={"file": ("empty.pdf", b"", "application/pdf")},
    )
    assert response.status_code == 400


def test_upload_rejects_wrong_content_type(client):
    response = client.post(
        "/documents/upload",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 415


def test_upload_rejects_oversized_file(client):
    response = client.post(
        "/documents/upload",
        files={"file": ("large.pdf", b"x" * 1025, "application/pdf")},
    )
    assert response.status_code == 413


def test_filename_is_sanitized_and_metadata_persisted(db_session):
    upload = UploadFile(
        filename="../../unsafe.pdf",
        file=BytesIO(b"%PDF-1.4 sample"),
        headers=Headers({"content-type": "application/pdf"}),
    )
    document = create_document(db_session, upload)
    stored = db_session.query(Document).one()
    assert document.original_filename == "unsafe.pdf"
    assert stored.storage_path.startswith("documents/")
