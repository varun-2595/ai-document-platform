import os
import json

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.chunk import DocumentChunk

from app.services.pdf_service import extract_text_from_pdf
from app.services.embedding_service import generate_embedding
from app.services.chunk_service import chunk_text
from app.services.cleaning_service import clean_text
from app.services.opensearch_service import index_chunk

UPLOAD_DIR = "uploads"


def save_document(
    db: Session,
    filename: str,
    content: bytes
):
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as file:
        file.write(content)

    raw_text = extract_text_from_pdf(file_path)

    extracted_text = clean_text(raw_text)

    document = Document(
        filename=filename,
        extracted_text=extracted_text
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    chunks = chunk_text(extracted_text)
    print(f"TOTAL CHUNKS: {len(chunks)}")

    for index, chunk in enumerate(chunks[:3]):
        print(f"\nCHUNK {index + 1}")
        print(chunk[:300])

    for chunk in chunks:
        embedding = generate_embedding(chunk)

        document_chunk = DocumentChunk(
            document_id=document.id,
            chunk_text=chunk,
            chunk_embedding=json.dumps(embedding)
        )

        db.add(document_chunk)
        db.flush()  # Get the chunk ID before committing

        index_chunk(
            chunk_id=document_chunk.id,
            document_id=document.id,
            chunk_text=chunk,
            embedding=embedding
        )

    db.commit()

    return document
