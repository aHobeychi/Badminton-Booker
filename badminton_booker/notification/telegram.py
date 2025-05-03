#!/usr/bin/env python3
"""Telegram notification module for badminton booker."""

import requests
import os
from dotenv import load_dotenv
from badminton_booker.datastore.chat_id_service import fetch_chat_ids_from_firestore

# Load environment variables from .env file if it exists
load_dotenv()

# Telegram bot configuration - get from environment variables
token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
chat_ids = fetch_chat_ids_from_firestore()


def send_notification(message=None):
    """Send a notification message via Telegram Bot API

    Args:
        message (str): Message to send. If None, a test message will be sent.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if message is None:
            message = "🔔 Test Message: Badminton notification system is working!"

        # Create the Telegram API URL
        url = f"https://api.telegram.org/bot{token}/sendMessage"

        for chat_id in chat_ids:
            # Request parameters
            params = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}

            # Send HTTP request to Telegram Bot API
            response = requests.post(url, params=params)

            # Check if request was successful
            if response.status_code == 200:
                print("Notification sent successfully!")
            else:
                print(
                    f"Failed to send notification. Status code: {response.status_code}"
                )
                print(f"Response: {response.json()}")

    except Exception as e:
        print(f"Failed to send notification: {e}")
        return False


def notify_about_reservations(reservations_data):
    """Send notification about available badminton reservations

    Args:
        reservations_data (dict): Dictionary containing reservation data

    Returns:
        bool: True if a notification was sent, False otherwise
    """
    try:
        # Extract reservations and filter for bookable ones
        reservations = reservations_data.get("reservations", [])
        bookable_reservations = [
            res for res in reservations if res.get("canReserve", False)
        ]

        # If no bookable reservations, do nothing and return False
        if not bookable_reservations:
            print("No bookable reservations found to notify about.")
            return False

        # Build message with available bookable reservations
        message = "🏸 <b>Badminton Reservations Available:</b>\n\n"

        for i, res in enumerate(bookable_reservations, 1):
            message += f"{i}. <b>{res.get('name', 'Unknown Location')}</b>\n"
            message += f"   📅 {res.get('date', 'No date')} {res.get('startTime', '')} - {res.get('endTime', '')}\n"
            message += f"   💰 ${res.get('price', 'N/A')}\n\n"

        # Include URL if available
        url = reservations_data.get("url", "")
        if url:
            message += f"\n🔗 <a href='{url}'>Book Now</a>"

        # Send the notification with bookable reservations
        return send_notification(message)

    except Exception as e:
        print(f"Error creating notification: {e}")
        return False

