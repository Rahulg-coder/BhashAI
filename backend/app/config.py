"""Configuration management for BhashAI."""

import os
from pathlib import Path
from typing import List
from pydantic import BaseModel

# Locate backend directory and .env file
BACKEND_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BACKEND_DIR / ".env"


def load_dotenv(env_path: Path) -> None:
    """Simple parser to load .env key-values into os.environ if not already set."""
    if not env_path.exists():
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("\"'")
            if key not in os.environ:
                os.environ[key] = val


# Load .env file
load_dotenv(ENV_FILE)


class Settings(BaseModel):
    """Application settings schema and defaults."""

    APP_NAME: str = os.getenv("APP_NAME", "BhashAI")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
        if origin.strip()
    ]

    # Languages
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "santhali")
    SUPPORTED_LANGUAGES: List[str] = [
        lang.strip()
        for lang in os.getenv("SUPPORTED_LANGUAGES", "santhali,mundari,ho").split(",")
        if lang.strip()
    ]

    # Model & Storage Paths
    ASR_MODEL_NAME: str = os.getenv("ASR_MODEL_NAME", "small")
    MODEL_CACHE_DIR: Path = BACKEND_DIR / os.getenv("MODEL_CACHE_DIR", "models/cache")

    # Database
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "bhashai")


# Global singleton instance
settings = Settings()
