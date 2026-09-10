"""Health check endpoint for BhashAI."""

from datetime import datetime, timezone
from typing import Any, Dict, List
from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
    environment: str
    timestamp: str
    supported_languages: List[str]
    components: Dict[str, Any]


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check API server health, environment, and component readiness."""
    return HealthResponse(
        status="ok",
        app=settings.APP_NAME,
        version="0.1.0",
        environment=settings.APP_ENV,
        timestamp=datetime.now(timezone.utc).isoformat(),
        supported_languages=settings.SUPPORTED_LANGUAGES,
        components={
            "api": "ready",
            "asr": "standby (whisper ready)",
            "translation": "standby",
            "tts": "standby",
            "database": "configured" if settings.MONGODB_URI else "offline_mode",
        },
    )
