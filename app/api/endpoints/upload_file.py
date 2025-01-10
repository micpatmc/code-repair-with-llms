from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/file/")

async def upload_file(file: UploadFile = File(...)):

    try:
        file_path = UPLOAD_DIR / file.filepathname
        with open(file_path, "wb") as f:
            content = await files.read()
            f.write(content)
        
        return {"filename": file.filename, "message": "File uploaded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")