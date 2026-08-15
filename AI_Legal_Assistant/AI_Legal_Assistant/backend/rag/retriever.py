from embeddings.embedding import embed_texts
from vector_store.vector_store import search

def retrieve(question, top_k=5):
    vector = embed_texts([question])[0]
    return search(vector, top_k=top_k)
