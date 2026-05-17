from typing import Protocol

from app.core.config import settings
from app.schemas.document import SearchResult


class SearchIndex(Protocol):
    def index_chunks(self, chunks: list[dict]) -> None: ...
    def search(self, query_vector: list[float], top_k: int) -> list[SearchResult]: ...


class OpenSearchIndex:
    def index_chunks(self, chunks: list[dict]) -> None:
        client = self._client()
        for chunk in chunks:
            client.index(index=settings.opensearch_index, id=chunk["chunk_id"], body=chunk)

    def search(self, query_vector: list[float], top_k: int) -> list[SearchResult]:
        client = self._client()
        response = client.search(
            index=settings.opensearch_index,
            body={
                "size": top_k,
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": query_vector,
                            "k": top_k,
                        }
                    }
                },
            },
        )
        return [
            SearchResult(
                document_id=hit["_source"]["document_id"],
                chunk_id=hit["_source"]["chunk_id"],
                content=hit["_source"]["content"],
                score=hit["_score"],
            )
            for hit in response["hits"]["hits"]
        ]

    def _client(self):
        try:
            from opensearchpy import OpenSearch
        except ImportError as exc:
            raise RuntimeError("Install opensearch-py to enable search.") from exc
        return OpenSearch(settings.opensearch_url)


def search_documents(question: str, top_k: int = 5) -> list[SearchResult]:
    from app.services.embedding_service import OpenAIEmbeddingProvider

    vector = OpenAIEmbeddingProvider().embed([question])[0]
    return OpenSearchIndex().search(vector, top_k=top_k)
