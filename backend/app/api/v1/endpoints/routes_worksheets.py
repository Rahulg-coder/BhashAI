"""Worksheets Route."""

from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.worksheet_service import worksheet_service

router = APIRouter()


class WorksheetGenerateRequest(BaseModel):
    outcome_id: str = Field(..., example="FLN-M1-LO1")
    lesson_id: Optional[str] = Field(None, example="LES-M1-01")
    language: str = Field("santhali", example="santhali")


@router.post("/worksheets/generate", tags=["Worksheets"])
async def generate_worksheet(req: WorksheetGenerateRequest):
    """Generate a bilingual printable worksheet aligned with NIPUN Bharat FLN."""
    try:
        return worksheet_service.generate_worksheet(
            outcome_id=req.outcome_id,
            lesson_id=req.lesson_id,
            language=req.language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate worksheet: {str(e)}")
