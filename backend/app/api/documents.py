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
from backend.app.services.search_service import (
    load_chunks,
    search_chunks,
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
        "chunks_filename": chunks_path.name,
        "text_preview": preview_text,
        "character_count": len(extracted_text),
        "chunk_count": len(chunks),
        "preview_chunks": preview_chunks
    }


@router.get("/search")
def search_document_chunks(
    chunks_filename: str,
    query: str,
    top_k: int = 3
):
    chunks = load_chunks(chunks_filename)

    if not chunks:
        return {
            "status": "error",
            "message": "Chunks file not found or empty.",
            "query": query,
            "results": []
        }

    results = search_chunks(
        chunks=chunks,
        query=query,
        top_k=top_k
    )

    return {
        "status": "success",
        "message": "Search completed successfully.",
        "query": query,
        "chunks_filename": chunks_filename,
        "result_count": len(results),
        "results": results
    }