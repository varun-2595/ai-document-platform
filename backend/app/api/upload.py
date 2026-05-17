from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db.sessions import get_db
from app.services.document_service import save_document
from app.schemas.document import DocumentResponse

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    document = save_document(db=db, filename=file.filename, content=content)
    return document