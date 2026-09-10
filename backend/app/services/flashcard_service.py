"""Bilingual Visual Flashcard Generator for MTB-MLE.

Reinforces foundational concepts with concrete visual graphics,
dual-script labels, and native audio triggers.
"""

from typing import Dict, List, Optional
from app.services.fln_service import fln_service
from app.services.languages import get_language_provider
from app.services.tts_service import tts_service


class FlashcardService:
    """Generates pedagogical flashcards reinforcing FLN concepts."""

    def generate_deck(
        self,
        outcome_id: str,
        language: str = "santhali"
    ) -> Dict:
        """Generate a complete deck of visual bilingual flashcards."""
        outcome = fln_service.get_outcome_by_id(outcome_id)
        if not outcome:
            all_outcomes = fln_service.get_outcomes()
            outcome = all_outcomes[0] if all_outcomes else {}

        provider = get_language_provider(language)

        cards: List[Dict] = []

        # Numeracy Counting Deck
        if "Counting" in outcome.get("concept", "") or "M1.1" in outcome.get("competency_code", ""):
            items = [
                {"count": 1, "visual": "🍎", "hindi": "एक सेब", "native": "ᱢᱤᱫᱴᱟᱝ ᱥᱮᱣ", "phonetic": "midtang sew"},
                {"count": 2, "visual": "🍃 🍃", "hindi": "दो पत्ते", "native": "ᱵᱟᱨᱭᱟ ᱥᱟᱠᱟᱢ", "phonetic": "barya sakam"},
                {"count": 3, "visual": "🐦 🐦 🐦", "hindi": "तीन चिड़ियाँ", "native": "ᱯᱮᱭᱟ ᱪᱮᱬᱮ", "phonetic": "peya chene"},
                {"count": 4, "visual": "✏️ ✏️ ✏️ ✏️", "hindi": "चार पेंसिल", "native": "ᱯᱩᱱᱭᱟᱹ ᱯᱮᱱᱥᱤᱞ", "phonetic": "punya pencil"},
                {"count": 5, "visual": "⭐ ⭐ ⭐ ⭐ ⭐", "hindi": "पाँच तारे", "native": "ᱢᱚᱬᱮᱭᱟ ᱤᱯᱤᱞ", "phonetic": "moneya ipil"},
            ]
        elif "Addition" in outcome.get("concept", ""):
            items = [
                {"count": "1 + 1", "visual": "🍎 + 🍎 = 🍎🍎", "hindi": "एक और एक दो", "native": "ᱢᱤᱫ ᱟᱨ ᱢᱤᱫ ᱵᱟᱨ", "phonetic": "mid ar mid bar"},
                {"count": "2 + 1", "visual": "🍃🍃 + 🍃 = 🍃🍃🍃", "hindi": "दो और एक तीन", "native": "ᱵᱟᱨ ᱟᱨ ᱢᱤᱫ ᱯᱮ", "phonetic": "bar ar mid pe"},
                {"count": "2 + 2", "visual": "⭐⭐ + ⭐⭐ = ⭐⭐⭐⭐", "hindi": "दो और दो चार", "native": "ᱵᱟᱨ ᱟᱨ ᱵᱟᱨ ᱯᱩᱱ", "phonetic": "bar ar bar pun"},
            ]
        else:
            items = [
                {"count": "Classroom", "visual": "🏫", "hindi": "विद्यालय / स्कूल", "native": "ᱟᱥᱲᱟ", "phonetic": "asda"},
                {"count": "Teacher", "visual": "👨‍🏫", "hindi": "शिक्षक", "native": "ᱢᱟᱪᱮᱛ", "phonetic": "machet"},
                {"count": "Book", "visual": "📖", "hindi": "किताब", "native": "ᱯᱩᱛᱷᱤ", "phonetic": "puthi"},
                {"count": "Student", "visual": "🎒", "hindi": "विद्यार्थी", "native": "ᱯᱟᱹᱴᱷᱩᱣᱟᱹ", "phonetic": "pathuwa"},
            ]

        for idx, item in enumerate(items, 1):
            # Synthesize or link audio
            audio_info = tts_service.synthesize(
                text=item["native"],
                language=language,
                phonetic=item["phonetic"]
            )

            cards.append({
                "card_id": f"FC-{outcome.get('code', 'LO')}-{idx}",
                "order": idx,
                "visual": item["visual"],
                "hindi_label": item["hindi"],
                "native_label": item["native"],
                "phonetic_label": item["phonetic"],
                "script": provider.script_name,
                "audio_url": audio_info["audio_url"],
                "concept": outcome.get("concept", "")
            })

        return {
            "deck_id": f"DECK-{outcome.get('outcome_id', 'LO')}-{language}",
            "outcome_id": outcome.get("outcome_id"),
            "learning_outcome": outcome.get("description"),
            "target_language": language,
            "card_count": len(cards),
            "cards": cards
        }


# Singleton instance
flashcard_service = FlashcardService()
