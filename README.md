---
title: Reachy Mini Email Notifier
emoji: 📧
colorFrom: purple
colorTo: blue
sdk: static
pinned: false
license: mit
tags:
  - reachy
  - reachy-mini
  - robotics
  - email
  - gmail
  - notification
  - automation
---

# 📧 Reachy Mini Email Notifier

A cute email notification app for Reachy Mini robots! Get notified with adorable animations when you receive new Gmail messages.

## Features

- **Real-time Gmail Monitoring**: Securely monitors your Gmail account for new emails
- **Voice Announcements**: Reachy speaks to announce new emails! 🔊
- **Cute Robot Animations**:
  - 👋 One email: Reachy says "You have a new email. Check your inbox!" then wiggles antennas
  - 👍 2-3 emails: Announces count, waves antennas + nods head
  - 🎉 4+ emails: Says "Wow! You have X new emails!" with a happy dance
- **Privacy-First**: All processing happens locally on your Reachy Mini
- **Easy Configuration**: Simple setup with Gmail API credentials
- **Open Source**: MIT licensed, community contributions welcome

## Quick Start

### 1. Install the App

Install directly from your Reachy Mini dashboard's Hugging Face app store with one click!

### 2. Set Up Gmail API

You'll need to create Gmail API credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download the `credentials.json` file

For detailed instructions, see the [Gmail API Setup Guide](https://github.com/jfuentesibanez/reachy-email-notifier#gmail-api-setup).

### 3. Install espeak-ng (for voice)

SSH into your Reachy Mini and run:
```bash
sudo apt update
sudo apt install -y espeak-ng
```

### 4. Configure the App

Copy your Gmail credentials to Reachy:
```bash
scp credentials.json pollen@reachy-mini.local:/home/pollen/.reachy_email_notifier/
```

### 5. Authenticate

On first run, you'll need to authenticate. Follow the URL in the logs to grant access.

### 6. Run!

Start the app from your Reachy Mini dashboard and enjoy!

## How It Works

The app:
1. Monitors your Gmail inbox every 60 seconds (configurable)
2. Detects new unread emails by tracking message IDs
3. Reachy speaks to announce the new emails
4. Performs cute animations (antenna wiggles, head nods, happy dances)
5. Logs email subjects for your reference

## Configuration

You can customize the behavior by setting environment variables:

- `CHECK_INTERVAL`: How often to check for emails (default: 60 seconds)
- `REACHY_IP`: IP address of your Reachy (default: localhost)

## Privacy & Security

- Uses OAuth2 for secure authentication
- Requires only read-only Gmail access
- No data is sent to external servers
- All processing happens on your local Reachy Mini

## Links

- [GitHub Repository](https://github.com/jfuentesibanez/reachy-email-notifier)
- [Full Documentation](https://github.com/jfuentesibanez/reachy-email-notifier/blob/master/README.md)
- [Contributing Guide](https://github.com/jfuentesibanez/reachy-email-notifier/blob/master/CONTRIBUTING.md)

## Requirements

- Reachy Mini robot
- Gmail account
- Gmail API credentials (free from Google Cloud Console)
- espeak-ng (for text-to-speech, install via `sudo apt install espeak-ng`)

## License

MIT License - See [LICENSE](https://github.com/jfuentesibanez/reachy-email-notifier/blob/master/LICENSE) for details.

## Support

- [Report Issues](https://github.com/jfuentesibanez/reachy-email-notifier/issues)
- [Pollen Robotics Forum](https://forum.pollen-robotics.com/)
- [Reachy Documentation](https://docs.pollen-robotics.com/)

---

Created with ❤️ for the Reachy community
