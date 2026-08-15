import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from ..config import (
    EMBEDDING_MODEL,
    FAISS_INDEX_FILE,
    FAISS_METADATA_FILE,
)


class LegalRetriever:

    def __init__(self):

        if not FAISS_INDEX_FILE.exists():
            raise FileNotFoundError(
                f"FAISS index not found: {FAISS_INDEX_FILE}"
            )

        if not FAISS_METADATA_FILE.exists():
            raise FileNotFoundError(
                f"FAISS metadata not found: {FAISS_METADATA_FILE}"
            )

        print("Loading FAISS index...")

        self.index = faiss.read_index(
            str(FAISS_INDEX_FILE)
        )

        with open(
            FAISS_METADATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            self.metadata = json.load(file)

        self.chunks = self.metadata["chunks"]

        print(
            f"Loaded {self.index.ntotal} vectors."
        )

        print(
            "Loading embedding model..."
        )

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )


    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        if not query.strip():
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index < 0:
                continue

            chunk = self.chunks[index].copy()

            chunk["score"] = float(score)

            results.append(chunk)

        return results


def create_retriever():

    return LegalRetriever()