from fastapi import FastAPI
from app.api.health import router as health_router
from app.core.config import settings
from app.db.database import engine
from app.models.document import Document
from app.api.upload import router as upload_router
from app.api.search import router as search_router
from app.models.chunk import DocumentChunk
from app.db.database import Base
from app.services.opensearch_service import create_index
from app.api.rag import router as rag_router


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

Base.metadata.create_all(bind=engine)
create_index()

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(rag_router)
