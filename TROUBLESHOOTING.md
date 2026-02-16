# Troubleshooting Guide

Common issues and their solutions.

## Installation Issues

### Error: "Could not find a version that satisfies the requirement textual==1.1.0"

**Cause**: The specified version doesn't exist.

**Solution**: Already fixed in `requirements.txt`. Use `textual==0.86.3` or install with:
```bash
pip install -r requirements.txt
```

### Error: "No module named 'google'"

**Cause**: Dependencies not installed.

**Solution**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Runtime Errors

### Error: "VisualError: unable to display 'YouTubeAPI' type"

**Cause**: UI components were passing API object as content to Static widget.

**Solution**: Already fixed. Each screen now has proper `__init__` method that:
- Accepts `youtube_api` parameter
- Calls `super().__init__()` properly
- Stores API as `self.youtube`

### Error: "Client secret file not found"

**Cause**: Missing OAuth2 credentials.

**Solution**:
1. Follow SETUP_GUIDE.md to create credentials
2. Place `client_secret.json` in `~/.config/yt-tui/`
3. Or set: `export YOUTUBE_CLIENT_SECRET=/path/to/file`

### Error: "Authentication failed"

**Cause**: Invalid or expired credentials.

**Solution**:
```bash
# Delete old token
rm ~/.config/yt-tui/token.json

# Re-authenticate
python main.py
```

### Error: "API quota exceeded"

**Cause**: Daily API limit reached (10,000 units).

**Solution**:
- Wait until next day (resets midnight PT)
- Use Trending tab (no quota cost)
- Reduce searches

## UI Issues

### App doesn't start / Black screen

**Cause**: Terminal incompatibility or Python version issue.

**Solution**:
```bash
# Check Python version (need 3.8+)
python3 --version

# Try with explicit terminal type
TERM=xterm-256color python main.py

# Check textual version
python -c "import textual; print(textual.__version__)"
```

### Keyboard shortcuts don't work

**Cause**: Terminal not capturing key events.

**Solution**:
- Use a modern terminal (GNOME Terminal, Konsole, Alacritty)
- Avoid screen/tmux unless properly configured
- Check terminal key bindings

### Videos don't open in browser

**Cause**: No default browser set or `xdg-open` not working.

**Solution**:
```bash
# Set default browser
xdg-settings set default-web-browser firefox.desktop

# Test xdg-open
xdg-open https://youtube.com

# Check installed browsers
ls /usr/share/applications/*browser*.desktop
```

## API Issues

### Error: "redirect_uri_mismatch"

**Cause**: OAuth client type is wrong.

**Solution**:
1. Go to Google Cloud Console
2. Delete OAuth client
3. Create new "Desktop app" credentials (NOT Web application)

### Error: "Access blocked: YT-TUI has not completed verification"

**Cause**: Not added as test user.

**Solution**:
1. Go to Google Cloud Console
2. Navigate to OAuth consent screen
3. Add your email under "Test users"

### Search returns no results

**Cause**: Network issue or API error.

**Solution**:
```bash
# Check internet
ping -c 1 google.com

# Try trending tab first (test API)
# Press '2' in app

# Check API status
# Visit: https://status.cloud.google.com/
```

## Performance Issues

### Slow loading

**Cause**: Slow internet or API response time.

**Solution**:
- Reduce `max_results` in config
- Check network speed
- Use wired connection if possible

### High memory usage

**Cause**: Loading too many results.

**Solution**:
Edit `~/.config/yt-tui/config.json`:
```json
{
  "results_per_page": 10,
  "max_results": 25
}
```

## Debugging

### Enable verbose logging

```bash
# Run with Python warnings
python -W all main.py

# Capture full traceback
python main.py 2>&1 | tee debug.log
```

### Check configuration

```bash
# View config
cat ~/.config/yt-tui/config.json

# Check credentials exist
ls -la ~/.config/yt-tui/
```

### Test YouTube API connection

```python
# Quick test script
python3 << 'EOF'
from auth import get_authenticated_service
from youtube_api import YouTubeAPI

try:
    service = get_authenticated_service()
    api = YouTubeAPI(service)
    results = api.get_trending_videos(max_results=1)
    print(f"✅ API working! Found: {results[0]['title']}")
except Exception as e:
    print(f"❌ API error: {e}")
EOF
```

## Getting Help

If none of these solutions work:

1. **Check versions**:
   ```bash
   python3 --version
   pip list | grep -E "textual|google"
   ```

2. **Clean install**:
   ```bash
   rm -rf venv
   ./install.sh
   ```

3. **Reset everything**:
   ```bash
   rm -rf venv ~/.config/yt-tui
   ./install.sh
   # Then set up OAuth again
   ```

4. **Report issue**:
   - Include Python version
   - Include error message
   - Include steps to reproduce
   - Check existing issues first

## Known Limitations

These are not bugs, but API/design limitations:

- **Watch history**: Limited by YouTube API restrictions
- **Live chat**: Not supported by API
- **Video playback**: Terminal can't play video (by design)
- **Comments**: Not implemented
- **Upload/Edit**: Read-only access only

## Quick Fixes Summary

```bash
# Broken installation
rm -rf venv && ./install.sh

# Authentication issues
rm ~/.config/yt-tui/token.json

# Start fresh
rm -rf venv ~/.config/yt-tui && ./install.sh

# Test API only
python3 -c "from youtube_api import YouTubeAPI; print('Import OK')"

# Check all files present
ls -la ui/*.py main.py auth.py config.py youtube_api.py
```

---

**Still stuck?** Check README.md and SETUP_GUIDE.md for detailed instructions.
