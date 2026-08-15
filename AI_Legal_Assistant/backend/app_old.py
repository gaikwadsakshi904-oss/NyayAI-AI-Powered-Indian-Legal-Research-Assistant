from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import shutil

from rag.rag_pipeline import answer_question
from document_analysis.contract_analyzer import analyze_contract
from ingestion.document_loader import load_document

app = FastAPI(title="AI Legal Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "AI Legal Assistant API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/chat")
def chat(data: Question):
    if not data.question.strip():
        raise HTTPException(400, "Question cannot be empty")
    return answer_question(data.question)

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    allowed = {".pdf", ".txt", ".docx"}
    suffix = Path(file.filename).suffix.lower()
    if suffix not in allowed:
        raise HTTPException(400, "Only PDF, TXT and DOCX files are supported.")
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)
    path = temp_dir / file.filename
    with path.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    try:
        text = load_document(path)
        return analyze_contract(text)
    finally:
        path.unlink(missing_ok=True)
