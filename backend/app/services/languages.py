"""Language Provider Architecture for Santhali, Mundari, and Ho.

Follows the SIH design principle of modular language expansion without
rewriting the core application.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class LanguageProvider(ABC):
    """Abstract base class for all vernacular tribal language providers."""

    @property
    @abstractmethod
    def code(self) -> str:
        """Standard ISO or FLN code (e.g. 'sat', 'mun', 'ho')."""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Display name in English and vernacular."""
        pass

    @property
    @abstractmethod
    def script_name(self) -> str:
        """Official native script (e.g., Ol Chiki, Bani Hisir, Warang Chiti)."""
        pass

    @abstractmethod
    def get_numerals(self) -> Dict[str, str]:
        """Mapping from Arabic/Hindi digits to vernacular digits."""
        pass

    @abstractmethod
    def format_bilingual(self, hindi_text: str, native_text: str, phonetic: Optional[str] = None) -> Dict[str, str]:
        """Format translated pair into structured bilingual payload."""
        pass


class SanthaliProvider(LanguageProvider):
    """Language provider for Santhali (Santali) using Ol Chiki script."""

    @property
    def code(self) -> str:
        return "santhali"

    @property
    def display_name(self) -> str:
        return "Santhali (ᱥᱟᱱᱛᱟᱲᱤ)"

    @property
    def script_name(self) -> str:
        return "Ol Chiki (sat_Olck)"

    def get_numerals(self) -> Dict[str, str]:
        # Ol Chiki digits 0-9: ᱐ ᱑ ᱒ ᱓ ᱔ ᱕ ᱖ ᱗ ᱘ ᱙
        return {
            "0": "᱐", "1": "᱑", "2": "᱒", "3": "᱓", "4": "᱔",
            "5": "᱕", "6": "᱖", "7": "᱗", "8": "᱘", "9": "᱙"
        }

    def convert_digits(self, text: str) -> str:
        """Replace standard digits with Ol Chiki digits."""
        res = text
        for d, ol in self.get_numerals().items():
            res = res.replace(d, ol)
        return res

    def format_bilingual(self, hindi_text: str, native_text: str, phonetic: Optional[str] = None) -> Dict[str, str]:
        return {
            "language": self.code,
            "script": self.script_name,
            "hindi_text": hindi_text,
            "native_text": native_text,
            "phonetic": phonetic or "",
            "display": f"{native_text} ({phonetic})" if phonetic else native_text,
        }


class MundariProvider(LanguageProvider):
    """Language provider for Mundari."""

    @property
    def code(self) -> str:
        return "mundari"

    @property
    def display_name(self) -> str:
        return "Mundari (ᱢᱩᱱᱰᱟᱨᱤ)"

    @property
    def script_name(self) -> str:
        return "Mundari Bani / Devanagari"

    def get_numerals(self) -> Dict[str, str]:
        return {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9"
        }

    def format_bilingual(self, hindi_text: str, native_text: str, phonetic: Optional[str] = None) -> Dict[str, str]:
        return {
            "language": self.code,
            "script": self.script_name,
            "hindi_text": hindi_text,
            "native_text": native_text,
            "phonetic": phonetic or "",
            "display": f"{native_text} ({phonetic})" if phonetic else native_text,
        }


class HoProvider(LanguageProvider):
    """Language provider for Ho."""

    @property
    def code(self) -> str:
        return "ho"

    @property
    def display_name(self) -> str:
        return "Ho (ᱦᱳ)"

    @property
    def script_name(self) -> str:
        return "Warang Chiti / Devanagari"

    def get_numerals(self) -> Dict[str, str]:
        return {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9"
        }

    def format_bilingual(self, hindi_text: str, native_text: str, phonetic: Optional[str] = None) -> Dict[str, str]:
        return {
            "language": self.code,
            "script": self.script_name,
            "hindi_text": hindi_text,
            "native_text": native_text,
            "phonetic": phonetic or "",
            "display": f"{native_text} ({phonetic})" if phonetic else native_text,
        }


# Registry of supported providers
_PROVIDERS: Dict[str, LanguageProvider] = {
    "santhali": SanthaliProvider(),
    "sat": SanthaliProvider(),
    "sat_olck": SanthaliProvider(),
    "mundari": MundariProvider(),
    "mun": MundariProvider(),
    "ho": HoProvider(),
}


def get_language_provider(language: str) -> LanguageProvider:
    """Factory retrieving language provider by name or code."""
    normalized = language.strip().lower()
    if normalized not in _PROVIDERS:
        # Default to Santhali per SIH requirements
        return _PROVIDERS["santhali"]
    return _PROVIDERS[normalized]


def list_supported_languages() -> List[Dict[str, str]]:
    """Return catalog of supported tribal languages."""
    return [
        {
            "code": p.code,
            "name": p.display_name,
            "script": p.script_name
        }
        for key, p in [("santhali", _PROVIDERS["santhali"]), ("mundari", _PROVIDERS["mundari"]), ("ho", _PROVIDERS["ho"])]
    ]
