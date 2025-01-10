from fastapi import APIRouter
from app.api.endpoints import file_upload

api_router = APIRouter()

api_router.include_router(file_upload.router, prefix="/api/files_upload", tags=["Files"])