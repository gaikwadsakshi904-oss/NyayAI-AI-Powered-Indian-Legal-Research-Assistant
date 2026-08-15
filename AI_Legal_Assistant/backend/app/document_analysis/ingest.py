import json
from pathlib import Path

from .loaders import load_document
from .text_processor import create_chunks

from ..config import (
    LEGAL_DOCUMENTS_DIR,
    CHUNKS_FILE,
)


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


def get_document_category(file_path: Path) -> str:
    name = file_path.name.lower()

    if "consumer" in name:
        return "consumer_protection"

    if "contract" in name:
        return "contract"

    if "sale" in name or "goods" in name:
        return "sale_of_goods"

    return "general_legal"


def process_document(file_path: Path) -> list[dict]:
    print(f"\nProcessing: {file_path.name}")

    text = load_document(file_path)

    if not text.strip():
        print("WARNING: No text extracted.")
        return []

    chunks = create_chunks(text)

    category = get_document_category(file_path)

    results = []

    for index, chunk in enumerate(chunks):
        results.append({
            "chunk_id": f"{file_path.stem}_{index}",
            "document_name": file_path.name,
            "document_category": category,
            "chunk_index": index,
            "text": chunk,
        })

    print(f"Characters extracted: {len(text):,}")
    print(f"Chunks created: {len(results)}")

    return results


def ingest_documents() -> list[dict]:

    files = [
        file
        for file in LEGAL_DOCUMENTS_DIR.rglob("*")
        if (
            file.is_file()
            and file.suffix.lower() in SUPPORTED_EXTENSIONS
        )
    ]

    if not files:
        print("No legal documents found.")
        print(f"Checked: {LEGAL_DOCUMENTS_DIR}")
        return []

    print(f"Found {len(files)} documents.")

    all_chunks = []

    for file_path in files:
        chunks = process_document(file_path)
        all_chunks.extend(chunks)

    with open(
        CHUNKS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            all_chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\n" + "=" * 60)
    print("DOCUMENT INGESTION COMPLETED")
    print("=" * 60)
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Saved to: {CHUNKS_FILE}")

    return all_chunks


if __name__ == "__main__":
    ingest_documents()
