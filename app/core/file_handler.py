from pathlib import Path
from typing import List
from app.utils.zip_handler import upload_zip
from app.utils.file_handler import upload_file
from app.utils.folder_handler import upload_folder
from app.core.session_manager import SessionManager
from fastapi import HTTPException, UploadFile, File

class FileHandler:
    '''
    Handles file-related operations for the REST & Websocket API's
    '''

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def process_files(self, session_id: str, files: List[UploadFile] = File(None)):

        directory: Path = self.session_manager.get_session_path(session_id)

        if not files:
            raise HTTPException(status_code=400, detail="No files uploaded")
        
            # Switch to determine which type of upload
        match len(files), files[0].filename.endswith(".zip") if files else False:
            
            case (1, True):
                return await upload_zip(directory, files[0])
            
            case (1, False):
                print("File")
                return await upload_file(directory, files[0])
            
            case (_, _):
                print("Folder")
                return await upload_folder(directory, files)

        