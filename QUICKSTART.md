# Quick Start Guide

Get your Reachy Email Notifier running in 5 minutes!

## Step 1: Install Dependencies (2 minutes)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Set Up Gmail API (2 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API (APIs & Services > Library > search "Gmail API" > Enable)
4. Create OAuth credentials (APIs & Services > Credentials > Create Credentials > OAuth client ID > Desktop app)
5. Download the JSON file and save it as `credentials.json` in this folder

## Step 3: Configure Your Settings (30 seconds)

```bash
# Copy example config
cp .env.example .env

# Edit .env with your Reachy's IP address
# For demo mode, leave it as localhost
nano .env  # or use your preferred editor
```

## Step 4: Run It! (30 seconds)

```bash
python run_notifier.py
```

On first run:
- Your browser will open
- Sign in to Gmail
- Grant read-only access
- Done! The app will start monitoring

## Testing Without a Robot

The app works in demo mode without a physical Reachy! It will print what the robot would do:
- "Reachy would wave hello!"
- "Reachy would do a happy dance!"

Perfect for testing before connecting your actual robot.

## Next Steps

- Customize animations in `reachy_email_notifier/reachy_controller.py`
- Adjust check interval in `.env`
- Share your setup with the community!

## Need Help?

Check the full [README.md](README.md) for detailed documentation.
