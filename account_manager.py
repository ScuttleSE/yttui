"""Account management for multiple YouTube accounts."""
import json
import pickle
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

from config import CONFIG_DIR, get_client_secret_path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

ACCOUNTS_FILE = CONFIG_DIR / "accounts.json"


@dataclass
class Account:
    """Represents a YouTube account."""
    id: str
    email: str
    name: str
    token_file: str
    is_active: bool = False


class AccountManager:
    """Manages multiple YouTube accounts."""

    def __init__(self):
        """Initialize account manager."""
        self.accounts: List[Account] = []
        self.load_accounts()

    def load_accounts(self):
        """Load accounts from file."""
        if ACCOUNTS_FILE.exists():
            try:
                with open(ACCOUNTS_FILE, 'r') as f:
                    data = json.load(f)
                    self.accounts = [Account(**acc) for acc in data]
            except (json.JSONDecodeError, IOError):
                self.accounts = []
        else:
            self.accounts = []

    def save_accounts(self):
        """Save accounts to file."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with open(ACCOUNTS_FILE, 'w') as f:
                json.dump([asdict(acc) for acc in self.accounts], f, indent=2)
        except IOError as e:
            print(f"Error saving accounts: {e}")

    def get_active_account(self) -> Optional[Account]:
        """Get the currently active account."""
        for account in self.accounts:
            if account.is_active:
                return account
        return None

    def get_all_accounts(self) -> List[Account]:
        """Get all accounts."""
        return self.accounts

    def add_account(self, email: str, name: str, credentials: Credentials) -> Account:
        """Add a new account."""
        import logging
        from pathlib import Path

        # Setup debug logging
        log_file = Path.home() / '.config' / 'yt-tui' / 'account_debug.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=str(log_file),
            level=logging.DEBUG,
            format='%(asctime)s - %(message)s'
        )
        logger = logging.getLogger(__name__)

        try:
            logger.info(f"=== ADD ACCOUNT DEBUG ===")
            logger.info(f"Email: {email}")
            logger.info(f"Name: {name}")
            logger.info(f"Credentials type: {type(credentials)}")
            logger.info(f"Credentials valid: {credentials.valid if hasattr(credentials, 'valid') else 'N/A'}")

            # Generate unique ID
            account_id = email.split('@')[0].replace('.', '_')
            logger.info(f"Generated account_id: {account_id}")

            # Check if account already exists
            existing = self.get_account_by_email(email)
            logger.info(f"Existing account found: {existing is not None}")

            if existing:
                # Update existing account
                token_file = existing.token_file
                logger.info(f"Using existing token_file: {token_file}")
            else:
                # Create new token file
                token_file = f"token_{account_id}.json"
                logger.info(f"Creating new token_file: {token_file}")

            # Save credentials
            token_path = CONFIG_DIR / token_file
            logger.info(f"Token path: {token_path}")
            logger.info(f"CONFIG_DIR exists: {CONFIG_DIR.exists()}")

            try:
                with open(token_path, 'wb') as f:
                    pickle.dump(credentials, f)
                logger.info(f"Credentials saved successfully")
                logger.info(f"Token file size: {token_path.stat().st_size} bytes")
            except Exception as e:
                logger.error(f"Failed to save credentials: {type(e).__name__}: {e}")
                import traceback
                logger.error(traceback.format_exc())
                raise

            # Create or update account
            account = Account(
                id=account_id,
                email=email,
                name=name,
                token_file=token_file,
                is_active=False
            )
            logger.info(f"Created Account object: {account}")

            if existing:
                # Update existing
                logger.info(f"Updating existing account in list")
                for i, acc in enumerate(self.accounts):
                    if acc.email == email:
                        self.accounts[i] = account
                        logger.info(f"Updated account at index {i}")
                        break
            else:
                # Add new
                logger.info(f"Appending new account to list")
                logger.info(f"Current accounts count: {len(self.accounts)}")
                self.accounts.append(account)
                logger.info(f"New accounts count: {len(self.accounts)}")

            logger.info(f"Saving accounts to file")
            self.save_accounts()
            logger.info(f"Accounts saved successfully")
            logger.info(f"===================\n")

            return account

        except Exception as e:
            logger.error(f"add_account failed with exception: {type(e).__name__}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def remove_account(self, account_id: str) -> bool:
        """Remove an account."""
        for i, account in enumerate(self.accounts):
            if account.id == account_id:
                # Delete token file
                token_path = CONFIG_DIR / account.token_file
                if token_path.exists():
                    token_path.unlink()

                # Remove from list
                self.accounts.pop(i)
                self.save_accounts()
                return True
        return False

    def switch_account(self, account_id: str) -> bool:
        """Switch to a different account."""
        found = False
        for account in self.accounts:
            if account.id == account_id:
                account.is_active = True
                found = True
            else:
                account.is_active = False

        if found:
            self.save_accounts()
        return found

    def get_account_by_email(self, email: str) -> Optional[Account]:
        """Get account by email."""
        for account in self.accounts:
            if account.email == email:
                return account
        return None

    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        """Get account by ID."""
        for account in self.accounts:
            if account.id == account_id:
                return account
        return None

    def get_credentials(self, account: Account) -> Optional[Credentials]:
        """Get credentials for an account."""
        token_path = CONFIG_DIR / account.token_file
        if not token_path.exists():
            return None

        try:
            with open(token_path, 'rb') as f:
                creds = pickle.load(f)

            # Check if scopes match current requirements
            if creds and creds.scopes:
                # Normalize scopes for comparison (Google may add/reorder scopes)
                current_scopes = set(SCOPES)
                token_scopes = set(creds.scopes)

                # Both should have the same scopes (allowing for Google's auto-additions)
                # Check if all required scopes are present
                required_scopes = {
                    'https://www.googleapis.com/auth/youtube.readonly',
                    'https://www.googleapis.com/auth/youtube.force-ssl',
                    'https://www.googleapis.com/auth/userinfo.email',
                    'https://www.googleapis.com/auth/userinfo.profile'
                }

                if not required_scopes.issubset(token_scopes):
                    print(f"Token missing required scopes. Deleting old token...")
                    print(f"  Required: {sorted(required_scopes)}")
                    print(f"  Got: {sorted(token_scopes)}")
                    # Delete incompatible token
                    token_path.unlink()
                    return None

            # Refresh if expired
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    # Save refreshed credentials
                    with open(token_path, 'wb') as f:
                        pickle.dump(creds, f)
                except Exception as e:
                    print(f"Failed to refresh credentials: {e}")
                    # Delete failed token
                    if token_path.exists():
                        token_path.unlink()
                    return None

            return creds
        except (pickle.PickleError, IOError, Exception) as e:
            print(f"Error loading credentials: {e}")
            # Delete corrupted token
            if token_path.exists():
                token_path.unlink()
            return None

    def authenticate_new_account(self) -> Optional[tuple[Account, Credentials]]:
        """Authenticate a new account."""
        import logging
        from pathlib import Path

        # Setup debug logging
        log_file = Path.home() / '.config' / 'yt-tui' / 'account_debug.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=str(log_file),
            level=logging.DEBUG,
            format='%(asctime)s - %(message)s'
        )
        logger = logging.getLogger(__name__)

        logger.info(f"=== AUTHENTICATE NEW ACCOUNT ===")

        client_secret = get_client_secret_path()
        logger.info(f"Client secret path: {client_secret}")

        if not client_secret:
            logger.error("No client secret found")
            return None

        try:
            logger.info(f"Creating OAuth flow with scopes: {SCOPES}")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(client_secret), SCOPES
            )
            logger.info("OAuth flow created, starting local server...")

            creds = flow.run_local_server(port=0)
            logger.info("OAuth flow completed successfully")
            logger.info(f"Credentials obtained: valid={creds.valid}, expired={creds.expired}")
            logger.info(f"Credentials scopes: {creds.scopes if hasattr(creds, 'scopes') else 'N/A'}")

            # Get user info
            logger.info("Getting user info from OAuth2 API...")
            from googleapiclient.discovery import build
            oauth2_service = build('oauth2', 'v2', credentials=creds)
            user_info = oauth2_service.userinfo().get().execute()
            logger.info(f"User info received: {user_info}")

            email = user_info.get('email', 'unknown@email.com')
            name = user_info.get('name', email.split('@')[0])
            logger.info(f"Extracted - Email: {email}, Name: {name}")

            # Add account
            logger.info("Calling add_account...")
            account = self.add_account(email, name, creds)
            logger.info(f"add_account returned: {account}")

            logger.info("===================\n")
            return account, creds

        except Exception as e:
            logger.error(f"Authentication failed: {type(e).__name__}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            print(f"Authentication failed: {e}")
            return None

    def has_accounts(self) -> bool:
        """Check if any accounts exist."""
        return len(self.accounts) > 0

    def ensure_active_account(self) -> Optional[Account]:
        """Ensure there's an active account, set first one if none active."""
        active = self.get_active_account()
        if active:
            return active

        if self.accounts:
            self.accounts[0].is_active = True
            self.save_accounts()
            return self.accounts[0]

        return None
