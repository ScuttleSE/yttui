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
        # Generate unique ID
        account_id = email.split('@')[0].replace('.', '_')

        # Check if account already exists
        existing = self.get_account_by_email(email)
        if existing:
            # Update existing account
            token_file = existing.token_file
        else:
            # Create new token file
            token_file = f"token_{account_id}.json"

        # Save credentials
        token_path = CONFIG_DIR / token_file
        with open(token_path, 'wb') as f:
            pickle.dump(credentials, f)

        # Create or update account
        account = Account(
            id=account_id,
            email=email,
            name=name,
            token_file=token_file,
            is_active=False
        )

        if existing:
            # Update existing
            for i, acc in enumerate(self.accounts):
                if acc.email == email:
                    self.accounts[i] = account
                    break
        else:
            # Add new
            self.accounts.append(account)

        self.save_accounts()
        return account

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

            # Refresh if expired
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    # Save refreshed credentials
                    with open(token_path, 'wb') as f:
                        pickle.dump(creds, f)
                except Exception as e:
                    print(f"Failed to refresh credentials: {e}")
                    return None

            return creds
        except (pickle.PickleError, IOError):
            return None

    def authenticate_new_account(self) -> Optional[tuple[Account, Credentials]]:
        """Authenticate a new account."""
        client_secret = get_client_secret_path()
        if not client_secret:
            return None

        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(client_secret), SCOPES
            )
            creds = flow.run_local_server(port=0)

            # Get user info
            from googleapiclient.discovery import build
            oauth2_service = build('oauth2', 'v2', credentials=creds)
            user_info = oauth2_service.userinfo().get().execute()

            email = user_info.get('email', 'unknown@email.com')
            name = user_info.get('name', email.split('@')[0])

            # Add account
            account = self.add_account(email, name, creds)

            return account, creds

        except Exception as e:
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
