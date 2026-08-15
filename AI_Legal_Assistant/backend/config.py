from pathlib import Path
import os

from dotenv import load_dotenv


# Load .env file
load_dotenv()


# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LEGAL_DOCUMENTS_DIR = (
    PROJECT_ROOT / "legal documents"
)

DATA_DIR = (
    PROJECT_ROOT / "data"
)

CHUNKS_DIR = (
    DATA_DIR / "chunks"
)

FAISS_DIR = (
    DATA_DIR / "faiss"
)


# ==========================================================
# DATA FILES
# ==========================================================

CHUNKS_FILE = (
    CHUNKS_DIR / "legal_chunks.json"
)

FAISS_INDEX_FILE = (
    FAISS_DIR / "legal.index"
)

FAISS_METADATA_FILE = (
    FAISS_DIR / "metadata.json"
)


# ==========================================================
# AI CONFIGURATION
# ==========================================================

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

OPENAI_MODEL = "gpt-5-mini"

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)


# ==========================================================
# CREATE REQUIRED DIRECTORIES
# ==========================================================

CHUNKS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

FAISS_DIR.mkdir(
    parents=True,
    exist_ok=True
)