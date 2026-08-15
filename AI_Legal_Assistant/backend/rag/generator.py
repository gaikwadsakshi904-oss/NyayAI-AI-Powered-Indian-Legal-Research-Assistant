from openai import OpenAI

from ..config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
)

from ..utils.safety import add_disclaimer


if OPENAI_API_KEY:
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )
else:
    client = None


SYSTEM_PROMPT = """
You are NyayAI, an AI-powered Indian legal research assistant.

Answer questions using ONLY the legal context provided.

Rules:

1. Do not invent legal provisions, sections, cases, or facts.
2. Use only the retrieved legal documents.
3. Explain legal information in simple language.
4. Mention the relevant source documents.
5. If the context is insufficient, clearly say so.
6. Do not provide professional legal advice.
"""


def fallback_answer(
    question: str,
    retrieved_chunks: list[dict]
) -> str:

    if not retrieved_chunks:
        return add_disclaimer(
            "No relevant legal information was found "
            "in the available documents."
        )

    answer_parts = [
        "OpenAI generation is currently unavailable. "
        "Below is the relevant legal information retrieved "
        "from the NyayAI legal knowledge base.\n"
    ]

    for index, chunk in enumerate(
        retrieved_chunks[:5],
        start=1
    ):

        document = chunk.get(
            "document_name",
            "Unknown document"
        )

        text = chunk.get(
            "text",
            ""
        )

        answer_parts.append(
            f"Relevant Source {index}:\n"
            f"{document}\n"
            f"{text}\n"
        )

    return add_disclaimer(
        "\n".join(answer_parts)
    )


def generate_answer(
    question: str,
    retrieved_chunks: list[dict]
) -> str:

    if not retrieved_chunks:
        return add_disclaimer(
            "I could not find relevant information "
            "in the available legal documents."
        )

    # Temporary fallback when no API key is available
    if client is None:
        return fallback_answer(
            question,
            retrieved_chunks
        )

    context_parts = []

    for index, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        context_parts.append(
            f"""
SOURCE {index}
Document: {chunk.get("document_name", "Unknown")}
Category: {chunk.get("document_category", "Unknown")}
Relevance Score: {chunk.get("score", 0):.4f}

Content:
{chunk.get("text", "")}
"""
        )

    context = "\n".join(
        context_parts
    )

    user_prompt = f"""
LEGAL DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

Answer the question using only the supplied legal context.

At the end provide:

Sources:
- Document names used.
"""

    try:

        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=SYSTEM_PROMPT,
            input=user_prompt,
        )

        return add_disclaimer(
            response.output_text
        )

    except Exception as error:

        print(
            f"OpenAI unavailable: {error}"
        )

        return fallback_answer(
            question,
            retrieved_chunks
        )