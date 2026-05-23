from fastapi import FastAPI, Request
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
from app.api.document_status import router as document_status_router
import time
from app.core.logger import logger


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Completed request: {request.method} {request.url} in {process_time:.4f}s with status code {response.status_code}")
    return response

Base.metadata.create_all(bind=engine)
create_index()

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(rag_router)
app.include_router(document_status_router)
