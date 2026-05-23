from pathlib import Path

from sqlalchemy.orm import Session

from app.models.document import Document
from app.tasks.document_tasks import process_document
from app.services.s3_services import upload_file_to_s3
from app.core.logger import logger

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"


def save_document(
    db: Session,
    filename: str,
    content: bytes
):
    logger.info(f"Uploading document: {filename}")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_path = UPLOAD_DIR / Path(filename).name

    with open(file_path, "wb") as file:
        file.write(content)

    s3_key = file_path.name
    upload_result = upload_file_to_s3(str(file_path), s3_key)

    if upload_result is None:
        raise RuntimeError("Failed to upload document to S3")

    document = Document(
        filename=filename,
        s3_key=upload_result,
        status="UPLOADED"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    logger.info(f"Document uploaded to s3: {s3_key}")

    process_document.delay(
        document.id,
        str(file_path)
    )
    logger.info(f"Queued document for processing: {document.id}")

    return document
