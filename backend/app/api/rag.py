from fastapi import APIRouter

from app.schemas.rag import QuestionRequest
from app.services.rag_service import ask_question

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


@router.post("/ask")
def ask_ai(
    request: QuestionRequest
):
    return ask_question(
        request.question
    )