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
        result = send_notification("Test message")
        
        # Assert
        self.assertTrue(result)
        mock_post.assert_called_once()
    
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
    
    @patch('badminton_booker.notification.telegram.send_notification')
    def test_notify_about_reservations_with_data(self, mock_send):
        """Test notifying about reservations with valid data."""
        # Setup
        mock_send.return_value = True
        test_data = {
            'reservations': [
                {
                    'name': 'Test Court',
                    'date': 'May 20',
                    'startTime': '18:00',
                    'endTime': '19:00',
                    'price': '15.00',
                    'canReserve': True
                }
            ],
            'url': 'https://example.com/booking'
        }
        
        # Execute
        result = notify_about_reservations(test_data)
        
        # Assert
        self.assertTrue(result)
        mock_send.assert_called_once()

    @patch('badminton_booker.notification.telegram.send_notification')
    def test_notify_about_empty_reservations(self, mock_send):
        """Test notifying about empty reservations."""
        # Setup
        mock_send.return_value = True
        test_data = {
            'reservations': [],
            'url': 'https://example.com/booking'
        }
        
        # Execute
        result = notify_about_reservations(test_data)
        
        # Assert
        self.assertTrue(result)
        mock_send.assert_called_once()


if __name__ == '__main__':
    unittest.main()