import re


def clean_text(text: str) -> str:
    if not text:
        return ""

    # Remove null characters
    text = text.replace("\x00", " ")

    # Normalize spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def create_chunks(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150
) -> list[str]:

    text = clean_text(text)

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0

    while start < len(text):

        end = min(
            start + chunk_size,
            len(text)
        )

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks