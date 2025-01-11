from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from typing import List, Optional
from app.api.utils.zip_handler import upload_zip
from app.api.utils.file_handler import upload_file
from app.api.utils.folder_handler import upload_folder
from pathlib import Path
import uuid

router = APIRouter()

# Path where files are to be uploaded to
UPLOAD_DIR = Path("./uploads")


@router.post("/user-upload")
async def user_upload(files: List[UploadFile] = File(...)):
    '''
    API Endpoint that handles user uploading file.

    Handles the upload of a Zip file, multiple files, and a single file.

    Creates a unique folder within ./uploads for each API call made to upload files

    Parameters:
    - files List[UploadFile]: File or files to be uploaded to the pipeline

    Returns:
    - message Str: Message for upload success
    '''
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")
    
    new_folder = UPLOAD_DIR / str(uuid.uuid4())
    new_folder.mkdir(parents=True, exist_ok=True)
    
    # Switch to determine which type of upload
    match len(files), files[0].filename.endswith(".zip") if files else False:
        
        case (1, True):
            return await upload_zip(new_folder, files[0])
        
        case (1, False):
            return await upload_file(new_folder, files[0])
        
        case (_, _):
            return await upload_folder(new_folder, files)