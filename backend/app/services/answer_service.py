def create_basic_answer(
    query: str,
    search_results: list[dict]
) -> dict:
    """
    Create a structured source-based answer from matching chunks.

    This is not an LLM answer yet.
    It only uses retrieved document chunks.
    """

    safety_note = (
        "This response is based only on the uploaded document. "
        "It does not provide medical advice, diagnosis, or treatment guidance. "
        "Please consult a qualified healthcare professional for medical decisions."
    )

    if not search_results:
        return {
            "answer": "I could not find relevant information in the uploaded document.",
            "confidence": "low",
            "reason": "No matching chunks were found for the question.",
            "source_chunks": [],
            "suggested_questions": [
                "Can you explain this document to me?",
                "What should I ask my doctor about this document?",
                "Are there any important follow-up instructions mentioned?"
            ],
            "safety_note": safety_note
        }

    top_result = search_results[0]

    answer = (
        "Based on the uploaded document, I found the following relevant information:\n\n"
        f"{top_result['text']}"
    )

    suggested_questions = [
        "Can you explain what this means for my health?",
        "Do I need any follow-up based on this document?",
        "Are there any medication or lifestyle changes I should understand?"
    ]

    return {
        "answer": answer,
        "confidence": "basic keyword match",
        "reason": (
            "The answer was created from the highest-scoring matching document chunk. "
            "This is keyword-based retrieval, not semantic AI reasoning yet."
        ),
        "source_chunks": [
            {
                "chunk_id": top_result["chunk_id"],
                "score": top_result["score"],
                "text": top_result["text"]
            }
        ],
        "suggested_questions": suggested_questions,
        "safety_note": safety_note
    }