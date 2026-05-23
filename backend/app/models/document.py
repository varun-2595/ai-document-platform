from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    extracted_text = Column(Text, nullable=True)
    embedding = Column(String, nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)
    s3_key = Column(String, nullable=False)
    status = Column(String, default="UPLOADED")
    error_message = Column(Text, nullable=True)