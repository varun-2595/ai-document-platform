import os
from sqlalchemy.orm import Session
from app.models.document import Document
from app.services.pdf_service import extract_text_from_pdf

UPLOAD_DIR = "uploads"

def save_document(db: Session, filename: str, content: bytes) -> Document:
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Save file to disk
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)
    
    # Create document record in database
    document = Document(filename=filename, extracted_text=extracted_text)
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return document