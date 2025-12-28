"""Reachy robot controller for cute email notifications."""

import time
from typing import Optional

try:
    from reachy_sdk import ReachySDK
except ImportError:
    print("Warning: reachy_sdk not installed. Install it to use with real robot.")
    ReachySDK = None


class ReachyNotifier:
    """Controls Reachy robot to perform cute notification gestures."""

    def __init__(self, host: str = 'localhost', port: int = 50055):
        """
        Initialize Reachy controller.

        Args:
            host: IP address of Reachy robot
            port: Port number for SDK connection
        """
        self.host = host
        self.port = port
        self.reachy: Optional[ReachySDK] = None
        self._connect()

    def _connect(self):
        """Connect to Reachy robot."""
        if ReachySDK is None:
            print("Reachy SDK not available. Running in demo mode.")
            return

        try:
            self.reachy = ReachySDK(host=self.host, port=self.port)
            print(f"Connected to Reachy at {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to Reachy: {e}")
            print("Running in demo mode.")
            self.reachy = None

    def wave_hello(self):
        """Make Reachy wave its arm to greet new email."""
        if not self.reachy:
            print("🤖 [DEMO] Reachy would wave hello!")
            return

        try:
            # Turn on the right arm
            self.reachy.r_arm.turn_on()

            # Perform a cute waving motion
            # This is a simple example - customize based on your Reachy model
            print("🤖 Reachy is waving!")

            # Move to a waving position
            # Note: Adjust these positions based on your Reachy model
            self.reachy.r_arm.shoulder.pitch.goal_position = -20
            self.reachy.r_arm.elbow.pitch.goal_position = -80

            time.sleep(1)

            # Wave motion
            for _ in range(3):
                self.reachy.r_arm.shoulder.roll.goal_position = -30
                time.sleep(0.3)
                self.reachy.r_arm.shoulder.roll.goal_position = 0
                time.sleep(0.3)

            # Return to rest position
            self.reachy.r_arm.shoulder.pitch.goal_position = 0
            self.reachy.r_arm.elbow.pitch.goal_position = 0
            time.sleep(1)

            # Turn off the arm to save power
            self.reachy.r_arm.turn_off()

        except Exception as e:
            print(f"Error during wave animation: {e}")

    def happy_dance(self):
        """Make Reachy do a happy dance for multiple emails."""
        if not self.reachy:
            print("🎉 [DEMO] Reachy would do a happy dance!")
            return

        try:
            # Turn on both arms
            self.reachy.l_arm.turn_on()
            self.reachy.r_arm.turn_on()

            print("🎉 Reachy is doing a happy dance!")

            # Simple happy dance - alternate arm movements
            for _ in range(2):
                # Raise left arm
                self.reachy.l_arm.shoulder.pitch.goal_position = -40
                self.reachy.r_arm.shoulder.pitch.goal_position = 0
                time.sleep(0.5)

                # Raise right arm
                self.reachy.l_arm.shoulder.pitch.goal_position = 0
                self.reachy.r_arm.shoulder.pitch.goal_position = -40
                time.sleep(0.5)

            # Return to rest
            self.reachy.l_arm.shoulder.pitch.goal_position = 0
            self.reachy.r_arm.shoulder.pitch.goal_position = 0
            time.sleep(1)

            # Turn off arms
            self.reachy.l_arm.turn_off()
            self.reachy.r_arm.turn_off()

        except Exception as e:
            print(f"Error during happy dance: {e}")

    def head_nod(self):
        """Make Reachy nod its head acknowledging the email."""
        if not self.reachy:
            print("👋 [DEMO] Reachy would nod its head!")
            return

        try:
            # Turn on the head if available
            if hasattr(self.reachy, 'head'):
                self.reachy.head.turn_on()

                print("👋 Reachy is nodding!")

                # Nod motion
                for _ in range(2):
                    self.reachy.head.neck.pitch.goal_position = 20
                    time.sleep(0.4)
                    self.reachy.head.neck.pitch.goal_position = 0
                    time.sleep(0.4)

                self.reachy.head.turn_off()
            else:
                print("Head control not available on this Reachy model")

        except Exception as e:
            print(f"Error during head nod: {e}")

    def notify(self, email_count: int = 1):
        """
        Perform notification gesture based on number of emails.

        Args:
            email_count: Number of new emails received
        """
        print(f"\n📧 You have {email_count} new email(s)!")

        if email_count == 1:
            self.wave_hello()
        elif email_count <= 3:
            self.wave_hello()
            time.sleep(0.5)
            self.head_nod()
        else:
            self.happy_dance()

    def disconnect(self):
        """Disconnect from Reachy."""
        if self.reachy:
            print("Disconnecting from Reachy...")
            # Add cleanup if needed
