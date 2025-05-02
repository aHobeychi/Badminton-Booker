#!/usr/bin/env python3
"""
Badminton Booker - Entry point for the badminton court booking application.
"""

import asyncio
import sys
from badminton_booker.cli.commands import parse_args
from badminton_booker.booking.courts import check_available_courts
from badminton_booker.notification.telegram import notify_about_reservations
from badminton_booker.config.settings import get_settings


async def main():
    """Main application entry point."""
    # Get settings and validate
    settings = get_settings()
    errors = settings.validate()
    if errors:
        print("Configuration errors detected:")
        for error in errors:
            print(f"  - {error}")
        print(
            "\nPlease check your .env file and set the required environment variables."
        )
        sys.exit(1)

    # Parse command line arguments
    args = parse_args()

    # Check for available courts
    results = await check_available_courts(args)

    # if results is empty, exit
    if not results:
        print("No available reservations found.")
        return

    # Notify about results if any were found and notifications are not muted
    if results and not args.mute:
        print("Sending notification...")
        notify_about_reservations(results)
    elif results and args.mute:
        print("Notifications are muted. Skipping notification.")


if __name__ == "__main__":
    asyncio.run(main())
