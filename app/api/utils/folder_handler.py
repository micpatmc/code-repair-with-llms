from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
from typing import List

async def upload_folder(new_folder: Path, session_id: str, files: List[UploadFile] = File(...)):
    '''
    Handles the upload of multiple or a folder of files
    Saves file to the given Path of the new folder

    Parameters:
    - new_folder: Path to the uploads folder with this instances own UUID folder
    - session_id: The unique id of current pipeline session also corresponds to folder within ./uploads
    - files: list of files to be uploaded
    
    Returns:
    - filename: list of files uploaded
    - message: success
    - session_id
    '''

    try:

        uploaded_files = []
        for file in files:

            uploaded_files.append(file.filename)

            relative_path = Path(file.filename)
            target_path = new_folder / relative_path

            target_path.parent.mkdir(parents=True, exist_ok=True)

            with open(target_path, "wb") as f:
                content = await file.read()
                f.write(content)

        return {"filenames": uploaded_files, "message": "Folder uploaded successfully.", "fid": fid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload folder: {e}")
    
    