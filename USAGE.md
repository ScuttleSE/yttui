# YT-TUI Usage Guide

Complete guide to using YT-TUI effectively.

## Starting the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
python main.py
```

## Interface Overview

YT-TUI has a tabbed interface with 5 main sections:

```
┌─ YT-TUI - YouTube Terminal Client ─────────────────────────┐
│ Navigate with Tab, Enter to play, / to search, q to quit   │
├─────────────────────────────────────────────────────────────┤
│ [Search] [Trending] [Subscriptions] [History] [Playlists] │
│                                                             │
│ (Content area - varies by tab)                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
 q quit | r refresh | / search
```

## Keyboard Shortcuts Reference

### Global Shortcuts (work in any tab)

| Shortcut | Action |
|----------|--------|
| `q` | Quit the application |
| `Tab` | Cycle through tabs |
| `Shift+Tab` | Cycle backwards through tabs |
| `1` | Jump to Search tab |
| `2` | Jump to Trending tab |
| `3` | Jump to Subscriptions tab |
| `4` | Jump to History tab |
| `5` | Jump to Playlists tab |
| `/` or `s` | Jump to Search and focus input |
| `r` | Refresh current view |

### Navigation Shortcuts

| Shortcut | Action |
|----------|--------|
| `↑` / `k` | Move up in list |
| `↓` / `j` | Move down in list |
| `Enter` | Open selected item |
| `Esc` | Go back (in sub-screens) |
| `Home` | Jump to first item |
| `End` | Jump to last item |
| `PgUp` | Scroll up one page |
| `PgDn` | Scroll down one page |

### Text Input

| Shortcut | Action |
|----------|--------|
| `Enter` | Submit search |
| `Esc` | Clear/unfocus input |
| `Ctrl+A` | Select all text |
| `Ctrl+K` | Delete to end of line |
| `Ctrl+U` | Delete entire line |

## Tab-by-Tab Guide

### 1. Search Tab 🔍

**Purpose**: Search for any video on YouTube

**How to use**:
1. Press `/` or click on the Search tab
2. Type your search query in the input field
3. Press `Enter` or click "Search" button
4. Use arrow keys to navigate results
5. Press `Enter` to open video in browser

**Example searches**:
- "python tutorial"
- "linux terminal tricks"
- "textual python tui"
- "ambient music"

**Tips**:
- More specific queries give better results
- Quotes for exact phrases: "machine learning basics"
- Use search operators like `channel:channelname`

### 2. Trending Tab 🔥

**Purpose**: Browse currently trending videos

**How to use**:
1. Click on Trending tab or press `2`
2. Videos automatically load
3. Navigate with arrow keys
4. Press `Enter` to open video

**Note**:
- Trending videos are region-specific (default: US)
- No authentication required for this tab
- Refreshes when you press `r`

### 3. Subscriptions Tab 📺

**Purpose**: View your subscribed channels and their latest videos

**Modes**:
1. **Channels Mode**: Lists all channels you're subscribed to
2. **Videos Mode**: Shows recent videos from your subscriptions

**How to use**:
1. Click Subscriptions tab or press `3`
2. Click "Show Latest Videos" to toggle between modes
3. In Channels mode: Press `Enter` to open channel page
4. In Videos mode: Press `Enter` to open video

**Tips**:
- Channels are sorted alphabetically
- Videos show most recent uploads first
- Use `r` to refresh and see new uploads

### 4. History Tab 🕐

**Purpose**: View your YouTube activity

**How to use**:
1. Click History tab or press `4`
2. Browse your recent activity
3. Press `Enter` to open video

**Important Note**:
The YouTube API has restrictions on watch history access. This tab shows your YouTube activity feed (uploads, recommendations) rather than true watch history.

**Alternative**:
For full watch history, visit: https://www.youtube.com/feed/history

### 5. Playlists Tab 📚

**Purpose**: Browse and view your playlists

**How to use**:
1. Click Playlists tab or press `5`
2. Select a playlist with `Enter`
3. A new screen opens showing playlist videos
4. Select a video with `Enter` to open in browser
5. Press `Esc` or `q` to go back to playlists list

**Playlist Information Shown**:
- Title
- Number of videos
- Description preview
- Creation date

## Common Workflows

### Finding and Watching Videos

```
1. Press / to open search
2. Type "cooking tutorial"
3. Press Enter
4. Use ↓ arrow to browse results
5. Press Enter on desired video
6. Video opens in browser
```

### Checking New Videos from Subscriptions

```
1. Press 3 to open Subscriptions
2. Click "Show Latest Videos" button
3. Browse with arrow keys
4. Press Enter to watch
```

### Browsing a Playlist

```
1. Press 5 to open Playlists
2. Use arrows to find desired playlist
3. Press Enter to open playlist
4. Browse videos with arrows
5. Press Enter to watch
6. Press Esc to go back
```

## Tips and Tricks

### Efficient Navigation

1. **Use Number Keys**: Press `1-5` to jump directly to tabs
2. **Vim Keys**: If you're a Vim user, `j/k` work for up/down
3. **Quick Search**: Press `/` from any tab to jump to search
4. **Refresh Often**: Press `r` to see new content

### Search Tips

1. **Be Specific**: "python asyncio tutorial" vs "python"
2. **Use Quotes**: "exact phrase here"
3. **Filter by Duration**: Search "short", "medium", or "long"
4. **Find Channels**: Add channel name for specific creators

### Browser Integration

- Videos open in your default browser
- Set default browser: `xdg-settings set default-web-browser firefox.desktop`
- Browser must be running or will launch automatically

### Performance

1. **Reduce Results**: Fewer results = faster loading
2. **Limit Searches**: API has daily quota (10,000 units/day)
3. **Cache**: Previously loaded data is shown immediately

## Configuration

Edit `~/.config/yt-tui/config.json`:

```json
{
  "results_per_page": 25,    // Number of results to fetch
  "last_section": "search",   // Last used tab
  "max_results": 50           // Maximum results per request
}
```

## Troubleshooting Common Issues

### Videos Not Opening

**Problem**: Pressing Enter doesn't open video

**Solutions**:
1. Check if row is actually selected (highlighted)
2. Verify default browser is set
3. Try opening a URL manually in terminal: `xdg-open https://youtube.com`

### Search Not Working

**Problem**: Search returns no results or error

**Solutions**:
1. Check internet connection
2. Verify API quota hasn't been exceeded
3. Try a different search query
4. Refresh with `r`

### Slow Loading

**Problem**: Videos take long to load

**Solutions**:
1. Reduce `max_results` in config
2. Check internet speed
3. API might be slow - wait a moment
4. Try refreshing with `r`

### Authentication Expired

**Problem**: "Authentication failed" error

**Solutions**:
```bash
# Delete token and re-authenticate
rm ~/.config/yt-tui/token.json
python main.py
```

## API Quota Management

YouTube API has daily limits:

| Operation | Cost (units) | Daily Limit |
|-----------|-------------|-------------|
| Search | 100 | 100 searches |
| List videos | 1 | 10,000 |
| List playlists | 1 | 10,000 |
| Activities | 1 | 10,000 |

**Tips to Conserve Quota**:
- Use Trending tab (no quota cost)
- Search less frequently
- Use specific search queries
- Avoid excessive refreshing

## Advanced Usage

### Environment Variables

```bash
# Custom client secret location
export YOUTUBE_CLIENT_SECRET=/path/to/client_secret.json

# Custom config directory
# (requires code modification)
```

### Multiple Accounts

```bash
# Save different configs
mv ~/.config/yt-tui ~/.config/yt-tui-account1
mkdir ~/.config/yt-tui
# Run with different credentials
```

### Scripting

```bash
# Quick launch alias
echo 'alias yt="cd ~/yt-tui && source venv/bin/activate && python main.py"' >> ~/.bashrc
source ~/.bashrc

# Now just type: yt
```

## Keyboard Layout Reference

```
┌─────────────────────────────────────┐
│ [1]    [2]    [3]    [4]    [5]    │  Tab selection
│                                     │
│ [/] [r] [q]                        │  Actions
│                                     │
│ [↑] [↓] or [j] [k]                │  Navigation
│                                     │
│ [Enter]                            │  Select
│ [Esc]                              │  Back
└─────────────────────────────────────┘
```

## Best Practices

1. **Start Simple**: Begin with Search and Trending
2. **Learn Shortcuts**: Memorize `/, r, q` first
3. **Manage Quota**: Don't over-search
4. **Keep Updated**: Pull latest changes regularly
5. **Report Issues**: File bugs on GitHub

## Limitations

- No video playback in terminal (browser only)
- No live chat access
- No comments (API limitation)
- Limited watch history (API restriction)
- Daily API quota limits

## Getting Help

- Press `q` to quit any time
- Check `README.md` for setup issues
- See `SETUP_GUIDE.md` for authentication help
- Report bugs on GitHub

---

**Happy browsing!** 🎥🚀
