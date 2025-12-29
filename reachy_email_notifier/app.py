"""Reachy Mini Email Notifier App - Main app class for Hugging Face integration."""

import sys
import threading
import time
import traceback

# CRITICAL: Output immediately at module load to verify module loads
print("[EMAIL_NOTIFIER] Module loading...", file=sys.stderr, flush=True)

# Helper function to ensure logs appear in journalctl
def log(msg):
    """Print to stderr for visibility in journalctl."""
    print(f"[EMAIL_NOTIFIER] {msg}", file=sys.stderr, flush=True)

try:
    from reachy_mini import ReachyMini, ReachyMiniApp
    from reachy_mini.utils import create_head_pose
    print("[EMAIL_NOTIFIER] reachy_mini imported successfully", file=sys.stderr, flush=True)
except ImportError as e:
    print(f"[EMAIL_NOTIFIER] WARNING: reachy_mini import failed: {e}", file=sys.stderr, flush=True)
    ReachyMiniApp = object

# Import config here, but delay gmail_checker import until runtime
try:
    from .config import Config
    print("[EMAIL_NOTIFIER] Config imported successfully", file=sys.stderr, flush=True)
except Exception as e:
    print(f"[EMAIL_NOTIFIER] ERROR importing config: {e}", file=sys.stderr, flush=True)
    print(f"[EMAIL_NOTIFIER] Traceback: {traceback.format_exc()}", file=sys.stderr, flush=True)
    Config = None

print("[EMAIL_NOTIFIER] Module loaded, defining class...", file=sys.stderr, flush=True)


print("[EMAIL_NOTIFIER] About to define ReachyMiniEmailNotifier class", file=sys.stderr, flush=True)

class ReachyMiniEmailNotifier(ReachyMiniApp):
    """
    Reachy Mini Email Notifier App.

    This app monitors your Gmail account and makes Reachy perform cute
    animations when new emails arrive.
    """

    # App name
    name: str = "reachy_email_notifier"

    # Optional: URL to custom configuration page
    custom_app_url: str | None = None

    def __new__(cls):
        print("[EMAIL_NOTIFIER] __new__() called - class is being instantiated!", file=sys.stderr, flush=True)
        instance = super().__new__(cls)
        print("[EMAIL_NOTIFIER] __new__() completed", file=sys.stderr, flush=True)
        return instance

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event):
        print("[EMAIL_NOTIFIER] run() method called!", file=sys.stderr, flush=True)
        """
        Main app logic - runs in background thread.

        Args:
            reachy_mini: Already initialized and connected Reachy Mini instance
            stop_event: Event to signal when app should stop
        """
        log("=" * 70)
        log("🚀 Starting Reachy Mini Email Notifier...")
        log("=" * 70)

        # Import GmailChecker here to avoid slow module-level imports
        try:
            from .gmail_checker import GmailChecker
            log("✓ Gmail checker module imported successfully")
        except Exception as e:
            log(f"❌ Failed to import Gmail checker: {e}")
            log(f"Traceback: {traceback.format_exc()}")
            return

        # Initialize instance variables
        gmail_checker = None

        # Initialize Gmail checker
        try:
            log("📧 Connecting to Gmail...")
            log(f"Credentials path: {Config.GMAIL_CREDENTIALS_PATH}")
            log(f"Token path: {Config.GMAIL_TOKEN_PATH}")

            gmail_checker = GmailChecker(
                credentials_path=Config.GMAIL_CREDENTIALS_PATH,
                token_path=Config.GMAIL_TOKEN_PATH
            )
            # First check initializes the tracker (returns 0)
            gmail_checker.check_for_new_emails()
            log(f"✅ Gmail connected. Now tracking inbox for new emails.")
        except Exception as e:
            log(f"❌ Failed to connect to Gmail: {e}")
            log(f"Traceback: {traceback.format_exc()}")
            log("Make sure credentials.json and token.pickle are in the correct location.")
            return

        log("=" * 70)
        log(f"✨ Email notifier is now running!")
        log(f"📊 Checking for emails every {Config.CHECK_INTERVAL} seconds")
        log("Stop the app from the dashboard to exit")
        log("=" * 70)

        # Main loop - check stop_event to gracefully exit
        while not stop_event.is_set():
            try:
                # Check for new emails (returns count of NEW emails since last check)
                new_email_count = gmail_checker.check_for_new_emails()

                # Trigger notification if we have new emails
                if new_email_count > 0:
                    log(f"🎉 {new_email_count} new email(s) detected!")

                    # Get the subject of the latest email
                    subject = gmail_checker.get_latest_email_subject()
                    if subject:
                        log(f"📬 Subject: {subject}")

                    # Trigger Reachy notification
                    self._notify_with_reachy(reachy_mini, new_email_count)

                # Wait for next check or until stop event
                stop_event.wait(Config.CHECK_INTERVAL)

            except Exception as e:
                log(f"❌ Error in main loop: {e}")
                log(f"Traceback: {traceback.format_exc()}")
                stop_event.wait(Config.CHECK_INTERVAL)

        log("👋 Email notifier stopped!")

    def _notify_with_reachy(self, reachy_mini: ReachyMini, email_count: int):
        """
        Perform notification gesture based on number of emails.

        Args:
            reachy_mini: Reachy Mini instance
            email_count: Number of new emails received
        """
        log(f"📧 You have {email_count} new email(s)!")

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
            log(f"Error during animation: {e}")
            log(f"Traceback: {traceback.format_exc()}")

    def _wave_hello(self, reachy_mini: ReachyMini):
        """Make Reachy wave its arm to greet new email."""
        log("🤖 Reachy is waving!")

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
            log(f"Error during wave animation: {e}")
            log(f"Traceback: {traceback.format_exc()}")

    def _head_nod(self, reachy_mini: ReachyMini):
        """Make Reachy nod its head acknowledging the email."""
        log("👋 Reachy is nodding!")

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
            log(f"Error during head nod: {e}")
            log(f"Traceback: {traceback.format_exc()}")

    def _happy_dance(self, reachy_mini: ReachyMini):
        """Make Reachy do a happy dance for multiple emails."""
        log("🎉 Reachy is doing a happy dance!")

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
            log(f"Error during happy dance: {e}")
            log(f"Traceback: {traceback.format_exc()}")

print("[EMAIL_NOTIFIER] Class defined successfully, module fully loaded!", file=sys.stderr, flush=True)


def main():
    """Entry point for the app when run as a script."""
    print("[EMAIL_NOTIFIER] main() function called!", file=sys.stderr, flush=True)
    app = ReachyMiniEmailNotifier()
    print("[EMAIL_NOTIFIER] App instance created, calling wrapped_run()", file=sys.stderr, flush=True)
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        print("[EMAIL_NOTIFIER] KeyboardInterrupt received, stopping...", file=sys.stderr, flush=True)
        app.stop()


if __name__ == "__main__":
    print("[EMAIL_NOTIFIER] __main__ block executing!", file=sys.stderr, flush=True)
    main()
