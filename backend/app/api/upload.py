from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.sessions import get_db
from app.schemas.document import DocumentResponse
from app.services.document_service import create_document, get_document
from app.services.exceptions import DocumentTooLargeError, EmptyDocumentError, UnsupportedDocumentTypeError
from app.services.queue_service import enqueue_document_processing

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        document = create_document(db=db, upload_file=file)
    except EmptyDocumentError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except UnsupportedDocumentTypeError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except DocumentTooLargeError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc

    enqueue_document_processing(document.id)
    return document


@router.get("/{document_id}", response_model=DocumentResponse)
def read_document(document_id: int, db: Session = Depends(get_db)):
    document = get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")
    return document
