from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path

async def upload_folder(new_folder: Path, fid: str, files: list[UploadFile] = File(...)):
    '''
    Handles the upload of multiple or a folder of files
    Saves file to the given Path of the new folder

    Parameters:
    - new_folder: Path to the uploads folder with this instances own UUID folder
    - fid: The unique folder id
    - files: list of files to be uploaded
    
    Returns:
    - filename: list of files uploaded
    - message: success
    - fid
    '''

    try:

        files = []
        for file in files:
            files.add(file.filename)
            relative_path = Path(file.filename)
            target_path = new_folder / relative_path
            target_path.parent.mkdir(parents=True, exist_ok=True)

            with open(target_path, "wb") as f:
                content = await file.read()
                f.write(content)

        return {"filenames": files, "message": "Folder uploaded successfully.", "fid": fid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload folder: {e}")
    
    