import json
from pathlib import Path


CHUNKS_DATA_DIR = Path("data/processed/chunks")


def load_chunks(chunks_filename: str) -> list[dict]:
    """
    Load chunks from a saved JSON file.
    """

    chunks_path = CHUNKS_DATA_DIR / chunks_filename

    if not chunks_path.exists():
        return []

    with open(chunks_path, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    return chunks


def search_chunks(
    chunks: list[dict],
    query: str,
    top_k: int = 3
) -> list[dict]:
    """
    Search chunks using simple keyword matching.

    This is not semantic search yet.
    It checks how often query words appear in each chunk.
    """

    query_words = query.lower().split()
    results = []

    for chunk in chunks:
        chunk_text = chunk["text"].lower()

        score = 0

        for word in query_words:
            if word in chunk_text:
                score += chunk_text.count(word)

        if score > 0:
            results.append(
                {
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                    "character_count": chunk["character_count"],
                    "score": score
                }
            )

    results = sorted(
        results,
        key=lambda result: result["score"],
        reverse=True
    )

    return results[:top_k]