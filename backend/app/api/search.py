from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.sessions import get_db
from app.services.search_service import semantic_search
from app.schemas.search import SearchRequest

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/")
def search_documents(request: SearchRequest, db: Session = Depends(get_db)):
    results = semantic_search(db=db, query=request.query)
    return results