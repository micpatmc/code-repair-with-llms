from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from typing import List, Optional
from app.core.session_manager import SessionManager
from app.core.file_handler import FileHandler

def user_upload(session_manager: SessionManager) -> APIRouter:

    api_router = APIRouter()

    file_manager = FileHandler(session_manager)

    @api_router.post("/user-upload")
    async def user_upload(files: List[UploadFile] = File(None, description="Files to be uploaded to the pipeline")):
        '''
        API Endpoint that handles user uploading file.
        Handles the upload of a Zip file, multiple files, and a single file.
        Creates a unique folder within ./uploads for each API call made to upload files

        Parameters:
        - files List[UploadFile]: File or files to be uploaded to the pipeline

        Returns:
        - Filename: Name of file uploaded
        - Message: Success of upload
        - fid: unique id of file directory within the backend server
        '''
        if not files:
            raise HTTPException(status_code=400, detail="No files uploaded.")
        
        token = session_manager.create_session()
        session_id = session_manager.validate_session(token)
        
        print(f"Session ID is : {session_id}")
        result = await file_manager.process_files(session_id, files)

        return {
            "message": "Files uploaded Successfully.",
            "session_id": session_id,
            "files": result,
        }

    return api_router