"""Comprehensive integration and unit test suite for BhashAI."""

import os
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

from main import app

BACKEND_DIR = Path(__file__).resolve().parent.parent
TEST_WAV = BACKEND_DIR / "test.wav"


class TestBhashAISystem(unittest.TestCase):
    """Test suite covering all core pedagogical and AI services."""

    def setUp(self):
        self.client = TestClient(app)

    def test_01_health_and_root(self):
        """Verify server status and supported languages."""
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("santhali", data["supported_languages"])

    def test_02_supported_languages(self):
        """Verify Santhali, Mundari, and Ho providers."""
        res = self.client.get("/api/v1/languages")
        self.assertEqual(res.status_code, 200)
        langs = [l["code"] for l in res.json()]
        self.assertIn("santhali", langs)
        self.assertIn("mundari", langs)
        self.assertIn("ho", langs)

    def test_03_fln_curriculum(self):
        """Verify NIPUN Bharat FLN learning outcomes and lessons."""
        # Grades
        res_g = self.client.get("/api/v1/fln/grades")
        self.assertEqual(res_g.status_code, 200)
        self.assertTrue(len(res_g.json()) >= 1)

        # Outcomes
        res_o = self.client.get("/api/v1/fln/outcomes?grade=1&subject=Mathematics")
        self.assertEqual(res_o.status_code, 200)
        outcomes = res_o.json()
        self.assertTrue(len(outcomes) >= 1)
        self.assertEqual(outcomes[0]["grade"], 1)

        # Lessons
        res_l = self.client.get("/api/v1/fln/lessons")
        self.assertEqual(res_l.status_code, 200)
        lessons = res_l.json()
        self.assertTrue(len(lessons) >= 1)
        lesson_id = lessons[0]["lesson_id"]

        res_detail = self.client.get(f"/api/v1/fln/lessons/{lesson_id}")
        self.assertEqual(res_detail.status_code, 200)
        self.assertIn("teacher_explanation", res_detail.json())

    def test_04_context_aware_translation(self):
        """Verify translation produces Ol Chiki text and respects educational context."""
        payload = {
            "hindi_text": "बच्चों, आज हम गिनती सीखेंगे।",
            "target_language": "santhali",
            "context": {
                "grade": 1,
                "subject": "Mathematics",
                "domain": "Numbers and Operations",
                "sentence_type": "classroom_instruction"
            }
        }
        res = self.client.post("/api/v1/translate", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("target_text", data)
        self.assertIn("ᱞᱮᱠᱷᱟ", data["target_text"])  # Ol Chiki 'lekha' for counting
        self.assertIn("validation", data)
        self.assertTrue(data["validation"]["confidence"] >= 0.70)

    def test_05_tts_synthesis(self):
        """Verify audio synthesis and cached audio serving."""
        payload = {
            "text": "ᱞᱮᱠᱷᱟ",
            "language": "santhali",
            "phonetic": "lekha"
        }
        res = self.client.post("/api/v1/tts", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("audio_url", data)

        # Retrieve audio file
        audio_res = self.client.get(data["audio_url"])
        self.assertEqual(audio_res.status_code, 200)
        self.assertTrue(len(audio_res.content) > 0)

    def test_06_worksheet_generation(self):
        """Verify FLN-aligned bilingual worksheet generation."""
        payload = {
            "outcome_id": "FLN-M1-LO1",
            "language": "santhali"
        }
        res = self.client.post("/api/v1/worksheets/generate", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["grade"], 1)
        self.assertTrue(len(data["questions"]) >= 1)
        self.assertIn("hindi_instruction", data["questions"][0])
        self.assertIn("native_instruction", data["questions"][0])

    def test_07_flashcard_generation(self):
        """Verify visual bilingual flashcard deck generation."""
        payload = {
            "outcome_id": "FLN-M1-LO1",
            "language": "santhali"
        }
        res = self.client.post("/api/v1/flashcards/generate", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["card_count"] >= 1)
        card = data["cards"][0]
        self.assertIn("visual", card)
        self.assertIn("hindi_label", card)
        self.assertIn("native_label", card)
        self.assertIn("audio_url", card)

    def test_08_native_validation_review(self):
        """Verify human-in-the-loop review recording."""
        payload = {
            "hindi_text": "पाँच",
            "ai_translation": "ᱢᱚᱬᱮ",
            "target_language": "santhali",
            "reviewer_name": "Birsa Hembram",
            "status": "approved",
            "corrected_translation": "ᱢᱚᱬᱮ",
            "phonetic": "mone",
            "domain": "mathematics",
            "add_to_glossary": True
        }
        res = self.client.post("/api/v1/validation/review", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "success")

        # List reviews
        res_list = self.client.get("/api/v1/validation/reviews?language=santhali")
        self.assertEqual(res_list.status_code, 200)
        self.assertTrue(len(res_list.json()) >= 1)

    def test_09_offline_sync(self):
        """Verify incremental sync payload."""
        res = self.client.get("/api/v1/sync?version=0")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["has_updates"])
        self.assertIn("fln_curriculum", data["delta"])
        self.assertIn("lessons", data["delta"])

    def test_10_live_translation_pipeline(self):
        """Verify end-to-end speech -> ASR -> Translate -> TTS pipeline."""
        if not TEST_WAV.exists():
            self.skipTest(f"Test audio {TEST_WAV} not found.")

        with open(TEST_WAV, "rb") as f:
            files = {"audio_file": ("test.wav", f, "audio/wav")}
            data = {
                "language": "santhali",
                "grade": "1",
                "subject": "Mathematics",
                "domain": "Numbers and Operations",
                "sentence_type": "classroom_instruction"
            }
            res = self.client.post("/api/v1/live-translate", files=files, data=data)

        self.assertEqual(res.status_code, 200)
        res_data = res.json()
        self.assertIn("hindi_text", res_data)
        self.assertIn("target_text", res_data)
        self.assertIn("latency_ms", res_data)
        self.assertIn("latency_breakdown", res_data)


if __name__ == "__main__":
    unittest.main()
