"""Test configuration for the badminton-booker tests."""

import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up environment variables for testing."""
    os.environ.setdefault("BOOKING_URL", "https://example.com/booking")
