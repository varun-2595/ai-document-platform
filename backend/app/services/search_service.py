import json
import numpy as np

from sqlalchemy.orm import Session

from app.models.document import Document
from app.services.embedding_service import generate_embedding


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )


def semantic_search(db: Session, query: str):
    query_embedding = generate_embedding(query)
    documents = db.query(Document).all()
    results = []
    for doc in documents:
        if not doc.embedding:
            continue

        stored_embedding = json.loads(doc.embedding)
        similarity = cosine_similarity(
            query_embedding,
            stored_embedding
        )
        results.append({
            "id": doc.id,
            "filename": doc.filename,
            "similarity": float(similarity)
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results[:5]