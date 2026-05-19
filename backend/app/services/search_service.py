import json
import numpy as np

from sqlalchemy.orm import Session

from app.models.chunk import DocumentChunk
from app.services.embedding_service import generate_embedding
from app.db.opensearch import client
from app.services.embedding_service import generate_embedding


INDEX_NAME = "document_chunks"

def semantic_search(query: str):
    query_embedding = generate_embedding(query)

    search_body = {
        "size": 5,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_embedding,
                    "k": 5
                }
            }
        }
    }

    response = client.search(index=INDEX_NAME, body=search_body)

    results = []
    for hit in response["hits"]["hits"]:
        source = hit["_source"]
        results.append({
            "document_id": source["document_id"],
            "chunk_text": source["chunk_text"],
            "score": hit["_score"]
        })

    return results