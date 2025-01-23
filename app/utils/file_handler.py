from fastapi import File, UploadFile, HTTPException
from pathlib import Path

async def upload_file(new_folder: Path, file: UploadFile = File(...)):
    '''
    Handles the upload of a single file
    Saves file to the given Path of the new folder

    Parameters:
    - new_folder: Path to the uploads folder with this instances own UUID folder
    - session_id: The unique id of current pipeline session also corresponds to folder within ./uploads
    - file: Uploaded file from frontend
    
    Returns:
    - filename: name of file uploaded
    - message: success
    - session_id
    '''

    try:
        file_path = new_folder / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        return {"filenames": file.filename, "message": "File uploaded successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")