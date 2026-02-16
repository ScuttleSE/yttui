# YT-TUI - YouTube Terminal User Interface

A modern, feature-rich Text User Interface (TUI) YouTube client for the Linux terminal. Browse YouTube, search videos, view your subscriptions, playlists, and more - all from the comfort of your terminal!

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🔍 **Search Videos** - Search YouTube with full metadata
- 🔥 **Trending** - Browse trending videos (no authentication required)
- 📺 **Subscriptions** - View your subscribed channels and their latest videos
- 📚 **Playlists** - Browse your playlists and their contents
- 🕐 **History** - Access your watch history (limited API access)
- 🌐 **Browser Integration** - Opens videos in your default web browser
- 🔐 **OAuth2 Authentication** - Secure authentication with YouTube
- ⌨️ **Keyboard Navigation** - Full keyboard control
- 🎨 **Modern UI** - Built with the Textual framework

## Screenshots

```
┌─────────────────────────────────────────────────────────────────┐
│ YT-TUI - YouTube Terminal Client                               │
├─────────────────────────────────────────────────────────────────┤
│ [Search] [Trending] [Subscriptions] [History] [Playlists]      │
│                                                                 │
│ 🔍 Search YouTube                                               │
│ ┌─────────────────────────────────────────────┐                │
│ │ Enter search query...                       │ [Search]       │
│ └─────────────────────────────────────────────┘                │
│                                                                 │
│ Title                    Channel      Duration  Views  Date    │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ How to build a TUI app  TechChannel  12:34    1.2M   2024-01  │
│ Python tips and tricks  CodeMaster   8:15     850K   2024-02  │
└─────────────────────────────────────────────────────────────────┘
 q quit | r refresh | / search
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Linux terminal/console
- Google Cloud account (free)

### Step 1: Clone the repository

```bash
git clone <repository-url>
cd yt-tui
```

### Step 2: Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

**Note**: If you encounter version issues, try using the latest compatible versions:
```bash
pip install -r requirements-latest.txt
```

### Step 4: Set up YouTube API credentials

This is the most important step! You need to create OAuth2 credentials to access YouTube API.

#### 4.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" > "New Project"
3. Give it a name (e.g., "YT-TUI") and click "Create"
4. Wait for the project to be created and select it

#### 4.2 Enable YouTube Data API v3

1. In the Google Cloud Console, go to **"APIs & Services"** > **"Library"**
2. Search for **"YouTube Data API v3"**
3. Click on it and press **"Enable"**
4. Wait for it to enable (takes a few seconds)

#### 4.3 Create OAuth 2.0 Credentials

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"Create Credentials"** > **"OAuth client ID"**
3. If prompted, configure the OAuth consent screen:
   - Choose **"External"** (unless you have a Google Workspace)
   - Fill in the required fields:
     - App name: `YT-TUI`
     - User support email: your email
     - Developer contact: your email
   - Click **"Save and Continue"**
   - Skip the "Scopes" section (click "Save and Continue")
   - Add yourself as a test user in the "Test users" section
   - Click **"Save and Continue"**
4. Back at "Create OAuth client ID":
   - Application type: **"Desktop app"**
   - Name: `YT-TUI Client`
   - Click **"Create"**
5. A dialog will appear with your credentials - click **"Download JSON"**
6. Save the file as `client_secret.json`

#### 4.4 Place the credentials file

```bash
# Create config directory
mkdir -p ~/.config/yt-tui

# Move the downloaded file
mv ~/Downloads/client_secret_*.json ~/.config/yt-tui/client_secret.json
```

Alternatively, you can set an environment variable:

```bash
export YOUTUBE_CLIENT_SECRET=/path/to/your/client_secret.json
```

### Step 5: Run YT-TUI

```bash
python main.py
```

On first run, a browser window will open asking you to:
1. Log in to your Google account
2. Grant permissions to YT-TUI
3. The credentials will be saved for future use

## Usage

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Tab` | Switch between tabs |
| `1-5` | Jump to specific tab (1=Search, 2=Trending, etc.) |
| `↑/↓` or `j/k` | Navigate lists |
| `Enter` | Open selected video/playlist in browser |
| `/` or `s` | Focus search input |
| `r` | Refresh current view |
| `Esc` | Go back (in playlist view) |
| `q` | Quit application |

### Navigation

- **Search Tab**: Type your query and press Enter or click "Search"
- **Trending Tab**: Automatically loads trending videos
- **Subscriptions Tab**: Toggle between viewing channels or latest videos
- **Playlists Tab**: Select a playlist to view its videos
- **History Tab**: Shows your recent activity (limited by API)

### Tips

- The app automatically refreshes OAuth tokens when they expire
- Press `r` to refresh the current view with latest data
- Use arrow keys or vim-style `j/k` keys for navigation
- Videos open in your default web browser

## Configuration

Configuration is stored in `~/.config/yt-tui/config.json`:

```json
{
  "results_per_page": 25,
  "last_section": "search",
  "max_results": 50
}
```

## API Quotas

YouTube Data API v3 has daily quotas:
- **Free tier**: 10,000 units per day
- **Cost per operation**:
  - Search: 100 units
  - List videos: 1 unit
  - List playlists: 1 unit

The free quota is usually sufficient for personal use. If you exceed it, you'll see an error message and need to wait until the next day (Pacific Time).

## Troubleshooting

### Authentication Issues

**Problem**: "Client secret file not found"
```bash
# Check if file exists
ls -la ~/.config/yt-tui/client_secret.json

# If not, place it there or set environment variable
export YOUTUBE_CLIENT_SECRET=/path/to/client_secret.json
```

**Problem**: "OAuth2 flow failed"
- Make sure you've enabled the YouTube Data API v3
- Check that you're using "Desktop app" type credentials
- Try deleting the token and re-authenticating:
  ```bash
  rm ~/.config/yt-tui/token.json
  python main.py
  ```

### API Quota Exceeded

**Problem**: "API quota exceeded"
- Wait until the next day (quota resets at midnight Pacific Time)
- Reduce the number of searches
- Consider applying for a quota increase in Google Cloud Console

### Watch History Not Available

The YouTube API has restrictions on watch history access. The app uses the activities API as an alternative, which shows your recent YouTube activity.

### Videos Not Opening in Browser

**Problem**: Browser doesn't open
- Check that you have a default browser set:
  ```bash
  xdg-settings get default-web-browser
  ```
- Try setting it manually:
  ```bash
  xdg-settings set default-web-browser firefox.desktop
  ```

## Project Structure

```
yt-tui/
├── main.py                 # Entry point
├── config.py              # Configuration management
├── auth.py                # OAuth2 authentication
├── youtube_api.py         # YouTube API wrapper
├── ui/
│   ├── __init__.py
│   ├── app.py            # Main Textual app
│   ├── search.py         # Search screen
│   ├── trending.py       # Trending screen
│   ├── subscriptions.py  # Subscriptions screen
│   ├── history.py        # History screen
│   └── playlists.py      # Playlists screen
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore            # Git ignore rules
```

## API Scopes Used

```python
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]
```

These scopes allow:
- Read-only access to your YouTube account
- Viewing subscriptions, playlists, and activity
- Searching public videos

## Security Notes

- Never commit `client_secret.json` or `token.json` to version control
- The `.gitignore` file is configured to exclude these automatically
- Tokens are stored locally in `~/.config/yt-tui/`
- OAuth tokens are automatically refreshed when expired

## Development

### Running in development mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run with Python
python main.py

# Or make it executable
chmod +x main.py
./main.py
```

### Adding new features

The codebase is modular:
- Add new API methods to `youtube_api.py`
- Create new screens in `ui/` directory
- Register new tabs in `ui/app.py`

## Known Limitations

1. **Watch History**: Limited by YouTube API restrictions
2. **Live Chat**: Not supported by YouTube Data API v3
3. **Comments**: Not implemented (can be added)
4. **Video Playback**: Opens in browser (terminal video playback not supported)
5. **Upload/Edit**: Read-only access only

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Acknowledgments

- Built with [Textual](https://github.com/Textualize/textual) - An amazing TUI framework
- Uses [YouTube Data API v3](https://developers.google.com/youtube/v3)
- Inspired by various terminal-based media clients

## FAQ

**Q: Is this free to use?**
A: Yes! Both YT-TUI and the YouTube API (within quota limits) are free.

**Q: Can I watch videos in the terminal?**
A: No, videos open in your web browser. Terminal video playback would require different tools (like `mpv` or `youtube-dl`).

**Q: Do I need a YouTube Premium account?**
A: No, this works with any Google account.

**Q: Can I use this on Windows or macOS?**
A: The app is designed for Linux but should work on macOS with minor adjustments. Windows support via WSL is possible.

**Q: How do I uninstall?**
A: Simply delete the directory and config:
```bash
rm -rf ~/path/to/yt-tui
rm -rf ~/.config/yt-tui
```

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Enjoy browsing YouTube in your terminal!** 🚀📺
