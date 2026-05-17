from app.core.config import settings
from app.schemas.document import QueryResponse, QuerySource
from app.services.search_service import search_documents


def answer_question(question: str, top_k: int = 5) -> QueryResponse:
    results = search_documents(question, top_k=top_k)
    if not results:
        return QueryResponse(answer="I could not find relevant information in the indexed documents.", sources=[])

    context = "\n\n".join(result.content for result in results)
    answer = _generate_answer(question, context)
    return QueryResponse(
        answer=answer,
        sources=[
            QuerySource(document_id=result.document_id, chunk_id=result.chunk_id, content=result.content)
            for result in results
        ],
    )


def _generate_answer(question: str, context: str) -> str:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required for AI querying.")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Install openai to enable AI querying.") from exc

    client = OpenAI(api_key=settings.openai_api_key)
    response = client.responses.create(
        model=settings.chat_model,
        input=[
            {
                "role": "system",
                "content": "Answer only from the supplied context. If the answer is absent, say so.",
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return response.output_text
