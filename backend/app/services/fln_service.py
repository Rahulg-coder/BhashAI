"""NIPUN Bharat Foundational Literacy and Numeracy (FLN) Curriculum Service."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import BACKEND_DIR

CURRICULUM_PATH = BACKEND_DIR.parent / "data" / "fln" / "curriculum.json"
LESSONS_PATH = BACKEND_DIR.parent / "data" / "fln" / "lessons.json"


class FLNService:
    """Provides official NIPUN Bharat curriculum data and verified lesson plans."""

    def __init__(self, curriculum_file: Path = CURRICULUM_PATH, lessons_file: Path = LESSONS_PATH):
        self.curriculum_file = curriculum_file
        self.lessons_file = lessons_file
        self.curriculum: Dict[str, Any] = {}
        self.lessons: List[Dict[str, Any]] = []
        self._load_data()

    def _load_data(self) -> None:
        """Load curriculum and lessons from storage."""
        if self.curriculum_file.exists():
            try:
                with open(self.curriculum_file, "r", encoding="utf-8") as f:
                    self.curriculum = json.load(f)
            except Exception as e:
                print(f"Error reading curriculum file: {e}")

        if self.lessons_file.exists():
            try:
                with open(self.lessons_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.lessons = data.get("lessons", [])
            except Exception as e:
                print(f"Error reading lessons file: {e}")

    def get_grades(self) -> List[Dict[str, Any]]:
        """List grades defined in curriculum."""
        grades = []
        for g in self.curriculum.get("grades", []):
            grades.append({
                "grade": g["grade"],
                "name": g["name"],
                "subjects": [s["subject"] for s in g.get("subjects", [])]
            })
        return grades

    def get_outcomes(self, grade: Optional[int] = None, subject: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve learning outcomes filtered by grade and subject."""
        outcomes = []
        for g in self.curriculum.get("grades", []):
            if grade is not None and g["grade"] != grade:
                continue
            for s in g.get("subjects", []):
                if subject and s["subject"].lower() != subject.lower():
                    continue
                for d in s.get("domains", []):
                    for c in d.get("competencies", []):
                        for lo in c.get("learning_outcomes", []):
                            outcomes.append({
                                "outcome_id": lo["outcome_id"],
                                "grade": g["grade"],
                                "subject": s["subject"],
                                "domain": d["domain"],
                                "competency_code": c["code"],
                                "competency": c["competency"],
                                "code": lo["code"],
                                "description": lo["description"],
                                "hindi_description": lo["hindi_description"],
                                "concept": lo["concept"],
                                "lesson_ids": lo.get("lesson_ids", [])
                            })
        return outcomes

    def get_outcome_by_id(self, outcome_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific learning outcome by its ID."""
        for lo in self.get_outcomes():
            if lo["outcome_id"] == outcome_id:
                return lo
        return None

    def get_lessons(self, grade: Optional[int] = None, subject: Optional[str] = None, outcome_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List structured lessons with filters."""
        results = []
        for l in self.lessons:
            if grade is not None and l.get("grade") != grade:
                continue
            if subject and l.get("subject", "").lower() != subject.lower():
                continue
            if outcome_id and l.get("fln_outcome_id") != outcome_id:
                continue
            results.append(l)
        return results

    def get_lesson_by_id(self, lesson_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve full structured lesson."""
        for l in self.lessons:
            if l.get("lesson_id") == lesson_id:
                return l
        return None


# Singleton instance
fln_service = FLNService()
