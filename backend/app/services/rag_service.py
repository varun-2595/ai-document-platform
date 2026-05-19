from app.services.search_service import semantic_search
from app.services.embedding_service import generate_answer


def ask_question(question: str):
    search_results = semantic_search(question)

    context_chunks = []

    for result in search_results:
        context_chunks.append(result["chunk_text"])

    context = "\n\n".join(context_chunks)

    answer = generate_answer(
        question=question,
        context=context
    )

    return {
        "question": question,
        "answer": answer,
        "context": context_chunks
    }