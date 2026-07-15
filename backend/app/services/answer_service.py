def create_basic_answer(
    query: str,
    search_results: list[dict]
) -> dict:
    """
    Create a basic source-based answer from matching chunks.

    This is not an LLM answer yet.
    It only uses retrieved chunk text.
    """

    if not search_results:
        return {
            "answer": "I could not find relevant information in the uploaded document.",
            "confidence": "low",
            "source_chunks": [],
            "safety_note": (
                "This response is based only on the uploaded document and "
                "does not provide medical advice."
            )
        }

    top_result = search_results[0]

    answer = (
        "Based on the uploaded document, the most relevant information found is:\n\n"
        f"{top_result['text']}"
    )

    return {
        "answer": answer,
        "confidence": "basic keyword match",
        "source_chunks": [
            {
                "chunk_id": top_result["chunk_id"],
                "score": top_result["score"],
                "text": top_result["text"]
            }
        ],
        "safety_note": (
            "This response is based only on the uploaded document and "
            "does not provide medical advice, diagnosis, or treatment guidance."
        )
    }