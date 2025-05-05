"""Tests for the notification module."""

import unittest
from unittest.mock import patch, MagicMock
from badminton_booker.notification.telegram import send_notification, notify_about_reservations


class TestNotification(unittest.TestCase):
    """Test cases for the notification module."""

    @patch('badminton_booker.notification.telegram.requests.post')
    def test_send_notification_success(self, mock_post):
        """Test sending a notification with success response."""
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ok": True}
        mock_post.return_value = mock_response
        
        # Execute
        send_notification("Test message")
        
        # Assert
        mock_post.assert_called()
    
    @patch('badminton_booker.notification.telegram.requests.post')
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
    

if __name__ == '__main__':
    unittest.main()