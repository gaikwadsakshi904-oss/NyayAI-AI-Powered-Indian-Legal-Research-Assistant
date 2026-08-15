import json
from pathlib import Path
import faiss
import numpy as np

BASE = Path(__file__).resolve().parents[1]
INDEX_PATH = BASE / "vector_store" / "faiss_index.bin"
CHUNKS_PATH = BASE / "models" / "chunks.json"
META_PATH = BASE / "models" / "metadata.json"

def load_store():
    if not INDEX_PATH.exists():
        return None, [], []
    index = faiss.read_index(str(INDEX_PATH))
    chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))
    metadata = json.loads(META_PATH.read_text(encoding="utf-8"))
    return index, chunks, metadata

def search(query_vector, top_k=5):
    index, chunks, metadata = load_store()
    if index is None:
        return []
    q = np.asarray(query_vector, dtype="float32")
    if q.ndim == 1:
        q = q.reshape(1, -1)
    scores, ids = index.search(q, min(top_k, index.ntotal))
    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx >= 0:
            results.append({
                "score": float(score),
                "text": chunks[idx],
                "metadata": metadata[idx]
            })
    return results
