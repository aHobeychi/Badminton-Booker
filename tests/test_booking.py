"""Tests for the booking module."""

import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from datetime import datetime
from badminton_booker.booking.courts import generate_selected_date, generate_available_booking_list


class TestBooking(unittest.TestCase):
    """Test cases for the booking module."""

    def test_generate_selected_date(self):
        """Test generating selected dates."""
        # Execute
        dates = generate_selected_date()
        
        # Assert
        self.assertEqual(len(dates), 4)
        for date in dates:
            self.assertIsInstance(date, str)
            self.assertEqual(len(date), 2)

    @patch('badminton_booker.booking.courts.datetime')
    def test_generate_selected_date_with_specific_date(self, mock_datetime):
        """Test generating selected dates with a specific date."""
        # Setup
        mock_date = MagicMock()
        mock_date.strftime.return_value = "15"
        mock_datetime.now.return_value = datetime(2025, 5, 15)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        # Execute
        dates = generate_selected_date()
        
        # Assert
        self.assertEqual(dates, ["15", "16", "17", "18"])

    def test_generate_available_booking_list(self):
        """Test generating booking list from reservation elements."""
        # This is an async test, so we need to run it in an event loop
        result = asyncio.run(self._test_generate_booking_list_async())
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Test Court')
        self.assertTrue(result[0]['canReserve'])

    async def _test_generate_booking_list_async(self):
        """Async test helper for generate_available_booking_list."""
        # Setup mock reservation element
        element = AsyncMock()
        
        # Mock name element
        name_elem = AsyncMock()
        name_elem.text_content.return_value = "Test Court"
        
        # Mock date elements
        date_elem1 = AsyncMock()
        date_elem1.text_content.return_value = "Monday, May 15, 18:00"
        date_elem2 = AsyncMock()
        date_elem2.text_content.return_value = "19:00"
        
        # Mock price element
        price_elem = AsyncMock()
        price_elem.text_content.return_value = "$15.00"
        
        # Mock reserve button - CRUCIAL FIX: return button classes WITHOUT "disabled" to make canReserve=True
        reserve_button = AsyncMock()
        reserve_button.get_attribute.side_effect = ["btn btn-primary", "reserve-btn-1"]
        
        # Configure query_selector_all to return the correct values for different calls
        element.query_selector_all.side_effect = [
            [date_elem1, date_elem2],  # For date elements
            [price_elem]               # For price elements
        ]
        
        # Ensure query_selector is called with the right parameters and returns the expected values
        def query_selector_side_effect(selector):
            if '.panel-heading .fake-link' in selector:
                return name_elem
            elif 'button[ng-click*="vm.onReserve"]' in selector:
                return reserve_button
            return None
        
        element.query_selector.side_effect = query_selector_side_effect
        
        # Execute
        result = await generate_available_booking_list([element])
        return result


if __name__ == '__main__':
    unittest.main()