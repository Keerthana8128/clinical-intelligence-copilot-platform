from pydantic import BaseModel


class ChunkPreview(BaseModel):
    chunk_id: int
    text: str
    character_count: int


class SearchResult(BaseModel):
    chunk_id: int
    text: str
    character_count: int
    score: int


class SourceChunk(BaseModel):
    chunk_id: int
    score: int
    text: str


class DocumentUploadResponse(BaseModel):
    status: str
    message: str
    document_id: str | None = None
    upload_timestamp: str | None = None
    metadata_path: str | None = None
    filename: str | None = None
    saved_path: str | None = None
    processed_text_path: str | None = None
    chunks_path: str | None = None
    chunks_filename: str | None = None
    file_size_kb: float | None = None
    page_count: int | None = None
    text_preview: str | None = None
    character_count: int | None = None
    chunk_count: int | None = None
    preview_chunks: list[ChunkPreview] = []



class DocumentSearchResponse(BaseModel):
    status: str
    message: str
    query: str
    chunks_filename: str | None = None
    result_count: int
    results: list[SearchResult] = []


class DocumentAskResponse(BaseModel):
    status: str
    message: str
    query: str
    chunks_filename: str | None = None
    result_count: int | None = None
    answer: str | None = None
    confidence: str | None = None
    reason: str | None = None
    source_chunks: list[SourceChunk] = []
    suggested_questions: list[str] = []
    safety_note: str | None = None

class DocumentMetadata(BaseModel):
    document_id: str
    filename: str
    saved_path: str
    processed_text_path: str
    chunks_path: str
    chunks_filename: str
    file_size_kb: float
    page_count: int
    character_count: int
    chunk_count: int
    upload_timestamp: str


class DocumentListResponse(BaseModel):
    status: str
    message: str
    document_count: int
    documents: list[DocumentMetadata] = []