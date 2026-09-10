"""Native Speaker Review and Human-in-the-Loop Validation Service.

Allows native speakers to review, correct, and approve translations to build
a high-quality domain-specific evaluation and fine-tuning dataset.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional

from app.config import BACKEND_DIR
from app.services.glossary_service import glossary_service
from app.services.sync_service import sync_service

REVIEWS_FILE = BACKEND_DIR.parent / "data" / "validation_reviews.json"


class ValidationReviewService:
    """Manages community and native-speaker validation workflows."""

    def __init__(self, storage_file: Path = REVIEWS_FILE):
        self.storage_file = storage_file
        self.reviews: List[Dict] = []
        self._load()

    def _load(self) -> None:
        if self.storage_file.exists():
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.reviews = data.get("reviews", [])
            except Exception:
                self.reviews = []

    def _save(self) -> None:
        try:
            self.storage_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump({"reviews": self.reviews, "total": len(self.reviews)}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving validation reviews: {e}")

    def submit_review(
        self,
        hindi_text: str,
        ai_translation: str,
        target_language: str,
        reviewer_name: str,
        status: str,  # 'approved', 'corrected', 'rejected'
        corrected_translation: Optional[str] = None,
        phonetic: Optional[str] = None,
        domain: str = "general",
        add_to_glossary: bool = False
    ) -> Dict:
        """Record reviewer validation or correction."""
        review_id = f"REV-{int(time.time())}-{len(self.reviews) + 1}"
        record = {
            "review_id": review_id,
            "timestamp": time.time(),
            "hindi_text": hindi_text,
            "ai_translation": ai_translation,
            "target_language": target_language,
            "reviewer_name": reviewer_name or "Native Reviewer",
            "status": status,
            "corrected_translation": corrected_translation or ai_translation,
            "phonetic": phonetic or "",
            "domain": domain,
            "approved": status in ("approved", "corrected"),
        }

        self.reviews.append(record)
        self._save()

        # If marked for glossary and approved/corrected, integrate into persistent glossary
        if add_to_glossary and record["approved"] and corrected_translation:
            glossary_service.add_approved_term(
                hindi_term=hindi_text,
                language=target_language,
                target_term=corrected_translation,
                phonetic=phonetic or "",
                domain=domain
            )
            # Increment content version so other offline clients receive this update
            sync_service.increment_version()

        return record

    def list_reviews(self, language: Optional[str] = None) -> List[Dict]:
        """Fetch past reviews."""
        if language:
            return [r for r in self.reviews if r.get("target_language") == language]
        return self.reviews


# Singleton instance
validation_review_service = ValidationReviewService()
