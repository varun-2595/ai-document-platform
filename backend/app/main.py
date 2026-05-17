from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.query import router as query_router
from app.api.search import router as search_router
from app.api.upload import router as upload_router
from app.core.config import settings
from app.core.logging import configure_logging


configure_logging()
app = FastAPI(title=settings.app_name, version=settings.app_version)
app.include_router(health_router)
app.include_router(search_router)
app.include_router(upload_router)
app.include_router(query_router)
