# Channel Management Guide

View and manage your YouTube channels in YT-TUI!

## Overview

A single Google account can have multiple YouTube channels:
- **Personal Channel** - Your main channel (created automatically)
- **Brand Channels** - Additional channels you've created or manage
- **Managed Channels** - Channels you have access to through brand accounts

YT-TUI lets you view all channels associated with your account.

## Features

✅ **View All Channels** - See all channels for your account
✅ **Channel Details** - Subscriber count, video count, views
✅ **Quick Access** - Click to open channel in browser
✅ **Channel Count** - See how many channels you have
✅ **Statistics** - View channel stats at a glance

## How to Use

### Viewing Your Channels

**Method 1: Keyboard Shortcut**
```
Press 'c' (anywhere in the app)
```

**Method 2: Click Channel Count**
```
Click "📺 X Channels" at the top of the screen
```

### Channel Switcher Interface

When you press `c`, you'll see:

```
┌────────────────────────────────────────────────────────────┐
│ 📺 Your YouTube Channels                                   │
│ These are all channels associated with your account:       │
│                                                            │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ 📺 My Personal Channel                                 │ │
│ │ 👥 1.2K subscribers • 🎥 45 videos • 👁 50K views     │ │
│ │ youtube.com/@mypersonalchannel                         │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                            │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ 📺 My Brand Channel                                    │ │
│ │ 👥 5.6K subscribers • 🎥 120 videos • 👁 230K views   │ │
│ │ youtube.com/@mybrandchannel                            │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                            │
│                    [Close]                                 │
└────────────────────────────────────────────────────────────┘
```

**Information Shown:**
- 📺 Channel name
- 👥 Subscriber count
- 🎥 Video count
- 👁 Total views
- 🔗 Channel URL (custom URL or channel ID)

**Actions:**
- **Click any channel** → Opens in browser
- **ESC or Close** → Returns to app

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `c` | Open channel viewer |
| `↑/↓` | Scroll through channels |
| `Click` | Open channel in browser |
| `Esc` | Close channel viewer |

## Use Cases

### Content Creators with Multiple Channels

```
Personal Channel:  Your vlog channel
Gaming Channel:    Your gaming content
Tutorial Channel:  Your how-to videos
```

View all your channels and their stats in one place!

### Brand Account Managers

```
Company Main:      Main brand channel
Company Gaming:    Gaming division
Company Music:     Music division
```

See all channels you manage!

### Personal + Brand Channels

```
Personal:  john.doe@gmail.com - Personal Channel
Brand:     Business Channel - Brand Account
```

Keep track of both!

## Channel Display

At the top of the app, you'll see:

```
👤 Your Name (email@gmail.com)  📺 2 Channels
```

- Shows account name/email
- Shows total channel count
- Click either to manage!

## Statistics Explained

### Subscriber Count
```
👥 1.2K subscribers
```
Total number of people subscribed to the channel.

### Video Count
```
🎥 45 videos
```
Total videos published on the channel.

### View Count
```
👁 50K views
```
Total views across all videos on the channel.

## Channel URLs

### Custom URL
If your channel has a custom URL:
```
youtube.com/@yourchannel
```

### Channel ID
If no custom URL:
```
Channel ID: UCxxxxxxxxxxxxxxxxxxxxx...
```

## Opening Channels

Click any channel to:
1. Open it in your default browser
2. View the channel page
3. Access channel settings (if you're logged in to YouTube)

## API Information

**Endpoint Used:**
- `channels().list()` with `mine=True`

**Data Retrieved:**
- Channel ID
- Title
- Description
- Thumbnail
- Custom URL (if available)
- Statistics (subscribers, videos, views)
- Publication date

**API Cost:**
- 1 unit per request
- Minimal quota usage

## Troubleshooting

### "No channels found"

**Cause**: Your Google account doesn't have any YouTube channels yet.

**Solution**: Create a channel at youtube.com first.

### "Error loading channels"

**Cause**: API error or authentication issue.

**Solution**:
```bash
# Refresh authentication
rm ~/.config/yt-tui/token*.json
python main.py
```

### Channel count shows "Loading..."

**Cause**: Channels haven't been fetched yet.

**Solution**: Press `c` to load channels, or wait for automatic load.

### Can't click on channel

**Cause**: UI focus issue or browser problem.

**Solution**:
- Try pressing ESC and reopening with `c`
- Check default browser is set

### Wrong channels showing

**Cause**: Using wrong account.

**Solution**:
- Press `a` to check active account
- Switch to correct account if needed

## Technical Details

### Channel Types

**Personal Channel:**
- Created automatically with Google account
- Uses your Google account name
- One per account

**Brand Channels:**
- Can create multiple
- Separate from personal channel
- Can have multiple managers
- Different name from your account

### Channel Management

Note: This feature is **read-only** for viewing channels. To:
- Create new channels → Use youtube.com
- Edit channel settings → Use YouTube Studio
- Delete channels → Use YouTube Studio

YT-TUI shows your channels but doesn't modify them.

## Privacy

**What the app can see:**
- Channel names
- Public statistics
- Channel descriptions
- Thumbnails

**What the app cannot see:**
- Private channel data
- Draft videos
- Analytics beyond basic stats
- Monetization info

## Best Practices

1. **Check Regularly**: View channels to track growth
2. **Multiple Accounts**: Switch accounts to see different channel sets
3. **Quick Access**: Use `c` shortcut for fast access
4. **Browser Integration**: Click to manage in YouTube Studio

## Future Enhancements

Planned features:
- 📊 Detailed channel analytics
- 🎨 Channel-specific themes
- 🔔 Per-channel notifications
- 📈 Growth tracking
- 🎯 Channel switching (set active context)
- 📝 Channel notes/labels

## FAQ

**Q: Can I switch between channels for operations?**
A: Currently, the app shows all channels. Most API operations use your account's default channel context. Full channel switching coming in future updates!

**Q: Why do I see multiple channels?**
A: You may have:
- Created brand channels
- Been added as a manager to other channels
- Created channels for different purposes

**Q: Can I create channels from the app?**
A: No, use youtube.com to create channels. The app is for viewing only.

**Q: Do all channels share API quota?**
A: Yes, they all use your Google Cloud Project's quota.

**Q: Can I hide certain channels?**
A: Not currently, but this feature may be added in future updates.

**Q: How often do stats update?**
A: Stats are fetched when you open the channel viewer. They reflect YouTube's current data.

## Examples

### Viewing Channels

```
1. Press 'c'
2. See all your channels
3. Click one to open in browser
4. Manage it in YouTube Studio!
```

### Content Creator Workflow

```
1. Open YT-TUI
2. Press 'c' to check channel stats
3. See subscriber growth
4. Continue working on content!
```

### Multi-Channel Manager

```
Account 1: Personal channels (Press 'a' → Select account 1)
Press 'c' → View personal channels

Account 2: Business channels (Press 'a' → Select account 2)
Press 'c' → View business channels
```

## Support

Having issues with channels?
- Check TROUBLESHOOTING.md
- Verify authentication is working
- Try refreshing (press 'r')
- Check YouTube API quota

---

**Enjoy managing your YouTube channels!** 📺✨
