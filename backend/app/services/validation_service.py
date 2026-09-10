"""Translation Validation Service for MTB-MLE.

Validates low-resource tribal language translations for educational context,
terminology consistency, and semantic alignment.
"""

from typing import Dict, List, Optional
from app.services.glossary_service import glossary_service


class ValidationService:
    """Evaluates candidate translations before presenting to teachers or students."""

    def validate_translation(
        self,
        hindi_text: str,
        target_text: str,
        target_language: str = "santhali",
        context: Optional[Dict] = None
    ) -> Dict:
        """Run validation checks on Hindi -> Vernacular translation."""
        context = context or {}
        domain = context.get("domain", "").lower()
        sentence_type = context.get("sentence_type", "general")

        notes: List[str] = []
        terminology_ok = True
        terminology_matches = 0
        terminology_required = 0

        # 1. Terminology consistency check
        glossary_terms = glossary_service.get_terms(language=target_language)
        for term in glossary_terms:
            ht = term["hindi_term"]
            if ht in hindi_text:
                terminology_required += 1
                native_expected = term["target_data"].get("ol_chiki") or term["target_data"].get("text", "")
                phonetic_expected = term["target_data"].get("phonetic", "")
                
                # Check if expected native term appears in translation
                if native_expected and (native_expected in target_text or phonetic_expected.lower() in target_text.lower()):
                    terminology_matches += 1
                else:
                    terminology_ok = False
                    notes.append(f"Approved terminology '{native_expected}' for Hindi '{ht}' was not found in translation.")

        # 2. Heuristic Semantic & Length sanity check
        hindi_words = len(hindi_text.split())
        target_words = len(target_text.split())
        length_ratio = target_words / max(hindi_words, 1)

        # In Santhali/Mundari, sentence word count is usually between 0.6x and 1.8x Hindi word count
        if 0.5 <= length_ratio <= 2.2:
            length_score = 0.95
        else:
            length_score = 0.70
            notes.append(f"Word length ratio {round(length_ratio, 2)} deviates from typical vernacular structure.")

        # 3. Context validation (Classroom instruction words)
        context_score = 0.90
        if sentence_type in ("instruction", "activity_instruction"):
            instruction_cues = ["ᱠᱟᱹᱢᱤ", "ᱯᱮ", "ᱞᱮᱠᱷᱟᱭ", "ᱫᱚᱦᱚᱭ", "ᱩᱫᱩᱜ", "ᱢᱮᱛᱟᱜ", "ᱫᱩᱲᱩᱵ"]
            if any(cue in target_text for cue in instruction_cues):
                context_score = 0.98
            else:
                context_score = 0.85
                notes.append("Sentence flagged as classroom instruction but lacks standard imperative markers.")

        # 4. Terminology score calculation
        if terminology_required > 0:
            terminology_score = round(terminology_matches / terminology_required, 2)
        else:
            terminology_score = 1.0

        # 5. Composite Confidence Calculation
        # Avoid arbitrary blackbox numbers; weight cleanly based on verified terminology and context
        confidence = round(
            (0.40 * terminology_score) +
            (0.35 * length_score) +
            (0.25 * context_score),
            2
        )

        requires_review = confidence < 0.80 or not terminology_ok

        return {
            "confidence": confidence,
            "terminology_ok": terminology_ok,
            "terminology_matches": f"{terminology_matches}/{terminology_required}",
            "semantic_score": round(length_score, 2),
            "context_score": round(context_score, 2),
            "requires_review": requires_review,
            "validation_notes": notes
        }


# Singleton instance
validation_service = ValidationService()
