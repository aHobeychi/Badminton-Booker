#!/usr/bin/env python3
# notify.py - Python version of the Telegram notification script
# You can get chat_id from curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates"

import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Telegram bot configuration - get from environment variables with fallback to hardcoded values
token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')

def send_notification(message=None):
    """Send a notification message via Telegram Bot API
    
    Args:
        message (str): Message to send. If None, a test message will be sent.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if message is None:
            message = '🔔 Test Message: Badminton notification system is working!'
        
        # Create the Telegram API URL
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        
        # Request parameters
        params = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        # Send HTTP request to Telegram Bot API
        response = requests.post(url, params=params)
        
        # Check if request was successful
        if response.status_code == 200:
            print('Notification sent successfully!')
            return True
        else:
            print(f'Failed to send notification. Status code: {response.status_code}')
            print(f'Response: {response.json()}')
            return False
            
    except Exception as e:
        print(f'Failed to send notification: {e}')
        return False


def notify_about_reservations(reservations_data):
    """Send notification about available badminton reservations
    
    Args:
        reservations_data (dict): Dictionary containing reservation data
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if there are any reservations
        reservations = reservations_data.get('reservations', [])
        
        if not reservations:
            message = "❌ No badminton reservations found."
            return send_notification(message)
        
        # Build message with available reservations
        message = "🏸 <b>Badminton Reservations Available:</b>\n\n"
        
        for i, res in enumerate(reservations, 1):
            # Only include reservations that can be booked
            if res.get('canReserve', False):
                message += f"{i}. <b>{res.get('name', 'Unknown Location')}</b>\n"
                message += f"   📅 {res.get('date', 'No date')} {res.get('startTime', '')} - {res.get('endTime', '')}\n"
                message += f"   💰 ${res.get('price', 'N/A')}\n\n"
        
        # Include URL if available
        url = reservations_data.get('url', '')
        if url:
            message += f"\n🔗 <a href='{url}'>Book Now</a>"
            
        return send_notification(message)
        
    except Exception as e:
        print(f"Error creating notification: {e}")
        return False


if __name__ == "__main__":
    send_notification()