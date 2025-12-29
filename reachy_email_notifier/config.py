"""Configuration management for Reachy Email Notifier."""

import os
import sys
from pathlib import Path

print("[EMAIL_NOTIFIER_CONFIG] Config module loading...", file=sys.stderr, flush=True)

# Don't load dotenv at import time - it's slow and we don't use .env anyway


class Config:
    """Application configuration."""

    # Reachy connection settings
    REACHY_IP = os.getenv('REACHY_IP', 'localhost')
    REACHY_PORT = int(os.getenv('REACHY_PORT', '50055'))

    # Gmail API settings
    # Use persistent directory that survives app updates
    PERSISTENT_DIR = Path(os.getenv('REACHY_EMAIL_NOTIFIER_DIR',
                                     Path.home() / '.reachy_email_notifier'))

    # Create persistent directory if it doesn't exist - wrapped in try/except
    try:
        PERSISTENT_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[EMAIL_NOTIFIER_CONFIG] Created persistent directory: {PERSISTENT_DIR}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"[EMAIL_NOTIFIER_CONFIG] WARNING: Failed to create persistent directory: {e}", file=sys.stderr, flush=True)
        print(f"[EMAIL_NOTIFIER_CONFIG] Continuing anyway, will fail later if credentials not found", file=sys.stderr, flush=True)

    GMAIL_CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS_PATH',
                                       str(PERSISTENT_DIR / 'credentials.json'))
    GMAIL_TOKEN_PATH = os.getenv('GMAIL_TOKEN_PATH',
                                 str(PERSISTENT_DIR / 'token.pickle'))

    print(f"[EMAIL_NOTIFIER_CONFIG] Credentials path: {GMAIL_CREDENTIALS_PATH}", file=sys.stderr, flush=True)
    print(f"[EMAIL_NOTIFIER_CONFIG] Token path: {GMAIL_TOKEN_PATH}", file=sys.stderr, flush=True)

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

print("[EMAIL_NOTIFIER_CONFIG] Config module loaded successfully!", file=sys.stderr, flush=True)
