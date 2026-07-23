from pathlib import Path

from fastapi import APIRouter, File, UploadFile
from backend.app.services.metadata_service import (
    create_document_id,
    get_current_timestamp,
    save_document_metadata,
    list_documents,
)

from backend.app.services.file_validation_service import (
    is_pdf_file,
    is_file_size_allowed,
    sanitize_filename,
)

from backend.app.services.metadata_service import (
    create_document_id,
    get_current_timestamp,
    save_document_metadata,
    list_documents,
)
from backend.app.services.pdf_service import (
    extract_text_from_pdf,
    save_extracted_text,
    get_pdf_page_count,
)
from backend.app.services.chunking_service import (
    split_text_into_chunks,
    save_chunks,
)
from backend.app.services.search_service import (
    load_chunks,
    search_chunks,
)
from backend.app.services.answer_service import create_basic_answer
from backend.app.schemas.document_schemas import (
    DocumentUploadResponse,
    DocumentSearchResponse,
    DocumentAskResponse,
    DocumentListResponse,
)
from backend.app.services.answer_service import create_basic_answer

router = APIRouter(prefix="/documents", tags=["Documents"])

RAW_DATA_DIR = Path("data/raw")


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not is_pdf_file(file.filename):
        return {
            "status": "error",
            "message": "Only PDF files are allowed."
        }

    safe_filename = sanitize_filename(file.filename)
    file_path = RAW_DATA_DIR / safe_filename

    content = await file.read()
    file_size_bytes = len(content)
    file_size_kb = round(file_size_bytes / 1024, 2)

    if not is_file_size_allowed(file_size_bytes):
        return {
            "status": "error",
            "message": "File size is too large. Maximum allowed size is 10 MB."
        }

    with open(file_path, "wb") as saved_file:
        saved_file.write(content)

    page_count = get_pdf_page_count(file_path)

    extracted_text = extract_text_from_pdf(file_path)
    processed_path = save_extracted_text(safe_filename, extracted_text)

    chunks = split_text_into_chunks(extracted_text)
    chunks_path = save_chunks(safe_filename, chunks)

    preview_text = extracted_text[:1000]
    preview_chunks = chunks[:3]
    
    document_id = create_document_id()
    upload_timestamp = get_current_timestamp()

    document_metadata = {
        "document_id": document_id,
        "filename": safe_filename,
        "saved_path": str(file_path),
        "processed_text_path": str(processed_path),
        "chunks_path": str(chunks_path),
        "chunks_filename": chunks_path.name,
        "file_size_kb": file_size_kb,
        "page_count": page_count,
        "character_count": len(extracted_text),
        "chunk_count": len(chunks),
        "upload_timestamp": upload_timestamp
    }

    metadata_path = save_document_metadata(document_metadata)
    return {
        "status": "success",
        "message": "PDF uploaded, validated, text extracted, chunks created, and metadata saved successfully.",
        "document_id": document_id,
        "filename": safe_filename,
        "saved_path": str(file_path),
        "processed_text_path": str(processed_path),
        "chunks_path": str(chunks_path),
        "chunks_filename": chunks_path.name,
        "file_size_kb": file_size_kb,
        "page_count": page_count,
        "text_preview": preview_text,
        "character_count": len(extracted_text),
        "chunk_count": len(chunks),
        "upload_timestamp": upload_timestamp,
        "metadata_path": str(metadata_path),
        "preview_chunks": preview_chunks
    }


@router.get("/search", response_model=DocumentSearchResponse)
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
    "chunks_filename": chunks_filename,
    "result_count": 0,
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


@router.get("/ask", response_model=DocumentAskResponse)
def ask_document_question(
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
    "chunks_filename": chunks_filename,
    "result_count": 0,
    "answer": None,
    "confidence": "low",
    "reason": "Chunks file was not found or empty.",
    "source_chunks": [],
    "suggested_questions": [],
    "safety_note": "This response is based only on the uploaded document and does not provide medical advice."
}

    results = search_chunks(
        chunks=chunks,
        query=query,
        top_k=top_k
    )

    answer_data = create_basic_answer(
        query=query,
        search_results=results
    )

    return {
    "status": "success",
    "message": "Structured source-based answer created successfully.",
    "query": query,
    "chunks_filename": chunks_filename,
    "result_count": len(results),
    "answer": answer_data["answer"],
    "confidence": answer_data["confidence"],
    "reason": answer_data["reason"],
    "source_chunks": answer_data["source_chunks"],
    "suggested_questions": answer_data["suggested_questions"],
    "safety_note": answer_data["safety_note"]
}
@router.get("/list", response_model=DocumentListResponse)
def list_uploaded_documents():
    documents = list_documents()

    return {
        "status": "success",
        "message": "Documents retrieved successfully.",
        "document_count": len(documents),
        "documents": documents
    }