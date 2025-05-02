#!/usr/bin/env python3
"""Firestore and chat ID updating module."""

import os
import requests
import logging
from typing import List, Dict
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
import firebase_admin

# Load environment variables
load_dotenv()

# Load Firebase certificate path from environment variable
firebase_cert_path = os.environ.get("FIREBASE_CERT_PATH", "firebase_service_account.json")
cred = credentials.Certificate(firebase_cert_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def validate_env_vars(required_vars: List[str]) -> None:
    """Validate that all required environment variables are set."""
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")



def fetch_chat_info_from_telegram_api() -> List[Dict[str, str]]:
    """
    Fetch chat info (chat ID and name) from Telegram API.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing chatId and name.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        chat_info = {}
        for result in data.get("result", []):
            message = result.get("message")
            if message and "chat" in message and "id" in message["chat"]:
                chat_id = message["chat"]["id"]
                first_name = message["chat"].get("first_name", "")
                last_name = message["chat"].get("last_name", "")
                name = (first_name + " " + last_name).strip()
                chat_info[chat_id] = {"chatId": str(chat_id), "name": name}
        return [chat_info[k] for k in sorted(chat_info.keys())]
    except requests.RequestException as e:
        logging.error(f"Failed to fetch chat info from Telegram API: {e}")
        raise

def fetch_chat_ids_from_firestore() -> List[str]:
    """
    Fetch chat IDs from Firestore.

    Returns:
        List[str]: A list of chat IDs.
    """
    try:
        chat_ids = []
        docs = db.collection("chat_ids").stream()
        for doc in docs:
            chat_ids.append(doc.id)
        return chat_ids
    except Exception as e:
        logging.error(f"Failed to fetch chat IDs from Firestore: {e}")
        raise

def update_chat_ids_in_firestore(chat_info: List[Dict[str, str]]) -> None:
    """
    Update chat IDs in Firestore.

    Args:
        chat_info (List[Dict[str, str]]): List of chat info dictionaries to update in Firestore.
    """
    try:
        batch = db.batch()
        for chat in chat_info:
            doc_ref = db.collection("chat_ids").document(chat["chatId"])
            batch.set(doc_ref, chat)
        batch.commit()
        logging.info(f"Successfully updated {len(chat_info)} chat IDs in Firestore.")
    except Exception as e:
        logging.error(f"Failed to update chat IDs in Firestore: {e}")
        raise


def main() -> None:
    """Main function to fetch and update chat IDs. Will run from the Github Action."""
    try:
        # Validate required environment variables
        validate_env_vars(["TELEGRAM_BOT_TOKEN"])

        # Fetch chat info from Telegram API
        chat_info = fetch_chat_info_from_telegram_api()
        logging.info(f"Fetched {len(chat_info)} chat IDs from Telegram API.")

        # Update chat IDs in Firestore
        update_chat_ids_in_firestore(chat_info)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()