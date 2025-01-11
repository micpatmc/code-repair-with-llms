from fastapi import APIRouter
from app.api.endpoints import user_upload


api_router = APIRouter()

api_router.include_router(user_upload.router, prefix="/api", tags=["Files"])
