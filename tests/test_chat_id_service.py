import os
import pytest
from unittest.mock import patch, MagicMock
from badminton_booker.datastore.chat_id_service import (
    validate_env_vars,
    fetch_chat_info_from_telegram_api,
    fetch_chat_ids_from_firestore,
    update_chat_ids_in_firestore
)

# Mock environment variables
@patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "mock_token"})
def test_validate_env_vars():
    # Test with required environment variable present
    validate_env_vars(["TELEGRAM_BOT_TOKEN"])

    # Test with missing environment variable
    with pytest.raises(EnvironmentError):
        validate_env_vars(["MISSING_ENV_VAR"])

@patch("requests.get")
def test_fetch_chat_info_from_telegram_api(mock_get):
    # Mock Telegram API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "result": [
            {
                "message": {
                    "chat": {
                        "id": 12345,
                        "first_name": "John",
                        "last_name": "Doe"
                    }
                }
            }
        ]
    }
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    chat_info = fetch_chat_info_from_telegram_api()
    assert len(chat_info) == 1
    assert chat_info[0]["chatId"] == "12345"
    assert chat_info[0]["name"] == "John Doe"

# Patch the 'db' object directly in the module where it's used
@patch("badminton_booker.datastore.chat_id_service.db")
def test_fetch_chat_ids_from_firestore(mock_db):
    # Mock Firestore collection and stream
    mock_db.collection.return_value.stream.return_value = [
        MagicMock(id="12345"),
        MagicMock(id="67890")
    ]

    chat_ids = fetch_chat_ids_from_firestore()
    assert chat_ids == ["12345", "67890"]

# Patch the 'db' object directly in the module where it's used
@patch("badminton_booker.datastore.chat_id_service.db")
def test_update_chat_ids_in_firestore(mock_db):
    # Mock Firestore batch and commit operations
    mock_batch = MagicMock()
    mock_db.batch.return_value = mock_batch

    chat_info = [
        {"chatId": "12345", "name": "John Doe"},
        {"chatId": "67890", "name": "Jane Smith"}
    ]

    update_chat_ids_in_firestore(chat_info)
    assert mock_batch.set.call_count == 2
    mock_batch.commit.assert_called_once()
