from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from backend.app.services.pdf_service import (
    extract_text_from_pdf,
    save_extracted_text,
)
from backend.app.services.chunking_service import (
    split_text_into_chunks,
    save_chunks,
)

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

    extracted_text = extract_text_from_pdf(file_path)
    processed_path = save_extracted_text(file.filename, extracted_text)

    chunks = split_text_into_chunks(extracted_text)
    chunks_path = save_chunks(file.filename, chunks)

    preview_text = extracted_text[:1000]
    preview_chunks = chunks[:3]

    return {
        "status": "success",
        "message": "PDF uploaded, text extracted, and chunks created successfully.",
        "filename": file.filename,
        "saved_path": str(file_path),
        "processed_text_path": str(processed_path),
        "chunks_path": str(chunks_path),
        "text_preview": preview_text,
        "character_count": len(extracted_text),
        "chunk_count": len(chunks),
        "preview_chunks": preview_chunks
    }