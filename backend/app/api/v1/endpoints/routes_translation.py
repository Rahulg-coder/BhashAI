"""Translation Route."""

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.translation_service import translation_service
from app.services.languages import list_supported_languages

router = APIRouter()


class TranslationRequest(BaseModel):
    hindi_text: str = Field(..., example="बच्चों, आज हम गिनती सीखेंगे।")
    target_language: str = Field("santhali", example="santhali")
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        example={
            "grade": 1,
            "subject": "Mathematics",
            "domain": "Numbers and Operations",
            "sentence_type": "classroom_instruction"
        }
    )


@router.post("/translate", tags=["Translation"])
async def translate_text(req: TranslationRequest):
    """Context-aware translation of Hindi curriculum text to Santhali, Mundari, or Ho."""
    try:
        res = translation_service.translate(
            hindi_text=req.hindi_text,
            target_language=req.target_language,
            context=req.context
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.get("/languages", tags=["Translation"])
async def get_supported_languages():
    """List supported vernacular languages and scripts."""
    return list_supported_languages()
