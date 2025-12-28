#!/bin/bash
# Helper script to publish Reachy Email Notifier to Hugging Face

set -e

echo "📧 Reachy Mini Email Notifier - Hugging Face Publisher"
echo "======================================================"
echo ""

# Check if huggingface_hub is installed
if ! python3 -c "import huggingface_hub" 2>/dev/null; then
    echo "❌ huggingface_hub not installed."
    echo "Install it with: pip install huggingface_hub"
    exit 1
fi

# Check if user is logged in
if ! huggingface-cli whoami &>/dev/null; then
    echo "❌ Not logged in to Hugging Face."
    echo "Login with: huggingface-cli login"
    exit 1
fi

USERNAME=$(huggingface-cli whoami | head -n 1)
echo "✅ Logged in as: $USERNAME"
echo ""

# Get Space name
read -p "Enter Space name [reachy_mini_email_notifier]: " SPACE_NAME
SPACE_NAME=${SPACE_NAME:-reachy_mini_email_notifier}

SPACE_URL="https://huggingface.co/spaces/$USERNAME/$SPACE_NAME"

echo ""
echo "Creating Space: $SPACE_URL"
echo ""

# Create temporary directory for Space
TEMP_DIR=$(mktemp -d)
echo "📁 Created temporary directory: $TEMP_DIR"

# Clone or create the Space
if huggingface-cli repo info "spaces/$USERNAME/$SPACE_NAME" &>/dev/null; then
    echo "📥 Space already exists, cloning..."
    git clone "https://huggingface.co/spaces/$USERNAME/$SPACE_NAME" "$TEMP_DIR"
else
    echo "🆕 Creating new Space..."
    huggingface-cli repo create --type=space --space_sdk=static "$SPACE_NAME"
    git clone "https://huggingface.co/spaces/$USERNAME/$SPACE_NAME" "$TEMP_DIR"
fi

# Copy files to Space
echo "📋 Copying files to Space..."
cp -r reachy_email_notifier "$TEMP_DIR/"
cp index.html "$TEMP_DIR/"
cp style.css "$TEMP_DIR/"
cp pyproject.toml "$TEMP_DIR/"
cp LICENSE "$TEMP_DIR/"
cp .gitignore "$TEMP_DIR/"

# Use HF-specific README
cp HF_README.md "$TEMP_DIR/README.md"

# Create requirements.txt for Reachy Mini
cat > "$TEMP_DIR/requirements.txt" << 'EOF'
reachy-mini>=0.1.0
google-auth>=2.0.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.0.0
python-dotenv>=1.0.0
EOF

# Commit and push to Hugging Face
echo "🚀 Publishing to Hugging Face..."
cd "$TEMP_DIR"
git add .
git commit -m "Update Reachy Mini Email Notifier app" || echo "No changes to commit"
git push

echo ""
echo "✅ Successfully published to Hugging Face!"
echo ""
echo "🔗 Your Space URL: $SPACE_URL"
echo ""
echo "Next steps:"
echo "1. Visit your Space and verify it looks correct"
echo "2. Test installation on your Reachy Mini"
echo "3. Request official listing with: reachy-mini-app-assistant publish --official"
echo "   (or create a PR at https://huggingface.co/datasets/pollen-robotics/reachy-mini-official-app-store)"
echo ""

# Clean up
cd -
rm -rf "$TEMP_DIR"
echo "🧹 Cleaned up temporary files"
