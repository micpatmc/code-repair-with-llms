from pathlib import Path
from typing import List
from app.api.utils.zip_handler import upload_zip
from app.api.utils.file_handler import upload_file
from app.api.utils.folder_handler import upload_folder
import uuid

class FileHandler:
    '''
    Handles file-related operations for the REST & Websocket API's
    '''

    def __init__(self, upload_dir: Path):
        self.upload_dir = upload_dir

    def create_upload_directory(self) -> Path:
        """
        Create unique dir for each user session
        """

        