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

    @ml_function(description="Format as ISO string")
    def toISOString(self) -> str:
        """Format as ISO 8601 string.

        Returns:
            ISO format datetime string
        """
        return self._dt.isoformat()

    @ml_function(description="Extract date component")
    def date(self) -> 'Date':
        """Extract date component (year, month, day).

        Returns:
            Date object with year, month, day
        """
        return Date(self._dt.date())

    @ml_function(description="Extract time component")
    def time(self) -> 'Time':
        """Extract time component (hour, minute, second).

        Returns:
            Time object with hour, minute, second
        """
        return Time(self._dt.time())

    @ml_function(description="Get difference between datetimes")
    def diff(self, other: 'DateTimeObject') -> 'TimeDelta':
        """Get difference between two datetimes as TimeDelta.

        Args:
            other: DateTimeObject to compare with

        Returns:
            TimeDelta representing the difference
        """
        delta = self._dt - other._dt
        return TimeDelta(delta)

    @ml_function(description="Add timedelta to datetime")
    def add(self, delta: 'TimeDelta') -> 'DateTimeObject':
        """Add a timedelta to this datetime.

        Args:
            delta: TimeDelta to add

        Returns:
            New DateTimeObject with delta added
        """
        new_dt = self._dt + delta._delta
        return DateTimeObject(new_dt)

    @ml_function(description="Subtract timedelta from datetime")
    def subtract(self, delta: 'TimeDelta') -> 'DateTimeObject':
        """Subtract a timedelta from this datetime.

        Args:
            delta: TimeDelta to subtract

        Returns:
            New DateTimeObject with delta subtracted
        """
        new_dt = self._dt - delta._delta
        return DateTimeObject(new_dt)

    @ml_function(description="Check if before another datetime")
    def isBefore(self, other: 'DateTimeObject') -> bool:
        """Check if this datetime is before another.

        Args:
            other: DateTimeObject to compare with

        Returns:
            True if this is before other, False otherwise
        """
        return self._dt < other._dt

    @ml_function(description="Check if after another datetime")
    def isAfter(self, other: 'DateTimeObject') -> bool:
        """Check if this datetime is after another.

        Args:
            other: DateTimeObject to compare with

        Returns:
            True if this is after other, False otherwise
        """
        return self._dt > other._dt

    @ml_function(description="Check if same as another datetime")
    def isSame(self, other: 'DateTimeObject') -> bool:
        """Check if this datetime is the same as another.

        Args:
            other: DateTimeObject to compare with

        Returns:
            True if this is the same as other, False otherwise
        """
        return self._dt == other._dt

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


@ml_class(description="Date object representing calendar date")
class Date:
    """Date object for ML code (year, month, day only)."""

    def __init__(self, date_obj: _dt.date):
        self._date = date_obj

    @ml_function(description="Get year")
    def year(self) -> int:
        return self._date.year

    @ml_function(description="Get month")
    def month(self) -> int:
        return self._date.month

    @ml_function(description="Get day")
    def day(self) -> int:
        return self._date.day

    @ml_function(description="Get weekday")
    def weekday(self) -> int:
        return self._date.weekday()

    @ml_function(description="Check if weekend")
    def isWeekend(self) -> bool:
        return self._date.weekday() >= 5

    @ml_function(description="Format as ISO string")
    def toISOString(self) -> str:
        return self._date.isoformat()

    @ml_function(description="Add days to date")
    def addDays(self, days: int) -> 'Date':
        new_date = self._date + _dt.timedelta(days=days)
        return Date(new_date)

    @ml_function(description="Subtract days from date")
    def subtractDays(self, days: int) -> 'Date':
        new_date = self._date - _dt.timedelta(days=days)
        return Date(new_date)

    @ml_function(description="Get difference in days between dates")
    def diff(self, other: 'Date') -> int:
        delta = self._date - other._date
        return delta.days


@ml_class(description="Time object representing time of day")
class Time:
    """Time object for ML code (hour, minute, second)."""

    def __init__(self, time_obj: _dt.time):
        self._time = time_obj

    @ml_function(description="Get hour")
    def hour(self) -> int:
        return self._time.hour

    @ml_function(description="Get minute")
    def minute(self) -> int:
        return self._time.minute

    @ml_function(description="Get second")
    def second(self) -> int:
        return self._time.second


@ml_class(description="Time delta representing duration")
class TimeDelta:
    """TimeDelta object for ML code."""

    def __init__(self, delta_obj: _dt.timedelta):
        self._delta = delta_obj

    @ml_function(description="Get days")
    def days(self) -> int:
        return self._delta.days

    @ml_function(description="Get seconds")
    def seconds(self) -> int:
        return self._delta.seconds

    @ml_function(description="Get total seconds")
    def totalSeconds(self) -> float:
        return self._delta.total_seconds()

    @ml_function(description="Get total minutes")
    def totalMinutes(self) -> float:
        return self._delta.total_seconds() / 60.0

    @ml_function(description="Get total hours")
    def totalHours(self) -> float:
        return self._delta.total_seconds() / 3600.0

    @ml_function(description="Get total days")
    def totalDays(self) -> float:
        return self._delta.total_seconds() / 86400.0

    @ml_function(description="Add two timedeltas")
    def add(self, other: 'TimeDelta') -> 'TimeDelta':
        new_delta = self._delta + other._delta
        return TimeDelta(new_delta)

    @ml_function(description="Subtract timedelta from this one")
    def subtract(self, other: 'TimeDelta') -> 'TimeDelta':
        new_delta = self._delta - other._delta
        return TimeDelta(new_delta)

    @ml_function(description="Multiply timedelta by scalar")
    def multiply(self, factor: float) -> 'TimeDelta':
        total_secs = self._delta.total_seconds() * factor
        new_delta = _dt.timedelta(seconds=total_secs)
        return TimeDelta(new_delta)

    @ml_function(description="Check if timedelta is negative")
    def isNegative(self) -> bool:
        return self._delta.total_seconds() < 0

    @ml_function(description="Get absolute value of timedelta")
    def abs(self) -> 'TimeDelta':
        if self._delta.total_seconds() < 0:
            return TimeDelta(-self._delta)
        return TimeDelta(self._delta)


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
    def now(self, timezone = None) -> DateTimeObject:
        """Get current date and time.

        Args:
            timezone: Optional timezone (use datetime.utc() for UTC)

        Returns:
            DateTimeObject representing current moment

        Example:
            now = datetime.now();
            year = now.year();
            month = now.month();

            // UTC time
            utc_tz = datetime.utc();
            utc_now = datetime.now(utc_tz);
        """
        if timezone is not None:
            # If timezone is provided, return UTC time
            return DateTimeObject(_dt.datetime.utcnow())
        return DateTimeObject(_dt.datetime.now())

    @ml_function(description="Get today's date", capabilities=["datetime.now"])
    def today(self) -> Date:
        """Get today's date.

        Returns:
            Date object representing today
        """
        return Date(_dt.date.today())

    @ml_function(description="Create date from components", capabilities=["datetime.create"])
    def createDate(self, year: int, month: int, day: int) -> Date:
        """Create date from components.

        Args:
            year: Year
            month: Month (1-12)
            day: Day (1-31)

        Returns:
            Date object
        """
        try:
            return Date(_dt.date(year, month, day))
        except ValueError as e:
            raise RuntimeError(f"Invalid date: {e}")

    @ml_function(description="Create time from components", capabilities=["datetime.create"])
    def createTime(self, hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0) -> Time:
        """Create time from components.

        Args:
            hour: Hour (0-23)
            minute: Minute (0-59)
            second: Second (0-59)
            microsecond: Microsecond (0-999999)

        Returns:
            Time object
        """
        try:
            return Time(_dt.time(hour, minute, second, microsecond))
        except ValueError as e:
            raise RuntimeError(f"Invalid time: {e}")

    @ml_function(description="Create time delta", capabilities=["datetime.create"])
    def createDelta(self, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> TimeDelta:
        """Create time delta.

        Args:
            days: Days
            hours: Hours
            minutes: Minutes
            seconds: Seconds

        Returns:
            TimeDelta object
        """
        return TimeDelta(_dt.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds))

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

    @ml_function(description="Parse ISO 8601 datetime string", capabilities=["datetime.create"])
    def parseISO(self, iso_string: str) -> DateTimeObject:
        """Parse ISO 8601 datetime string.

        Args:
            iso_string: ISO 8601 formatted string (e.g., "2025-10-05T14:30:00")

        Returns:
            DateTimeObject parsed from string

        Raises:
            RuntimeError: If string format is invalid
        """
        try:
            dt_obj = _dt.datetime.fromisoformat(iso_string)
            return DateTimeObject(dt_obj)
        except ValueError as e:
            raise RuntimeError(f"Invalid ISO datetime string '{iso_string}': {e}")

    @ml_function(description="Check if year is a leap year")
    def isLeapYear(self, year: int) -> bool:
        """Check if a year is a leap year.

        Args:
            year: Year to check

        Returns:
            True if leap year, False otherwise
        """
        return calendar.isleap(year)

    @ml_function(description="Get UTC timezone marker")
    def utc(self) -> str:
        """Get UTC timezone marker.

        Returns:
            UTC timezone marker to use with now() and other functions

        Example:
            utc_tz = datetime.utc();
            utc_now = datetime.now(utc_tz);
        """
        return "UTC"

    @ml_function(description="Create custom timezone", capabilities=["datetime.create"])
    def createTimeZone(self, hours: int, minutes: int = 0, name: str = "") -> dict:
        """Create a custom timezone.

        Args:
            hours: UTC offset in hours
            minutes: UTC offset in minutes (default 0)
            name: Timezone name (e.g., "EST", "JST")

        Returns:
            Timezone object

        Example:
            tokyo = datetime.createTimeZone(9, 0, "JST");
            ny = datetime.createTimeZone(-5, 0, "EST");
        """
        return {
            "hours": hours,
            "minutes": minutes,
            "name": name or f"UTC{hours:+d}:{minutes:02d}"
        }

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
    "Date",
    "Time",
    "TimeDelta",
    "datetime",
]
