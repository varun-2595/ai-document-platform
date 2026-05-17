from fastapi import APIRouter

from app.schemas.document import QueryRequest, QueryResponse
from app.services.query_service import answer_question

router = APIRouter(tags=["Query"])


@router.post("/query", response_model=QueryResponse)
def query_documents(payload: QueryRequest):
    return answer_question(payload.question, top_k=payload.top_k)
