from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    filename: str
    extracted_text: str | None
    upload_time: datetime

    class Config:
        from_attributes = True