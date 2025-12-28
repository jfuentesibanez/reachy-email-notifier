# Publishing to Hugging Face as a Reachy Mini Community App

This guide shows you how to publish your email notifier to Hugging Face so it appears in the Reachy Mini app store.

## Prerequisites

- Hugging Face account (create one at https://huggingface.co/)
- Hugging Face CLI installed: `pip install huggingface_hub`
- Login to Hugging Face: `huggingface-cli login`

## Option 1: Manual Publishing (Recommended)

### Step 1: Create a Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Fill in the details:
   - **Owner**: Your username
   - **Space name**: `reachy_mini_email_notifier` (must use underscores)
   - **License**: MIT
   - **SDK**: Static
   - **Visibility**: Public

3. Click "Create Space"

### Step 2: Clone Your New Space Locally

```bash
cd /tmp
git clone https://huggingface.co/spaces/YOUR_USERNAME/reachy_mini_email_notifier
cd reachy_mini_email_notifier
```

### Step 3: Copy Files from This Repository

Copy the required files to your Space:

```bash
# Copy Python package
cp -r /Users/javier/Documents/Desarrollo/reachy-email-notifier/reachy_email_notifier .

# Copy Space files
cp /Users/javier/Documents/Desarrollo/reachy-email-notifier/index.html .
cp /Users/javier/Documents/Desarrollo/reachy-email-notifier/style.css .
cp /Users/javier/Documents/Desarrollo/reachy-email-notifier/pyproject.toml .

# Use the HF-specific README
cp /Users/javier/Documents/Desarrollo/reachy-email-notifier/HF_README.md README.md

# Copy license and other files
cp /Users/javier/Documents/Desarrollo/reachy-email-notifier/LICENSE .
cp /Users/javier/Documents/Desarrollo/reachy-email-notifier/.gitignore .
```

### Step 4: Create requirements.txt for the Space

Create a `requirements.txt` file specific to Reachy Mini:

```bash
cat > requirements.txt << 'EOF'
reachy-mini>=0.1.0
google-auth>=2.0.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.0.0
python-dotenv>=1.0.0
EOF
```

### Step 5: Commit and Push to Hugging Face

```bash
git add .
git commit -m "Initial commit: Reachy Mini Email Notifier app"
git push
```

### Step 6: Verify Your Space

1. Go to https://huggingface.co/spaces/YOUR_USERNAME/reachy_mini_email_notifier
2. Check that the Space page displays correctly
3. Verify the `index.html` page shows your app description

## Option 2: Using reachy-mini-app-assistant (If Available)

If you have a Reachy Mini with `reachy-mini` installed:

```bash
# Install the SDK and tools
pip install reachy-mini

# Navigate to your app directory
cd /Users/javier/Documents/Desarrollo/reachy-email-notifier

# Publish to Hugging Face
reachy-mini-app-assistant publish

# Follow the interactive prompts:
# - Local path: . (current directory)
# - Privacy: public
```

## Option 3: Push from Your Existing Repository

If you want to keep using your GitHub repo and mirror to Hugging Face:

```bash
cd /Users/javier/Documents/Desarrollo/reachy-email-notifier

# Add Hugging Face as a remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/reachy_mini_email_notifier

# Create a branch with the Space files
git checkout -b huggingface

# Copy the HF-specific README
cp HF_README.md README.md
git add README.md
git commit -m "Use Hugging Face README for Space"

# Push to Hugging Face
git push hf huggingface:main
```

## Step 7: Request Official App Store Listing

Once your app is working and tested:

1. Make sure your Space is **public**
2. Test it thoroughly on your Reachy Mini
3. Use the command (if using reachy-mini-app-assistant):
   ```bash
   reachy-mini-app-assistant publish --official
   ```

   OR manually:
   - Go to https://huggingface.co/datasets/pollen-robotics/reachy-mini-official-app-store
   - Click "Edit" to create a pull request
   - Add your app to the list with a brief description

4. Wait for review by the Pollen Robotics team

## Testing Your Space

Before requesting official listing, test your app:

1. Install from your Space on your Reachy Mini:
   - Open the Reachy Mini dashboard
   - Go to "Advanced: Install private space"
   - Enter: `YOUR_USERNAME/reachy_mini_email_notifier`

2. Verify it installs and runs correctly

3. Check for any errors in the app logs

## Metadata for Your Space

Your `README.md` (HF_README.md) already includes the required metadata:

```yaml
---
title: Reachy Mini Email Notifier
emoji: 📧
sdk: static
license: mit
tags:
  - reachy
  - reachy-mini
  - robotics
  - email
---
```

## Support

If you encounter issues:
- Check the [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/spaces)
- Visit the [Pollen Robotics forum](https://forum.pollen-robotics.com/)
- See the [official guide](https://huggingface.co/blog/pollen-robotics/make-and-publish-your-reachy-mini-apps)

## Next Steps

After publishing:
1. Share your Space on social media
2. Post on the Pollen Robotics forum
3. Update the GitHub README with the Space link
4. Create a demo video showing the app in action

Good luck with your community app! 🎉
