"""Hindi ASR Route."""

from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.asr_service import asr_service

router = APIRouter()


@router.post("/asr", tags=["Speech Recognition"])
async def transcribe_speech(audio_file: UploadFile = File(...)):
    """Transcribe spoken Hindi classroom audio into Devanagari text."""
    try:
        content = await audio_file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty audio file provided.")

        ext = audio_file.filename.split(".")[-1] if audio_file.filename and "." in audio_file.filename else "wav"
        result = asr_service.transcribe_bytes(content, file_extension=ext)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ASR transcription failed: {str(e)}")
