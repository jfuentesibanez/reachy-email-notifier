"""Configuration management for Reachy Email Notifier."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""

    # Reachy connection settings
    REACHY_IP = os.getenv('REACHY_IP', 'localhost')
    REACHY_PORT = int(os.getenv('REACHY_PORT', '50055'))

    # Gmail API settings
    # Use persistent directory that survives app updates
    PERSISTENT_DIR = Path(os.getenv('REACHY_EMAIL_NOTIFIER_DIR',
                                     Path.home() / '.reachy_email_notifier'))

    # Create persistent directory if it doesn't exist
    PERSISTENT_DIR.mkdir(parents=True, exist_ok=True)

    GMAIL_CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS_PATH',
                                       str(PERSISTENT_DIR / 'credentials.json'))
    GMAIL_TOKEN_PATH = os.getenv('GMAIL_TOKEN_PATH',
                                 str(PERSISTENT_DIR / 'token.pickle'))

    # Email checking interval (seconds)
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '60'))

    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not os.path.exists(cls.GMAIL_CREDENTIALS_PATH):
            raise FileNotFoundError(
                f"Gmail credentials file not found at {cls.GMAIL_CREDENTIALS_PATH}. "
                "Please download credentials.json from Google Cloud Console."
            )

        if cls.CHECK_INTERVAL < 10:
            raise ValueError("CHECK_INTERVAL must be at least 10 seconds to avoid rate limiting")

        return True
