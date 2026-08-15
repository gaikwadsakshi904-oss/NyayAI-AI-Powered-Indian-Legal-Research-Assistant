from .retriever import LegalRetriever
from .generator import generate_answer


retriever = LegalRetriever()


def answer_question(
    question: str,
    top_k: int = 5
) -> dict:

    question = question.strip()

    if not question:
        return {
            "answer": "Please enter a legal question.",
            "sources": [],
        }

    retrieved_chunks = retriever.search(
        question,
        top_k
    )

    if not retrieved_chunks:

        return {
            "answer": (
                "I could not find relevant information "
                "in the available legal documents."
            ),
            "sources": [],
        }

    answer = generate_answer(
        question,
        retrieved_chunks
    )

    sources = []

    seen = set()

    for chunk in retrieved_chunks:

        document_name = chunk.get(
            "document_name",
            "Unknown"
        )

        if document_name not in seen:

            sources.append({
                "document": document_name,
                "score": round(
                    chunk.get("score", 0),
                    4
                ),
            })

            seen.add(document_name)

    return {
        "answer": answer,
        "sources": sources,
    }