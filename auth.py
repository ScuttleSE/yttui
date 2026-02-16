"""OAuth2 authentication for YouTube API with multi-account support."""
import os
import pickle
from pathlib import Path
from typing import Optional, Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import TOKEN_FILE, get_client_secret_path, CONFIG_DIR
from account_manager import AccountManager, Account

# OAuth2 scopes required for the app
# Note: 'openid' is automatically added by Google when requesting userinfo scopes
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass


def get_authenticated_service(account_manager: Optional[AccountManager] = None):
    """
    Authenticate with YouTube API using OAuth2 with multi-account support.

    Args:
        account_manager: Optional AccountManager instance for multi-account support

    Returns:
        Tuple of (YouTube API service object, Account or None)

    Raises:
        AuthenticationError: If authentication fails.
    """
    # Use multi-account system if available
    if account_manager:
        return get_authenticated_service_multi_account(account_manager)

    # Fallback to legacy single-account system
    return get_authenticated_service_legacy(), None


def get_authenticated_service_multi_account(account_manager: AccountManager) -> Tuple:
    """
    Authenticate using multi-account system.

    Args:
        account_manager: AccountManager instance

    Returns:
        Tuple of (YouTube API service, Account)

    Raises:
        AuthenticationError: If authentication fails.
    """
    # Get active account
    account = account_manager.ensure_active_account()

    if account:
        # Try to use existing credentials
        creds = account_manager.get_credentials(account)
        if creds and creds.valid:
            # Check if scopes match
            if creds.scopes and set(creds.scopes) != set(SCOPES):
                print(f"Warning: Token scopes changed, need to re-authenticate...")
                # Scopes changed, need to re-authenticate
                creds = None
            else:
                try:
                    service = build('youtube', 'v3', credentials=creds)
                    return service, account
                except Exception as e:
                    print(f"Failed to build service with existing creds: {e}")
                    creds = None

    # No valid account or scopes changed, need to authenticate
    try:
        result = account_manager.authenticate_new_account()
        if not result:
            raise AuthenticationError("Failed to authenticate new account")

        account, creds = result

        # Set as active
        account_manager.switch_account(account.id)

        service = build('youtube', 'v3', credentials=creds)
        return service, account
    except Exception as e:
        raise AuthenticationError(f"Failed to authenticate new account: {e}")


def get_authenticated_service_legacy():
    """
    Legacy single-account authentication (backwards compatibility).

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


def is_authenticated(account_manager: Optional[AccountManager] = None) -> bool:
    """
    Check if user is authenticated.

    Args:
        account_manager: Optional AccountManager for multi-account check

    Returns:
        True if authenticated, False otherwise
    """
    if account_manager:
        account = account_manager.get_active_account()
        if not account:
            return False
        creds = account_manager.get_credentials(account)
        return creds is not None and creds.valid

    # Legacy check
    if not TOKEN_FILE.exists():
        return False

    try:
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
            return creds and creds.valid
    except (pickle.PickleError, IOError):
        return False


def clear_credentials():
    """Clear saved credentials (legacy)."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
