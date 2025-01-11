from fastapi import File, UploadFile, HTTPException
from pathlib import Path

async def upload_file(new_folder: Path, file: UploadFile = File(...)):
    '''
    Handles the upload of a single file

    Saves file to the given Path of the new folder

    Returns:

    '''

    try:
        file_path = new_folder / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        return {"filename": file.filename, "message": "File uploaded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")