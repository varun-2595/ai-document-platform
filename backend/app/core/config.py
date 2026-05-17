import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field


BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / "app" / ".env")


def _bool(value: str | None, default: bool = False) -> bool:
    return default if value is None else value.lower() in {"1", "true", "yes", "on"}


def _csv(value: str | None, default: tuple[str, ...]) -> tuple[str, ...]:
    return default if not value else tuple(item.strip() for item in value.split(",") if item.strip())


class Settings(BaseModel):
    app_name: str = "AI Document Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    database_url: str
    upload_dir: Path = BACKEND_DIR / "uploads"
    max_upload_size_bytes: int = Field(default=10 * 1024 * 1024, gt=0)
    allowed_upload_content_types: tuple[str, ...] = ("application/pdf",)
    queue_enabled: bool = False
    redis_url: str = "redis://localhost:6379/0"
    opensearch_url: str = "http://localhost:9200"
    opensearch_index: str = "document-chunks"
    openai_api_key: str | None = None
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4.1-mini"
    chunk_size_words: int = Field(default=350, gt=0)
    chunk_overlap_words: int = Field(default=50, ge=0)

    @classmethod
    def from_env(cls) -> "Settings":
        upload_dir = Path(os.getenv("UPLOAD_DIR", str(BACKEND_DIR / "uploads")))
        if not upload_dir.is_absolute():
            upload_dir = BACKEND_DIR / upload_dir
        return cls(
            app_name=os.getenv("APP_NAME", "AI Document Platform"),
            app_version=os.getenv("APP_VERSION", "1.0.0"),
            debug=_bool(os.getenv("DEBUG")),
            database_url=os.environ["DATABASE_URL"],
            upload_dir=upload_dir,
            max_upload_size_bytes=int(os.getenv("MAX_UPLOAD_SIZE_BYTES", str(10 * 1024 * 1024))),
            allowed_upload_content_types=_csv(
                os.getenv("ALLOWED_UPLOAD_CONTENT_TYPES"),
                ("application/pdf",),
            ),
            queue_enabled=_bool(os.getenv("QUEUE_ENABLED")),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            opensearch_url=os.getenv("OPENSEARCH_URL", "http://localhost:9200"),
            opensearch_index=os.getenv("OPENSEARCH_INDEX", "document-chunks"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
            chat_model=os.getenv("CHAT_MODEL", "gpt-4.1-mini"),
            chunk_size_words=int(os.getenv("CHUNK_SIZE_WORDS", "350")),
            chunk_overlap_words=int(os.getenv("CHUNK_OVERLAP_WORDS", "50")),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()


settings = get_settings()
