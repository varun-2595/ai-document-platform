from typing import Protocol

from app.core.config import settings


class EmbeddingProvider(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...


class OpenAIEmbeddingProvider:
    def embed(self, texts: list[str]) -> list[list[float]]:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required for embeddings.")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install openai to enable embeddings.") from exc

        client = OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(model=settings.embedding_model, input=texts)
        return [item.embedding for item in response.data]
