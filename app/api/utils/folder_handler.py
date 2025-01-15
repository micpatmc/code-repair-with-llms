from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path

async def upload_folder(new_folder: Path, fid: str, files: list[UploadFile] = File(...)):
    '''
    Handles the upload of multiple or a folder of files

    Saves file to the given Path of the new folder

    Returns:

    '''

    try:
        for file in files:

            relative_path = Path(file.filename)
            target_path = new_folder / relative_path
            target_path.parent.mkdir(parents=True, exist_ok=True)

            with open(target_path, "wb") as f:
                content = await file.read()
                f.write(content)

        return {"filename": file.filename, "message": "Folder uploaded successfully.", "fid": fid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload folder: {e}")
    
    