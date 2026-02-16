#!/usr/bin/env python3
"""
Migration script to clean up old tokens when upgrading to multi-account.
Run this if you're getting scope mismatch errors.
"""
import sys
from pathlib import Path
from config import CONFIG_DIR, TOKEN_FILE

def migrate_tokens():
    """Clean up old tokens that may have incompatible scopes."""
    print("YT-TUI Token Migration")
    print("=" * 50)
    print()

    # Check for old single-account token
    if TOKEN_FILE.exists():
        print(f"Found old token: {TOKEN_FILE}")
        response = input("Delete old token? (y/n): ")
        if response.lower() == 'y':
            TOKEN_FILE.unlink()
            print("✓ Deleted old token")
        else:
            print("Skipped")
    else:
        print("No old single-account token found")

    print()

    # Check for multi-account tokens
    if CONFIG_DIR.exists():
        token_files = list(CONFIG_DIR.glob("token_*.json"))
        if token_files:
            print(f"Found {len(token_files)} account token(s):")
            for token_file in token_files:
                print(f"  - {token_file.name}")
            print()
            response = input("Delete all account tokens? (y/n): ")
            if response.lower() == 'y':
                for token_file in token_files:
                    token_file.unlink()
                    print(f"✓ Deleted {token_file.name}")
            else:
                print("Skipped")
        else:
            print("No multi-account tokens found")

    print()
    print("=" * 50)
    print("Migration complete!")
    print()
    print("Next steps:")
    print("1. Run: python main.py")
    print("2. Authenticate when prompted")
    print("3. Your account will be added with correct scopes")
    print()

if __name__ == "__main__":
    try:
        migrate_tokens()
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)
