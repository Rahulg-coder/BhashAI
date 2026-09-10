"""Validation & Human-in-the-Loop Review Route."""

from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.validation_review_service import validation_review_service

router = APIRouter()


class ReviewSubmissionRequest(BaseModel):
    hindi_text: str = Field(..., example="बच्चों, आज हम गिनती सीखेंगे।")
    ai_translation: str = Field(..., example="ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ, ᱛᱮᱦᱮᱧ ᱫᱚ ᱟᱵᱚ ᱞᱮᱠᱷᱟ ᱵᱚ ᱪᱮᱫ-ᱟ᱾")
    target_language: str = Field("santhali", example="santhali")
    reviewer_name: Optional[str] = Field("Native Teacher Reviewer", example="Soma Murmu")
    status: str = Field("approved", example="approved")  # 'approved', 'corrected', 'rejected'
    corrected_translation: Optional[str] = Field(None, example="ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ, ᱛᱮᱦᱮᱧ ᱫᱚ ᱟᱵᱚ ᱞᱮᱠᱷᱟ ᱵᱚ ᱪᱮᱫ-ᱟ᱾")
    phonetic: Optional[str] = Field(None, example="Gidra ko, teheñ do abo lekha bo ched-a.")
    domain: Optional[str] = Field("mathematics", example="mathematics")
    add_to_glossary: Optional[bool] = Field(True, example=True)


@router.post("/validation/review", tags=["Validation"])
async def submit_review(req: ReviewSubmissionRequest):
    """Submit human validation or correction for an AI-generated translation."""
    try:
        record = validation_review_service.submit_review(
            hindi_text=req.hindi_text,
            ai_translation=req.ai_translation,
            target_language=req.target_language,
            reviewer_name=req.reviewer_name,
            status=req.status,
            corrected_translation=req.corrected_translation,
            phonetic=req.phonetic,
            domain=req.domain,
            add_to_glossary=req.add_to_glossary
        )
        return {"status": "success", "message": "Review submitted successfully", "review": record}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit review: {str(e)}")


@router.get("/validation/reviews", tags=["Validation"])
async def get_reviews(language: Optional[str] = None):
    """List historical validation reviews and corrections."""
    return validation_review_service.list_reviews(language=language)
