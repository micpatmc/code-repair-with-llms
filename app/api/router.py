from fastapi import APIRouter
from app.api.rest.user_upload import user_upload
from app.core.session_manager import SessionManager

'''
    Router for defined API endpoints
'''
def api_router(session_manager: SessionManager) -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(user_upload(session_manager), prefix="/api", tags=["Files"])

    return api_router
