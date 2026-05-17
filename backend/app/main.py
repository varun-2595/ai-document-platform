from fastapi import FastAPI
from app.api.health import router as health_router
from app.core.config import settings
from app.db.database import engine
from app.models.document import Document


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

Document.metadata.create_all(bind=engine)

app.include_router(health_router)