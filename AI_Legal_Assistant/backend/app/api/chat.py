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

    try:

        result = answer_question(
            request.question,
            request.top_k
        )

        return result

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
