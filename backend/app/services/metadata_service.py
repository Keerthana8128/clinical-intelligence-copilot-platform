import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


METADATA_DIR = Path("data/processed/metadata")
METADATA_FILE = METADATA_DIR / "documents.json"


def create_document_id() -> str:
    """
    Create a unique document ID for each uploaded document.
    """

    return str(uuid.uuid4())


def get_current_timestamp() -> str:
    """
    Create a UTC timestamp for when the document was processed.
    """

    return datetime.now(timezone.utc).isoformat()


def load_document_metadata() -> list[dict]:
    """
    Load existing document metadata from JSON file.
    """

    if not METADATA_FILE.exists():
        return []

    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_document_metadata(document_metadata: dict) -> Path:
    """
    Save one document metadata record into documents.json.
    """

    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    existing_metadata = load_document_metadata()
    existing_metadata.append(document_metadata)

    with open(METADATA_FILE, "w", encoding="utf-8") as file:
        json.dump(existing_metadata, file, indent=2)

    return METADATA_FILE


def list_documents() -> list[dict]:
    """
    Return all saved document metadata records.
    """

    return load_document_metadata()