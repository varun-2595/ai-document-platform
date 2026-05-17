import os
from sqlalchemy.orm import Session
from app.models.document import Document

UPLOAD_DIR = "uploads"

def save_document(db: Session, filename: str, content: bytes) -> Document:
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Save file to disk
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Create document record in database
    document = Document(filename=filename)
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return document