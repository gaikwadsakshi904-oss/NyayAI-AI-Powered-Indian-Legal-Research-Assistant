# AI Legal Assistant 🇮🇳

A hackathon-ready Retrieval-Augmented Generation (RAG) prototype for Indian legal information.

## 1. Features

- Legal question answering using source documents
- FAISS vector search
- Sentence-Transformers embeddings
- Optional local LLM using Ollama
- PDF, DOCX and TXT document upload
- Basic contract/clause analysis
- Source cards and similarity scores
- Legal-information disclaimer
- React + Vite frontend
- FastAPI backend

## 2. Project flow

Documents
→ Text extraction
→ Cleaning
→ Chunking
→ Embeddings
→ FAISS
→ Retrieve relevant chunks
→ Prompt local LLM
→ Answer + sources

## 3. Install backend

Create a virtual environment:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

## 4. Add legal documents

Put official legal PDFs/TXT/DOCX files into:

```text
legal_documents/
```

Example:

```text
legal_documents/
└── consumer_protection/
    ├── acts/
    ├── rules/
    └── regulations/
```

Only use documents you are allowed to use. For a hackathon, prefer current official Indian government/regulator publications.

## 5. Build the FAISS index

From the `backend` directory:

```bash
python embeddings/create_embeddings.py
```

This creates:

```text
backend/vector_store/faiss_index.bin
backend/models/chunks.json
backend/models/metadata.json
```

The first embedding-model run downloads the Sentence-Transformers model.

## 6. Optional local LLM

Install Ollama separately and make sure it is running. Then install a small model, for example:

```bash
ollama pull llama3.2:3b
```

The backend expects:

```text
http://localhost:11434/api/generate
```

You can change the model with:

```text
OLLAMA_MODEL=your-model
```

If you do not run Ollama, retrieval still works, but generated answers will show a message telling you to start the local LLM.

## 7. Start backend

From `backend/`:

```bash
uvicorn app:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

## 8. Start frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally:

```text
http://localhost:5173
```

## 9. API endpoints

### Health
`GET /health`

### Legal chat
`POST /api/chat`

Body:
```json
{
  "question": "What are my consumer rights?"
}
```

### Document analysis
`POST /api/analyze`

Multipart file:
- PDF
- DOCX
- TXT

## 10. Hackathon demo

1. Add 2–5 official legal documents.
2. Build the FAISS index.
3. Start Ollama.
4. Start FastAPI.
5. Start React.
6. Ask a legal question.
7. Show the answer and source cards.
8. Upload a sample contract.
9. Demonstrate extracted clauses and potential risk terms.

## 11. Important limitation

This is an educational prototype. It should not be presented as a lawyer, court, government authority, or guaranteed legal-advice service. Always verify important legal information against current official sources and consult a qualified lawyer where appropriate.
