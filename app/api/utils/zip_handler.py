import os
import zipfile
from fastapi import File, UploadFile, HTTPException, Depends
from pathlib import Path

async def upload_zip(new_folder: Path, file: UploadFile = File(...)):
    '''
    Handles the upload of a Zip file

    Unzips and stores all the files to the given Path of the new folder

    Returns:

    '''

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

    return {"message": "Zip File uploaded and extracted successfully", "extracted_files": extracted_files}
    
