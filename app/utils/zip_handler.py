import os
import zipfile
from fastapi import File, UploadFile, HTTPException, Depends
from pathlib import Path

async def upload_zip(new_folder: Path, file: UploadFile = File(...)):
    '''
    Handles the upload of a Zip file
    Unzips and stores all the files to the given Path of the new folder

    Parameters:
    - new_folder: Path to the uploads folder with this instances own UUID folder
    - session_id: The unique id of current pipeline session also corresponds to folder within ./uploads
    - file: zip file uploaded
    
    Returns:
    - extracted_files: list of files extracted from the zip
    - message: success
    - session_id
    '''

    # Shouldn't ever reach this point this is checked in user_upload.py
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=500, detail="Only ZIP files allowed.")
    
    try:
        zip_path = new_folder / file.filename
        with open(zip_path, "wb") as buffer:
            buffer.write(await file.read())

        # Extracts files from the zip 
        extracted_files = []
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(new_folder)
            extracted_files = zip_ref.namelist()
        
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid Zip File.")
    
    os.remove(zip_path)

    return {"extracted_files": extracted_files, "message": "Zip File uploaded and extracted successfully"}
    
