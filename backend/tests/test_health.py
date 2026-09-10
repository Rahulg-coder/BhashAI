"""Tests for Health Check and API bootstrap."""

import unittest
from fastapi.testclient import TestClient
from main import app


class TestHealthEndpoints(unittest.TestCase):
    """Test suite for health and basic bootstrap endpoints."""

    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        """Verify GET / returns 200 and valid JSON info."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["project"], "BhashAI")
        self.assertEqual(data["status"], "online")

    def test_health_root_endpoint(self):
        """Verify GET /health returns 200 with required SIH fields."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["app"], "BhashAI")
        self.assertIn("santhali", data["supported_languages"])
        self.assertIn("components", data)
        self.assertEqual(data["components"]["api"], "ready")

    def test_api_v1_health_endpoint(self):
        """Verify GET /api/v1/health returns matching payload."""
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")


if __name__ == "__main__":
    unittest.main()
