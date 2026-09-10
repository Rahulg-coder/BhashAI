"""Text-to-Speech Route."""

from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional

from app.services.tts_service import tts_service, AUDIO_CACHE_DIR

router = APIRouter()


class TTSRequest(BaseModel):
    text: str = Field(..., example="ᱞᱮᱠᱷᱟ")
    language: str = Field("santhali", example="santhali")
    phonetic: Optional[str] = Field(None, example="lekha")


@router.post("/tts", tags=["Text-to-Speech"])
async def synthesize_speech(req: TTSRequest):
    """Generate spoken audio for tribal language text."""
    try:
        res = tts_service.synthesize(
            text=req.text,
            language=req.language,
            phonetic=req.phonetic
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {str(e)}")


@router.get("/tts/audio/{filename}", tags=["Text-to-Speech"])
async def get_audio_file(filename: str):
    """Serve cached vernacular audio file for playback."""
    file_path = AUDIO_CACHE_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found.")

    media_type = "audio/mpeg" if filename.endswith(".mp3") else "audio/wav"
    return FileResponse(file_path, media_type=media_type, filename=filename)
