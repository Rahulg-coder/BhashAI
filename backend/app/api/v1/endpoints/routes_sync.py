"""Offline Synchronization Route."""

from fastapi import APIRouter, Query
from app.services.sync_service import sync_service

router = APIRouter()


@router.get("/sync", tags=["Offline Sync"])
async def sync_content(version: int = Query(0, description="Local content version on Android tablet")):
    """Incremental sync endpoint for offline Android devices."""
    return sync_service.get_sync_delta(client_version=version)
