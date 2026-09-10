"""Central API v1 Router registering all BhashAI service endpoints."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
    routes_asr,
    routes_translation,
    routes_tts,
    routes_live,
    routes_fln,
    routes_worksheets,
    routes_flashcards,
    routes_validation,
    routes_sync
)

api_router = APIRouter()

# Health check
api_router.include_router(health.router, tags=["Health"])

# Speech & Translation Core
api_router.include_router(routes_asr.router, tags=["Speech Recognition"])
api_router.include_router(routes_translation.router, tags=["Translation"])
api_router.include_router(routes_tts.router, tags=["Text-to-Speech"])
api_router.include_router(routes_live.router, tags=["Live Translation"])

# Curriculum & Pedagogy
api_router.include_router(routes_fln.router, tags=["Curriculum"])
api_router.include_router(routes_worksheets.router, tags=["Worksheets"])
api_router.include_router(routes_flashcards.router, tags=["Flashcards"])

# Validation & Offline Sync
api_router.include_router(routes_validation.router, tags=["Validation"])
api_router.include_router(routes_sync.router, tags=["Offline Sync"])
