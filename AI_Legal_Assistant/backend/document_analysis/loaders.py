from pathlib import Path

import pymupdf
from docx import Document


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


def load_pdf(file_path: Path) -> str:
    pages = []

    with pymupdf.open(file_path) as document:
        for page in document:
            text = page.get_text("text")

            if text:
                pages.append(text)

    return "\n".join(pages)


def load_docx(file_path: Path) -> str:
    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def load_txt(file_path: Path) -> str:
    return file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def load_document(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    if extension == ".docx":
        return load_docx(file_path)

    if extension == ".txt":
        return load_txt(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )