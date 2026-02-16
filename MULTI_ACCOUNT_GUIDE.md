# Multi-Account Support Guide

YT-TUI now supports multiple YouTube accounts! Switch between accounts just like you do in the YouTube web interface.

## Features

- ✅ **Multiple Accounts**: Add and manage multiple YouTube accounts
- ✅ **Quick Switching**: Switch between accounts with a single key press
- ✅ **Account Display**: See which account you're currently using
- ✅ **Automatic Token Management**: Each account has its own token file
- ✅ **Profile Information**: Display account name and email

## How to Use

### Adding Your First Account

When you first run YT-TUI, it will automatically prompt you to authenticate:

```bash
python main.py
```

1. Browser opens automatically
2. Sign in to your YouTube/Google account
3. Grant permissions
4. You're in!

### Adding Additional Accounts

Once in the app:

1. **Press `a`** (or click on the account name at the top)
2. Click **"Add Account"**
3. Browser opens for authentication
4. Sign in to a different Google account
5. Grant permissions
6. New account is added!

### Switching Between Accounts

**Method 1: Keyboard Shortcut**
```
Press 'a' → Select account from list → Enter
```

**Method 2: Click Account Name**
```
Click account name at top → Select account → Click
```

### Account Switcher Interface

When you press `a`, you'll see:

```
┌──────────────────────────────────────────────┐
│ Switch YouTube Account                       │
│ Select an account or add a new one:          │
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ 👤 John Doe                              │ │
│ │ john.doe@gmail.com                       │ │
│ │ ✓ Active                                 │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ 👤 Jane Smith                            │ │
│ │ jane.smith@gmail.com                     │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│     [Add Account]  [Close]                   │
└──────────────────────────────────────────────┘
```

- **Green border** = Currently active account
- **Click any account** to switch
- **Add Account button** = Add new account
- **ESC or Close** = Cancel

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `a` | Open account switcher |
| `↑/↓` | Navigate accounts (in switcher) |
| `Enter` | Select account |
| `Esc` | Close account switcher |

## How It Works

### Account Storage

Each account is stored separately:

```
~/.config/yt-tui/
├── accounts.json           # Account metadata
├── token_johndoe.json      # John's OAuth token
├── token_janesmith.json    # Jane's OAuth token
└── client_secret.json      # Your API credentials
```

### Account Information Stored

For each account:
- **Email**: Your Google/YouTube email
- **Name**: Display name
- **Token**: OAuth2 credentials (secure, encrypted)
- **Active status**: Which account is currently active

### Switching Mechanism

When you switch accounts:
1. App updates active account flag
2. Loads that account's OAuth token
3. Creates new YouTube API service
4. Updates all screens with new API
5. Refreshes current view

Everything happens instantly - no app restart needed!

## Use Cases

### Personal and Work Accounts

```
Personal: john.personal@gmail.com
Work:     john.work@company.com
```

Switch between them seamlessly!

### Family Shared Computer

```
Dad:      dad@gmail.com
Mom:      mom@gmail.com
Kid:      kid@gmail.com
```

Each family member has their own subscriptions and playlists!

### Content Creators

```
Main Channel:   creator@gmail.com
Second Channel: creator.gaming@gmail.com
Personal:       creator.personal@gmail.com
```

Manage multiple channels easily!

## Managing Accounts

### View All Accounts

Press `a` to see all your accounts at any time.

### Remove an Account

Currently, you can remove accounts by:

```bash
# Edit accounts file
nano ~/.config/yt-tui/accounts.json

# Or delete specific token
rm ~/.config/yt-tui/token_accountname.json
```

(GUI removal coming in future update!)

### Switch Active Account

The last selected account becomes active and will be used when you restart the app.

## Troubleshooting

### "Account switching not available"

**Cause**: App started without account manager.

**Solution**: Restart the app:
```bash
python main.py
```

### Account not switching

**Cause**: Credentials expired or invalid.

**Solution**:
1. Try removing and re-adding the account
2. Delete token file: `rm ~/.config/yt-tui/token_*.json`
3. Re-authenticate

### Can't add new account

**Cause**: OAuth flow interrupted or failed.

**Solution**:
1. Make sure browser opens successfully
2. Check internet connection
3. Verify client_secret.json is valid
4. Try again

### Wrong account showing

**Cause**: Account state not saved properly.

**Solution**:
```bash
# Check accounts file
cat ~/.config/yt-tui/accounts.json

# Look for "is_active": true
# Only one should be active
```

### Account credentials invalid

**Cause**: Token expired or corrupted.

**Solution**:
```bash
# Delete the specific token
rm ~/.config/yt-tui/token_accountname.json

# Switch to that account in app
# It will re-authenticate automatically
```

## Technical Details

### OAuth Scopes

Multi-account requires additional scopes:
```python
'https://www.googleapis.com/auth/userinfo.email'
'https://www.googleapis.com/auth/userinfo.profile'
```

These allow the app to identify your account (name and email) for display purposes.

### Security

- Each account's token is stored separately
- Tokens are encrypted by Google's libraries
- No passwords are stored
- OAuth2 is secure and standard
- Tokens can be revoked at: https://myaccount.google.com/permissions

### Backwards Compatibility

If you were using YT-TUI before multi-account support:
- Your existing token will continue to work
- On first run with new version, it migrates automatically
- Or simply add as a new account

## API Quota

**Important**: Each account has its own API quota, but they all share the same Google Cloud Project quota.

If you have:
- 3 accounts
- Each searches 50 times

That's **15,000 units total** from your project's daily 10,000 limit!

**Tip**: Use Trending tab (no quota cost) when possible.

## Best Practices

1. **Name Recognition**: Use clear, distinct names for accounts
2. **Primary Account**: Keep your most-used account as primary
3. **Quota Awareness**: Remember searches cost quota
4. **Regular Switching**: Don't forget which account you're on!
5. **Token Backup**: Back up `~/.config/yt-tui/` occasionally

## Future Enhancements

Planned features:
- 🔄 GUI account removal
- 📊 Per-account usage statistics
- 🎨 Account-specific themes
- 🔔 Notifications per account
- 📝 Account nicknames/labels
- 🔄 Auto-switch on startup

## FAQ

**Q: How many accounts can I add?**
A: No hard limit, but we recommend 3-5 for usability.

**Q: Do I need separate API credentials for each account?**
A: No! One `client_secret.json` works for all accounts.

**Q: Will my subscriptions/playlists mix between accounts?**
A: No, each account is completely separate.

**Q: Can I use the same account on multiple computers?**
A: Yes! Just authenticate on each computer.

**Q: Is this secure?**
A: Yes, uses standard OAuth2, same as YouTube website.

**Q: Can I export my accounts?**
A: Copy `~/.config/yt-tui/` directory to backup/transfer.

## Examples

### Quick Account Switch

```
Current: john@gmail.com (watching gaming videos)
Press 'a'
Select: jane@gmail.com
Now viewing Jane's subscriptions!
```

### Adding Work Account

```
1. Press 'a'
2. Click "Add Account"
3. Browser opens
4. Sign in: work@company.com
5. Done! Work account added
```

### Family Usage

```
Dad starts app → Sees his subscriptions
Presses 'a' → Switches to kid's account
Kid watches videos → Dad switches back later
```

## Support

Having issues with multi-account?
- Check TROUBLESHOOTING.md
- Verify token files exist
- Check accounts.json format
- Try re-authenticating

---

**Enjoy seamless account switching!** 🔄👥
