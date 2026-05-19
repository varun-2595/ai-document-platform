from app.db.opensearch import client

INDEX_NAME = "document_chunks"

def create_index():
    if client.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists.")
        return
    
    body = {
        "settings": {
            "index": {
                "knn": True,
            }
    },
        "mappings": {
            "properties": {
                "document_id": {"type": "integer"},
                "chunk_text": {"type": "text"},
                "embedding": {"type": "knn_vector", "dimension": 1536}
            }
        }
    }

    client.indices.create(index=INDEX_NAME, body=body)


def index_chunk(chunk_id: int, document_id: int, chunk_text: str, embedding: list):
    body = {
        "document_id": document_id,
        "chunk_text": chunk_text,
        "embedding": embedding
    }

    client.index(index=INDEX_NAME, id=chunk_id, body=body)
