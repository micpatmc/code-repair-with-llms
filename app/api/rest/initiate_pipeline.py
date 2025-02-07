from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from typing import List
from app.core.session_manager import SessionManager
from app.core.file_handler import FileHandler
from app.utils.decode_pipeline_steps import decode_pipeline_steps

def initiate_pipeline(session_manager: SessionManager) -> APIRouter:

    api_router = APIRouter()

    file_manager = FileHandler(session_manager)

    @api_router.post("/initiate_pipeline")
    async def initiate_pipeline(
            files: List[UploadFile] = File(None, description="Files to be uploaded to the pipeline"), 
            pipeline_steps: int = Query(
            default=0, 
            description="Binary representation of pipeline steps to execute (e.g., 21 for steps 1, 3, 5)"
        )
    ):
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
        if pipeline_steps == 0:
            raise HTTPException(status_code=400, detail="No stages of pipeline selected.")
        
        if pipeline_steps > 63:
            raise HTTPException(status_code=400, detail="Unknown stage selected.")
        
        if not files:
            raise HTTPException(status_code=400, detail="No files uploaded.")
        
        selected_steps = decode_pipeline_steps(pipeline_binary=pipeline_steps)
        token = session_manager.create_session(selected_steps)
        session_id = session_manager.validate_session(token)

        result = await file_manager.process_files(session_id, files)

        for step in selected_steps:
            print(f"Executing pipeline step {step}")

        return {
            "message": result["message"],
            "session_token": token,
            "files": result["filenames"],

            ### ONLY FOR TESTING
            "session_id": session_id
        }

    return api_router