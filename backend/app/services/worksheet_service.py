"""Bilingual FLN-Aligned Worksheet Generator.

Strictly links educational content to official NIPUN Bharat learning outcomes.
"""

from typing import Dict, List, Optional
from app.services.fln_service import fln_service
from app.services.languages import get_language_provider


class WorksheetService:
    """Generates bilingual student worksheets aligned with FLN competencies."""

    def generate_worksheet(
        self,
        outcome_id: str,
        lesson_id: Optional[str] = None,
        language: str = "santhali"
    ) -> Dict:
        """Generate a complete bilingual worksheet for classroom use."""
        outcome = fln_service.get_outcome_by_id(outcome_id)
        if not outcome:
            # Fallback to first outcome if not found
            all_outcomes = fln_service.get_outcomes()
            outcome = all_outcomes[0] if all_outcomes else {}

        lesson = None
        if lesson_id:
            lesson = fln_service.get_lesson_by_id(lesson_id)
        elif outcome.get("lesson_ids"):
            lesson = fln_service.get_lesson_by_id(outcome["lesson_ids"][0])

        provider = get_language_provider(language)

        # Build questions strictly aligned with the learning outcome
        if "FLN-M1-LO1" in outcome.get("outcome_id", "") or "Counting" in outcome.get("concept", ""):
            questions = [
                {
                    "q_num": 1,
                    "type": "count_and_write",
                    "hindi_instruction": "चित्र में दी गई पत्तियों को गिनें और संख्या लिखें:",
                    "native_instruction": "ᱪᱤᱛᱟᱹᱨ ᱨᱮ ᱮᱢ ᱟᱠᱟᱱ ᱥᱟᱠᱟᱢ ᱠᱚ ᱞᱮᱠᱷᱟᱭ ᱯᱮ ᱟᱨ ᱮᱞ ᱚᱞ ᱯᱮ:",
                    "phonetic_instruction": "Chitar re em akan sakam ko lekhay pe ar el ol pe:",
                    "visual_hint": "🍃 🍃 🍃",
                    "answer_key": "3 / ᱓ (ᱯᱮ)",
                },
                {
                    "q_num": 2,
                    "type": "count_and_match",
                    "hindi_instruction": "कंकड़ों की सही संख्या से मिलान करें:",
                    "native_instruction": "ᱫᱷᱤᱨᱤ ᱨᱮᱱᱟᱜ ᱴᱷᱤᱠ ᱮᱞ ᱥᱟᱶᱛᱮ ᱡᱚᱲᱟᱣ ᱯᱮ:",
                    "phonetic_instruction": "Dhiri renag thik el sawte jodaw pe:",
                    "visual_hint": "🌑 🌑 🌑 🌑 🌑  --> [ ? ]",
                    "answer_key": "5 / ᱕ (ᱢᱚᱬᱮ)",
                },
                {
                    "q_num": 3,
                    "type": "fill_in_the_blank",
                    "hindi_instruction": "छूटी हुई संख्या लिखें: 1, 2, __, 4, 5",
                    "native_instruction": "ᱥᱟᱨᱮᱡ ᱟᱠᱟᱱ ᱮᱞ ᱚᱞ ᱯᱮ: ᱑, ᱒, __, ᱔, ᱕",
                    "phonetic_instruction": "Sarej akan el ol pe: 1, 2, __, 4, 5",
                    "visual_hint": "1, 2, [ ? ], 4, 5",
                    "answer_key": "3 / ᱓",
                }
            ]
        elif "Addition" in outcome.get("concept", "") or "FLN-M1-LO3" in outcome.get("outcome_id", ""):
            questions = [
                {
                    "q_num": 1,
                    "type": "addition_concrete",
                    "hindi_instruction": "जोड़िए और कुल संख्या लिखिए: 2 आम + 1 आम =",
                    "native_instruction": "ᱢᱮᱥᱟᱭ ᱯᱮ ᱟᱨ ᱡᱚᱛᱚ ᱛᱮ ᱮᱞ ᱚᱞ ᱯᱮ: ᱒ ᱩᱞ + ᱑ ᱩᱞ =",
                    "phonetic_instruction": "Mesay pe ar joto te el ol pe: 2 ul + 1 ul =",
                    "visual_hint": "🥭 🥭  +  🥭  =  [ ? ]",
                    "answer_key": "3 / ᱓",
                },
                {
                    "q_num": 2,
                    "type": "addition_digits",
                    "hindi_instruction": "3 + 2 = कितना होगा?",
                    "native_instruction": "᱓ + ᱒ = ᱛᱤᱱᱟᱹᱜ ᱦᱩᱭᱩᱜ-ᱟ?",
                    "phonetic_instruction": "3 + 2 = tinag huyug-a?",
                    "visual_hint": "🔴 🔴 🔴  +  🔴 🔴  =  [ ? ]",
                    "answer_key": "5 / ᱕",
                }
            ]
        else:
            questions = [
                {
                    "q_num": 1,
                    "type": "comprehension",
                    "hindi_instruction": "शिक्षक के निर्देश को ध्यान से सुनकर दोहराइए:",
                    "native_instruction": "ᱢᱟᱪᱮᱛ ᱟᱜ ᱦᱩᱠᱩᱢ ᱫᱷᱮᱭᱟᱱ ᱛᱮ ᱟᱸᱡᱚᱢ ᱠᱟᱛᱮ ᱫᱚᱦᱲᱟᱭ ᱯᱮ:",
                    "phonetic_instruction": "Machet ag hukum dhiyan te añjom kate dohoray pe:",
                    "visual_hint": "👂 🗣️",
                    "answer_key": "Active participation",
                }
            ]

        worksheet_id = f"WS-{outcome.get('code', 'FLN')}-{language[:3].upper()}"

        return {
            "worksheet_id": worksheet_id,
            "title": f"BhashAI Bilingual Worksheet: {outcome.get('concept', 'FLN Practice')}",
            "grade": outcome.get("grade", 1),
            "subject": outcome.get("subject", "Mathematics"),
            "domain": outcome.get("domain", "Foundational Numeracy"),
            "competency": outcome.get("competency", ""),
            "learning_outcome_code": outcome.get("code", ""),
            "learning_outcome_hindi": outcome.get("hindi_description", ""),
            "target_language": language,
            "script": provider.script_name,
            "lesson_id": lesson.get("lesson_id") if lesson else None,
            "lesson_title": lesson.get("title_hindi") if lesson else None,
            "instructions": {
                "hindi": "सभी प्रश्नों को ध्यान से देखें और उत्तर लिखें।",
                "native": "ᱡᱚᱛᱚ ᱠᱩᱠᱞᱤ ᱫᱷᱮᱭᱟᱱ ᱛᱮ ᱧᱮᱞ ᱯᱮ ᱟᱨ ᱛᱮᱞᱟ ᱚᱞ ᱯᱮ᱾",
                "phonetic": "Joto kukli dhiyan te ñel pe ar tela ol pe."
            },
            "questions": questions,
            "student_fields": {
                "student_name_label": "विद्यार्थी का नाम / ᱯᱟᱹᱴᱷᱩᱣᱟᱹ ᱧᱩᱛᱩᱢ:",
                "date_label": "दिनांक / ᱢᱟᱹᱦᱤᱛ:"
            }
        }


# Singleton instance
worksheet_service = WorksheetService()
