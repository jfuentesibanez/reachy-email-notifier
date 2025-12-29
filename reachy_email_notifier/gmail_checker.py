"""Gmail API integration for checking new emails."""

import os
import pickle
from datetime import datetime, timedelta
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailChecker:
    """Monitors Gmail account for new emails."""

    def __init__(self, credentials_path: str = 'credentials.json', token_path: str = 'token.pickle'):
        """
        Initialize Gmail checker.

        Args:
            credentials_path: Path to Gmail API credentials file
            token_path: Path to store/load authentication token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.last_check_time = None
        self.last_message_id = None  # Track the most recent message ID we've seen
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API."""
        creds = None

        # Load existing token if available
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Gmail API credentials file not found at {self.credentials_path}. "
                        "Please download it from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for future use
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        self.last_check_time = datetime.now()

    def check_for_new_emails(self) -> int:
        """
        Check for new emails since last check.

        Returns:
            Number of new emails since last check
        """
        if not self.service:
            self._authenticate()

        try:
            import sys
            # Query for unread emails in inbox only, sorted by most recent first
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread in:inbox',
                maxResults=20  # Get last 20 unread emails
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                self.last_check_time = datetime.now()
                return 0

            # Get the ID of the most recent message
            latest_message_id = messages[0]['id']

            # First run - just store the latest ID and return 0
            if self.last_message_id is None:
                self.last_message_id = latest_message_id
                self.last_check_time = datetime.now()
                return 0

            # Check if there are new messages
            if latest_message_id == self.last_message_id:
                self.last_check_time = datetime.now()
                return 0

            # Count new messages until we hit the last one we saw
            new_email_count = 0
            for msg in messages:
                if msg['id'] == self.last_message_id:
                    break
                new_email_count += 1

            # Update to track the new latest message
            self.last_message_id = latest_message_id
            self.last_check_time = datetime.now()
            return new_email_count

        except Exception as e:
            import sys
            print(f"[GMAIL_API] Error: {e}", file=sys.stderr, flush=True)
            return 0

    def get_latest_email_subject(self) -> Optional[str]:
        """
        Get the subject of the most recent unread email.

        Returns:
            Email subject or None if no unread emails
        """
        if not self.service:
            self._authenticate()

        try:
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=1
            ).execute()

            messages = results.get('messages', [])
            if not messages:
                return None

            message = self.service.users().messages().get(
                userId='me',
                id=messages[0]['id'],
                format='metadata',
                metadataHeaders=['Subject']
            ).execute()

            headers = message.get('payload', {}).get('headers', [])
            for header in headers:
                if header['name'] == 'Subject':
                    return header['value']

            return None

        except Exception as e:
            print(f"Error getting email subject: {e}")
            return None
