from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.chat import router as chat_router
from .api.documents import router as documents_router


app = FastAPI(
    title="NyayAI",
    description="AI-powered Indian Legal Research Assistant",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


@app.get("/")
def root():

    return {
        "message": "NyayAI API is running."
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


app.include_router(
    chat_router
)

app.include_router(
    documents_router
)