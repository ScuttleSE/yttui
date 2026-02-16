#!/usr/bin/env python3
"""Add an account manually using OAuth tokens."""
import pickle
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from account_manager import AccountManager, SCOPES
from config import CONFIG_DIR


def add_account_with_tokens(
    access_token: str,
    refresh_token: str,
    client_id: str,
    client_secret: str,
    token_uri: str = "https://oauth2.googleapis.com/token"
):
    """
    Add an account using manually obtained OAuth tokens.

    Args:
        access_token: The access token
        refresh_token: The refresh token
        client_id: Your OAuth client ID
        client_secret: Your OAuth client secret
        token_uri: OAuth token URI (default is Google's)
    """
    print("Creating credentials object...")

    # Create credentials object
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri=token_uri,
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES
    )

    print("Testing credentials by fetching user info...")

    try:
        # Get user info to verify credentials work
        oauth2_service = build('oauth2', 'v2', credentials=creds)
        user_info = oauth2_service.userinfo().get().execute()

        email = user_info.get('email', 'unknown@email.com')
        name = user_info.get('name', email.split('@')[0])

        print(f"✓ Credentials valid!")
        print(f"  Email: {email}")
        print(f"  Name: {name}")

        # Add to account manager
        print("\nAdding account to account manager...")
        account_manager = AccountManager()
        account = account_manager.add_account(email, name, creds)

        print(f"✓ Account added successfully!")
        print(f"  Account ID: {account.id}")
        print(f"  Token file: {account.token_file}")
        print(f"\nYou can now use this account in the app by pressing 'a' to switch accounts.")

        return account

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_client_credentials():
    """Get client ID and secret from client_secrets.json."""
    import json
    from config import get_client_secret_path

    client_secret_path = get_client_secret_path()
    if not client_secret_path:
        print("Error: client_secrets.json not found")
        return None, None

    with open(client_secret_path, 'r') as f:
        data = json.load(f)
        client_id = data['installed']['client_id']
        client_secret = data['installed']['client_secret']
        return client_id, client_secret


if __name__ == "__main__":
    print("=== Manual Account Addition ===\n")

    # Get client credentials from client_secrets.json
    client_id, client_secret = get_client_credentials()

    if not client_id:
        print("Failed to get client credentials")
        exit(1)

    print("Enter your OAuth tokens:")
    print("(These should be from the brand account OAuth flow)\n")

    access_token = input("Access token: ").strip()
    refresh_token = input("Refresh token: ").strip()

    if not access_token or not refresh_token:
        print("Error: Both tokens are required")
        exit(1)

    print(f"\nUsing client_id: {client_id[:20]}...")
    print(f"Using client_secret: {client_secret[:10]}...")

    result = add_account_with_tokens(
        access_token=access_token,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret
    )

    if result:
        print("\n✓ Success! Your brand account is now available in the app.")
    else:
        print("\n✗ Failed to add account.")
