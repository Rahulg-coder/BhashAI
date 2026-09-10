"""Flashcards Route."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.flashcard_service import flashcard_service

router = APIRouter()


class FlashcardGenerateRequest(BaseModel):
    outcome_id: str = Field(..., example="FLN-M1-LO1")
    language: str = Field("santhali", example="santhali")


@router.post("/flashcards/generate", tags=["Flashcards"])
async def generate_flashcards(req: FlashcardGenerateRequest):
    """Generate visual bilingual flashcards aligned with learning outcomes."""
    try:
        return flashcard_service.generate_deck(
            outcome_id=req.outcome_id,
            language=req.language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate flashcards: {str(e)}")
