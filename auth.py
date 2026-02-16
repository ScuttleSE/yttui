"""OAuth2 authentication for YouTube API."""
import os
import pickle
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import TOKEN_FILE, get_client_secret_path

# OAuth2 scopes required for the app
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass


def get_authenticated_service():
    """
    Authenticate with YouTube API using OAuth2.

    Returns:
        Authenticated YouTube API service object.

    Raises:
        AuthenticationError: If authentication fails.
    """
    creds = None

    # Load existing credentials
    if TOKEN_FILE.exists():
        try:
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        except (pickle.PickleError, IOError) as e:
            print(f"Error loading credentials: {e}")

    # If credentials are invalid or don't exist, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                raise AuthenticationError(f"Failed to refresh token: {e}")
        else:
            # Get client secret file
            client_secret = get_client_secret_path()
            if not client_secret:
                raise AuthenticationError(
                    "Client secret file not found. Please place client_secret.json "
                    f"in {TOKEN_FILE.parent} or set YOUTUBE_CLIENT_SECRET environment variable."
                )

            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(client_secret), SCOPES
                )
                creds = flow.run_local_server(port=0)
            except Exception as e:
                raise AuthenticationError(f"OAuth2 flow failed: {e}")

        # Save credentials for next run
        try:
            TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        except IOError as e:
            print(f"Warning: Could not save credentials: {e}")

    try:
        return build('youtube', 'v3', credentials=creds)
    except Exception as e:
        raise AuthenticationError(f"Failed to build YouTube service: {e}")


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    if not TOKEN_FILE.exists():
        return False

    try:
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
            return creds and creds.valid
    except (pickle.PickleError, IOError):
        return False


def clear_credentials():
    """Clear saved credentials."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
