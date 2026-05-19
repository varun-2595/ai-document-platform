from fastapi import APIRouter
from app.services.search_service import semantic_search
from app.schemas.search import SearchRequest

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/")
def search_documents(request: SearchRequest):
    results = semantic_search(query=request.query)
    return results