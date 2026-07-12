from pathlib import Path

from fastapi import APIRouter, File, UploadFile

router = APIRouter(prefix="/documents", tags=["Documents"])

RAW_DATA_DIR = Path("data/raw")


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not file.filename.lower().endswith(".pdf"):
        return {
            "status": "error",
            "message": "Only PDF files are allowed."
        }

    file_path = RAW_DATA_DIR / file.filename

    content = await file.read()

    with open(file_path, "wb") as saved_file:
        saved_file.write(content)

    return {
        "status": "success",
        "message": "PDF uploaded successfully.",
        "filename": file.filename,
        "saved_path": str(file_path)
    }