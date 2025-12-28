"""Reachy Mini Email Notifier App - Main app class for Hugging Face integration."""

import logging
import sys
import threading
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Use stderr to ensure it appears in logs
)
logger = logging.getLogger(__name__)

try:
    from reachy_mini import ReachyMini, ReachyMiniApp
    from reachy_mini.utils import create_head_pose
except ImportError:
    logger.warning("reachy_mini not installed. For Hugging Face app, install reachy-mini package.")
    ReachyMiniApp = object

# Import config here, but delay gmail_checker import until runtime
from .config import Config


class ReachyMiniEmailNotifier(ReachyMiniApp):
    """
    Reachy Mini Email Notifier App.

    This app monitors your Gmail account and makes Reachy perform cute
    animations when new emails arrive.
    """

    # Optional: URL to custom configuration page
    custom_app_url: str | None = None

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event):
        """
        Main app logic - runs in background thread.

        Args:
            reachy_mini: Already initialized and connected Reachy Mini instance
            stop_event: Event to signal when app should stop
        """
        logger.info("=" * 70)
        logger.info("🚀 Starting Reachy Mini Email Notifier...")
        logger.info("=" * 70)

        # Import GmailChecker here to avoid slow module-level imports
        try:
            from .gmail_checker import GmailChecker
            logger.info("✓ Gmail checker module imported successfully")
        except Exception as e:
            logger.error(f"❌ Failed to import Gmail checker: {e}", exc_info=True)
            return

        # Initialize instance variables
        gmail_checker = None
        previous_unread_count = 0

        # Initialize Gmail checker
        try:
            logger.info("📧 Connecting to Gmail...")
            logger.info(f"Credentials path: {Config.GMAIL_CREDENTIALS_PATH}")
            logger.info(f"Token path: {Config.GMAIL_TOKEN_PATH}")

            gmail_checker = GmailChecker(
                credentials_path=Config.GMAIL_CREDENTIALS_PATH,
                token_path=Config.GMAIL_TOKEN_PATH
            )
            previous_unread_count = gmail_checker.check_for_new_emails()
            logger.info(f"✅ Gmail connected. Current unread emails: {previous_unread_count}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Gmail: {e}", exc_info=True)
            logger.error("Make sure credentials.json and token.pickle are in the correct location.")
            return

        logger.info("=" * 70)
        logger.info(f"✨ Email notifier is now running!")
        logger.info(f"📊 Checking for emails every {Config.CHECK_INTERVAL} seconds")
        logger.info("Stop the app from the dashboard to exit")
        logger.info("=" * 70)

        # Main loop - check stop_event to gracefully exit
        while not stop_event.is_set():
            try:
                # Check for new emails
                current_unread_count = gmail_checker.check_for_new_emails()

                # Detect new emails
                if current_unread_count > previous_unread_count:
                    new_emails = current_unread_count - previous_unread_count
                    logger.info(f"🎉 New email(s) detected! Count: {new_emails}")

                    # Get the subject of the latest email
                    subject = gmail_checker.get_latest_email_subject()
                    if subject:
                        logger.info(f"📬 Subject: {subject}")

                    # Trigger Reachy notification
                    self._notify_with_reachy(reachy_mini, new_emails)

                    # Update previous count
                    previous_unread_count = current_unread_count

                elif current_unread_count < previous_unread_count:
                    # Emails were read
                    previous_unread_count = current_unread_count
                    logger.info(f"📭 Emails read. Current unread: {current_unread_count}")

                # Wait for next check or until stop event
                stop_event.wait(Config.CHECK_INTERVAL)

            except Exception as e:
                logger.error(f"❌ Error in main loop: {e}", exc_info=True)
                stop_event.wait(Config.CHECK_INTERVAL)

        logger.info("👋 Email notifier stopped!")

    def _notify_with_reachy(self, reachy_mini: ReachyMini, email_count: int):
        """
        Perform notification gesture based on number of emails.

        Args:
            reachy_mini: Reachy Mini instance
            email_count: Number of new emails received
        """
        logger.info(f"📧 You have {email_count} new email(s)!")

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
            logger.error(f"Error during animation: {e}", exc_info=True)

    def _wave_hello(self, reachy_mini: ReachyMini):
        """Make Reachy wave its arm to greet new email."""
        logger.info("🤖 Reachy is waving!")

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
            logger.error(f"Error during wave animation: {e}", exc_info=True)

    def _head_nod(self, reachy_mini: ReachyMini):
        """Make Reachy nod its head acknowledging the email."""
        logger.info("👋 Reachy is nodding!")

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
            logger.error(f"Error during head nod: {e}", exc_info=True)

    def _happy_dance(self, reachy_mini: ReachyMini):
        """Make Reachy do a happy dance for multiple emails."""
        logger.info("🎉 Reachy is doing a happy dance!")

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
            logger.error(f"Error during happy dance: {e}", exc_info=True)
