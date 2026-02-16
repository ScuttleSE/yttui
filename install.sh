#!/bin/bash
# YT-TUI Installation Script

set -e

echo "=================================="
echo "YT-TUI Installation Script"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Check if version is at least 3.8
REQUIRED_VERSION="3.8"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION or higher is required. You have $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip -q

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Create config directory
echo ""
echo "Creating config directory..."
mkdir -p ~/.config/yt-tui
echo "✓ Config directory created at ~/.config/yt-tui"

# Make main.py executable
chmod +x main.py

# Check for client secret
echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Obtain YouTube API credentials:"
echo "   - Visit: https://console.cloud.google.com/"
echo "   - Create a project and enable YouTube Data API v3"
echo "   - Create OAuth 2.0 Desktop credentials"
echo "   - Download as client_secret.json"
echo ""
echo "2. Place credentials file:"
echo "   mv ~/Downloads/client_secret*.json ~/.config/yt-tui/client_secret.json"
echo ""
echo "3. Run YT-TUI:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "For detailed setup instructions, see SETUP_GUIDE.md"
echo ""

# Check if client_secret.json already exists
if [ -f ~/.config/yt-tui/client_secret.json ]; then
    echo "✓ Found existing client_secret.json"
    echo ""
    echo "You can now run the app:"
    echo "  source venv/bin/activate"
    echo "  python main.py"
    echo ""
else
    echo "⚠️  client_secret.json not found"
    echo "Please follow the setup guide to obtain API credentials"
    echo ""
    echo "After obtaining credentials, run:"
    echo "  source venv/bin/activate"
    echo "  python main.py"
    echo ""
fi
