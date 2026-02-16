"""Configuration management for YT-TUI."""
import os
import json
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path.home() / ".config" / "yt-tui"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
TOKEN_FILE = CONFIG_DIR / "token.json"
CLIENT_SECRET_FILE = CONFIG_DIR / "client_secret.json"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "results_per_page": 25,
    "last_section": "search",
    "max_results": 50
}


def ensure_config_dir():
    """Ensure the configuration directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """Load configuration from file or return defaults."""
    ensure_config_dir()

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return {**DEFAULT_CONFIG, **config}
        except (json.JSONDecodeError, IOError):
            pass

    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    """Save configuration to file."""
    ensure_config_dir()

    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"Error saving config: {e}")


def get_client_secret_path() -> Optional[Path]:
    """Get the path to the client secret file."""
    # Check environment variable first
    env_path = os.getenv("YOUTUBE_CLIENT_SECRET")
    if env_path and Path(env_path).exists():
        return Path(env_path)

    # Check default location
    if CLIENT_SECRET_FILE.exists():
        return CLIENT_SECRET_FILE

    return None
