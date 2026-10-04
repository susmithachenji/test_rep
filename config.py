"""Central configuration for the expandtesting.com automation suite.

Every value can be overridden with an environment variable or through a local
``.env`` file (copy ``.env.example``).
"""

import os
import uuid
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

BASE_URL = os.getenv("BASE_URL", "https://practice.expandtesting.com").rstrip("/")

NOTES_API_URL = os.getenv("NOTES_API_URL", f"{BASE_URL}/notes/api").rstrip("/")
HEALTH_CHECK_URL = os.getenv("HEALTH_CHECK_URL", f"{NOTES_API_URL}/health-check")
CARS_API_URL = os.getenv("CARS_API_URL", f"{BASE_URL}/api/cars")

UI_USERNAME = os.getenv("UI_USERNAME", "practice")
UI_PASSWORD = os.getenv("UI_PASSWORD", "SuperSecretPassword!")
UI_INVALID_USERNAME = os.getenv("UI_INVALID_USERNAME", "no-such-user-1234")
UI_INVALID_PASSWORD = os.getenv("UI_INVALID_PASSWORD", "WrongPassword123")

HEADLESS = os.getenv("HEADLESS", "true").strip().lower() in {"1", "true", "yes", "on"}
SLOW_MO = int(os.getenv("SLOW_MO", "0"))

DEFAULT_TIMEOUT_MS = int(os.getenv("UI_TIMEOUT_MS", "15000"))
API_TIMEOUT_S = float(os.getenv("API_TIMEOUT_S", "30"))

TEST_USER_NAME = "Playtest User"
TEST_USER_PASSWORD = "Test@12345"

BLOCKED_URL_PATTERNS = (
    "*googletagmanager.com*",
    "*googlesyndication.com*",
    "*google-analytics.com*",
    "*doubleclick.net*",
    "*googleadservices.com*",
    "*amazon-adsystem.com*",
)


def unique_email(prefix: str = "playtest") -> str:
    """Return a fresh e-mail so every API test run gets an isolated account."""

    return f"{prefix}.{uuid.uuid4().hex[:12]}@example.com"