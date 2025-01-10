import os
import zipfile
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends

router = APIRouter()

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/zip/")
async def upload_zip(file: UploadFile = File(...)):

    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=500, detail="Only ZIP files allowed.")
    
    zip_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(zip_path, "wb") as buffer:
        buffer.write(await file.read())

    extracted_files = []

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(UPLOAD_DIR)
            extracted_files = zip_ref.namelist()
    
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid Zip File.")
    
    os.remove(zip_path)

    return {"message": "Zip File uploaded and extracted successfully", "extracted_files": extracted_files}
    
