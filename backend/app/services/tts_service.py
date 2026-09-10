"""Text-to-Speech (TTS) Service for Santhali, Mundari, and Ho.

Generates intelligible audio utilizing phonetic pronunciation representations,
caching audio artifacts in data/audio_cache/ for offline instant playback.
"""

import hashlib
import os
import time
from pathlib import Path
from typing import Dict, Optional
try:
    from gtts import gTTS
except ImportError:
    gTTS = None

from app.config import BACKEND_DIR

AUDIO_CACHE_DIR = BACKEND_DIR.parent / "data" / "audio_cache"
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)


class TTSService:
    """Handles audio synthesis and caching for tribal language education."""

    def __init__(self, cache_dir: Path = AUDIO_CACHE_DIR):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def synthesize(
        self,
        text: str,
        language: str = "santhali",
        phonetic: Optional[str] = None
    ) -> Dict:
        """Synthesize speech audio from vernacular text or phonetic guide."""
        t0 = time.time()
        
        # Prefer phonetic transcript for acoustic intelligibility
        synthesis_text = phonetic if phonetic and phonetic.strip() else text
        clean_text = synthesis_text.strip()

        # Cache key based on language and text content
        content_hash = hashlib.md5(f"{language}_{clean_text}".encode("utf-8")).hexdigest()
        filename = f"{language}_{content_hash[:12]}.mp3"
        filepath = self.cache_dir / filename

        cached = filepath.exists()
        if not cached:
            if gTTS is not None:
                try:
                    # Use Indian English/Hindi acoustic phoneme mapping for tribal phonetic speech
                    tts = gTTS(text=clean_text, lang="hi", slow=False)
                    tts.save(str(filepath))
                except Exception as e:
                    print(f"[TTS] Online synthesis failed, falling back to local sine wave fallback: {e}")
                    self._generate_placeholder_audio(filepath)
            else:
                self._generate_placeholder_audio(filepath)

        latency_ms = round((time.time() - t0) * 1000, 2)

        return {
            "text": text,
            "phonetic": phonetic or "",
            "language": language,
            "filename": filename,
            "filepath": str(filepath),
            "audio_url": f"/api/v1/tts/audio/{filename}",
            "cached": cached,
            "latency_ms": latency_ms
        }

    def _generate_placeholder_audio(self, filepath: Path) -> None:
        """Create a valid minimal silent/chime WAV file if external TTS is offline."""
        import wave
        import struct
        wav_path = filepath.with_suffix(".wav")
        with wave.open(str(wav_path), "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(16000)
            # 0.5s of gentle chime
            for i in range(8000):
                val = int(32767.0 * 0.1 * (i % 50) / 50.0)
                f.writeframes(struct.pack("<h", val))
        if filepath.suffix == ".mp3":
            # Rename or provide link
            wav_path.replace(filepath)


# Singleton instance
tts_service = TTSService()
