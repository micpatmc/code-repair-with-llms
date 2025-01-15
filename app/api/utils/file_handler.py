from fastapi import File, UploadFile, HTTPException
from pathlib import Path

async def upload_file(new_folder: Path, fid: str, file: UploadFile = File(...)):
    '''
    Handles the upload of a single file
    Saves file to the given Path of the new folder

    Parameters:
    - new_folder: Path to the uploads folder with this instances own UUID folder
    - fid: The unique folder id
    - file: Uploaded file from frontend
    
    Returns:
    - filename: name of file uploaded
    - message: success
    - fid
    '''

    try:
        file_path = new_folder / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        return {"filename": file.filename, "message": "File uploaded successfully", "fid": fid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")