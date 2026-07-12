from fastapi import FastAPI

from backend.app.api.routes import router as main_router
from backend.app.api.documents import router as documents_router
from backend.app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version
)

app.include_router(main_router)
app.include_router(documents_router)