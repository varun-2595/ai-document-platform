from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.sessions import get_db
from app.models.document import Document

router = APIRouter(prefix="/document_status", tags=["Document Status"])

@router.get("/{document_id}")
def get_document_status(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        return {"error": "Document not found"}

    return {
        "document_id": document.id,
        "filename": document.filename,
        "status": document.status,
        "error_message": document.error_message
    }