# YT-TUI Quick Start Guide

Get up and running with YT-TUI in 10 minutes!

## Prerequisites Checklist

- [ ] Linux system (Ubuntu/Debian/Fedora/Arch/etc.)
- [ ] Python 3.8 or higher installed
- [ ] Internet connection
- [ ] Google account
- [ ] Default web browser configured

## Installation Steps

### 1. Install Dependencies (2 minutes)

```bash
# Navigate to project directory
cd yt-tui

# Run the installation script
./install.sh
```

The script will:
- Check Python version
- Create virtual environment
- Install all dependencies
- Create config directory

### 2. Get YouTube API Credentials (5 minutes)

**A. Create Google Cloud Project**
1. Visit: https://console.cloud.google.com/
2. Click "New Project"
3. Name: "YT-TUI"
4. Click "Create"

**B. Enable YouTube API**
1. Go to "APIs & Services" → "Library"
2. Search "YouTube Data API v3"
3. Click "Enable"

**C. Create OAuth Credentials**
1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External", click "Create"
3. Fill in:
   - App name: YT-TUI
   - Your email (2 places)
4. Click "Save and Continue" (3 times)
5. Go to "Credentials" tab
6. Click "Create Credentials" → "OAuth client ID"
7. Application type: "Desktop app"
8. Name: "YT-TUI Client"
9. Click "Create"
10. Click "Download JSON"

**D. Install Credentials**
```bash
# Move downloaded file
mv ~/Downloads/client_secret_*.json ~/.config/yt-tui/client_secret.json
```

### 3. Run YT-TUI (1 minute)

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
python main.py
```

### 4. First Authentication (2 minutes)

1. Browser opens automatically
2. Sign in to Google
3. Click "Advanced" → "Go to YT-TUI (unsafe)"
4. Click "Continue"
5. Return to terminal
6. YT-TUI is now running!

## First Use

Once the app starts:

1. **Search for videos**: Press `/` and type a query
2. **Browse trending**: Press `2`
3. **View subscriptions**: Press `3`
4. **Navigate**: Use arrow keys
5. **Open video**: Press `Enter`
6. **Quit**: Press `q`

## Keyboard Shortcuts Quick Reference

```
/  - Search
1  - Search tab
2  - Trending tab
3  - Subscriptions tab
4  - History tab
5  - Playlists tab
r  - Refresh
q  - Quit
↑↓ - Navigate
Enter - Open video
```

## Troubleshooting

### "Client secret file not found"
```bash
ls ~/.config/yt-tui/client_secret.json
# If not there, download again and place correctly
```

### "Python version too old"
```bash
python3 --version  # Must be 3.8+
# If older, install newer Python
```

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Browser doesn't open"
```bash
# Set default browser
xdg-settings set default-web-browser firefox.desktop
```

## What's Next?

- Read `USAGE.md` for detailed features
- Check `SETUP_GUIDE.md` if you have auth issues
- Read `README.md` for full documentation

## Common Questions

**Q: Is this free?**
A: Yes! Completely free.

**Q: Do I need YouTube Premium?**
A: No, any Google account works.

**Q: Can I watch videos in the terminal?**
A: No, videos open in your browser.

**Q: Why do I need API credentials?**
A: To access YouTube data securely via their official API.

**Q: Is my data safe?**
A: Yes, credentials are stored locally and never shared.

## Quick Commands

```bash
# Start YT-TUI
cd yt-tui
source venv/bin/activate
python main.py

# Update dependencies
pip install -r requirements.txt --upgrade

# Reset authentication
rm ~/.config/yt-tui/token.json

# View logs
python main.py 2>&1 | tee yt-tui.log
```

## Success Checklist

After setup, you should be able to:
- [x] Start YT-TUI without errors
- [x] Search for videos
- [x] See trending videos
- [x] View your subscriptions
- [x] Open videos in browser
- [x] Navigate with keyboard

## Getting Help

- **Setup issues**: See `SETUP_GUIDE.md`
- **Usage questions**: See `USAGE.md`
- **Bugs**: Report on GitHub
- **Everything else**: See `README.md`

---

**Time to first video: ~10 minutes** ⚡
**Enjoy YT-TUI!** 🚀
