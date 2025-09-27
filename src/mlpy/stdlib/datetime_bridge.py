"""Python bridge implementations for ML datetime module."""

import calendar
import datetime as dt


def create_datetime_timestamp(
    year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0
) -> float:
    """Create datetime timestamp from components."""
    try:
        date_obj = dt.datetime(year, month, day, hour, minute, second)
        return date_obj.timestamp()
    except ValueError:
        return 0.0


def add_timedelta(timestamp: float, days: int = 0, hours: int = 0, minutes: int = 0) -> float:
    """Add time delta to timestamp."""
    try:
        date_obj = dt.datetime.fromtimestamp(timestamp)
        delta = dt.timedelta(days=days, hours=hours, minutes=minutes)
        new_date = date_obj + delta
        return new_date.timestamp()
    except (ValueError, OSError):
        return timestamp


def start_of_day(timestamp: float) -> float:
    """Get timestamp for start of day."""
    try:
        date_obj = dt.datetime.fromtimestamp(timestamp)
        start = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp()
    except (ValueError, OSError):
        return timestamp


def end_of_day(timestamp: float) -> float:
    """Get timestamp for end of day."""
    try:
        date_obj = dt.datetime.fromtimestamp(timestamp)
        end = date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)
        return end.timestamp()
    except (ValueError, OSError):
        return timestamp


def start_of_month(timestamp: float) -> float:
    """Get timestamp for start of month."""
    try:
        date_obj = dt.datetime.fromtimestamp(timestamp)
        start = date_obj.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp()
    except (ValueError, OSError):
        return timestamp


def end_of_month(timestamp: float) -> float:
    """Get timestamp for end of month."""
    try:
        date_obj = dt.datetime.fromtimestamp(timestamp)
        last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
        end = date_obj.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)
        return end.timestamp()
    except (ValueError, OSError):
        return timestamp


def start_of_year(timestamp: float) -> float:
    """Get timestamp for start of year."""
    try:
        date_obj = dt.datetime.fromtimestamp(timestamp)
        start = date_obj.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp()
    except (ValueError, OSError):
        return timestamp


def end_of_year(timestamp: float) -> float:
    """Get timestamp for end of year."""
    try:
        date_obj = dt.datetime.fromtimestamp(timestamp)
        end = date_obj.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        return end.timestamp()
    except (ValueError, OSError):
        return timestamp


def days_in_month(year: int, month: int) -> int:
    """Get number of days in a month."""
    try:
        return calendar.monthrange(year, month)[1]
    except ValueError:
        return 0


def calculate_age_years(birth_timestamp: float, current_timestamp: float) -> int:
    """Calculate age in years."""
    try:
        birth_date = dt.datetime.fromtimestamp(birth_timestamp).date()
        current_date = dt.datetime.fromtimestamp(current_timestamp).date()

        age = current_date.year - birth_date.year
        if current_date.month < birth_date.month or (
            current_date.month == birth_date.month and current_date.day < birth_date.day
        ):
            age -= 1
        return age
    except (ValueError, OSError):
        return 0


def is_same_day(timestamp1: float, timestamp2: float) -> bool:
    """Check if two timestamps are on the same day."""
    try:
        date1 = dt.datetime.fromtimestamp(timestamp1).date()
        date2 = dt.datetime.fromtimestamp(timestamp2).date()
        return date1 == date2
    except (ValueError, OSError):
        return False


def add_business_days(timestamp: float, days: int) -> float:
    """Add business days to timestamp (excludes weekends)."""
    try:
        date_obj = dt.datetime.fromtimestamp(timestamp)

        if days == 0:
            return timestamp

        # Determine direction
        direction = 1 if days > 0 else -1
        days = abs(days)

        while days > 0:
            date_obj += dt.timedelta(days=direction)
            # Check if it's a weekday (Monday=0, Sunday=6)
            if date_obj.weekday() < 5:  # Monday to Friday
                days -= 1

        return date_obj.timestamp()
    except (ValueError, OSError):
        return timestamp


def business_days_between(start_timestamp: float, end_timestamp: float) -> int:
    """Count business days between two timestamps."""
    try:
        start_date = dt.datetime.fromtimestamp(start_timestamp).date()
        end_date = dt.datetime.fromtimestamp(end_timestamp).date()

        # Ensure start is before end
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        business_days = 0
        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() < 5:  # Monday to Friday
                business_days += 1
            current_date += dt.timedelta(days=1)

        return business_days
    except (ValueError, OSError):
        return 0


def convert_timezone(timestamp: float, from_tz: str, to_tz: str) -> float:
    """Convert timestamp between timezones."""
    # This is a simplified implementation
    # In a full implementation, you'd use pytz or zoneinfo
    try:
        date_obj = dt.datetime.fromtimestamp(timestamp)
        # For now, just return the same timestamp
        # A full implementation would handle timezone conversion
        return date_obj.timestamp()
    except (ValueError, OSError):
        return timestamp


class DateTime:
    """DateTime module interface for ML compatibility."""

    @staticmethod
    def createTimestamp(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> float:
        """Create a timestamp from date components."""
        return create_datetime_timestamp(year, month, day, hour, minute, second)

    @staticmethod
    def addTimedelta(timestamp: float, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> float:
        """Add time delta to timestamp."""
        return add_timedelta(timestamp, days, hours, minutes, seconds)

    @staticmethod
    def startOfDay(timestamp: float) -> float:
        """Get start of day for timestamp."""
        return start_of_day(timestamp)

    @staticmethod
    def endOfDay(timestamp: float) -> float:
        """Get end of day for timestamp."""
        return end_of_day(timestamp)

    @staticmethod
    def startOfMonth(timestamp: float) -> float:
        """Get start of month for timestamp."""
        return start_of_month(timestamp)

    @staticmethod
    def endOfMonth(timestamp: float) -> float:
        """Get end of month for timestamp."""
        return end_of_month(timestamp)

    @staticmethod
    def startOfYear(timestamp: float) -> float:
        """Get start of year for timestamp."""
        return start_of_year(timestamp)

    @staticmethod
    def endOfYear(timestamp: float) -> float:
        """Get end of year for timestamp."""
        return end_of_year(timestamp)

    @staticmethod
    def daysInMonth(timestamp: float) -> int:
        """Get number of days in month."""
        return days_in_month(timestamp)

    @staticmethod
    def calculateAgeYears(birth_timestamp: float, current_timestamp: float = None) -> int:
        """Calculate age in years."""
        return calculate_age_years(birth_timestamp, current_timestamp)

    @staticmethod
    def isSameDay(timestamp1: float, timestamp2: float) -> bool:
        """Check if two timestamps are on the same day."""
        return is_same_day(timestamp1, timestamp2)

    @staticmethod
    def addBusinessDays(timestamp: float, days: int) -> float:
        """Add business days to timestamp."""
        return add_business_days(timestamp, days)

    @staticmethod
    def businessDaysBetween(start_timestamp: float, end_timestamp: float) -> int:
        """Calculate business days between timestamps."""
        return business_days_between(start_timestamp, end_timestamp)

    @staticmethod
    def convertTimezone(timestamp: float, from_tz: str, to_tz: str) -> float:
        """Convert timestamp between timezones."""
        return convert_timezone(timestamp, from_tz, to_tz)


# Create global datetime instance for ML compatibility
datetime = DateTime()

# Export all bridge functions
__all__ = [
    "datetime",
    "create_datetime_timestamp",
    "add_timedelta",
    "start_of_day",
    "end_of_day",
    "start_of_month",
    "end_of_month",
    "start_of_year",
    "end_of_year",
    "days_in_month",
    "calculate_age_years",
    "is_same_day",
    "add_business_days",
    "business_days_between",
    "convert_timezone",
]
