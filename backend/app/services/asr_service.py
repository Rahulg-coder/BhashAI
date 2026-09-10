"""Hindi Automatic Speech Recognition (ASR) Service using Whisper.

Optimized with CUDA auto-detection, lazy loading, and latency tracking.
"""

import math
import os
import tempfile
import time
from pathlib import Path
from typing import BinaryIO, Dict, Optional, Union
import torch
import whisper

from app.config import settings


class ASRService:
    """Manages Whisper model for Hindi classroom speech recognition."""

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.ASR_MODEL_NAME
        self._model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.fp16 = self.device == "cuda"

    @property
    def model(self):
        """Lazy-load Whisper model on first use."""
        if self._model is None:
            print(f"[ASR] Loading Whisper model '{self.model_name}' on {self.device.upper()}...")
            t0 = time.time()
            self._model = whisper.load_model(self.model_name, device=self.device)
            load_time = round((time.time() - t0) * 1000, 2)
            print(f"[ASR] Whisper loaded in {load_time}ms on {self.device.upper()}")
        return self._model

    def transcribe_file(self, file_path: Union[str, Path]) -> Dict:
        """Transcribe an audio file on disk to Hindi text."""
        start_time = time.time()
        res = self.model.transcribe(
            str(file_path),
            language="hi",
            fp16=self.fp16,
            temperature=0.0
        )
        latency_ms = round((time.time() - start_time) * 1000, 2)
        text = res.get("text", "").strip()

        # Compute confidence score from segment probabilities
        segments = res.get("segments", [])
        if segments:
            avg_logprob = sum(s.get("avg_logprob", -1.0) for s in segments) / len(segments)
            # Map logprob [-2.0, 0.0] to [0.2, 0.99]
            confidence = round(min(max(math.exp(avg_logprob), 0.1), 0.99), 2)
        else:
            confidence = 0.85 if text else 0.0

        return {
            "hindi_text": text,
            "language": "hi",
            "confidence": confidence,
            "latency_ms": latency_ms,
            "device": self.device,
            "segments_count": len(segments)
        }

    def transcribe_bytes(self, audio_bytes: bytes, file_extension: str = ".wav") -> Dict:
        """Transcribe in-memory audio bytes by writing temporarily."""
        suffix = file_extension if file_extension.startswith(".") else f".{file_extension}"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            return self.transcribe_file(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass


# Singleton instance
asr_service = ASRService()
