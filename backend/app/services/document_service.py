import os
import json

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.chunk import DocumentChunk

from app.services.pdf_service import extract_text_from_pdf
from app.services.embedding_service import generate_embedding
from app.services.chunk_service import chunk_text

UPLOAD_DIR = "uploads"


def save_document(
    db: Session,
    filename: str,
    content: bytes
):
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as file:
        file.write(content)

    extracted_text = extract_text_from_pdf(file_path)

    document = Document(
        filename=filename,
        extracted_text=extracted_text
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    chunks = chunk_text(extracted_text)

    for chunk in chunks:
        embedding = generate_embedding(chunk)

        document_chunk = DocumentChunk(
            document_id=document.id,
            chunk_text=chunk,
            chunk_embedding=json.dumps(embedding)
        )

        db.add(document_chunk)

    db.commit()

    return document
