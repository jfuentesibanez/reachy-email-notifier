"""Reachy Mini Email Notifier App - Main app class for Hugging Face integration."""

import threading
import time
from typing import Optional

try:
    from reachy_mini import ReachyMini, ReachyMiniApp
    from reachy_mini.utils import create_head_pose
except ImportError:
    print("Warning: reachy_mini not installed. For Hugging Face app, install reachy-mini package.")
    ReachyMiniApp = object

from .gmail_checker import GmailChecker
from .config import Config


class ReachyMiniEmailNotifier(ReachyMiniApp):
    """
    Reachy Mini Email Notifier App.

    This app monitors your Gmail account and makes Reachy perform cute
    animations when new emails arrive.
    """

    # Optional: URL to custom configuration page
    # custom_app_url: str | None = "http://localhost:5173"
    custom_app_url: str | None = None

    def __init__(self):
        """Initialize the email notifier app."""
        super().__init__()
        self.gmail_checker: Optional[GmailChecker] = None
        self.previous_unread_count = 0

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event):
        """
        Main app logic - runs in background thread.

        Args:
            reachy_mini: Already initialized and connected Reachy Mini instance
            stop_event: Event to signal when app should stop
        """
        print("🚀 Starting Reachy Mini Email Notifier...")
        print("=" * 50)

        # Initialize Gmail checker
        try:
            print("\n📧 Connecting to Gmail...")
            self.gmail_checker = GmailChecker(
                credentials_path=Config.GMAIL_CREDENTIALS_PATH,
                token_path=Config.GMAIL_TOKEN_PATH
            )
            self.previous_unread_count = self.gmail_checker.check_for_new_emails()
            print(f"✅ Gmail connected. Current unread emails: {self.previous_unread_count}")
        except Exception as e:
            print(f"❌ Failed to connect to Gmail: {e}")
            print("Make sure credentials.json is configured properly.")
            return

        print("\n" + "=" * 50)
        print(f"✨ Email notifier is now running!")
        print(f"📊 Checking for emails every {Config.CHECK_INTERVAL} seconds")
        print("Stop the app from the dashboard to exit\n")

        # Main loop - check stop_event to gracefully exit
        while not stop_event.is_set():
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
                    self._notify_with_reachy(reachy_mini, new_emails)

                    # Update previous count
                    self.previous_unread_count = current_unread_count

                elif current_unread_count < self.previous_unread_count:
                    # Emails were read
                    self.previous_unread_count = current_unread_count
                    print(f"📭 Emails read. Current unread: {current_unread_count}")

                # Wait for next check or until stop event
                stop_event.wait(Config.CHECK_INTERVAL)

            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                stop_event.wait(Config.CHECK_INTERVAL)

        print("\n👋 Email notifier stopped!")

    def _notify_with_reachy(self, reachy_mini: ReachyMini, email_count: int):
        """
        Perform notification gesture based on number of emails.

        Args:
            reachy_mini: Reachy Mini instance
            email_count: Number of new emails received
        """
        print(f"\n📧 You have {email_count} new email(s)!")

        try:
            if email_count == 1:
                self._wave_hello(reachy_mini)
            elif email_count <= 3:
                self._wave_hello(reachy_mini)
                time.sleep(0.5)
                self._head_nod(reachy_mini)
            else:
                self._happy_dance(reachy_mini)
        except Exception as e:
            print(f"Error during animation: {e}")

    def _wave_hello(self, reachy_mini: ReachyMini):
        """Make Reachy wave its arm to greet new email."""
        print("🤖 Reachy is waving!")

        try:
            # Turn on the right arm
            reachy_mini.r_arm.turn_on()

            # Move to a waving position
            reachy_mini.r_arm.shoulder.pitch.goal_position = -20
            reachy_mini.r_arm.elbow.pitch.goal_position = -80
            time.sleep(1)

            # Wave motion
            for _ in range(3):
                reachy_mini.r_arm.shoulder.roll.goal_position = -30
                time.sleep(0.3)
                reachy_mini.r_arm.shoulder.roll.goal_position = 0
                time.sleep(0.3)

            # Return to rest position
            reachy_mini.r_arm.shoulder.pitch.goal_position = 0
            reachy_mini.r_arm.elbow.pitch.goal_position = 0
            time.sleep(1)

            # Turn off the arm to save power
            reachy_mini.r_arm.turn_off()

        except Exception as e:
            print(f"Error during wave animation: {e}")

    def _head_nod(self, reachy_mini: ReachyMini):
        """Make Reachy nod its head acknowledging the email."""
        print("👋 Reachy is nodding!")

        try:
            # Turn on the head
            reachy_mini.head.turn_on()

            # Nod motion
            for _ in range(2):
                reachy_mini.head.neck.pitch.goal_position = 20
                time.sleep(0.4)
                reachy_mini.head.neck.pitch.goal_position = 0
                time.sleep(0.4)

            reachy_mini.head.turn_off()

        except Exception as e:
            print(f"Error during head nod: {e}")

    def _happy_dance(self, reachy_mini: ReachyMini):
        """Make Reachy do a happy dance for multiple emails."""
        print("🎉 Reachy is doing a happy dance!")

        try:
            # Turn on both arms
            reachy_mini.l_arm.turn_on()
            reachy_mini.r_arm.turn_on()

            # Simple happy dance - alternate arm movements
            for _ in range(2):
                # Raise left arm
                reachy_mini.l_arm.shoulder.pitch.goal_position = -40
                reachy_mini.r_arm.shoulder.pitch.goal_position = 0
                time.sleep(0.5)

                # Raise right arm
                reachy_mini.l_arm.shoulder.pitch.goal_position = 0
                reachy_mini.r_arm.shoulder.pitch.goal_position = -40
                time.sleep(0.5)

            # Return to rest
            reachy_mini.l_arm.shoulder.pitch.goal_position = 0
            reachy_mini.r_arm.shoulder.pitch.goal_position = 0
            time.sleep(1)

            # Turn off arms
            reachy_mini.l_arm.turn_off()
            reachy_mini.r_arm.turn_off()

        except Exception as e:
            print(f"Error during happy dance: {e}")
