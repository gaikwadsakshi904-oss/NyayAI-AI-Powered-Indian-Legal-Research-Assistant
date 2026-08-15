import sys
from pathlib import Path
import json
import numpy as np
import faiss

sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import DOCUMENTS_DIR, VECTOR_DIR, MODEL_DIR
from ingestion.document_loader import load_document
from ingestion.text_cleaner import clean_text
from ingestion.chunker import chunk_text
from embeddings.embedding import embed_texts

def build_index():
    VECTOR_DIR.mkdir(exist_ok=True)
    MODEL_DIR.mkdir(exist_ok=True)

    chunks = []
    metadata = []

    for path in DOCUMENTS_DIR.rglob("*"):
        if path.suffix.lower() not in {".pdf", ".txt", ".docx"}:
            continue
        try:
            text = clean_text(load_document(path))
            for i, chunk in enumerate(chunk_text(text)):
                chunks.append(chunk)
                metadata.append({
                    "source": path.name,
                    "path": str(path.relative_to(DOCUMENTS_DIR)),
                    "chunk_id": i
                })
        except Exception as e:
            print(f"Skipping {path}: {e}")

    if not chunks:
        raise RuntimeError("No legal documents found in legal_documents/")

    vectors = np.asarray(embed_texts(chunks), dtype="float32")
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, str(VECTOR_DIR / "faiss_index.bin"))
    (MODEL_DIR / "chunks.json").write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (MODEL_DIR / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Indexed {len(chunks)} chunks.")

if __name__ == "__main__":
    build_index()
