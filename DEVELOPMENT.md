# Development Journal - Reachy Mini Email Notifier

## Project Overview
A Reachy Mini app that monitors Gmail and announces new emails with voice + cute animations.

**Current Version:** 2.0.0
**Status:** Production Ready ✅
**Author:** Javier Fuentes (jfuentesibanez)

## Development Timeline

### Initial Concept
- **Goal**: Create a Reachy Mini app that notifies about new Gmail emails
- **Features Planned**:
  - Gmail monitoring
  - Cute robot animations
  - Different gestures based on email count

### Phase 1: Basic Implementation (v1.0.x)
**Key Decisions:**
- Used Reachy Mini App framework with `ReachyMiniApp` base class
- Gmail API with OAuth2 for read-only access
- Persistent storage in `/home/pollen/.reachy_email_notifier/`

**Technical Challenges & Solutions:**

1. **Entry Point Discovery Issue**
   - **Problem**: App appeared in dashboard but wouldn't run
   - **Root Cause**: Used wrong entry point group `reachy_mini.app` instead of `reachy_mini_apps`
   - **Solution**: Fixed `pyproject.toml` entry point group name
   - **Files**: `pyproject.toml:52`, `setup.py:14`

2. **Import Timeout (KeyboardInterrupt)**
   - **Problem**: Module import timing out during regex compilation in python-dotenv
   - **Root Cause**: `load_dotenv()` in config.py taking too long
   - **Solution**: Removed python-dotenv dependency entirely
   - **Files**: `reachy_email_notifier/config.py`

3. **Module Loads But Never Executes**
   - **Problem**: Logs showed class definition but `run()` never called
   - **Root Cause**: Missing `main()` function and `[project.scripts]` entry point
   - **Discovery**: Examined official `reachy_mini_greetings` app structure
   - **Solution**: Added `main()` function that calls `wrapped_run()`
   - **Files**: `reachy_email_notifier/app.py:304-314`, `pyproject.toml:56`

### Phase 2: Email Detection Improvements (v1.1.x)

**Challenge: Email Detection Not Working with Many Unread Emails**

4. **Gmail API Pagination Limit**
   - **Problem**: User had 200+ unread emails, API only returns 100 max
   - **Root Cause**: Counting returned messages instead of using `resultSizeEstimate`
   - **Initial Fix (v1.0.7)**: Used `resultSizeEstimate` for total count
   - **Still Broken**: Count-based detection unreliable with many unread emails
   - **Files**: `reachy_email_notifier/gmail_checker.py:63-99`

5. **Message ID Tracking (v1.1.0)**
   - **Problem**: Counting all unread emails across all folders was unreliable
   - **Better Approach**: Track the latest message ID instead of counts
   - **Solution**:
     - Query only inbox (`is:unread in:inbox`)
     - Track `last_message_id` of most recent email
     - Detect new emails by comparing message IDs
   - **Benefits**: Works with any number of unread emails
   - **Files**: `reachy_email_notifier/gmail_checker.py:64-130`

### Phase 3: Correct Robot API (v1.1.1)

**Challenge: Wrong Hardware API**

6. **Reachy Mini Has No Arms!**
   - **Problem**: Code tried to control `r_arm` and `l_arm` attributes
   - **Error**: `'ReachyMini' object has no attribute 'r_arm'`
   - **Discovery**: Reachy Mini only has head, antennas, and body_yaw
   - **Solution**: Completely rewrote animations using correct API:
     - `goto_target()` method with parameters:
       - `head=create_head_pose(z=10, mm=True)`
       - `antennas=np.deg2rad([45, 45])`
       - `body_yaw=np.deg2rad(30)`
       - `duration=2.0`
       - `method="minjerk"` or `"cartoon"`
   - **Files**: `reachy_email_notifier/app.py:204-301`

**New Animations:**
- **1 email**: Antenna wiggle (3 cycles)
- **2-3 emails**: Antenna wiggle + head nod
- **4+ emails**: Happy dance (body spin + excited antennas)

### Phase 4: Text-to-Speech (v1.2.x)

**Feature Addition: Voice Announcements**

7. **TTS Implementation Challenges**
   - **First Attempt (v1.2.0)**: Used `pyttsx3` library
   - **Problem**: `pyttsx3` generated malformed WAV files
   - **Error**: `soundfile.LibsndfileError: Format not recognised`
   - **Root Cause**: pyttsx3 on Linux creates incompatible audio files
   - **Files**: Initial implementation in `app.py:167-246`

8. **Direct espeak-ng Implementation (v1.2.1)**
   - **Solution**: Call `espeak-ng` directly via subprocess
   - **Process**:
     1. Generate audio: `espeak-ng -w temp.wav -s 150 "text"`
     2. Load with soundfile: `sf.read(temp.wav, dtype='float32')`
     3. Resample to match Reachy's audio rate
     4. Convert to mono if needed
     5. Push to speaker: `reachy_mini.media.push_audio_sample(chunk)`
   - **System Requirement**: `sudo apt install espeak-ng`
   - **Files**: `reachy_email_notifier/app.py:167-202`

**Voice Messages:**
- 1 email: "You have a new email. Check your inbox!"
- 2-3 emails: "You have X new emails. Check your inbox!"
- 4+ emails: "Wow! You have X new emails!"

### Phase 5: Production Release (v2.0.0)

**Cleanup for Official App Store**

9. **Debug Logging Cleanup**
   - **Removed**: All development debug statements
   - **Kept**: Essential user-facing messages only
   - **Files**:
     - `reachy_email_notifier/__init__.py` (simplified to 3 lines)
     - `reachy_email_notifier/config.py` (removed all print statements)
     - `reachy_email_notifier/app.py` (cleaned up excessive logging)
     - `reachy_email_notifier/gmail_checker.py` (minimal error logging)

10. **Documentation Updates**
    - Updated README with TTS features
    - Added espeak-ng requirement
    - Improved setup instructions
    - Clear feature descriptions

## Architecture

### Application Structure
```
reachy_email_notifier/
├── __init__.py          # Package initialization, version
├── app.py               # Main ReachyMiniApp class
├── config.py            # Configuration management
└── gmail_checker.py     # Gmail API integration
```

### Key Components

**1. ReachyMiniEmailNotifier (app.py)**
- Inherits from `ReachyMiniApp`
- Implements `run(reachy_mini, stop_event)` method
- Main loop checks Gmail every 60 seconds
- Coordinates speech + animations

**2. GmailChecker (gmail_checker.py)**
- Handles Gmail OAuth2 authentication
- Tracks latest message ID (not counts!)
- Returns number of NEW emails detected
- Query: `is:unread in:inbox` (maxResults=20)

**3. Config (config.py)**
- Persistent directory: `/home/pollen/.reachy_email_notifier/`
- Credentials path: `credentials.json`
- Token path: `token.pickle`
- Check interval: 60 seconds (configurable)

### Entry Points
```toml
[project.entry-points."reachy_mini_apps"]
reachy_email_notifier = "reachy_email_notifier.app:ReachyMiniEmailNotifier"

[project.scripts]
reachy-email-notifier = "reachy_email_notifier.app:main"
```

## Critical Code Patterns

### 1. Main Entry Point (Required!)
```python
def main():
    """Entry point for the app when run as a script."""
    app = ReachyMiniEmailNotifier()
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()

if __name__ == "__main__":
    main()
```

### 2. Graceful Shutdown
```python
def run(self, reachy_mini: ReachyMini, stop_event: threading.Event):
    while not stop_event.is_set():
        # Do work
        stop_event.wait(CHECK_INTERVAL)  # Interruptible sleep
```

### 3. Lazy Imports
```python
def run(self, reachy_mini, stop_event):
    # Import heavy packages inside run(), not at module level
    from .gmail_checker import GmailChecker
```

### 4. Message ID Tracking
```python
# Store latest message ID seen
self.last_message_id = None

# On each check:
latest_id = messages[0]['id']
if self.last_message_id is None:
    self.last_message_id = latest_id
    return 0  # First run, no notification

if latest_id == self.last_message_id:
    return 0  # No new emails

# Count new emails by comparing IDs
new_count = 0
for msg in messages:
    if msg['id'] == self.last_message_id:
        break
    new_count += 1

self.last_message_id = latest_id
return new_count
```

## Dependencies

### Python Packages
```
google-auth>=2.0.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.0.0
soundfile>=0.12.1
scipy>=1.10.0
```

### System Dependencies
```bash
sudo apt install espeak-ng
```

## Configuration & Setup

### Gmail API Setup
1. Google Cloud Console → Create project
2. Enable Gmail API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download `credentials.json`

### Reachy Installation
```bash
# Copy credentials
scp credentials.json pollen@reachy-mini.local:/home/pollen/.reachy_email_notifier/

# Install espeak-ng
ssh pollen@reachy-mini.local
sudo apt update && sudo apt install -y espeak-ng

# Install app
source /venvs/apps_venv/bin/activate
pip install --no-cache-dir "git+https://github.com/jfuentesibanez/reachy-email-notifier.git@main"
deactivate

# Restart daemon
sudo systemctl restart reachy-mini-daemon
```

### First-Time Authentication
On first run, check logs for authentication URL:
```bash
journalctl -u reachy-mini-daemon -f
```
Open the URL in browser, grant access, copy code back to terminal.

## Testing & Debugging

### View Logs
```bash
# Real-time logs
journalctl -u reachy-mini-daemon -f

# Recent logs
journalctl -u reachy-mini-daemon -n 100 --no-pager

# Daemon status
sudo systemctl status reachy-mini-daemon
```

### Check App Status
```bash
# Via API
curl -s http://localhost:8000/api/apps/current-app-status

# Check installed version
source /venvs/apps_venv/bin/activate
pip show reachy-email-notifier
deactivate
```

### Force Update
```bash
source /venvs/apps_venv/bin/activate
pip uninstall -y reachy-email-notifier
pip cache purge
pip install --no-cache-dir "git+https://github.com/jfuentesibanez/reachy-email-notifier.git@main"
deactivate
sudo systemctl restart reachy-mini-daemon
```

## Known Issues & Solutions

### Issue: App Won't Start
**Symptoms**: App shows in dashboard but logs show nothing
**Check**:
1. Is app installed in `/venvs/apps_venv`?
2. Entry point group correct? (`reachy_mini_apps` not `reachy_mini.app`)
3. Does `main()` function exist?

### Issue: Email Detection Not Working
**Symptoms**: Reachy doesn't react to new emails
**Check**:
1. Are credentials in `/home/pollen/.reachy_email_notifier/`?
2. Is `token.pickle` present and valid?
3. Check logs for Gmail API errors
4. Verify emails going to inbox (not promotions/social)

### Issue: No Sound
**Symptoms**: Animations work but no voice
**Check**:
1. Is espeak-ng installed? `which espeak-ng`
2. Check logs for TTS errors
3. Verify Reachy's speaker is working

### Issue: Import Timeout
**Symptoms**: KeyboardInterrupt during module load
**Solution**: Remove slow imports from module level, use lazy imports in `run()`

## Future Improvements

### Potential Features
- [ ] Configurable voice (different languages/accents)
- [ ] Email priority detection (important vs regular)
- [ ] Customizable animations per email sender
- [ ] Web UI for configuration
- [ ] Support for multiple email accounts
- [ ] Read email subjects aloud
- [ ] Mark emails as read from Reachy
- [ ] Integration with calendar events

### Code Quality
- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Type hints throughout
- [ ] Async email checking for better performance
- [ ] Rate limiting protection

## Resources

**Official Documentation:**
- [Reachy Mini SDK](https://github.com/pollen-robotics/reachy_mini)
- [Publishing Apps Guide](https://huggingface.co/blog/pollen-robotics/make-and-publish-your-reachy-mini-apps)
- [Gmail API Docs](https://developers.google.com/gmail/api)

**Project Links:**
- GitHub: https://github.com/jfuentesibanez/reachy-email-notifier
- Hugging Face: https://huggingface.co/spaces/jfiba/reachy_mini_email_notifier

**Community:**
- Pollen Robotics Discord: https://discord.com/invite/Kg3mZHTKgs
- Official App Store: https://huggingface.co/datasets/pollen-robotics/reachy-mini-official-app-store

## Version History

- **v2.0.0** (Dec 2025) - Production release, cleaned logging, updated docs
- **v1.2.1** (Dec 2025) - Fixed TTS with direct espeak-ng
- **v1.2.0** (Dec 2025) - Added text-to-speech feature
- **v1.1.1** (Dec 2025) - Fixed animations for correct Reachy Mini API
- **v1.1.0** (Dec 2025) - Message ID tracking instead of counts
- **v1.0.7** (Dec 2025) - Used resultSizeEstimate for email count
- **v1.0.4** (Dec 2025) - Added main() function
- **v1.0.3** (Dec 2025) - Removed python-dotenv
- **v1.0.2** (Dec 2025) - Fixed entry point group
- **v1.0.0** (Dec 2025) - Initial release

---

**Last Updated:** December 29, 2025
**Maintained by:** Javier Fuentes (jfuentesibanez)
