// @description: Date and time operations with timezone support and object-oriented interface
// @capability: read:system_time
// @capability: read:timezone_data
// @version: 2.0.0

/**
 * ML DateTime Standard Library
 * Provides date and time operations with security validation and object-oriented API
 */

capability DateTimeOperations {
    allow read "system_time";
    allow read "timezone_data";
}

// Timestamp object constructor - creates object with methods and properties
function create_timestamp(timestamp_value: number) {
    return {
        value: timestamp_value,

        // Property access methods
        year: function() {
            return __python_bridge("datetime.datetime.fromtimestamp", timestamp_obj.value, "year");
        },

        month: function() {
            return __python_bridge("datetime.datetime.fromtimestamp", timestamp_obj.value, "month");
        },

        day: function() {
            return __python_bridge("datetime.datetime.fromtimestamp", timestamp_obj.value, "day");
        },

        hour: function() {
            return __python_bridge("datetime.datetime.fromtimestamp", timestamp_obj.value, "hour");
        },

        minute: function() {
            return __python_bridge("datetime.datetime.fromtimestamp", timestamp_obj.value, "minute");
        },

        second: function() {
            return __python_bridge("datetime.datetime.fromtimestamp", timestamp_obj.value, "second");
        },

        weekday: function() {
            return __python_bridge("datetime.datetime.fromtimestamp", timestamp_obj.value, "weekday");
        },

        // Formatting methods
        format: function(format_string) {
            return __python_bridge("datetime.datetime.fromtimestamp", timestamp_obj.value, format_string);
        },

        to_iso: function() {
            return timestamp_obj.format("%Y-%m-%dT%H:%M:%SZ");
        },

        to_readable: function() {
            return timestamp_obj.format("%Y-%m-%d %H:%M:%S");
        },

        to_date_string: function() {
            return timestamp_obj.format("%Y-%m-%d");
        },

        to_time_string: function() {
            return timestamp_obj.format("%H:%M:%S");
        },

        // Arithmetic methods
        add_days: function(days) {
            new_timestamp = __python_bridge("add_timedelta", timestamp_obj.value, days, 0, 0);
            return create_timestamp(new_timestamp);
        },

        add_hours: function(hours) {
            new_timestamp = __python_bridge("add_timedelta", timestamp_obj.value, 0, hours, 0);
            return create_timestamp(new_timestamp);
        },

        add_minutes: function(minutes) {
            new_timestamp = __python_bridge("add_timedelta", timestamp_obj.value, 0, 0, minutes);
            return create_timestamp(new_timestamp);
        },

        add_seconds: function(seconds) {
            return create_timestamp(timestamp_obj.value + seconds);
        },

        subtract_days: function(days) {
            return timestamp_obj.add_days(-days);
        },

        subtract_hours: function(hours) {
            return timestamp_obj.add_hours(-hours);
        },

        subtract_minutes: function(minutes) {
            return timestamp_obj.add_minutes(-minutes);
        },

        subtract_seconds: function(seconds) {
            return timestamp_obj.add_seconds(-seconds);
        },

        // Comparison methods
        is_before: function(other_timestamp) {
            other_value = other_timestamp.value != null ? other_timestamp.value : other_timestamp;
            return timestamp_obj.value < other_value;
        },

        is_after: function(other_timestamp) {
            other_value = other_timestamp.value != null ? other_timestamp.value : other_timestamp;
            return timestamp_obj.value > other_value;
        },

        is_same: function(other_timestamp) {
            other_value = other_timestamp.value != null ? other_timestamp.value : other_timestamp;
            return timestamp_obj.value == other_value;
        },

        is_same_day: function(other_timestamp) {
            other_value = other_timestamp.value != null ? other_timestamp.value : other_timestamp;
            return __python_bridge("is_same_day", timestamp_obj.value, other_value);
        },

        is_same_month: function(other_timestamp) {
            other_value = other_timestamp.value != null ? other_timestamp.value : other_timestamp;
            return timestamp_obj.year() == other_timestamp.year() &&
                   timestamp_obj.month() == other_timestamp.month();
        },

        is_same_year: function(other_timestamp) {
            other_value = other_timestamp.value != null ? other_timestamp.value : other_timestamp;
            return timestamp_obj.year() == other_timestamp.year();
        },

        // Time difference methods
        days_until: function(other_timestamp) {
            other_value = other_timestamp.value != null ? other_timestamp.value : other_timestamp;
            diff = other_value - timestamp_obj.value;
            return diff / (24 * 60 * 60);
        },

        hours_until: function(other_timestamp) {
            other_value = other_timestamp.value != null ? other_timestamp.value : other_timestamp;
            diff = other_value - timestamp_obj.value;
            return diff / (60 * 60);
        },

        minutes_until: function(other_timestamp) {
            other_value = other_timestamp.value != null ? other_timestamp.value : other_timestamp;
            diff = other_value - timestamp_obj.value;
            return diff / 60;
        },

        seconds_until: function(other_timestamp) {
            other_value = other_timestamp.value != null ? other_timestamp.value : other_timestamp;
            return other_value - timestamp_obj.value;
        },

        // Utility methods
        start_of_day: function() {
            new_timestamp = __python_bridge("start_of_day", timestamp_obj.value);
            return create_timestamp(new_timestamp);
        },

        end_of_day: function() {
            new_timestamp = __python_bridge("end_of_day", timestamp_obj.value);
            return create_timestamp(new_timestamp);
        },

        start_of_month: function() {
            new_timestamp = __python_bridge("start_of_month", timestamp_obj.value);
            return create_timestamp(new_timestamp);
        },

        end_of_month: function() {
            new_timestamp = __python_bridge("end_of_month", timestamp_obj.value);
            return create_timestamp(new_timestamp);
        },

        start_of_year: function() {
            new_timestamp = __python_bridge("start_of_year", timestamp_obj.value);
            return create_timestamp(new_timestamp);
        },

        end_of_year: function() {
            new_timestamp = __python_bridge("end_of_year", timestamp_obj.value);
            return create_timestamp(new_timestamp);
        },

        // Validation methods
        is_weekend: function() {
            weekday_val = timestamp_obj.weekday();
            return weekday_val == 5 || weekday_val == 6; // Saturday = 5, Sunday = 6
        },

        is_business_day: function() {
            weekday_val = timestamp_obj.weekday();
            return weekday_val >= 0 && weekday_val <= 4; // Monday to Friday
        },

        is_leap_year: function() {
            year_val = timestamp_obj.year();
            return (year_val % 4 == 0 && year_val % 100 != 0) || (year_val % 400 == 0);
        },

        // Age calculation
        age_in_years: function(current_timestamp) {
            current_value = current_timestamp != null ?
                (current_timestamp.value != null ? current_timestamp.value : current_timestamp) :
                now();
            return __python_bridge("calculate_age_years", timestamp_obj.value, current_value);
        },

        age_in_days: function(current_timestamp) {
            current_value = current_timestamp != null ?
                (current_timestamp.value != null ? current_timestamp.value : current_timestamp) :
                now();
            return timestamp_obj.days_until(current_value);
        },

        // Business day operations
        add_business_days: function(days) {
            new_timestamp = __python_bridge("add_business_days", timestamp_obj.value, days);
            return create_timestamp(new_timestamp);
        },

        business_days_until: function(other_timestamp) {
            other_value = other_timestamp.value != null ? other_timestamp.value : other_timestamp;
            return __python_bridge("business_days_between", timestamp_obj.value, other_value);
        },

        // Timezone operations
        to_utc: function(timezone) {
            new_timestamp = __python_bridge("convert_timezone", timestamp_obj.value, timezone, "UTC");
            return create_timestamp(new_timestamp);
        },

        from_utc: function(timezone) {
            new_timestamp = __python_bridge("convert_timezone", timestamp_obj.value, "UTC", timezone);
            return create_timestamp(new_timestamp);
        },

        // String representation
        toString: function() {
            return timestamp_obj.to_readable();
        }
    };
}

// TimeDelta object constructor - represents time differences
function create_timedelta(days: number, hours: number, minutes: number, seconds: number) {
    total_seconds = days * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60 + seconds;

    return {
        days: days,
        hours: hours,
        minutes: minutes,
        seconds: seconds,
        total_seconds: total_seconds,

        // Property getters
        get_days: function() {
            return timedelta_obj.days;
        },

        get_hours: function() {
            return timedelta_obj.hours;
        },

        get_minutes: function() {
            return timedelta_obj.minutes;
        },

        get_seconds: function() {
            return timedelta_obj.seconds;
        },

        get_total_seconds: function() {
            return timedelta_obj.total_seconds;
        },

        get_total_minutes: function() {
            return timedelta_obj.total_seconds / 60;
        },

        get_total_hours: function() {
            return timedelta_obj.total_seconds / (60 * 60);
        },

        get_total_days: function() {
            return timedelta_obj.total_seconds / (24 * 60 * 60);
        },

        // Arithmetic operations
        add: function(other_timedelta) {
            return create_timedelta(
                timedelta_obj.days + other_timedelta.days,
                timedelta_obj.hours + other_timedelta.hours,
                timedelta_obj.minutes + other_timedelta.minutes,
                timedelta_obj.seconds + other_timedelta.seconds
            );
        },

        subtract: function(other_timedelta) {
            return create_timedelta(
                timedelta_obj.days - other_timedelta.days,
                timedelta_obj.hours - other_timedelta.hours,
                timedelta_obj.minutes - other_timedelta.minutes,
                timedelta_obj.seconds - other_timedelta.seconds
            );
        },

        multiply: function(factor) {
            return create_timedelta(
                timedelta_obj.days * factor,
                timedelta_obj.hours * factor,
                timedelta_obj.minutes * factor,
                timedelta_obj.seconds * factor
            );
        },

        // Comparison operations
        is_positive: function() {
            return timedelta_obj.total_seconds > 0;
        },

        is_negative: function() {
            return timedelta_obj.total_seconds < 0;
        },

        is_zero: function() {
            return timedelta_obj.total_seconds == 0;
        },

        abs: function() {
            if (timedelta_obj.is_negative()) {
                return timedelta_obj.multiply(-1);
            }
            return timedelta_obj;
        },

        // String representation
        toString: function() {
            if (timedelta_obj.is_zero()) {
                return "0 seconds";
            }

            parts = [];
            if (timedelta_obj.days != 0) {
                parts = safe_append(parts, string.toString(timedelta_obj.days) + " days");
            }
            if (timedelta_obj.hours != 0) {
                parts = safe_append(parts, string.toString(timedelta_obj.hours) + " hours");
            }
            if (timedelta_obj.minutes != 0) {
                parts = safe_append(parts, string.toString(timedelta_obj.minutes) + " minutes");
            }
            if (timedelta_obj.seconds != 0) {
                parts = safe_append(parts, string.toString(timedelta_obj.seconds) + " seconds");
            }

            return string.join(", ", parts);
        }
    };
}

// Factory functions for creating timestamp objects
function now() {
    timestamp_value = __python_bridge("time.time");
    return create_timestamp(timestamp_value);
}

function today() {
    return now().start_of_day();
}

function create_date(year: number, month: number, day: number) {
    timestamp_value = __python_bridge("create_datetime_timestamp", year, month, day, 0, 0, 0);
    return create_timestamp(timestamp_value);
}

function create_datetime(year: number, month: number, day: number,
                        hour: number, minute: number, second: number) {
    timestamp_value = __python_bridge("create_datetime_timestamp", year, month, day, hour, minute, second);
    return create_timestamp(timestamp_value);
}

function parse_iso(iso_string: string) {
    timestamp_value = __python_bridge("datetime.datetime.fromisoformat", iso_string);
    return create_timestamp(timestamp_value);
}

function parse_date(date_string: string, format: string) {
    timestamp_value = __python_bridge("datetime.datetime.strptime", date_string, format);
    return create_timestamp(timestamp_value);
}

// TimeDelta factory functions
function days(count: number) {
    return create_timedelta(count, 0, 0, 0);
}

function hours(count: number) {
    return create_timedelta(0, count, 0, 0);
}

function minutes(count: number) {
    return create_timedelta(0, 0, count, 0);
}

function seconds(count: number) {
    return create_timedelta(0, 0, 0, count);
}

// Date validation functions
function is_valid_date(year: number, month: number, day: number): boolean {
    if (month < 1 || month > 12) {
        return false;
    }

    if (day < 1) {
        return false;
    }

    days_in_month_array = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    // Check for leap year
    if (month == 2 && is_leap_year_func(year)) {
        return day <= 29;
    }

    return day <= days_in_month_array[month - 1];
}

function is_leap_year_func(year: number): boolean {
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

// Utility functions for month and weekday names
function get_month_name(month: number): string {
    month_names = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"];
    if (month >= 1 && month <= 12) {
        return month_names[month - 1];
    }
    return "Invalid";
}

function get_short_month_name(month: number): string {
    short_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    if (month >= 1 && month <= 12) {
        return short_names[month - 1];
    }
    return "Invalid";
}

function get_weekday_name(weekday: number): string {
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    if (weekday >= 0 && weekday <= 6) {
        return day_names[weekday];
    }
    return "Invalid";
}

function get_short_weekday_name(weekday: number): string {
    short_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    if (weekday >= 0 && weekday <= 6) {
        return short_names[weekday];
    }
    return "Invalid";
}

// Sleep function (with limits for security)
function sleep(seconds: number): void {
    // Limit sleep duration for security
    if (seconds > 300) { // Max 5 minutes
        seconds = 300;
    }

    __python_bridge("time.sleep", seconds);
}

// Legacy function compatibility (for backward compatibility)
function format_date(timestamp: number, format: string): string {
    return __python_bridge("datetime.datetime.fromtimestamp", timestamp, format);
}

function format_iso(timestamp: number): string {
    return format_date(timestamp, "%Y-%m-%dT%H:%M:%SZ");
}

function format_readable(timestamp: number): string {
    return format_date(timestamp, "%Y-%m-%d %H:%M:%S");
}

function add_days(timestamp: number, days: number): number {
    return __python_bridge("add_timedelta", timestamp, days, 0, 0);
}

function add_hours(timestamp: number, hours: number): number {
    return __python_bridge("add_timedelta", timestamp, 0, hours, 0);
}

function add_minutes(timestamp: number, minutes: number): number {
    return __python_bridge("add_timedelta", timestamp, 0, 0, minutes);
}

function days_between(timestamp1: number, timestamp2: number): number {
    diff = timestamp2 - timestamp1;
    return diff / (24 * 60 * 60);
}

function hours_between(timestamp1: number, timestamp2: number): number {
    diff = timestamp2 - timestamp1;
    return diff / (60 * 60);
}

function minutes_between(timestamp1: number, timestamp2: number): number {
    diff = timestamp2 - timestamp1;
    return diff / 60;
}