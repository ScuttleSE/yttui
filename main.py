#!/usr/bin/env python3
"""
YT-TUI - YouTube Terminal User Interface
A TUI client for browsing YouTube in the terminal.
"""
import sys
from pathlib import Path

from auth import get_authenticated_service, AuthenticationError, is_authenticated
from youtube_api import YouTubeAPI
from ui.app import YouTubeApp
from config import ensure_config_dir, get_client_secret_path
from account_manager import AccountManager


def print_setup_instructions():
    """Print OAuth2 setup instructions."""
    print("\n" + "=" * 70)
    print("YT-TUI - YouTube Terminal Client")
    print("=" * 70)
    print("\n⚠️  First-time setup required!\n")
    print("To use YT-TUI, you need to set up YouTube API credentials:\n")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a new project (or select an existing one)")
    print("3. Enable the YouTube Data API v3:")
    print("   - Go to 'APIs & Services' > 'Library'")
    print("   - Search for 'YouTube Data API v3'")
    print("   - Click 'Enable'")
    print("4. Create OAuth 2.0 credentials:")
    print("   - Go to 'APIs & Services' > 'Credentials'")
    print("   - Click 'Create Credentials' > 'OAuth client ID'")
    print("   - Choose 'Desktop app' as application type")
    print("   - Give it a name (e.g., 'YT-TUI')")
    print("   - Click 'Create'")
    print("5. Download the credentials:")
    print("   - Click the download icon next to your OAuth client")
    print("   - Save as 'client_secret.json'")
    print(f"6. Place the file in: {get_client_secret_path() or Path.home() / '.config' / 'yt-tui' / 'client_secret.json'}")
    print("\nAlternatively, set the YOUTUBE_CLIENT_SECRET environment variable")
    print("to the path of your client_secret.json file.\n")
    print("After setup, run this command again to authenticate.\n")
    print("=" * 70 + "\n")


def main():
    """Main entry point."""
    # Ensure config directory exists
    ensure_config_dir()

    # Check if client secret exists
    client_secret = get_client_secret_path()
    if not client_secret:
        print_setup_instructions()
        sys.exit(1)

    print("Authenticating with YouTube...")
    print("A browser window will open for authentication if needed.\n")

    try:
        # Initialize account manager
        account_manager = AccountManager()

        # Authenticate and get YouTube service
        youtube_service, account = get_authenticated_service(account_manager)
        youtube_api = YouTubeAPI(youtube_service)

        print("✓ Authentication successful!")
        if account:
            print(f"✓ Logged in as: {account.name} ({account.email})")
        print("Starting YT-TUI...\n")

        # Run the app with account manager
        app = YouTubeApp(youtube_api, account_manager)
        app.run()

    except AuthenticationError as e:
        print(f"\n❌ Authentication failed: {e}")
        print("\nPlease check your credentials and try again.")
        print("If the problem persists, delete the token file and re-authenticate:")
        print(f"  rm {Path.home() / '.config' / 'yt-tui' / 'token.json'}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
