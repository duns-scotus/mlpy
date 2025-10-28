"""Unit tests for datetime_bridge module migration."""

import pytest
import datetime as py_dt
from mlpy.stdlib.datetime_bridge import DateTime, DateTimeObject, datetime
from mlpy.stdlib.decorators import get_module_metadata
from mlpy.stdlib.module_registry import get_registry


class TestDateTimeModuleRegistration:
    """Test that DateTime module is properly registered."""

    def test_datetime_module_registered(self):
        """Test that datetime module is available in registry."""
        registry = get_registry()
        assert registry.is_available("datetime")
        datetime_instance = registry.get_module("datetime")
        assert datetime_instance is not None
        assert type(datetime_instance).__name__ == "DateTime"

    def test_datetime_module_metadata(self):
        """Test datetime module metadata is correct."""
        metadata = get_module_metadata("datetime")
        assert metadata is not None
        assert metadata.name == "datetime"
        assert metadata.description == "Date and time manipulation with timezone support"
        assert "datetime.create" in metadata.capabilities
        assert "datetime.now" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_datetime_has_function_metadata(self):
        """Test that datetime module has registered functions."""
        metadata = get_module_metadata("datetime")

        # Check key methods are registered
        assert "now" in metadata.functions
        assert "create" in metadata.functions
        assert "fromTimestamp" in metadata.functions
        assert "daysInMonth" in metadata.functions
        assert "calculateAge" in metadata.functions
        assert "addBusinessDays" in metadata.functions
        assert "businessDaysBetween" in metadata.functions
        assert "isWeekend" in metadata.functions
        assert "isWeekday" in metadata.functions

        # Should have many functions (15+)
        assert len(metadata.functions) >= 15


class TestDateTimeObjectBasics:
    """Test DateTimeObject class basic functionality."""

    def test_datetime_now_returns_datetime_object(self):
        """Test that datetime.now() returns DateTimeObject."""
        now = datetime.now()
        assert isinstance(now, DateTimeObject)

    def test_datetime_create_returns_datetime_object(self):
        """Test that datetime.create() returns DateTimeObject."""
        dt = datetime.create(2024, 1, 15, 10, 30, 45)
        assert isinstance(dt, DateTimeObject)

    def test_datetime_from_timestamp_returns_datetime_object(self):
        """Test that datetime.fromTimestamp() returns DateTimeObject."""
        timestamp = 1700000000.0
        dt = datetime.fromTimestamp(timestamp)
        assert isinstance(dt, DateTimeObject)

    def test_datetime_object_components(self):
        """Test DateTimeObject component access."""
        dt = datetime.create(2024, 3, 15, 14, 30, 45)
        assert dt.year() == 2024
        assert dt.month() == 3
        assert dt.day() == 15
        assert dt.hour() == 14
        assert dt.minute() == 30
        assert dt.second() == 45

    def test_datetime_object_weekday(self):
        """Test DateTimeObject weekday method."""
        # 2024-01-01 is a Monday (weekday 0)
        dt = datetime.create(2024, 1, 1)
        assert dt.weekday() == 0

        # 2024-01-06 is a Saturday (weekday 5)
        dt = datetime.create(2024, 1, 6)
        assert dt.weekday() == 5


class TestDateTimeObjectManipulation:
    """Test DateTimeObject manipulation methods."""

    def test_add_days(self):
        """Test addDays() method."""
        dt = datetime.create(2024, 1, 15)
        future = dt.addDays(7)
        assert isinstance(future, DateTimeObject)
        assert future.year() == 2024
        assert future.month() == 1
        assert future.day() == 22

    def test_add_hours(self):
        """Test addHours() method."""
        dt = datetime.create(2024, 1, 15, 10, 0)
        future = dt.addHours(5)
        assert isinstance(future, DateTimeObject)
        assert future.hour() == 15

    def test_add_minutes(self):
        """Test addMinutes() method."""
        dt = datetime.create(2024, 1, 15, 10, 30)
        future = dt.addMinutes(45)
        assert isinstance(future, DateTimeObject)
        assert future.hour() == 11
        assert future.minute() == 15

    def test_add_seconds(self):
        """Test addSeconds() method."""
        dt = datetime.create(2024, 1, 15, 10, 30, 30)
        future = dt.addSeconds(45)
        assert isinstance(future, DateTimeObject)
        assert future.second() == 15  # 30 + 45 = 75 -> 1:15

    def test_add_negative_days(self):
        """Test adding negative days (going back in time)."""
        dt = datetime.create(2024, 1, 15)
        past = dt.addDays(-10)
        assert isinstance(past, DateTimeObject)
        assert past.year() == 2024
        assert past.month() == 1
        assert past.day() == 5


class TestDateTimeObjectBoundaries:
    """Test DateTimeObject boundary methods (start/end of day/month/year)."""

    def test_start_of_day(self):
        """Test startOfDay() method."""
        dt = datetime.create(2024, 3, 15, 14, 30, 45)
        start = dt.startOfDay()
        assert isinstance(start, DateTimeObject)
        assert start.hour() == 0
        assert start.minute() == 0
        assert start.second() == 0

    def test_end_of_day(self):
        """Test endOfDay() method."""
        dt = datetime.create(2024, 3, 15, 10, 0, 0)
        end = dt.endOfDay()
        assert isinstance(end, DateTimeObject)
        assert end.hour() == 23
        assert end.minute() == 59
        assert end.second() == 59

    def test_start_of_month(self):
        """Test startOfMonth() method."""
        dt = datetime.create(2024, 3, 15, 14, 30)
        start = dt.startOfMonth()
        assert isinstance(start, DateTimeObject)
        assert start.day() == 1
        assert start.hour() == 0

    def test_end_of_month(self):
        """Test endOfMonth() method."""
        dt = datetime.create(2024, 3, 15)
        end = dt.endOfMonth()
        assert isinstance(end, DateTimeObject)
        assert end.day() == 31  # March has 31 days

    def test_start_of_year(self):
        """Test startOfYear() method."""
        dt = datetime.create(2024, 6, 15, 14, 30)
        start = dt.startOfYear()
        assert isinstance(start, DateTimeObject)
        assert start.month() == 1
        assert start.day() == 1
        assert start.hour() == 0

    def test_end_of_year(self):
        """Test endOfYear() method."""
        dt = datetime.create(2024, 6, 15)
        end = dt.endOfYear()
        assert isinstance(end, DateTimeObject)
        assert end.month() == 12
        assert end.day() == 31


class TestDateTimeObjectComparison:
    """Test DateTimeObject comparison methods."""

    def test_is_same_day_true(self):
        """Test isSameDay() returns True for same day."""
        dt1 = datetime.create(2024, 3, 15, 10, 0)
        dt2 = datetime.create(2024, 3, 15, 18, 30)
        assert dt1.isSameDay(dt2) is True

    def test_is_same_day_false(self):
        """Test isSameDay() returns False for different days."""
        dt1 = datetime.create(2024, 3, 15, 10, 0)
        dt2 = datetime.create(2024, 3, 16, 10, 0)
        assert dt1.isSameDay(dt2) is False


class TestDateTimeObjectFormatting:
    """Test DateTimeObject formatting methods."""

    def test_timestamp(self):
        """Test timestamp() method."""
        dt = datetime.create(2024, 1, 1, 0, 0, 0)
        timestamp = dt.timestamp()
        assert isinstance(timestamp, float)
        assert timestamp > 0

    def test_format_default(self):
        """Test format() with default format string."""
        dt = datetime.create(2024, 3, 15, 14, 30, 45)
        formatted = dt.format()
        assert "2024" in formatted
        assert "03" in formatted or "3" in formatted
        assert "15" in formatted
        assert "14" in formatted
        assert "30" in formatted

    def test_format_custom(self):
        """Test format() with custom format string."""
        dt = datetime.create(2024, 3, 15, 14, 30)
        formatted = dt.format("%Y-%m-%d")
        assert formatted == "2024-03-15"

    def test_to_string(self):
        """Test toString() method returns ISO format."""
        dt = datetime.create(2024, 3, 15, 14, 30, 45)
        result = dt.toString()
        assert isinstance(result, str)
        assert "2024" in result


class TestDateTimeModuleMethods:
    """Test DateTime module-level methods."""

    def test_days_in_month(self):
        """Test daysInMonth() method."""
        # January has 31 days
        assert datetime.daysInMonth(2024, 1) == 31
        # February 2024 (leap year) has 29 days
        assert datetime.daysInMonth(2024, 2) == 29
        # February 2023 (non-leap year) has 28 days
        assert datetime.daysInMonth(2023, 2) == 28
        # April has 30 days
        assert datetime.daysInMonth(2024, 4) == 30

    def test_calculate_age(self):
        """Test calculateAge() method."""
        birth = datetime.create(1990, 5, 15)
        current = datetime.create(2024, 5, 15)
        age = datetime.calculateAge(birth, current)
        assert age == 34

    def test_calculate_age_before_birthday(self):
        """Test age calculation before birthday in current year."""
        birth = datetime.create(1990, 5, 15)
        current = datetime.create(2024, 3, 1)  # Before birthday
        age = datetime.calculateAge(birth, current)
        assert age == 33  # Haven't had birthday yet

    def test_is_weekend(self):
        """Test isWeekend() method."""
        # 2024-01-06 is a Saturday
        saturday = datetime.create(2024, 1, 6)
        assert datetime.isWeekend(saturday) is True

        # 2024-01-01 is a Monday
        monday = datetime.create(2024, 1, 1)
        assert datetime.isWeekend(monday) is False

    def test_is_weekday(self):
        """Test isWeekday() method."""
        # 2024-01-01 is a Monday
        monday = datetime.create(2024, 1, 1)
        assert datetime.isWeekday(monday) is True

        # 2024-01-06 is a Saturday
        saturday = datetime.create(2024, 1, 6)
        assert datetime.isWeekday(saturday) is False


class TestDateTimeBusinessDays:
    """Test business day calculation methods."""

    def test_add_business_days_forward(self):
        """Test adding business days forward."""
        # Start on Monday 2024-01-01
        start = datetime.create(2024, 1, 1)  # Monday
        result = datetime.addBusinessDays(start, 5)
        # 5 business days from Monday is Monday next week (skips weekend)
        assert result.day() == 8

    def test_add_business_days_backward(self):
        """Test adding negative business days (going back)."""
        # Start on Friday 2024-01-05
        start = datetime.create(2024, 1, 5)  # Friday
        result = datetime.addBusinessDays(start, -5)
        # 5 business days back from Friday is Friday previous week
        assert result.day() in [29, 30, 31]  # Previous week

    def test_add_zero_business_days(self):
        """Test adding zero business days."""
        start = datetime.create(2024, 1, 1)
        result = datetime.addBusinessDays(start, 0)
        assert result.day() == start.day()

    def test_business_days_between(self):
        """Test counting business days between dates."""
        # Monday to Friday (same week)
        start = datetime.create(2024, 1, 1)  # Monday
        end = datetime.create(2024, 1, 5)    # Friday
        count = datetime.businessDaysBetween(start, end)
        assert count == 5  # Mon, Tue, Wed, Thu, Fri

    def test_business_days_between_with_weekend(self):
        """Test counting business days over a weekend."""
        # Friday to Monday (crossing weekend)
        start = datetime.create(2024, 1, 5)  # Friday
        end = datetime.create(2024, 1, 8)    # Monday
        count = datetime.businessDaysBetween(start, end)
        assert count == 2  # Friday and Monday only


class TestDateTimeSnakeCaseAliases:
    """Test snake_case aliases for all methods."""

    def test_datetime_object_aliases(self):
        """Test DateTimeObject snake_case aliases."""
        dt = datetime.create(2024, 1, 15, 10, 30)

        # add_days alias
        future = dt.add_days(7)
        assert isinstance(future, DateTimeObject)
        assert future.day() == 22

        # add_hours alias
        future_hours = dt.add_hours(5)
        assert future_hours.hour() == 15

        # start_of_day alias
        start = dt.start_of_day()
        assert start.hour() == 0

    def test_datetime_module_aliases(self):
        """Test DateTime module snake_case aliases."""
        # from_timestamp alias
        dt = datetime.from_timestamp(1700000000.0)
        assert isinstance(dt, DateTimeObject)

        # days_in_month alias
        days = datetime.days_in_month(2024, 2)
        assert days == 29

        # is_weekend alias
        saturday = datetime.create(2024, 1, 6)
        assert datetime.is_weekend(saturday) is True


class TestDateTimeInstance:
    """Test global datetime instance."""

    def test_datetime_is_instance_of_datetime_class(self):
        """Test that datetime is an instance of DateTime."""
        assert isinstance(datetime, DateTime)

    def test_datetime_has_decorated_methods(self):
        """Test that datetime instance has decorated methods with metadata."""
        assert hasattr(datetime, "now")
        assert hasattr(datetime, "create")
        assert hasattr(datetime, "fromTimestamp")

        # Check they have metadata
        assert hasattr(datetime.now, "_ml_function_metadata")
        assert hasattr(datetime.create, "_ml_function_metadata")
        assert hasattr(datetime.fromTimestamp, "_ml_function_metadata")


class TestDateTimeObjectMetadata:
    """Test DateTimeObject class metadata."""

    def test_datetime_object_class_has_metadata(self):
        """Test that DateTimeObject class has metadata."""
        assert hasattr(DateTimeObject, "_ml_class_metadata")

    def test_datetime_object_methods_have_metadata(self):
        """Test that DateTimeObject methods have metadata."""
        dt = datetime.create(2024, 1, 1)
        assert hasattr(dt.timestamp, "_ml_function_metadata")
        assert hasattr(dt.addDays, "_ml_function_metadata")
        assert hasattr(dt.format, "_ml_function_metadata")


class TestDateTimeErrorHandling:
    """Test error handling for invalid inputs."""

    def test_invalid_datetime_components(self):
        """Test that invalid datetime raises RuntimeError."""
        with pytest.raises(RuntimeError) as exc_info:
            datetime.create(2024, 13, 1)  # Invalid month
        assert "Invalid datetime components" in str(exc_info.value)

    def test_invalid_timestamp(self):
        """Test that invalid timestamp raises RuntimeError."""
        with pytest.raises(RuntimeError) as exc_info:
            datetime.fromTimestamp(-999999999999999)  # Invalid timestamp
        assert "Invalid timestamp" in str(exc_info.value)

    def test_invalid_days_in_month(self):
        """Test invalid month returns 0 days."""
        days = datetime.daysInMonth(2024, 13)  # Invalid month
        assert days == 0


class TestDateTimeMissingCoverage:
    """Test cases to improve coverage for datetime_bridge."""

    def test_to_iso_string(self):
        """Test toISOString() method."""
        dt = datetime.create(2024, 10, 24, 15, 30, 45)
        iso_string = dt.toISOString()
        assert "2024-10-24" in iso_string
        assert "15:30:45" in iso_string

    def test_date_extraction(self):
        """Test date() method to extract date component."""
        dt = datetime.create(2024, 10, 24, 15, 30, 45)
        date_obj = dt.date()
        assert date_obj is not None
        # Date object should have year, month, day
        assert hasattr(date_obj, '_date')

    def test_time_extraction(self):
        """Test time() method to extract time component."""
        dt = datetime.create(2024, 10, 24, 15, 30, 45)
        time_obj = dt.time()
        assert time_obj is not None
        # Time object should have hour, minute, second
        assert hasattr(time_obj, '_time')

    def test_diff_method(self):
        """Test diff() method between two datetimes."""
        dt1 = datetime.create(2024, 10, 24, 12, 0, 0)
        dt2 = datetime.create(2024, 10, 24, 15, 0, 0)
        delta = dt2.diff(dt1)
        assert delta is not None
        # Delta should represent 3 hours difference
        assert hasattr(delta, '_delta')

    def test_add_timedelta(self):
        """Test add() method with timedelta."""
        dt = datetime.create(2024, 10, 24, 12, 0, 0)
        # Create a timedelta (we'll use the TimeDelta class)
        from datetime import timedelta as py_timedelta
        from mlpy.stdlib.datetime_bridge import TimeDelta
        delta = TimeDelta(py_timedelta(hours=3))
        new_dt = dt.add(delta)
        assert new_dt.hour() == 15

    def test_subtract_timedelta(self):
        """Test subtract() method with timedelta."""
        dt = datetime.create(2024, 10, 24, 15, 0, 0)
        from datetime import timedelta as py_timedelta
        from mlpy.stdlib.datetime_bridge import TimeDelta
        delta = TimeDelta(py_timedelta(hours=3))
        new_dt = dt.subtract(delta)
        assert new_dt.hour() == 12

    def test_is_before(self):
        """Test isBefore() comparison method."""
        dt1 = datetime.create(2024, 10, 24, 12, 0, 0)
        dt2 = datetime.create(2024, 10, 24, 15, 0, 0)
        assert dt1.isBefore(dt2) is True
        assert dt2.isBefore(dt1) is False

    def test_is_after(self):
        """Test isAfter() comparison method."""
        dt1 = datetime.create(2024, 10, 24, 12, 0, 0)
        dt2 = datetime.create(2024, 10, 24, 15, 0, 0)
        assert dt2.isAfter(dt1) is True
        assert dt1.isAfter(dt2) is False

    def test_is_same(self):
        """Test isSame() comparison method."""
        dt1 = datetime.create(2024, 10, 24, 12, 0, 0)
        dt2 = datetime.create(2024, 10, 24, 12, 0, 0)
        dt3 = datetime.create(2024, 10, 24, 15, 0, 0)
        assert dt1.isSame(dt2) is True
        assert dt1.isSame(dt3) is False

    def test_get_year(self):
        """Test year() getter method."""
        dt = datetime.create(2024, 10, 24, 12, 0, 0)
        assert dt.year() == 2024

    def test_get_month(self):
        """Test month() getter method."""
        dt = datetime.create(2024, 10, 24, 12, 0, 0)
        assert dt.month() == 10

    def test_get_day(self):
        """Test day() getter method."""
        dt = datetime.create(2024, 10, 24, 12, 0, 0)
        assert dt.day() == 24

    def test_get_hour(self):
        """Test hour() getter method."""
        dt = datetime.create(2024, 10, 24, 15, 30, 45)
        assert dt.hour() == 15

    def test_get_minute(self):
        """Test minute() getter method."""
        dt = datetime.create(2024, 10, 24, 15, 30, 45)
        assert dt.minute() == 30

    def test_get_second(self):
        """Test second() getter method."""
        dt = datetime.create(2024, 10, 24, 15, 30, 45)
        assert dt.second() == 45

    def test_weekday(self):
        """Test weekday() method (0=Monday, 6=Sunday)."""
        dt = datetime.create(2024, 10, 24, 12, 0, 0)  # Thursday
        weekday = dt.weekday()
        assert 0 <= weekday <= 6

    def test_is_same_day(self):
        """Test isSameDay() method."""
        dt1 = datetime.create(2024, 10, 24, 12, 0, 0)
        dt2 = datetime.create(2024, 10, 24, 18, 30, 0)  # Same day, different time
        dt3 = datetime.create(2024, 10, 25, 12, 0, 0)  # Different day
        assert dt1.isSameDay(dt2) is True
        assert dt1.isSameDay(dt3) is False

    def test_timestamp(self):
        """Test timestamp() method."""
        dt = datetime.create(2024, 10, 24, 12, 0, 0)
        ts = dt.timestamp()
        assert isinstance(ts, (int, float))
        assert ts > 0

    def test_format_custom(self):
        """Test format() method with custom format string."""
        dt = datetime.create(2024, 10, 24, 15, 30, 45)
        formatted = dt.format("%Y-%m-%d %H:%M:%S")
        assert "2024-10-24" in formatted
        assert "15:30:45" in formatted
