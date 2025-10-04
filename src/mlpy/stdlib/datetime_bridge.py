"""Python bridge implementations for ML datetime module.

The datetime module provides date and time manipulation capabilities.
When imported in ML code as 'import datetime;', it creates a 'datetime' object with
methods for date/time operations.

Usage in ML:
    import datetime;

    // Get current datetime
    now = datetime.now();
    year = now.year();

    // Create specific datetime
    dt = datetime.create(2024, 1, 15, 10, 30);

    // Add time
    future = dt.addDays(7);
    timestamp = future.timestamp();
"""

import calendar
import datetime as _dt  # Use underscore to avoid naming collision with ML 'datetime' object
from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_class(description="Date and time object with manipulation methods")
class DateTimeObject:
    """Date and time object for ML code.

    This class represents a specific point in time and provides methods
    for querying and manipulating dates.
    """

    def __init__(self, dt_obj: _dt.datetime):
        """Create a DateTimeObject from Python datetime.

        Args:
            dt_obj: Python datetime object
        """
        self._dt = dt_obj

    @ml_function(description="Get Unix timestamp")
    def timestamp(self) -> float:
        """Get Unix timestamp (seconds since epoch).

        Returns:
            Unix timestamp as float
        """
        return self._dt.timestamp()

    @ml_function(description="Get year component")
    def year(self) -> int:
        """Get the year.

        Returns:
            Year as integer (e.g., 2024)
        """
        return self._dt.year

    @ml_function(description="Get month component")
    def month(self) -> int:
        """Get the month.

        Returns:
            Month as integer (1-12)
        """
        return self._dt.month

    @ml_function(description="Get day component")
    def day(self) -> int:
        """Get the day of month.

        Returns:
            Day as integer (1-31)
        """
        return self._dt.day

    @ml_function(description="Get hour component")
    def hour(self) -> int:
        """Get the hour.

        Returns:
            Hour as integer (0-23)
        """
        return self._dt.hour

    @ml_function(description="Get minute component")
    def minute(self) -> int:
        """Get the minute.

        Returns:
            Minute as integer (0-59)
        """
        return self._dt.minute

    @ml_function(description="Get second component")
    def second(self) -> int:
        """Get the second.

        Returns:
            Second as integer (0-59)
        """
        return self._dt.second

    @ml_function(description="Get weekday")
    def weekday(self) -> int:
        """Get the day of week.

        Returns:
            Weekday as integer (0=Monday, 6=Sunday)
        """
        return self._dt.weekday()

    @ml_function(description="Add days to datetime")
    def addDays(self, days: int) -> 'DateTimeObject':
        """Add days to this datetime.

        Args:
            days: Number of days to add (can be negative)

        Returns:
            New DateTimeObject with days added
        """
        new_dt = self._dt + _dt.timedelta(days=days)
        return DateTimeObject(new_dt)

    @ml_function(description="Add hours to datetime")
    def addHours(self, hours: int) -> 'DateTimeObject':
        """Add hours to this datetime.

        Args:
            hours: Number of hours to add (can be negative)

        Returns:
            New DateTimeObject with hours added
        """
        new_dt = self._dt + _dt.timedelta(hours=hours)
        return DateTimeObject(new_dt)

    @ml_function(description="Add minutes to datetime")
    def addMinutes(self, minutes: int) -> 'DateTimeObject':
        """Add minutes to this datetime.

        Args:
            minutes: Number of minutes to add (can be negative)

        Returns:
            New DateTimeObject with minutes added
        """
        new_dt = self._dt + _dt.timedelta(minutes=minutes)
        return DateTimeObject(new_dt)

    @ml_function(description="Add seconds to datetime")
    def addSeconds(self, seconds: int) -> 'DateTimeObject':
        """Add seconds to this datetime.

        Args:
            seconds: Number of seconds to add (can be negative)

        Returns:
            New DateTimeObject with seconds added
        """
        new_dt = self._dt + _dt.timedelta(seconds=seconds)
        return DateTimeObject(new_dt)

    @ml_function(description="Get start of day")
    def startOfDay(self) -> 'DateTimeObject':
        """Get datetime at start of this day (00:00:00).

        Returns:
            New DateTimeObject at start of day
        """
        start = self._dt.replace(hour=0, minute=0, second=0, microsecond=0)
        return DateTimeObject(start)

    @ml_function(description="Get end of day")
    def endOfDay(self) -> 'DateTimeObject':
        """Get datetime at end of this day (23:59:59).

        Returns:
            New DateTimeObject at end of day
        """
        end = self._dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        return DateTimeObject(end)

    @ml_function(description="Get start of month")
    def startOfMonth(self) -> 'DateTimeObject':
        """Get datetime at start of this month.

        Returns:
            New DateTimeObject at start of month
        """
        start = self._dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return DateTimeObject(start)

    @ml_function(description="Get end of month")
    def endOfMonth(self) -> 'DateTimeObject':
        """Get datetime at end of this month.

        Returns:
            New DateTimeObject at end of month
        """
        last_day = calendar.monthrange(self._dt.year, self._dt.month)[1]
        end = self._dt.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)
        return DateTimeObject(end)

    @ml_function(description="Get start of year")
    def startOfYear(self) -> 'DateTimeObject':
        """Get datetime at start of this year.

        Returns:
            New DateTimeObject at start of year
        """
        start = self._dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        return DateTimeObject(start)

    @ml_function(description="Get end of year")
    def endOfYear(self) -> 'DateTimeObject':
        """Get datetime at end of this year.

        Returns:
            New DateTimeObject at end of year
        """
        end = self._dt.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        return DateTimeObject(end)

    @ml_function(description="Check if same day as another datetime")
    def isSameDay(self, other: 'DateTimeObject') -> bool:
        """Check if this is on the same day as another datetime.

        Args:
            other: DateTimeObject to compare with

        Returns:
            True if same day, False otherwise
        """
        return self._dt.date() == other._dt.date()

    @ml_function(description="Format datetime as string")
    def format(self, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format datetime as string.

        Args:
            format_str: Python strftime format string (default: "%Y-%m-%d %H:%M:%S")

        Returns:
            Formatted datetime string
        """
        return self._dt.strftime(format_str)

    @ml_function(description="Get string representation")
    def toString(self) -> str:
        """Get string representation of datetime.

        Returns:
            ISO format datetime string
        """
        return self._dt.isoformat()

    # Snake_case aliases for convenience
    @ml_function(description="Add days (snake_case alias)")
    def add_days(self, days: int) -> 'DateTimeObject':
        """Alias for addDays()."""
        return self.addDays(days)

    @ml_function(description="Add hours (snake_case alias)")
    def add_hours(self, hours: int) -> 'DateTimeObject':
        """Alias for addHours()."""
        return self.addHours(hours)

    @ml_function(description="Add minutes (snake_case alias)")
    def add_minutes(self, minutes: int) -> 'DateTimeObject':
        """Alias for addMinutes()."""
        return self.addMinutes(minutes)

    @ml_function(description="Add seconds (snake_case alias)")
    def add_seconds(self, seconds: int) -> 'DateTimeObject':
        """Alias for addSeconds()."""
        return self.addSeconds(seconds)

    @ml_function(description="Start of day (snake_case alias)")
    def start_of_day(self) -> 'DateTimeObject':
        """Alias for startOfDay()."""
        return self.startOfDay()

    @ml_function(description="End of day (snake_case alias)")
    def end_of_day(self) -> 'DateTimeObject':
        """Alias for endOfDay()."""
        return self.endOfDay()

    @ml_function(description="Start of month (snake_case alias)")
    def start_of_month(self) -> 'DateTimeObject':
        """Alias for startOfMonth()."""
        return self.startOfMonth()

    @ml_function(description="End of month (snake_case alias)")
    def end_of_month(self) -> 'DateTimeObject':
        """Alias for endOfMonth()."""
        return self.endOfMonth()

    @ml_function(description="Start of year (snake_case alias)")
    def start_of_year(self) -> 'DateTimeObject':
        """Alias for startOfYear()."""
        return self.startOfYear()

    @ml_function(description="End of year (snake_case alias)")
    def end_of_year(self) -> 'DateTimeObject':
        """Alias for endOfYear()."""
        return self.endOfYear()

    @ml_function(description="Same day check (snake_case alias)")
    def is_same_day(self, other: 'DateTimeObject') -> bool:
        """Alias for isSameDay()."""
        return self.isSameDay(other)

    @ml_function(description="String representation (snake_case alias)")
    def to_string(self) -> str:
        """Alias for toString()."""
        return self.toString()


@ml_module(
    name="datetime",
    description="Date and time manipulation with timezone support",
    capabilities=["datetime.create", "datetime.now"],
    version="1.0.0"
)
class DateTime:
    """DateTime module interface for ML code.

    This class provides the main API for date and time operations in ML.
    Methods return DateTimeObject instances for further manipulation.
    """

    @ml_function(description="Get current datetime", capabilities=["datetime.now"])
    def now(self) -> DateTimeObject:
        """Get current date and time.

        Returns:
            DateTimeObject representing current moment

        Example:
            now = datetime.now();
            year = now.year();
            month = now.month();
        """
        return DateTimeObject(_dt.datetime.now())

    @ml_function(description="Create datetime from components", capabilities=["datetime.create"])
    def create(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0
    ) -> DateTimeObject:
        """Create datetime from year, month, day, and optional time components.

        Args:
            year: Year (e.g., 2024)
            month: Month (1-12)
            day: Day of month (1-31)
            hour: Hour (0-23, default 0)
            minute: Minute (0-59, default 0)
            second: Second (0-59, default 0)

        Returns:
            DateTimeObject for specified date/time

        Raises:
            RuntimeError: If date components are invalid

        Example:
            dt = datetime.create(2024, 12, 25, 10, 30);
            timestamp = dt.timestamp();
        """
        try:
            dt_obj = _dt.datetime(year, month, day, hour, minute, second)
            return DateTimeObject(dt_obj)
        except ValueError as e:
            raise RuntimeError(f"Invalid datetime components: {e}")

    @ml_function(description="Create datetime from timestamp", capabilities=["datetime.create"])
    def fromTimestamp(self, timestamp: float) -> DateTimeObject:
        """Create datetime from Unix timestamp.

        Args:
            timestamp: Unix timestamp (seconds since epoch)

        Returns:
            DateTimeObject for specified timestamp

        Raises:
            RuntimeError: If timestamp is invalid
        """
        try:
            dt_obj = _dt.datetime.fromtimestamp(timestamp)
            return DateTimeObject(dt_obj)
        except (ValueError, OSError) as e:
            raise RuntimeError(f"Invalid timestamp {timestamp}: {e}")

    @ml_function(description="Get days in month")
    def daysInMonth(self, year: int, month: int) -> int:
        """Get number of days in a specific month.

        Args:
            year: Year (e.g., 2024)
            month: Month (1-12)

        Returns:
            Number of days in month
        """
        try:
            return calendar.monthrange(year, month)[1]
        except ValueError:
            return 0

    @ml_function(description="Calculate age in years", capabilities=["datetime.create"])
    def calculateAge(self, birth_date: DateTimeObject, current_date: DateTimeObject = None) -> int:
        """Calculate age in years between two dates.

        Args:
            birth_date: Birth date as DateTimeObject
            current_date: Current date as DateTimeObject (default: now)

        Returns:
            Age in years
        """
        if current_date is None:
            current_date = self.now()

        birth = birth_date._dt.date()
        current = current_date._dt.date()

        age = current.year - birth.year
        if current.month < birth.month or (current.month == birth.month and current.day < birth.day):
            age -= 1
        return age

    @ml_function(description="Add business days to datetime", capabilities=["datetime.create"])
    def addBusinessDays(self, dt_obj: DateTimeObject, days: int) -> DateTimeObject:
        """Add business days (excludes weekends) to datetime.

        Args:
            dt_obj: Starting DateTimeObject
            days: Number of business days to add (can be negative)

        Returns:
            New DateTimeObject with business days added
        """
        date_obj = dt_obj._dt

        if days == 0:
            return dt_obj

        # Determine direction
        direction = 1 if days > 0 else -1
        days_remaining = abs(days)

        while days_remaining > 0:
            date_obj += _dt.timedelta(days=direction)
            # Check if it's a weekday (Monday=0, Sunday=6)
            if date_obj.weekday() < 5:  # Monday to Friday
                days_remaining -= 1

        return DateTimeObject(date_obj)

    @ml_function(description="Count business days between dates")
    def businessDaysBetween(self, start: DateTimeObject, end: DateTimeObject) -> int:
        """Count business days between two dates.

        Args:
            start: Start DateTimeObject
            end: End DateTimeObject

        Returns:
            Number of business days between dates
        """
        start_date = start._dt.date()
        end_date = end._dt.date()

        # Ensure start is before end
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        business_days = 0
        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() < 5:  # Monday to Friday
                business_days += 1
            current_date += _dt.timedelta(days=1)

        return business_days

    @ml_function(description="Check if date is weekend")
    def isWeekend(self, dt_obj: DateTimeObject) -> bool:
        """Check if datetime is on a weekend.

        Args:
            dt_obj: DateTimeObject to check

        Returns:
            True if weekend (Saturday or Sunday), False otherwise
        """
        return dt_obj._dt.weekday() >= 5

    @ml_function(description="Check if date is weekday")
    def isWeekday(self, dt_obj: DateTimeObject) -> bool:
        """Check if datetime is on a weekday.

        Args:
            dt_obj: DateTimeObject to check

        Returns:
            True if weekday (Monday-Friday), False otherwise
        """
        return dt_obj._dt.weekday() < 5

    # Snake_case aliases for backward compatibility
    @ml_function(description="Create datetime (snake_case alias)", capabilities=["datetime.create"])
    def from_timestamp(self, timestamp: float) -> DateTimeObject:
        """Alias for fromTimestamp()."""
        return self.fromTimestamp(timestamp)

    @ml_function(description="Days in month (snake_case alias)")
    def days_in_month(self, year: int, month: int) -> int:
        """Alias for daysInMonth()."""
        return self.daysInMonth(year, month)

    @ml_function(description="Calculate age (snake_case alias)", capabilities=["datetime.create"])
    def calculate_age(self, birth_date: DateTimeObject, current_date: DateTimeObject = None) -> int:
        """Alias for calculateAge()."""
        return self.calculateAge(birth_date, current_date)

    @ml_function(description="Add business days (snake_case alias)", capabilities=["datetime.create"])
    def add_business_days(self, dt_obj: DateTimeObject, days: int) -> DateTimeObject:
        """Alias for addBusinessDays()."""
        return self.addBusinessDays(dt_obj, days)

    @ml_function(description="Business days between (snake_case alias)")
    def business_days_between(self, start: DateTimeObject, end: DateTimeObject) -> int:
        """Alias for businessDaysBetween()."""
        return self.businessDaysBetween(start, end)

    @ml_function(description="Check weekend (snake_case alias)")
    def is_weekend(self, dt_obj: DateTimeObject) -> bool:
        """Alias for isWeekend()."""
        return self.isWeekend(dt_obj)

    @ml_function(description="Check weekday (snake_case alias)")
    def is_weekday(self, dt_obj: DateTimeObject) -> bool:
        """Alias for isWeekday()."""
        return self.isWeekday(dt_obj)


# Create global datetime instance for ML import
# When ML code does 'import datetime;', this creates the 'datetime' object
datetime = DateTime()

# Export public API
__all__ = [
    "DateTime",
    "DateTimeObject",
    "datetime",
]
