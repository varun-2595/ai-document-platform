import os

from sqlalchemy.orm import Session

from app.models.document import Document
from app.tasks.document_tasks import process_document

UPLOAD_DIR = "uploads"


def save_document(
    db: Session,
    filename: str,
    content: bytes
):
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as file:
        file.write(content)

    document = Document(
        filename=filename
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    process_document.delay(
        document.id,
        file_path
    )

    return document