# YT-TUI Project Summary

## Overview

YT-TUI is a complete, production-ready Text User Interface (TUI) YouTube client built with Python. It provides a modern terminal-based interface for browsing YouTube, searching videos, managing subscriptions, and viewing playlists.

## Project Structure

```
yt-tui/
├── main.py                 # Entry point and authentication flow
├── config.py              # Configuration management
├── auth.py                # OAuth2 authentication handler
├── youtube_api.py         # YouTube Data API v3 wrapper
├── ui/                    # User interface components
│   ├── __init__.py
│   ├── app.py            # Main Textual application
│   ├── search.py         # Search screen
│   ├── trending.py       # Trending videos screen
│   ├── subscriptions.py  # Subscriptions screen
│   ├── history.py        # Watch history screen
│   └── playlists.py      # Playlists screen
├── requirements.txt       # Python dependencies
├── install.sh            # Automated installation script
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
├── README.md             # Main documentation
├── SETUP_GUIDE.md        # Detailed OAuth2 setup guide
└── USAGE.md              # User guide and shortcuts
```

## Core Components

### 1. Authentication System (auth.py)

**Purpose**: Handles OAuth2 authentication with Google/YouTube API

**Key Functions**:
- `get_authenticated_service()` - Main authentication function
- `is_authenticated()` - Check authentication status
- `clear_credentials()` - Remove saved tokens

**Features**:
- Automatic token refresh
- Secure credential storage
- Error handling for auth failures
- First-time setup flow

**OAuth Flow**:
1. Check for existing token
2. If expired, refresh automatically
3. If missing, launch OAuth flow
4. Save credentials for future use

### 2. API Wrapper (youtube_api.py)

**Purpose**: Clean interface to YouTube Data API v3

**Key Methods**:
- `search_videos(query, max_results)` - Search for videos
- `get_subscriptions(max_results)` - Get user's subscriptions
- `get_subscription_videos(max_results)` - Get recent uploads from subscriptions
- `get_watch_history(max_results)` - Get activity feed
- `get_playlists(max_results)` - Get user's playlists
- `get_playlist_videos(playlist_id, max_results)` - Get playlist contents
- `get_trending_videos(max_results, region_code)` - Get trending videos

**Data Parsing**:
- Video metadata extraction
- Duration formatting (ISO 8601 → readable)
- Number formatting (1234567 → 1.2M)
- Date formatting (ISO 8601 → YYYY-MM-DD)

**Error Handling**:
- API quota exceeded detection
- Network error handling
- Permission error handling
- Custom `YouTubeAPIError` exception

### 3. Configuration System (config.py)

**Purpose**: Manage application configuration and file paths

**Configuration Locations**:
- Config directory: `~/.config/yt-tui/`
- Credentials: `~/.config/yt-tui/client_secret.json`
- Token: `~/.config/yt-tui/token.json`
- Config: `~/.config/yt-tui/config.json`

**Settings**:
```json
{
  "results_per_page": 25,
  "last_section": "search",
  "max_results": 50
}
```

### 4. User Interface (ui/)

Built with the Textual framework - a modern Python TUI library.

#### Main App (ui/app.py)

**Features**:
- Tabbed interface with 5 sections
- Global keyboard shortcuts
- Header and footer with hints
- Screen management for nested views

**Global Bindings**:
- `q` - Quit
- `r` - Refresh current view
- `/` - Jump to search
- `1-5` - Switch tabs
- `Tab` - Cycle tabs

#### Search Screen (ui/search.py)

**Components**:
- Search input field
- Search button
- Results data table

**Features**:
- Real-time search execution
- Results display with metadata
- Row selection to open videos
- Error message display

#### Trending Screen (ui/trending.py)

**Features**:
- Auto-loads on mount
- No authentication required
- Displays popular videos
- Refreshable

#### Subscriptions Screen (ui/subscriptions.py)

**Modes**:
1. Channels mode - List all subscriptions
2. Videos mode - Recent uploads from subscriptions

**Features**:
- Toggle button to switch modes
- Opens channels or videos
- Requires authentication

#### History Screen (ui/history.py)

**Features**:
- Shows YouTube activity feed
- Limited by API restrictions
- Displays video metadata

**Note**: True watch history requires special API access.

#### Playlists Screen (ui/playlists.py)

**Features**:
- Lists user's playlists
- Pushes new screen for playlist contents
- Back navigation with Esc/q
- Shows video counts

**Nested Screen**:
- `PlaylistVideosScreen` - Displays videos in a playlist

## Technology Stack

### Core Dependencies

```python
# YouTube API
google-api-python-client==2.149.0  # API client
google-auth==2.35.0                 # Authentication
google-auth-oauthlib==1.2.1        # OAuth2 flow
google-auth-httplib2==0.2.0        # HTTP transport

# TUI Framework
textual==1.1.0                      # Main TUI framework
rich==13.9.4                        # Terminal formatting

# Utilities
httplib2==0.22.0                    # HTTP library
uritemplate==4.1.1                  # URL templates
isodate==0.7.2                      # ISO date parsing
```

## API Integration

### YouTube Data API v3 Endpoints Used

1. **search().list()**
   - Search for videos
   - Cost: 100 units per request
   - Returns: Video IDs, snippets

2. **videos().list()**
   - Get video details
   - Cost: 1 unit per request
   - Returns: Full metadata, statistics

3. **subscriptions().list()**
   - Get user's subscriptions
   - Cost: 1 unit per request
   - Requires: Authentication

4. **activities().list()**
   - Get user activity
   - Cost: 1 unit per request
   - Requires: Authentication

5. **playlists().list()**
   - Get user's playlists
   - Cost: 1 unit per request
   - Requires: Authentication

6. **playlistItems().list()**
   - Get playlist contents
   - Cost: 1 unit per request

### OAuth2 Scopes

```python
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]
```

**Permissions Granted**:
- View YouTube account information
- View subscriptions
- View playlists
- View activity (limited)
- Read-only access (no modifications)

## Installation Process

### Quick Install

```bash
# Run installation script
./install.sh

# Place credentials
mv client_secret.json ~/.config/yt-tui/

# Run app
source venv/bin/activate
python main.py
```

### Manual Install

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up config directory
mkdir -p ~/.config/yt-tui

# Place credentials and run
python main.py
```

## OAuth2 Setup Process

Detailed in `SETUP_GUIDE.md`, summary:

1. Create Google Cloud project
2. Enable YouTube Data API v3
3. Configure OAuth consent screen
4. Create Desktop app credentials
5. Download client_secret.json
6. Place in `~/.config/yt-tui/`

## Features Implementation

### Implemented ✅

- ✅ Search videos with full metadata
- ✅ View trending videos
- ✅ Browse subscriptions (channels + videos)
- ✅ View playlists and contents
- ✅ Activity feed (history alternative)
- ✅ OAuth2 authentication
- ✅ Automatic token refresh
- ✅ Open videos in browser
- ✅ Keyboard navigation
- ✅ Tabbed interface
- ✅ Error handling
- ✅ Configuration management
- ✅ Quota error detection

### Limitations

- ❌ No video playback in terminal (by design)
- ❌ No live chat access (API limitation)
- ❌ No comments (not implemented)
- ❌ Limited watch history (API restriction)
- ❌ No video upload/edit (read-only scope)

## Error Handling

### Authentication Errors
- Missing credentials → Setup instructions
- Expired token → Auto-refresh
- Invalid token → Re-authenticate prompt

### API Errors
- Quota exceeded → Clear error message
- Network errors → Retry suggestion
- Permission errors → Scope information

### UI Errors
- Browser launch failure → Error notification
- Invalid selection → Graceful handling
- Empty results → Informative messages

## Security Considerations

1. **Credential Storage**
   - Credentials in `~/.config/yt-tui/`
   - Token file permissions: 600 (owner only)
   - Never committed to git (.gitignore)

2. **OAuth Flow**
   - Uses official Google libraries
   - Desktop app flow (localhost redirect)
   - Tokens stored with encryption

3. **API Security**
   - Read-only scopes
   - No sensitive data modification
   - User consent required

## Performance Optimizations

1. **API Calls**
   - Batch video details requests
   - Cache configuration
   - Limit results to reduce quota usage

2. **UI Rendering**
   - Textual's efficient rendering
   - Lazy loading of content
   - Minimal re-renders

3. **Network**
   - Single API client instance
   - Connection reuse
   - Timeout handling

## Testing Strategy

### Manual Testing Checklist

- [ ] Fresh installation
- [ ] OAuth flow completion
- [ ] Each tab loads correctly
- [ ] Search functionality
- [ ] Video opening in browser
- [ ] Playlist navigation
- [ ] Keyboard shortcuts
- [ ] Error scenarios
- [ ] Token refresh
- [ ] Quota limit handling

### Test Scenarios

1. **First-time setup**: No credentials → Setup instructions
2. **Authentication**: OAuth flow → Token saved
3. **Search**: Query → Results displayed → Video opens
4. **Subscriptions**: View channels → View videos
5. **Playlists**: Select playlist → View videos → Play video
6. **Navigation**: All keyboard shortcuts work
7. **Errors**: Handle gracefully with messages

## Documentation

### User Documentation
- `README.md` - Main overview and quick start
- `SETUP_GUIDE.md` - Detailed OAuth2 setup
- `USAGE.md` - Comprehensive user guide
- `PROJECT_SUMMARY.md` - This document

### Code Documentation
- Docstrings in all modules
- Type hints throughout
- Inline comments for complex logic

## Future Enhancements

### Potential Features
1. Video recommendations
2. Comments display
3. Channel browsing
4. Download integration (youtube-dl)
5. Offline mode
6. Multiple accounts
7. Customizable themes
8. Playlist creation/editing
9. Video queue
10. Keyboard customization

### Technical Improvements
1. Async API calls
2. Result caching
3. Background loading
4. Pagination support
5. Unit tests
6. Integration tests
7. CI/CD pipeline
8. Package distribution (PyPI)

## Deployment

### Distribution Methods

1. **Git Clone** (current)
   ```bash
   git clone <repo>
   cd yt-tui
   ./install.sh
   ```

2. **PyPI Package** (future)
   ```bash
   pip install yt-tui
   yt-tui
   ```

3. **System Package** (future)
   ```bash
   apt install yt-tui  # Debian/Ubuntu
   dnf install yt-tui  # Fedora
   ```

## Maintenance

### Regular Tasks
- Update dependencies
- Monitor API changes
- Review user feedback
- Fix bugs
- Update documentation

### Version Control
- Semantic versioning
- Changelog maintenance
- Tag releases
- Branch strategy

## Support Resources

- GitHub Issues for bug reports
- README.md for quick help
- SETUP_GUIDE.md for authentication
- USAGE.md for feature help

## License

MIT License - Open source and free to use/modify.

## Credits

- **Textual** - Modern TUI framework
- **Google APIs** - YouTube Data API v3
- **Python Community** - Excellent libraries

---

**Project Status**: ✅ Complete and functional
**Version**: 1.0.0
**Last Updated**: 2024
