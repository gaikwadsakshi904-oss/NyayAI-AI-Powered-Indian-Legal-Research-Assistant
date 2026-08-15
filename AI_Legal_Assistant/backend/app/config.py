from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LEGAL_DOCUMENTS_DIR = PROJECT_ROOT / "legal documents"

DATA_DIR = PROJECT_ROOT / "data"

CHUNKS_DIR = DATA_DIR / "chunks"

FAISS_DIR = DATA_DIR / "faiss"

CHUNKS_FILE = CHUNKS_DIR / "legal_chunks.json"

FAISS_INDEX_FILE = FAISS_DIR / "legal.index"

FAISS_METADATA_FILE = FAISS_DIR / "metadata.json"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

OPENAI_MODEL = "gpt-5-mini"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHUNKS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

FAISS_DIR.mkdir(
    parents=True,
    exist_ok=True
)
