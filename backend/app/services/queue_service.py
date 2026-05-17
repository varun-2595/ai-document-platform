from app.core.config import settings


def enqueue_document_processing(document_id: int) -> None:
    if not settings.queue_enabled:
        return

    from app.worker.tasks import process_document

    process_document.delay(document_id)
