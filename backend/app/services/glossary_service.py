"""Educational Terminology Glossary Service.

Ensures foundational educational terms (FLN) maintain consistent, approved
vernacular translations across lessons, activities, and worksheets.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from app.config import BACKEND_DIR

GLOSSARY_PATH = BACKEND_DIR.parent / "data" / "terminology" / "glossary.json"


class GlossaryService:
    """Manages verified educational terminology mappings."""

    def __init__(self, file_path: Path = GLOSSARY_PATH):
        self.file_path = file_path
        self.terms: List[Dict] = []
        self._load_glossary()

    def _load_glossary(self) -> None:
        """Load glossary definitions from disk."""
        if not self.file_path.exists():
            self.terms = []
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.terms = data.get("terms", [])
        except Exception as e:
            print(f"Warning: Failed to load glossary file {self.file_path}: {e}")
            self.terms = []

    def get_terms(self, domain: Optional[str] = None, language: str = "santhali") -> List[Dict]:
        """Fetch all terms matching domain and language."""
        results = []
        for item in self.terms:
            if domain and item.get("domain", "").lower() != domain.lower():
                continue
            if language in item:
                results.append({
                    "hindi_term": item["hindi_term"],
                    "domain": item.get("domain", "general"),
                    "grade": item.get("grade", 1),
                    "target_language": language,
                    "target_data": item[language],
                    "approved": item[language].get("approved", True)
                })
        return results

    def find_term(self, hindi_term: str, language: str = "santhali") -> Optional[Dict]:
        """Exact lookup of a Hindi educational term."""
        query = hindi_term.strip()
        for item in self.terms:
            if item["hindi_term"] == query and language in item:
                return {
                    "hindi_term": item["hindi_term"],
                    "target_term": item[language].get("ol_chiki") or item[language].get("text"),
                    "phonetic": item[language].get("phonetic", ""),
                    "domain": item.get("domain"),
                    "approved": item[language].get("approved", True),
                }
        return None

    def replace_glossary_terms(self, text: str, language: str = "santhali") -> str:
        """Inject approved glossary terms into sentence if found."""
        modified = text
        for item in self.terms:
            ht = item["hindi_term"]
            if ht in modified and language in item:
                target_word = item[language].get("ol_chiki") or item[language].get("text")
                if target_word:
                    modified = modified.replace(ht, target_word)
        return modified

    def add_approved_term(
        self,
        hindi_term: str,
        language: str,
        target_term: str,
        phonetic: str = "",
        domain: str = "general",
        grade: int = 1
    ) -> Dict:
        """Add or update an approved native educational term."""
        found = False
        for item in self.terms:
            if item["hindi_term"] == hindi_term:
                item[language] = {
                    "ol_chiki" if language == "santhali" else "text": target_term,
                    "phonetic": phonetic,
                    "approved": True
                }
                found = True
                break

        if not found:
            new_entry = {
                "hindi_term": hindi_term,
                "domain": domain,
                "grade": grade,
                language: {
                    "ol_chiki" if language == "santhali" else "text": target_term,
                    "phonetic": phonetic,
                    "approved": True
                }
            }
            self.terms.append(new_entry)

        self._save_glossary()
        return {"hindi_term": hindi_term, "target_term": target_term, "status": "saved"}

    def _save_glossary(self) -> None:
        """Persist glossary to JSON."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0.0", "languages": ["santhali", "mundari", "ho"], "terms": self.terms}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to persist glossary: {e}")


# Singleton instance
glossary_service = GlossaryService()
