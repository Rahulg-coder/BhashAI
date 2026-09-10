"""Main FastAPI Application Entrypoint for BhashAI.

Smart India Hackathon 2026 - Problem Statement SIH26042:
Mother Tongue-Based Multilingual Education (MTB-MLE) Assistant.
"""

import sys
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings, BACKEND_DIR
from app.api.v1.api import api_router
from app.api.v1.endpoints.health import health_check

FRONTEND_DIR = BACKEND_DIR.parent / "frontend"

# Force UTF-8 on Windows standard streams if needed
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

app = FastAPI(
    title="BhashAI — Vernacular Pedagogy & Real-Time Translation API",
    description=(
        "AI-powered vernacular pedagogy and real-time translation system for "
        "Mother Tongue-Based Multilingual Education (MTB-MLE) in tribal languages "
        "(Santhali, Mundari, Ho)."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS if "*" not in settings.ALLOWED_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root-level health check endpoint (as specified in SIH requirements: GET /health)
app.add_api_route("/health", health_check, methods=["GET"], tags=["Health"])

# API v1 Router prefix
app.include_router(api_router, prefix="/api/v1")

# Mount frontend files
if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")


@app.get("/", tags=["Root"])
async def root_view():
    """Serve the Teacher Tablet Application at root URL."""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {
        "project": "BhashAI",
        "description": "Vernacular Pedagogy & Real-Time Translation API (SIH 2026)",
        "version": "0.1.0",
        "health_check": "/health",
        "documentation": "/docs",
        "status": "online",
    }


@app.get("/manifest.json", tags=["Root"])
async def manifest_view():
    """Serve PWA manifest."""
    manifest_path = FRONTEND_DIR / "manifest.json"
    if manifest_path.exists():
        return FileResponse(str(manifest_path), media_type="application/manifest+json")


@app.get("/sw.js", tags=["Root"])
async def service_worker_view():
    """Serve Service Worker."""
    sw_path = FRONTEND_DIR / "sw.js"
    if sw_path.exists():
        return FileResponse(str(sw_path), media_type="application/javascript")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
