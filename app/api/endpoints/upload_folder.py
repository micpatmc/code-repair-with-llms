from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/folder/")
async def upload_folder(files: list[UploadFile] = File(...)):

    try:
        for file in files:

            relative_path = Path(file.filename)
            target_path = UPLOAD_DIR / relative_path

            target_path.parent.mkdir(parents=True, exist_ok=True)

            with open(target_path, "wb") as f:
                content = await file.read()
                f.write(content)

        return {"message": "Folder uploaded successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload folder: {e}")
    
    