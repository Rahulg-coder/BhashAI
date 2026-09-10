"""Real-Time Live Translation Pipeline Route.

Executes pipelined Audio Chunk -> ASR -> Context-Aware Translation -> Validation -> TTS
Tracking authentic latency against the SIH <= 3s target.
"""

import json
import time
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from typing import Optional

from app.services.asr_service import asr_service
from app.services.translation_service import translation_service
from app.services.tts_service import tts_service

router = APIRouter()


@router.post("/live-translate", tags=["Live Translation"])
async def live_translate(
    audio_file: UploadFile = File(...),
    language: str = Form("santhali"),
    grade: Optional[int] = Form(1),
    subject: Optional[str] = Form("Mathematics"),
    domain: Optional[str] = Form("Numbers and Operations"),
    lesson_id: Optional[str] = Form(None),
    sentence_type: Optional[str] = Form("classroom_instruction")
):
    """End-to-end real-time speech translation pipeline for classroom teachers."""
    t_start = time.time()

    # Read audio payload
    content = await audio_file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty audio chunk received.")

    ext = audio_file.filename.split(".")[-1] if audio_file.filename and "." in audio_file.filename else "wav"

    # 1. Hindi ASR
    asr_res = asr_service.transcribe_bytes(content, file_extension=ext)
    hindi_text = asr_res.get("hindi_text", "").strip()

    if not hindi_text:
        total_latency = round((time.time() - t_start) * 1000, 2)
        return {
            "hindi_text": "",
            "target_text": "",
            "phonetic": "",
            "audio_url": "",
            "confidence": 0.0,
            "latency_ms": total_latency,
            "latency_breakdown": {
                "asr_ms": asr_res.get("latency_ms", 0),
                "translation_ms": 0,
                "tts_ms": 0,
                "total_ms": total_latency
            },
            "requires_review": True,
            "status": "no_speech_detected"
        }

    # 2. Context-Aware Translation
    context = {
        "grade": grade,
        "subject": subject,
        "domain": domain,
        "lesson_id": lesson_id,
        "sentence_type": sentence_type
    }
    trans_res = translation_service.translate(
        hindi_text=hindi_text,
        target_language=language,
        context=context
    )

    # 3. Vernacular Audio Synthesis (TTS)
    tts_res = tts_service.synthesize(
        text=trans_res["target_text"],
        language=language,
        phonetic=trans_res.get("phonetic")
    )

    t_end = time.time()
    total_latency = round((t_end - t_start) * 1000, 2)

    val_data = trans_res.get("validation", {})
    confidence = val_data.get("confidence", 0.85)

    return {
        "hindi_text": hindi_text,
        "target_text": trans_res["target_text"],
        "phonetic": trans_res.get("phonetic", ""),
        "display": trans_res.get("display", trans_res["target_text"]),
        "target_language": language,
        "audio_url": tts_res["audio_url"],
        "confidence": confidence,
        "latency_ms": total_latency,
        "latency_breakdown": {
            "asr_ms": asr_res.get("latency_ms", 0),
            "translation_ms": trans_res.get("latency_ms", 0),
            "tts_ms": tts_res.get("latency_ms", 0),
            "total_ms": total_latency
        },
        "target_sih_met": total_latency <= 3000,
        "requires_review": val_data.get("requires_review", False),
        "validation": val_data
    }
