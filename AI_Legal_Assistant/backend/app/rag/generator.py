from openai import OpenAI

from ..config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
)

from ..utils.safety import add_disclaimer


# ==========================================================
# OPENAI CONFIGURATION
# ==========================================================

# Set this to True only when your OpenAI account has credits.
#
# Currently your account has:
# credit_balance_exhausted
#
# Therefore we keep OpenAI disabled and use the
# FAISS legal-document retrieval fallback.
#
USE_OPENAI = False


client = None

if USE_OPENAI and OPENAI_API_KEY:

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )


# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are NyayAI, an AI-powered Indian legal research assistant.

Answer questions using ONLY the legal context provided by
the retrieval system.

Rules:

1. Do not invent legal provisions, sections, cases, or facts.
2. Use only the retrieved legal documents.
3. Explain legal information in simple language.
4. Mention the relevant source documents.
5. If the context is insufficient, clearly say so.
6. Do not provide professional legal advice.
"""


# ==========================================================
# FALLBACK ANSWER
# ==========================================================

def fallback_answer(
    question: str,
    retrieved_chunks: list[dict]
) -> str:

    if not retrieved_chunks:

        return add_disclaimer(
            "I could not find relevant information "
            "in the available legal documents."
        )


    answer_parts = [

        "The following relevant information was "
        "retrieved from the NyayAI legal knowledge base:"
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

        score = chunk.get(
            "score",
            0
        )


        answer_parts.append(

            f"""
Relevant Source {index}:

Document:
{document}

Relevance Score:
{score:.4f}

Legal Information:
{text}
"""
        )


    return add_disclaimer(
        "\n".join(answer_parts)
    )


# ==========================================================
# GENERATE ANSWER
# ==========================================================

def generate_answer(
    question: str,
    retrieved_chunks: list[dict]
) -> str:

    # ------------------------------------------------------
    # No retrieved information
    # ------------------------------------------------------

    if not retrieved_chunks:

        return add_disclaimer(

            "No relevant legal information was found "
            "in the available legal documents."
        )


    # ------------------------------------------------------
    # OpenAI disabled
    # ------------------------------------------------------

    if not USE_OPENAI:

        print(
            "OpenAI generation disabled."
        )

        print(
            "Using legal-document retrieval fallback..."
        )

        return fallback_answer(
            question,
            retrieved_chunks
        )


    # ------------------------------------------------------
    # OpenAI client unavailable
    # ------------------------------------------------------

    if client is None:

        print(
            "OpenAI client unavailable."
        )

        print(
            "Using legal-document retrieval fallback..."
        )

        return fallback_answer(
            question,
            retrieved_chunks
        )


    # ------------------------------------------------------
    # Build legal context
    # ------------------------------------------------------

    context_parts = []


    for index, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        context_parts.append(

            f"""
SOURCE {index}

Document:
{chunk.get(
    "document_name",
    "Unknown"
)}

Category:
{chunk.get(
    "document_category",
    "Unknown"
)}

Relevance Score:
{chunk.get(
    "score",
    0
):.4f}

Content:
{chunk.get(
    "text",
    ""
)}
"""
        )


    context = "\n".join(
        context_parts
    )


    # ------------------------------------------------------
    # User prompt
    # ------------------------------------------------------

    user_prompt = f"""

LEGAL DOCUMENT CONTEXT:

{context}


USER QUESTION:

{question}


Answer the question using ONLY the supplied legal context.

Explain the answer clearly and concisely.

At the end provide:

Sources:
- Document names used.
"""


    # ------------------------------------------------------
    # OpenAI request
    # ------------------------------------------------------

    try:

        response = client.responses.create(

            model=OPENAI_MODEL,

            instructions=SYSTEM_PROMPT,

            input=user_prompt,
        )


        return add_disclaimer(

            response.output_text
        )


    # ------------------------------------------------------
    # API error fallback
    # ------------------------------------------------------

    except Exception as error:

        print(
            "\nOpenAI generation unavailable."
        )

        print(
            f"Reason: {error}"
        )

        print(
            "Using legal-document retrieval fallback..."
        )


        return fallback_answer(
            question,
            retrieved_chunks
        )
