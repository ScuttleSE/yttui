# YT-TUI Setup Guide

This guide will walk you through setting up YT-TUI from scratch, including obtaining YouTube API credentials.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Detailed Setup](#detailed-setup)
3. [OAuth2 Configuration](#oauth2-configuration)
4. [First Run](#first-run)
5. [Troubleshooting](#troubleshooting)

## Quick Start

If you already have a `client_secret.json` file:

```bash
# Clone and enter directory
cd yt-tui

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Place your client_secret.json
mkdir -p ~/.config/yt-tui
cp /path/to/your/client_secret.json ~/.config/yt-tui/

# Run the app
python main.py
```

## Detailed Setup

### 1. System Requirements

- **Operating System**: Linux (tested on Ubuntu 20.04+, Debian, Fedora, Arch)
- **Python**: 3.8 or higher
- **Terminal**: Any modern terminal emulator (GNOME Terminal, Konsole, Alacritty, etc.)
- **Browser**: Default web browser configured (Firefox, Chrome, etc.)

Check your Python version:
```bash
python3 --version
```

### 2. Install Python Dependencies

First, create a virtual environment:

```bash
# Navigate to the project directory
cd yt-tui

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

You should see output confirming installation of:
- google-api-python-client
- google-auth
- google-auth-oauthlib
- textual
- rich

## OAuth2 Configuration

This is the most critical part. Follow carefully!

### Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console**
   - Open [https://console.cloud.google.com/](https://console.cloud.google.com/)
   - Sign in with your Google account

2. **Create New Project**
   - Click the project dropdown at the top (says "Select a project")
   - Click "NEW PROJECT"
   - Project name: `YT-TUI` (or any name you prefer)
   - Location: Leave as "No organization"
   - Click "CREATE"
   - Wait 10-30 seconds for creation

3. **Select Your Project**
   - Click the project dropdown again
   - Select your newly created project

### Step 2: Enable YouTube Data API v3

1. **Navigate to APIs & Services**
   - Click the hamburger menu (☰) in the top-left
   - Select "APIs & Services" → "Library"

2. **Find YouTube Data API v3**
   - In the search box, type: `YouTube Data API v3`
   - Click on "YouTube Data API v3" from results

3. **Enable the API**
   - Click the blue "ENABLE" button
   - Wait for it to enable (shows a progress bar)
   - You'll see "API enabled" when done

### Step 3: Configure OAuth Consent Screen

Before creating credentials, you need to configure the consent screen:

1. **Navigate to OAuth Consent Screen**
   - Go to "APIs & Services" → "OAuth consent screen"

2. **Choose User Type**
   - Select "External" (unless you have Google Workspace)
   - Click "CREATE"

3. **Fill in App Information**
   - **App name**: `YT-TUI`
   - **User support email**: Your email address
   - **App logo**: (Optional - can skip)
   - **App domain**: (Skip all fields)
   - **Authorized domains**: (Leave empty)
   - **Developer contact**: Your email address
   - Click "SAVE AND CONTINUE"

4. **Scopes**
   - Click "ADD OR REMOVE SCOPES"
   - Find and select:
     - `.../auth/youtube.readonly`
     - `.../auth/youtube.force-ssl`
   - Click "UPDATE"
   - Click "SAVE AND CONTINUE"

5. **Test Users**
   - Click "ADD USERS"
   - Enter your Gmail address
   - Click "ADD"
   - Click "SAVE AND CONTINUE"

6. **Summary**
   - Review the information
   - Click "BACK TO DASHBOARD"

### Step 4: Create OAuth Client ID

1. **Navigate to Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "CREATE CREDENTIALS" → "OAuth client ID"

2. **Configure OAuth Client**
   - **Application type**: Select "Desktop app"
   - **Name**: `YT-TUI Desktop Client`
   - Click "CREATE"

3. **Download Credentials**
   - A modal will appear showing your Client ID and Secret
   - Click "DOWNLOAD JSON"
   - Save the file (it will be named something like `client_secret_123456789.apps.googleusercontent.com.json`)

### Step 5: Install Credentials

```bash
# Create config directory
mkdir -p ~/.config/yt-tui

# Rename and move the file
# Replace the filename with your actual downloaded file
mv ~/Downloads/client_secret_*.json ~/.config/yt-tui/client_secret.json

# Verify it's there
ls -la ~/.config/yt-tui/client_secret.json

# Check permissions
chmod 600 ~/.config/yt-tui/client_secret.json
```

## First Run

### Running the Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the app
python main.py
```

### Authentication Flow

1. **Browser Opens Automatically**
   - A browser window/tab will open automatically
   - You'll see Google's OAuth consent screen

2. **Sign In**
   - Sign in with your Google account (the one you added as a test user)

3. **Grant Permissions**
   - You'll see a warning: "Google hasn't verified this app"
   - Click "Advanced"
   - Click "Go to YT-TUI (unsafe)"
   - Click "Continue"

4. **Authorize Access**
   - Review the permissions:
     - View your YouTube account
     - Manage your YouTube account
   - Click "Continue"

5. **Success**
   - You'll see "The authentication flow has completed"
   - Close the browser tab
   - Return to your terminal

6. **YT-TUI Launches**
   - The app should now start in your terminal
   - You're ready to browse YouTube!

### What Gets Saved

After successful authentication:
- `~/.config/yt-tui/token.json` - Your OAuth token (refreshable)
- `~/.config/yt-tui/config.json` - App configuration

## Troubleshooting

### "Client secret file not found"

**Cause**: The app can't find your credentials file.

**Solution**:
```bash
# Check if file exists
ls -la ~/.config/yt-tui/client_secret.json

# If not there, place it correctly
cp /path/to/downloaded/client_secret.json ~/.config/yt-tui/client_secret.json

# Or set environment variable
export YOUTUBE_CLIENT_SECRET=/path/to/client_secret.json
```

### "redirect_uri_mismatch" Error

**Cause**: OAuth redirect URI not configured correctly.

**Solution**:
1. This shouldn't happen with "Desktop app" type
2. If it does, go back to Google Cloud Console
3. Delete the OAuth client and create a new one
4. Make sure to select "Desktop app" not "Web application"

### "Access blocked: YT-TUI has not completed Google verification"

**Cause**: App is in testing mode and you're not a test user.

**Solution**:
1. Go to Google Cloud Console
2. Navigate to "APIs & Services" → "OAuth consent screen"
3. Scroll to "Test users"
4. Add your Gmail address as a test user

### "API quota exceeded"

**Cause**: You've used too many API requests.

**Details**:
- Free quota: 10,000 units/day
- Search costs: 100 units
- Other operations: 1-50 units

**Solution**:
- Wait until next day (quota resets at midnight Pacific Time)
- Reduce number of searches
- Request quota increase (for heavy use)

### Browser Doesn't Open Automatically

**Cause**: No default browser configured or `xdg-open` not working.

**Solution**:
```bash
# Check default browser
xdg-settings get default-web-browser

# Set default browser (example with Firefox)
xdg-settings set default-web-browser firefox.desktop

# Or manually open the URL shown in terminal
```

### Token Expired / Invalid

**Solution**:
```bash
# Delete old token
rm ~/.config/yt-tui/token.json

# Run app again - it will re-authenticate
python main.py
```

### "ImportError: No module named 'google'"

**Cause**: Dependencies not installed or wrong Python environment.

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep google
```

### Terminal Display Issues

**Cause**: Terminal doesn't support required features.

**Solution**:
- Use a modern terminal emulator (GNOME Terminal, Konsole, Alacritty)
- Make sure terminal is at least 80x24 characters
- Try running with TERM set: `TERM=xterm-256color python main.py`

## Advanced Configuration

### Using Environment Variables

Instead of placing `client_secret.json` in the config directory:

```bash
# Add to ~/.bashrc or ~/.zshrc
export YOUTUBE_CLIENT_SECRET="/path/to/your/client_secret.json"

# Reload shell
source ~/.bashrc
```

### Custom Config Directory

```bash
# You can modify config.py to change CONFIG_DIR
# Default: ~/.config/yt-tui
```

### Quota Management

To monitor your API usage:
1. Go to Google Cloud Console
2. Navigate to "APIs & Services" → "Dashboard"
3. Click "YouTube Data API v3"
4. View "Quota" tab

## Security Best Practices

1. **Never share your client_secret.json**
2. **Never commit credentials to git** (already in .gitignore)
3. **Keep token.json private**
4. **Use test users during development**
5. **Revoke access when done**: [https://myaccount.google.com/permissions](https://myaccount.google.com/permissions)

## Next Steps

Once set up successfully:
1. Press `/` to search for videos
2. Use arrow keys to navigate
3. Press Enter to open videos in browser
4. Press `r` to refresh current view
5. Press `q` to quit

Enjoy YT-TUI! 🚀
