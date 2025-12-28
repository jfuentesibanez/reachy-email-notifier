# Reachy Email Notifier

A cute email notification app that makes your Reachy robot notify you whenever you receive new emails in your Gmail account!

## Features

- Real-time Gmail monitoring for new emails
- Cute robot animations based on the number of emails:
  - 1 email: Friendly wave
  - 2-3 emails: Wave + head nod
  - 4+ emails: Happy dance!
- Configurable check intervals
- Works with both physical Reachy robots and simulation
- Demo mode for testing without a robot

## Prerequisites

- Python 3.8 or higher
- A Reachy robot (physical or simulation) or run in demo mode
- Gmail account with API access enabled

## Installation

### 1. Clone or Download This Project

```bash
cd reachy-email-notifier
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Gmail API Setup

To allow the app to check your Gmail, you need to set up Google Cloud credentials:

### 1. Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### 2. Create OAuth Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in app name (e.g., "Reachy Email Notifier")
   - Add your email as a test user
4. For application type, choose "Desktop app"
5. Download the credentials JSON file
6. Save it as `credentials.json` in the project root directory

## Configuration

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` to configure your settings:

```bash
# For physical Reachy, use its IP address
REACHY_IP=192.168.1.100

# For simulation or demo mode
REACHY_IP=localhost

# Port (default is usually fine)
REACHY_PORT=50055

# How often to check for emails (in seconds)
CHECK_INTERVAL=60
```

## Usage

### Running the Notifier

```bash
python run_notifier.py
```

On first run, the app will:
1. Open your browser for Gmail authentication
2. Ask you to grant read-only access to your Gmail
3. Save the authentication token for future use

### Demo Mode

If you don't have a Reachy robot connected, the app will automatically run in demo mode, printing what the robot would do instead of actually moving it.

### Stopping the Notifier

Press `Ctrl+C` to gracefully stop the application.

## Project Structure

```
reachy-email-notifier/
├── reachy_email_notifier/
│   ├── __init__.py
│   ├── main.py              # Main application logic
│   ├── gmail_checker.py     # Gmail API integration
│   ├── reachy_controller.py # Reachy robot control
│   └── config.py            # Configuration management
├── run_notifier.py          # Entry point script
├── requirements.txt         # Python dependencies
├── .env.example             # Example configuration
├── .env                     # Your configuration (not in git)
├── .gitignore
└── README.md
```

## Customizing Animations

You can customize the robot's animations by editing `reachy_email_notifier/reachy_controller.py`:

- `wave_hello()`: Single email notification
- `head_nod()`: Acknowledgment gesture
- `happy_dance()`: Multiple emails celebration
- `notify()`: Main notification logic

Feel free to adjust joint positions and timing to match your Reachy model and preferences!

## Testing with Reachy Simulation

If you want to test with Reachy simulation:

1. Follow the [Reachy simulation setup guide](https://docs.pollen-robotics.com/developing-with-reachy-2/simulation/simulation-introduction/)
2. Start the simulation Docker container
3. Set `REACHY_IP=localhost` in your `.env` file
4. Run the notifier

## Troubleshooting

### "Reachy SDK not installed"

Make sure you activated your virtual environment and installed dependencies:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Gmail credentials file not found"

Make sure you:
1. Downloaded `credentials.json` from Google Cloud Console
2. Placed it in the project root directory

### "Failed to connect to Reachy"

- Check that your Reachy is powered on and connected to the network
- Verify the IP address in your `.env` file
- For simulation, ensure the Docker container is running
- The app will run in demo mode if connection fails

### Rate Limiting

Gmail API has rate limits. The default check interval is 60 seconds, which is safe. Don't set CHECK_INTERVAL below 10 seconds.

## Contributing

This project is open source and community contributions are welcome!

Ideas for enhancements:
- Support for other email providers
- More animation varieties
- Voice notifications using Reachy's speakers
- Integration with calendar events
- Mobile app for configuration
- Web dashboard for monitoring

## License

MIT License - feel free to use and modify for your own Reachy projects!

## Credits

Created for the Reachy community. Special thanks to Pollen Robotics for creating the amazing Reachy robot!

## Support

- Reachy Documentation: https://docs.pollen-robotics.com/
- Pollen Robotics Forum: https://forum.pollen-robotics.com/
- Report issues: Create an issue in this repository
