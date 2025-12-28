"""Main application for Reachy Email Notifier.

This module provides both:
1. Standalone mode (for Reachy 2 with reachy-sdk)
2. Reachy Mini App mode (for Hugging Face community apps)
"""

import time
import signal
import sys
from typing import Optional

from .config import Config
from .gmail_checker import GmailChecker

# Try to import for standalone mode
try:
    from .reachy_controller import ReachyNotifier
    STANDALONE_MODE_AVAILABLE = True
except ImportError:
    STANDALONE_MODE_AVAILABLE = False

# Try to import for Reachy Mini App mode
try:
    from .app import ReachyMiniEmailNotifier
    REACHY_MINI_APP_AVAILABLE = True
except ImportError:
    REACHY_MINI_APP_AVAILABLE = False


class EmailNotifierApp:
    """Main application that monitors Gmail and controls Reachy."""

    def __init__(self):
        """Initialize the email notifier application."""
        self.running = False
        self.gmail_checker: Optional[GmailChecker] = None
        self.reachy_notifier: Optional[ReachyNotifier] = None
        self.previous_unread_count = 0

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, sig, frame):
        """Handle shutdown signals."""
        print("\n\nShutting down gracefully...")
        self.running = False

    def setup(self):
        """Set up Gmail and Reachy connections."""
        print("🚀 Starting Reachy Email Notifier...")
        print("=" * 50)

        # Validate configuration
        try:
            Config.validate()
        except (FileNotFoundError, ValueError) as e:
            print(f"❌ Configuration error: {e}")
            return False

        # Initialize Gmail checker
        print("\n📧 Connecting to Gmail...")
        try:
            self.gmail_checker = GmailChecker(
                credentials_path=Config.GMAIL_CREDENTIALS_PATH,
                token_path=Config.GMAIL_TOKEN_PATH
            )
            # Get initial unread count
            self.previous_unread_count = self.gmail_checker.check_for_new_emails()
            print(f"✅ Gmail connected. Current unread emails: {self.previous_unread_count}")
        except Exception as e:
            print(f"❌ Failed to connect to Gmail: {e}")
            return False

        # Initialize Reachy controller
        print(f"\n🤖 Connecting to Reachy at {Config.REACHY_IP}:{Config.REACHY_PORT}...")
        try:
            self.reachy_notifier = ReachyNotifier(
                host=Config.REACHY_IP,
                port=Config.REACHY_PORT
            )
            print("✅ Reachy controller initialized")
        except Exception as e:
            print(f"⚠️  Reachy connection issue: {e}")
            print("Continuing in demo mode...")

        print("\n" + "=" * 50)
        print(f"✨ Email notifier is now running!")
        print(f"📊 Checking for emails every {Config.CHECK_INTERVAL} seconds")
        print("Press Ctrl+C to stop\n")

        return True

    def run(self):
        """Main application loop."""
        if not self.setup():
            return

        self.running = True

        while self.running:
            try:
                # Check for new emails
                current_unread_count = self.gmail_checker.check_for_new_emails()

                # Detect new emails
                if current_unread_count > self.previous_unread_count:
                    new_emails = current_unread_count - self.previous_unread_count
                    print(f"\n🎉 New email(s) detected! Count: {new_emails}")

                    # Get the subject of the latest email
                    subject = self.gmail_checker.get_latest_email_subject()
                    if subject:
                        print(f"📬 Subject: {subject}")

                    # Trigger Reachy notification
                    self.reachy_notifier.notify(new_emails)

                    # Update previous count
                    self.previous_unread_count = current_unread_count
                elif current_unread_count < self.previous_unread_count:
                    # Emails were read
                    self.previous_unread_count = current_unread_count
                    print(f"📭 Emails read. Current unread: {current_unread_count}")

                # Wait for next check
                time.sleep(Config.CHECK_INTERVAL)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(Config.CHECK_INTERVAL)

        self.cleanup()

    def cleanup(self):
        """Clean up resources before exit."""
        print("\n🧹 Cleaning up...")
        if self.reachy_notifier:
            self.reachy_notifier.disconnect()
        print("👋 Goodbye!")

    @staticmethod
    def start():
        """Static method to start the application."""
        app = EmailNotifierApp()
        app.run()


def main():
    """Entry point for the application."""
    # For Reachy Mini App mode, export the app class
    if REACHY_MINI_APP_AVAILABLE:
        return ReachyMiniEmailNotifier()

    # For standalone mode, run the full application
    if STANDALONE_MODE_AVAILABLE:
        EmailNotifierApp.start()
    else:
        print("Error: Neither reachy-mini nor reachy-sdk is available.")
        print("Please install one of:")
        print("  - pip install reachy-mini (for Reachy Mini)")
        print("  - pip install reachy-sdk (for Reachy 2)")


if __name__ == '__main__':
    main()
