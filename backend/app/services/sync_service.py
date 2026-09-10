"""Offline Synchronization Service for Android Tablets & Central Cloud.

Implements incremental content sync using monotonic content versions.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import BACKEND_DIR
from app.services.fln_service import fln_service
from app.services.glossary_service import glossary_service

SYNC_METADATA_FILE = BACKEND_DIR.parent / "data" / "sync_version.json"


class SyncService:
    """Provides incremental delta synchronization for offline Android devices."""

    def __init__(self, metadata_file: Path = SYNC_METADATA_FILE):
        self.metadata_file = metadata_file
        self.current_version = 1
        self._load_version()

    def _load_version(self) -> None:
        """Load or initialize sync metadata."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.current_version = data.get("content_version", 1)
            except Exception:
                self.current_version = 1
        else:
            self._save_version()

    def _save_version(self) -> None:
        """Save sync metadata."""
        try:
            self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump({"content_version": self.current_version, "last_updated": time.time()}, f, indent=2)
        except Exception as e:
            print(f"Error saving sync version: {e}")

    def increment_version(self) -> int:
        """Increment version when content is modified or approved."""
        self.current_version += 1
        self._save_version()
        return self.current_version

    def get_sync_delta(self, client_version: int = 0) -> Dict[str, Any]:
        """Compute sync payload for an Android client."""
        # If client is already up to date, return empty delta
        if client_version >= self.current_version:
            return {
                "server_version": self.current_version,
                "client_version": client_version,
                "has_updates": False,
                "message": "Local device is already synchronized with master.",
                "delta": {}
            }

        # Otherwise package delta content
        delta = {
            "fln_curriculum": fln_service.curriculum,
            "lessons": fln_service.lessons,
            "glossary": glossary_service.terms,
            "supported_languages": ["santhali", "mundari", "ho"]
        }

        return {
            "server_version": self.current_version,
            "client_version": client_version,
            "has_updates": True,
            "message": f"Updated from version {client_version} to {self.current_version}.",
            "delta": delta
        }


# Singleton instance
sync_service = SyncService()
