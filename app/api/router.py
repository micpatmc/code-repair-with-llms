from fastapi import APIRouter
from app.api.endpoints import upload_file
from app.api.endpoints import upload_folder
from app.api.endpoints import upload_zip

api_router = APIRouter()

api_router.include_router(upload_file.router, prefix="/api/upload", tags=["Files"])
api_router.include_router(upload_folder.router, prefix="/api/upload", tags=["Files"])
api_router.include_router(upload_zip.router, prefix="/api/upload", tags=["Files"])