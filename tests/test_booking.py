"""Tests for the booking module."""

import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from datetime import datetime, timedelta
import json
import os
from badminton_booker.booking.courts import (
    generate_selected_date, 
    generate_available_booking_list,
    select_time_on_page,
    check_available_courts
)


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
        mock_now = datetime(2025, 5, 15)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        # Execute
        dates = generate_selected_date()
        
        # Assert
        expected_dates = []
        for i in range(4):
            date = mock_now + timedelta(days=i)
            expected_dates.append(date.strftime("%d"))
            
        self.assertEqual(dates, expected_dates)

    def test_generate_available_booking_list(self):
        """Test generating booking list from reservation elements."""
        # This is an async test, so we need to run it in an event loop
        result = asyncio.run(self._test_generate_booking_list_async())
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Test Court')
        self.assertTrue(result[0]['canReserve'])
        self.assertEqual(result[0]['price'], '15.00')

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
        
        # Mock reserve button - return button classes WITHOUT "disabled" to make canReserve=True
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

    def test_generate_available_booking_list_disabled(self):
        """Test generating booking list with disabled reserve button."""
        result = asyncio.run(self._test_generate_booking_list_disabled_async())
        self.assertEqual(len(result), 1)
        self.assertFalse(result[0]['canReserve'])

    async def _test_generate_booking_list_disabled_async(self):
        """Async test helper for generate_available_booking_list with disabled button."""
        element = AsyncMock()
        
        # Basic element setup
        name_elem = AsyncMock()
        name_elem.text_content.return_value = "Test Court"
        
        date_elem1 = AsyncMock()
        date_elem1.text_content.return_value = "Monday, May 15, 18:00"
        date_elem2 = AsyncMock()
        date_elem2.text_content.return_value = "19:00"
        
        price_elem = AsyncMock()
        price_elem.text_content.return_value = "$15.00"
        
        # Mock reserve button WITH "disabled" class
        reserve_button = AsyncMock()
        reserve_button.get_attribute.side_effect = ["btn btn-primary disabled", "reserve-btn-1"]
        
        element.query_selector_all.side_effect = [
            [date_elem1, date_elem2],
            [price_elem]
        ]
        
        def query_selector_side_effect(selector):
            if '.panel-heading .fake-link' in selector:
                return name_elem
            elif 'button[ng-click*="vm.onReserve"]' in selector:
                return reserve_button
            return None
        
        element.query_selector.side_effect = query_selector_side_effect
        
        result = await generate_available_booking_list([element])
        return result

    def test_generate_available_booking_list_missing_elements(self):
        """Test generating booking list with missing elements."""
        result = asyncio.run(self._test_generate_booking_list_missing_elements_async())
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], '')
        self.assertIsNone(result[0]['startTime'])
        self.assertIsNone(result[0]['endTime'])

    async def _test_generate_booking_list_missing_elements_async(self):
        """Async test helper for generate_available_booking_list with missing elements."""
        element = AsyncMock()
        
        # Return None for name element
        element.query_selector.return_value = None
        
        # Empty arrays for date and price elements
        element.query_selector_all.side_effect = [[], []]
        
        result = await generate_available_booking_list([element])
        return result
        
    async def _test_check_available_courts_async(self, mock_playwright, mock_generate_dates, mock_generate_list, mock_select_time):
        """Async test helper for check_available_courts."""
        # Create mock objects
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
        mock_context = AsyncMock()
        mock_playwright_instance = AsyncMock()
        
        # Mock the reservation elements
        mock_elements = [AsyncMock(), AsyncMock()]
        mock_page.query_selector_all.return_value = mock_elements
        
        # Mock dates
        mock_generate_dates.return_value = ["15", "16", "17", "18"]
        
        # Mock URL
        mock_page.url = "https://example.com/booking"
        
        # Configure mock for generate_available_booking_list
        sample_reservations = [
            {
                'name': 'Court 1',
                'date': 'May 15, 2025',
                'startTime': datetime(2025, 5, 15, 18, 0),
                'endTime': datetime(2025, 5, 15, 19, 0),
                'price': '15.00',
                'canReserve': True,
                'buttonId': 'btn-1'
            },
            {
                'name': 'Court 2',
                'date': 'May 15, 2025',
                'startTime': datetime(2025, 5, 15, 19, 0),
                'endTime': datetime(2025, 5, 15, 20, 0),
                'price': '20.00',
                'canReserve': False,
                'buttonId': 'btn-2'
            }
        ]
        mock_generate_list.return_value = sample_reservations
        
        # Setup the playwright mock chain
        mock_playwright.return_value.__aenter__.return_value = mock_playwright_instance
        mock_playwright_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page
        
        # Mock the locator for calendar button
        mock_calendar_button = AsyncMock()
        mock_page.locator.return_value.nth.return_value = mock_calendar_button
        
        # Mock the locator for date buttons
        mock_date_buttons = [AsyncMock(), AsyncMock()]
        mock_page.locator.return_value.all.return_value = mock_date_buttons
        
        # Create args mock
        args = MagicMock()
        args.headless = True
        args.slow = 0
        args.test = False
        
        # Execute
        result = await check_available_courts(args)
        
        # Verify the basic calls were made
        mock_playwright.assert_called_once()
        mock_browser.new_page.assert_called_once()
        mock_page.goto.assert_called_once_with("https://example.com")
        mock_select_time.assert_called_once_with(mock_page)
        mock_browser.close.assert_called_once()
        
        return result

    @patch('badminton_booker.booking.courts.async_playwright')
    @patch.dict(os.environ, {"NEIGHBORHOODS": "Test1,Test2"})
    def test_check_available_courts_missing_url(self, mock_playwright):
        """Test checking available courts with missing URL."""
        args = MagicMock()
        args.headless = True
        args.slow = 0
        args.test = False
        
        # Remove BOOKING_URL from environment
        with patch.dict(os.environ, {}, clear=True):
            result = asyncio.run(check_available_courts(args))
            self.assertIsNone(result)

    async def test_select_time_on_page(self):
        """Test selecting time on the page."""
        # Create mock page
        page = AsyncMock()
        
        # Create mock locators
        start_time_hh = AsyncMock()
        start_time_mm = AsyncMock()
        end_time_hh = AsyncMock()
        
        # Setup page.locator to return correct mock based on selector
        def mock_locator_side_effect(selector):
            if selector == '#u6510_edFacilityReservationSearchStartTime':
                mock_locator = AsyncMock()
                mock_locator.get_by_role.side_effect = lambda role, name: start_time_hh if name == 'HH' else start_time_mm
                return mock_locator
            elif selector == '#u6510_edFacilityReservationSearchEndTime':
                mock_locator = AsyncMock()
                mock_locator.get_by_role.return_value = end_time_hh
                return mock_locator
            return AsyncMock()
        
        page.locator.side_effect = mock_locator_side_effect
        
        # Execute
        await select_time_on_page(page)
        
        # Verify the correct methods were called with proper arguments
        start_time_hh.click.assert_called()
        start_time_hh.fill.assert_called_with('18')
        start_time_mm.click.assert_called()
        start_time_mm.fill.assert_called_with('00')
        end_time_hh.click.assert_called()
        end_time_hh.fill.assert_called_with('22')
        end_time_hh.press.assert_called_with('Enter')


if __name__ == '__main__':
    unittest.main()