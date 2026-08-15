import os
import time

from google import genai


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.7-flash"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


def build_context(results):

    if not results:
        return "No relevant legal information was retrieved."

    parts = []

    for index, result in enumerate(results, start=1):

        if not isinstance(result, dict):
            continue

        document = result.get(
            "document_name",
            result.get(
                "document",
                "Unknown document"
            )
        )

        score = result.get(
            "score",
            0
        )

        text = result.get(
            "text",
            ""
        )

        parts.append(
            f"""
SOURCE {index}

Document:
{document}

Relevance Score:
{score}

Legal Information:
{text}
"""
        )

    if not parts:
        return "No usable legal information was retrieved."

    return "\n".join(parts)


def generate_with_gemini(
    question: str,
    context
):

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is not set."
        )

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    context_text = build_context(
        context
    )

    prompt = f"""
You are NyayAI, an Indian legal research assistant.

Answer the user's question ONLY using the legal information
provided below.

IMPORTANT RULES:

- Give a direct answer first.
- Explain the answer in simple language.
- Use relevant sections when they appear in the source.
- Do not invent laws, sections, cases, penalties, dates,
  or legal rights.
- Do not use outside information.
- Do not copy large portions of the source.
- If the sources do not contain enough information,
  clearly say that.
- Do not provide personalized legal advice.
- Mention the source document.

LEGAL KNOWLEDGE BASE:

{context_text}

USER QUESTION:

{question}

Return the answer using this structure:

Direct Answer:
[answer]

Explanation:
[short explanation]

Relevant Law:
[relevant sections if available]

Source:
[source document]
"""

    last_error = None

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            answer = getattr(
                response,
                "text",
                None
            )

            if not answer:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return answer.strip()

        except Exception as error:

            last_error = error

            error_text = str(error)

            print(
                f"Gemini attempt {attempt + 1}/3 failed:"
            )

            print(error_text)

            # Retry temporary server errors.
            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
            ):

                if attempt < 2:

                    time.sleep(
                        2 ** attempt
                    )

                    continue

            break

    raise RuntimeError(
        f"Gemini generation failed: {last_error}"
    )


def generate_answer(
    question: str,
    context
):

    try:

        answer = generate_with_gemini(
            question,
            context
        )

        print(
            "Gemini generation successful."
        )

        return answer

    except Exception as error:

        print(
            "Gemini generation unavailable."
        )

        print(
            f"Reason: {error}"
        )

        print(
            "Using legal-document retrieval fallback..."
        )

        context_text = build_context(
            context
        )

        return (
            "The AI generation service is temporarily "
            "unavailable.\n\n"
            "Relevant legal information retrieved "
            "from the NyayAI knowledge base:\n\n"
            + context_text
        )