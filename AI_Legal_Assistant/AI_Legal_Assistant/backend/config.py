from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = BASE_DIR / "legal_documents"
VECTOR_DIR = BASE_DIR / "backend" / "vector_store"
MODEL_DIR = BASE_DIR / "backend" / "models"

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)
TOP_K = int(os.getenv("TOP_K", "5"))

# Optional local LLM through Ollama.
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
