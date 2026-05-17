from app.db.database import SessionLocal
from app.models.document import Document, DocumentStatus
from app.services.processing_service import DocumentProcessor
from app.worker.celery_app import celery_app


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def process_document(self, document_id: int) -> None:
    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == document_id).one_or_none()
        if document is None or document.status == DocumentStatus.PROCESSED.value:
            return
        DocumentProcessor().process(db, document)
    except Exception as exc:
        document = db.query(Document).filter(Document.id == document_id).one_or_none()
        if document is not None:
            document.status = DocumentStatus.FAILED.value
            document.error_message = str(exc)
            db.commit()
        raise
    finally:
        db.close()
