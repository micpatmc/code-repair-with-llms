from fastapi import APIRouter
from app.api.rest.endpoints import user_upload

'''
    Router for defined API endpoints
'''
api_router = APIRouter()
api_router.include_router(user_upload.router, prefix="/api", tags=["Files"])
