#!/usr/bin/env python3
"""Configuration handling module for badminton booker."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Settings:
    """Settings class to manage configuration."""

    def __init__(self):
        """Initialize settings from environment variables."""
        self.telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        self.telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
        self.neighborhoods = [
            n.strip() for n in os.environ.get('NEIGHBORHOODS', '').split(',')
        ]
        self.booking_url = os.environ.get('BOOKING_URL', '')
        self.data_dir = Path('data')
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(exist_ok=True)
        
    def validate(self):
        """Validate settings and provide helpful error messages."""
        errors = []
        
        if not self.telegram_bot_token:
            errors.append("TELEGRAM_BOT_TOKEN is not set")
        
        if not self.telegram_chat_id:
            errors.append("TELEGRAM_CHAT_ID is not set")
            
        if not self.neighborhoods or (len(self.neighborhoods) == 1 and not self.neighborhoods[0]):
            errors.append("NEIGHBORHOODS is not set")
            
        if not self.booking_url:
            errors.append("BOOKING_URL is not set")
        
        return errors


# Create a global instance of Settings
settings = Settings()


def get_settings():
    """Get the settings instance."""
    return settings


if __name__ == "__main__":
    # Print current settings when run directly
    s = get_settings()
    print("Current settings:")
    print(f"- Telegram Bot Token: {'*' * 10 if s.telegram_bot_token else 'Not set'}")
    print(f"- Telegram Chat ID: {s.telegram_chat_id or 'Not set'}")
    print(f"- Neighborhoods: {', '.join(s.neighborhoods) or 'Not set'}")
    print(f"- Booking URL: {s.booking_url or 'Not set'}")
    
    # Validate settings
    errors = s.validate()
    if errors:
        print("\nConfiguration errors:")
        for error in errors:
            print(f"- {error}")
    else:
        print("\nAll required settings are configured correctly.")