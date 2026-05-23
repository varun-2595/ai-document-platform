import os
import json

from app.core.celery_app import celery

from app.db.database import SessionLocal
from app.models.document import Document
from app.models.chunk import DocumentChunk

from app.services.pdf_service import extract_text_from_pdf
from app.services.cleaning_service import clean_text
from app.services.chunk_service import chunk_text
from app.services.embedding_service import generate_embedding
from app.services.opensearch_service import index_chunk
from app.core.logger import logger


@celery.task
def process_document(
    document_id: int,
    file_path: str
):
    try:
        logger.info(f"Processing document: {document_id}")
        db = SessionLocal()

        document = db.query(Document).filter(
            Document.id == document_id
        ).first()

        raw_text = extract_text_from_pdf(file_path)
        cleaned_text = clean_text(raw_text)
        document.extracted_text = cleaned_text
        document.status = "PROCESSED"
        db.commit()

        logger.info(f"Extracted and cleaned text for document: {document_id}")

        chunks = chunk_text(cleaned_text)

        for chunk in chunks:
            embedding = generate_embedding(chunk)

            document_chunk = DocumentChunk(
                document_id=document.id,
                chunk_text=chunk,
                chunk_embedding=json.dumps(embedding)
            )

            db.add(document_chunk)

            db.flush()

            index_chunk(
                chunk_id=document_chunk.id,
                document_id=document.id,
                chunk_text=chunk,
                embedding=embedding
            )

        document.status = "COMPLETED"

        db.commit()
        db.close()

        logger.info(f"Completed processing document: {document_id}")

    except Exception as e:
        document.status = "FAILED"
        document.error_message = str(e)
        logger.error(f"Error processing document {document_id}: {str(e)}")
        db.commit()
        raise e

    finally:
            logger.info(f"Finished processing document: {document_id}")
            db.close()
