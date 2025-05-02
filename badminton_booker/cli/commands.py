#!/usr/bin/env python3
"""Command line interface for badminton booker."""

import argparse


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Badminton court booking automation")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("-slow", type=int, default=10, help="Slow mode delay in milliseconds")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    parser.add_argument("--mute", action="store_true", help="Disable notifications (do not send Telegram message)")
    return parser.parse_args()