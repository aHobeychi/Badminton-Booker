"""Tests for the notification module."""

import unittest
from unittest.mock import patch, MagicMock, call
from datetime import datetime, timezone
from badminton_booker.notification.telegram import send_notification, notify_about_reservations


class TestNotification(unittest.TestCase):
    """Test cases for the notification module."""

    @patch('badminton_booker.notification.telegram.requests.post')
    @patch('badminton_booker.notification.telegram.token', 'test-token')
    @patch('badminton_booker.notification.telegram.chat_ids', ['123456', '789012'])
    def test_send_notification_success(self, mock_post):
        """Test sending a notification with success response."""
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ok": True}
        mock_post.return_value = mock_response
        
        # Execute
        result = send_notification("Test message")
        
        # Assert
        self.assertTrue(result)
        self.assertEqual(mock_post.call_count, 2)  # Should be called for each chat ID
        
        # Verify correct parameters were used
        expected_url = "https://api.telegram.org/bottest-token/sendMessage"
        expected_calls = [
            call(
                expected_url, 
                params={"chat_id": "123456", "text": "Test message", "parse_mode": "HTML"}
            ),
            call(
                expected_url, 
                params={"chat_id": "789012", "text": "Test message", "parse_mode": "HTML"}
            )
        ]
        mock_post.assert_has_calls(expected_calls, any_order=True)
    
    @patch('badminton_booker.notification.telegram.requests.post')
    @patch('badminton_booker.notification.telegram.chat_ids', ['123456'])
    def test_send_notification_failure(self, mock_post):
        """Test sending a notification with failure response."""
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Bad request"}
        mock_post.return_value = mock_response
        
        # Execute
        result = send_notification("Test message")
        
        # Assert
        self.assertFalse(result)
        mock_post.assert_called_once()

    @patch('badminton_booker.notification.telegram.requests.post')
    @patch('badminton_booker.notification.telegram.chat_ids', ['123456'])
    def test_send_notification_exception(self, mock_post):
        """Test sending a notification that raises an exception."""
        # Setup
        mock_post.side_effect = Exception("Network error")
        
        # Execute
        result = send_notification("Test message")
        
        # Assert
        self.assertFalse(result)
        mock_post.assert_called_once()

    @patch('badminton_booker.notification.telegram.requests.post')
    @patch('badminton_booker.notification.telegram.chat_ids', [])
    def test_send_notification_no_chat_ids(self, mock_post):
        """Test sending a notification with no chat IDs."""
        # Execute
        result = send_notification("Test message")
        
        # Assert
        self.assertTrue(result)  # Function should succeed even if no messages are sent
        mock_post.assert_not_called()

    @patch('badminton_booker.notification.telegram.send_notification')
    def test_notify_about_reservations_with_bookable_courts(self, mock_send):
        """Test notification with bookable reservations."""
        # Setup
        mock_send.return_value = True
        
        test_date = "2025-05-05T18:00:00Z"
        test_end_date = "2025-05-05T19:00:00Z"
        
        reservations_data = {
            "reservations": [
                {
                    "name": "Court A",
                    "startTime": test_date,
                    "endTime": test_end_date,
                    "price": "15.00",
                    "canReserve": True
                },
                {
                    "name": "Court B",
                    "startTime": test_date,
                    "endTime": test_end_date,
                    "price": "20.00",
                    "canReserve": False
                }
            ],
            "timezone": "UTC",
            "url": "https://example.com/booking"
        }
        
        # Execute
        result = notify_about_reservations(reservations_data)
        
        # Assert
        self.assertTrue(result)
        mock_send.assert_called_once()
        # Check that the message contains Court A but not Court B
        message = mock_send.call_args[0][0]
        self.assertIn("Court A", message)
        self.assertIn("$15.00", message)
        self.assertNotIn("Court B", message)
        self.assertIn("https://example.com/booking", message)

    @patch('badminton_booker.notification.telegram.send_notification')
    def test_notify_about_reservations_no_bookable_courts(self, mock_send):
        """Test notification with no bookable reservations."""
        # Setup
        reservations_data = {
            "reservations": [
                {
                    "name": "Court A",
                    "startTime": "2025-05-05T18:00:00Z",
                    "endTime": "2025-05-05T19:00:00Z",
                    "price": "15.00",
                    "canReserve": False
                }
            ],
            "timezone": "UTC"
        }
        
        # Execute
        result = notify_about_reservations(reservations_data)
        
        # Assert
        self.assertFalse(result)
        mock_send.assert_not_called()

    @patch('badminton_booker.notification.telegram.send_notification')
    def test_notify_about_reservations_empty_data(self, mock_send):
        """Test notification with empty reservations data."""
        # Setup
        reservations_data = {
            "reservations": [],
            "timezone": "UTC"
        }
        
        # Execute
        result = notify_about_reservations(reservations_data)
        
        # Assert
        self.assertFalse(result)
        mock_send.assert_not_called()

    @patch('badminton_booker.notification.telegram.send_notification')
    def test_notify_about_reservations_malformed_data(self, mock_send):
        """Test notification with malformed data."""
        # Setup
        reservations_data = {"invalid": "data"}
        
        # Execute
        result = notify_about_reservations(reservations_data)
        
        # Assert
        self.assertFalse(result)
        mock_send.assert_not_called()

if __name__ == '__main__':
    unittest.main()