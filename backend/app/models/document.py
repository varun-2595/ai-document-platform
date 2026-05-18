from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    extracted_text = Column(String, nullable=True)
    embedding = Column(String, nullable=True)
    upload_time = Column(DateTime, default=datetime.utcnow)