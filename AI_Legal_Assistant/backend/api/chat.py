from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..rag.rag_pipeline import answer_question


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10
    )


class Source(BaseModel):
    document: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


@router.post(
    "/",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        result = answer_question(
            question,
            request.top_k
        )

        return {
            "answer": result.get(
                "answer",
                "No answer generated."
            ),
            "sources": result.get(
                "sources",
                []
            )
        }

    except Exception as error:

        print(
            f"Chat API error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to process the legal question."
        )