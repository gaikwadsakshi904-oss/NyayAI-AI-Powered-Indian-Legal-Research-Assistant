import json

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from ..config import (
    CHUNKS_FILE,
    FAISS_INDEX_FILE,
    FAISS_METADATA_FILE,
    EMBEDDING_MODEL,
)


def load_chunks():

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_FILE}. "
            "Run document ingestion first."
        )

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def build_vector_store():

    print("=" * 60)
    print("BUILDING NYAYAI FAISS VECTOR DATABASE")
    print("=" * 60)

    chunks = load_chunks()

    if not chunks:
        raise ValueError(
            "No document chunks found."
        )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print(
        f"Loading embedding model: {EMBEDDING_MODEL}"
    )

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    print(
        f"Creating embeddings for {len(texts)} chunks..."
    )

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    print(
        f"Embedding dimension: {dimension}"
    )

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(embeddings)

    faiss.write_index(
        index,
        str(FAISS_INDEX_FILE)
    )

    metadata = {
        "embedding_model": EMBEDDING_MODEL,
        "dimension": dimension,
        "total_vectors": index.ntotal,
        "chunks": chunks,
    }

    with open(
        FAISS_METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\n" + "=" * 60)
    print("FAISS VECTOR DATABASE CREATED")
    print("=" * 60)

    print(
        f"Vectors stored: {index.ntotal}"
    )

    print(
        f"Index: {FAISS_INDEX_FILE}"
    )

    print(
        f"Metadata: {FAISS_METADATA_FILE}"
    )

    return index


if __name__ == "__main__":
    build_vector_store()
