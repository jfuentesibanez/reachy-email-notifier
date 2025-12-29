"""Reachy Mini Email Notifier App - Main app class for Hugging Face integration."""

import sys
import threading
import time
import traceback
import tempfile
import os

def log(msg):
    """Print to stderr for visibility in journalctl."""
    print(f"[EMAIL_NOTIFIER] {msg}", file=sys.stderr, flush=True)

try:
    from reachy_mini import ReachyMini, ReachyMiniApp
    from reachy_mini.utils import create_head_pose
    import numpy as np
except ImportError as e:
    ReachyMiniApp = object
    np = None

from .config import Config

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

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event):
        """
        Main app logic - runs in background thread.

        Args:
            reachy_mini: Already initialized and connected Reachy Mini instance
            stop_event: Event to signal when app should stop
        """
        log("🚀 Starting Email Notifier...")

        # Import GmailChecker here to avoid slow module-level imports
        try:
            from .gmail_checker import GmailChecker
        except Exception as e:
            log(f"❌ Failed to import Gmail checker: {e}")
            return

        # Initialize instance variables
        gmail_checker = None

        # Initialize Gmail checker
        try:
            log("📧 Connecting to Gmail...")
            gmail_checker = GmailChecker(
                credentials_path=Config.GMAIL_CREDENTIALS_PATH,
                token_path=Config.GMAIL_TOKEN_PATH
            )
            # First check initializes the tracker (returns 0)
            gmail_checker.check_for_new_emails()
            log(f"✅ Connected! Checking for emails every {Config.CHECK_INTERVAL} seconds")
        except Exception as e:
            log(f"❌ Failed to connect to Gmail: {e}")
            log("Make sure credentials.json and token.pickle are configured correctly.")
            return

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
                log(f"❌ Error: {e}")
                stop_event.wait(Config.CHECK_INTERVAL)

        log("✋ Stopped")

    def _notify_with_reachy(self, reachy_mini: ReachyMini, email_count: int):
        """
        Perform notification gesture based on number of emails.

        Args:
            reachy_mini: Reachy Mini instance
            email_count: Number of new emails received
        """
        log(f"📧 You have {email_count} new email(s)!")

        try:
            # Speak the notification
            if email_count == 1:
                self._speak(reachy_mini, "You have a new email. Check your inbox!")
                self._wave_hello(reachy_mini)
            elif email_count <= 3:
                self._speak(reachy_mini, f"You have {email_count} new emails. Check your inbox!")
                self._wave_hello(reachy_mini)
                time.sleep(0.5)
                self._head_nod(reachy_mini)
            else:
                self._speak(reachy_mini, f"Wow! You have {email_count} new emails!")
                self._happy_dance(reachy_mini)
        except Exception as e:
            log(f"Animation error: {e}")

    def _speak(self, reachy_mini: ReachyMini, text: str):
        """
        Make Reachy speak the given text using TTS.

        Args:
            reachy_mini: Reachy Mini instance
            text: Text to speak
        """
        log(f"🔊 Speaking: {text}")

        try:
            import subprocess
            import soundfile as sf
            from scipy import signal

            # Create temp file for audio
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                temp_path = tmp_file.name

            try:
                # Generate TTS audio using espeak-ng directly
                # This is more reliable than pyttsx3
                result = subprocess.run(
                    ['espeak-ng', '-w', temp_path, '-s', '150', text],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode != 0:
                    log(f"⚠️  espeak-ng error: {result.stderr}")
                    return

                # Load the audio file
                data, samplerate_in = sf.read(temp_path, dtype='float32')

                # Get Reachy's audio sample rate
                samplerate_out = reachy_mini.media.get_output_audio_samplerate()

                # Resample if needed
                if samplerate_in != samplerate_out:
                    num_samples = int(len(data) * samplerate_out / samplerate_in)
                    data = signal.resample(data, num_samples)

                # Convert to mono if stereo
                if len(data.shape) > 1:
                    data = np.mean(data, axis=1)

                # Ensure data is 1D float32 numpy array
                data = np.asarray(data, dtype='float32')
                if len(data.shape) > 1:
                    data = data.flatten()

                # Play audio through Reachy's speaker
                reachy_mini.media.start_playing()
                chunk_size = 1024
                for i in range(0, len(data), chunk_size):
                    chunk = data[i : i + chunk_size]
                    reachy_mini.media.push_audio_sample(chunk)

                # Wait for audio to finish (approximate)
                duration = len(data) / samplerate_out
                time.sleep(duration + 0.5)  # Add buffer

                reachy_mini.media.stop_playing()

            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        except FileNotFoundError:
            log(f"⚠️  espeak-ng not installed (sudo apt install espeak-ng)")
        except ImportError as e:
            log(f"⚠️  Missing TTS dependencies: {e}")
        except Exception as e:
            log(f"Speech error: {e}")

    def _wave_hello(self, reachy_mini: ReachyMini):
        """Make Reachy wave its antennas to greet new email."""
        log("🤖 Reachy is waving antennas!")

        try:
            # Wave antennas side to side
            for _ in range(3):
                reachy_mini.goto_target(
                    antennas=np.deg2rad([60, 60]),  # Antennas out
                    duration=0.3,
                    method="minjerk"
                )
                time.sleep(0.3)
                reachy_mini.goto_target(
                    antennas=np.deg2rad([-30, -30]),  # Antennas in
                    duration=0.3,
                    method="minjerk"
                )
                time.sleep(0.3)

            # Return to neutral
            reachy_mini.goto_target(
                antennas=np.deg2rad([0, 0]),
                duration=0.5,
                method="minjerk"
            )

        except Exception as e:
            log(f"Wave animation error: {e}")

    def _head_nod(self, reachy_mini: ReachyMini):
        """Make Reachy nod its head acknowledging the email."""
        log("👋 Reachy is nodding!")

        try:
            # Nod motion - move head up and down
            for _ in range(2):
                reachy_mini.goto_target(
                    head=create_head_pose(z=-15, mm=True),  # Nod down
                    duration=0.4,
                    method="minjerk"
                )
                time.sleep(0.4)
                reachy_mini.goto_target(
                    head=create_head_pose(z=0, mm=True),  # Back to center
                    duration=0.4,
                    method="minjerk"
                )
                time.sleep(0.4)

        except Exception as e:
            log(f"Head nod error: {e}")

    def _happy_dance(self, reachy_mini: ReachyMini):
        """Make Reachy do a happy dance for multiple emails."""
        log("🎉 Reachy is doing a happy dance!")

        try:
            # Happy dance - spin body and wiggle antennas
            for _ in range(2):
                # Spin right with excited antennas
                reachy_mini.goto_target(
                    body_yaw=np.deg2rad(30),
                    antennas=np.deg2rad([90, 30]),
                    head=create_head_pose(z=5, mm=True),
                    duration=0.5,
                    method="cartoon"  # Fun bouncy movement
                )
                time.sleep(0.5)

                # Spin left with excited antennas
                reachy_mini.goto_target(
                    body_yaw=np.deg2rad(-30),
                    antennas=np.deg2rad([30, 90]),
                    head=create_head_pose(z=5, mm=True),
                    duration=0.5,
                    method="cartoon"
                )
                time.sleep(0.5)

            # Return to center with happy antennas up
            reachy_mini.goto_target(
                body_yaw=np.deg2rad(0),
                antennas=np.deg2rad([45, 45]),
                head=create_head_pose(z=0, mm=True),
                duration=0.8,
                method="minjerk"
            )
            time.sleep(0.5)

            # Antennas back to neutral
            reachy_mini.goto_target(
                antennas=np.deg2rad([0, 0]),
                duration=0.5
            )

        except Exception as e:
            log(f"Happy dance error: {e}")


def main():
    """Entry point for the app when run as a script."""
    app = ReachyMiniEmailNotifier()
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()


if __name__ == "__main__":
    main()
