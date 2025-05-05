"""Badminton court booking and availability checking module."""

from datetime import datetime
from zoneinfo import ZoneInfo


french_months = {
    'janvier': 'January',
    'février': 'February',
    'mars': 'March',
    'avril': 'April',
    'mai': 'May',
    'juin': 'June',
    'juillet': 'July',
    'août': 'August',
    'septembre': 'September',
    'octobre': 'October',
    'novembre': 'November',
    'décembre': 'December',
}

def generate_time_object(date_str: str, time_str: str) -> datetime:
    """Generate a datetime object from date and time strings."""
    # Convert French month to English
    for fr_month, en_month in french_months.items():
        if fr_month in date_str.lower():
            date_str = date_str.lower().replace(fr_month, en_month)
            break

    # Parse the date and time strings
    date_time_str = f"{date_str} {time_str}"
    
    # Handle different date formats
    try:
        # Try with full format first (day, month, year)
        return datetime.strptime(date_time_str, "%d %B %Y %H:%M").astimezone()
    except ValueError:
        # If no year in the string, use current year
        current_year = datetime.now().year
        try:
            dt = datetime.strptime(f"{date_time_str} {current_year}", "%d %B %H:%M %Y").astimezone()
            return dt
        except ValueError:
            # Handle other variations
            if "," in date_time_str:
                # Format like "May 15, 18:00"
                parts = date_time_str.split(",")
                month_day = parts[0].strip()
                time_part = parts[1].strip()
                return datetime.strptime(f"{month_day} {current_year} {time_part}", "%B %d %Y %H:%M").astimezone()
            else:
                # Try month day format
                return datetime.strptime(f"{date_time_str} {current_year}", "%B %d %H:%M %Y").astimezone()

def convert_to_proper_timezone(time: datetime) -> datetime:
    """Convert time to the proper timezone."""
    return time.astimezone(ZoneInfo("America/New_York"))

