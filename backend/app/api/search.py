from fastapi import APIRouter, Query

from app.schemas.document import SearchResult
from app.services.search_service import search_documents

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/search", response_model=list[SearchResult])
def search(q: str = Query(..., min_length=1), top_k: int = Query(5, ge=1, le=20)):
    return search_documents(q, top_k=top_k)
