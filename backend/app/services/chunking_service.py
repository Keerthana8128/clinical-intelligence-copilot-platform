from pathlib import Path
import json


CHUNKS_DATA_DIR = Path("data/processed/chunks")


def split_text_into_chunks(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150
) -> list[dict]:
    """
    Split long document text into smaller overlapping chunks.

    Each chunk contains:
    - chunk_id
    - text
    - character_count
    """

    chunks = []
    start = 0
    chunk_id = 1

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "character_count": len(chunk_text)
                }
            )

        chunk_id += 1
        start += chunk_size - chunk_overlap

    return chunks


def save_chunks(filename: str, chunks: list[dict]) -> Path:
    """
    Save document chunks into a JSON file.
    """

    CHUNKS_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_filename = filename.replace(".pdf", "_chunks.json")
    output_path = CHUNKS_DATA_DIR / output_filename

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(chunks, file, indent=2)

    return output_path