// @description: Date and time operations with timezone support
// @capability: read:system_time
// @capability: read:timezone_data
// @version: 1.0.0

/**
 * ML DateTime Standard Library
 * Provides date and time operations with security validation
 */

capability DateTimeOperations {
    allow read "system_time";
    allow read "timezone_data";
}

// Get current timestamp
function now(): number {
    return __python_bridge("time.time");
}

function today(): string {
    return __python_bridge("datetime.date.today");
}

function utcnow(): string {
    return __python_bridge("datetime.datetime.utcnow");
}

// Date formatting functions
function format_date(timestamp: number, format: string): string {
    return __python_bridge("datetime.datetime.fromtimestamp", timestamp, format);
}

function format_iso(timestamp: number): string {
    return format_date(timestamp, "%Y-%m-%dT%H:%M:%SZ");
}

function format_readable(timestamp: number): string {
    return format_date(timestamp, "%Y-%m-%d %H:%M:%S");
}

// Date parsing functions
function parse_iso(iso_string: string): number {
    return __python_bridge("datetime.datetime.fromisoformat", iso_string);
}

function parse_date(date_string: string, format: string): number {
    return __python_bridge("datetime.datetime.strptime", date_string, format);
}

// Date arithmetic functions
function add_days(timestamp: number, days: number): number {
    return __python_bridge("add_timedelta", timestamp, days, 0, 0);
}

function add_hours(timestamp: number, hours: number): number {
    return __python_bridge("add_timedelta", timestamp, 0, hours, 0);
}

function add_minutes(timestamp: number, minutes: number): number {
    return __python_bridge("add_timedelta", timestamp, 0, 0, minutes);
}

function add_seconds(timestamp: number, seconds: number): number {
    return timestamp + seconds;
}

// Date comparison functions
function days_between(timestamp1: number, timestamp2: number): number {
    diff = timestamp2 - timestamp1;
    return diff / (24 * 60 * 60); // Convert seconds to days
}

function hours_between(timestamp1: number, timestamp2: number): number {
    diff = timestamp2 - timestamp1;
    return diff / (60 * 60); // Convert seconds to hours
}

function minutes_between(timestamp1: number, timestamp2: number): number {
    diff = timestamp2 - timestamp1;
    return diff / 60; // Convert seconds to minutes
}

// Date component extraction
function get_year(timestamp: number): number {
    return __python_bridge("datetime.datetime.fromtimestamp", timestamp, "year");
}

function get_month(timestamp: number): number {
    return __python_bridge("datetime.datetime.fromtimestamp", timestamp, "month");
}

function get_day(timestamp: number): number {
    return __python_bridge("datetime.datetime.fromtimestamp", timestamp, "day");
}

function get_hour(timestamp: number): number {
    return __python_bridge("datetime.datetime.fromtimestamp", timestamp, "hour");
}

function get_minute(timestamp: number): number {
    return __python_bridge("datetime.datetime.fromtimestamp", timestamp, "minute");
}

function get_second(timestamp: number): number {
    return __python_bridge("datetime.datetime.fromtimestamp", timestamp, "second");
}

function get_weekday(timestamp: number): number {
    return __python_bridge("datetime.datetime.fromtimestamp", timestamp, "weekday");
}

// Timezone functions
function to_utc(timestamp: number, timezone: string): number {
    return __python_bridge("convert_timezone", timestamp, timezone, "UTC");
}

function from_utc(timestamp: number, timezone: string): number {
    return __python_bridge("convert_timezone", timestamp, "UTC", timezone);
}

// Date validation functions
function is_valid_date(year: number, month: number, day: number): boolean {
    if (month < 1 || month > 12) {
        return false;
    }

    if (day < 1) {
        return false;
    }

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    // Check for leap year
    if (month == 2 && is_leap_year(year)) {
        return day <= 29;
    }

    return day <= days_in_month[month - 1];
}

function is_leap_year(year: number): boolean {
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

function is_weekend(timestamp: number): boolean {
    weekday = get_weekday(timestamp);
    return weekday == 5 || weekday == 6; // Saturday = 5, Sunday = 6
}

// Sleep and timing functions (with limits)
function sleep(seconds: number): void {
    // Limit sleep duration for security
    if (seconds > 300) { // Max 5 minutes
        seconds = 300;
    }

    __python_bridge("time.sleep", seconds);
}

// Utility functions
function timestamp_to_date(timestamp: number): string {
    return format_readable(timestamp);
}

function date_to_timestamp(date_string: string): number {
    return parse_iso(date_string);
}

// Additional date creation functions
function create_date(year: number, month: number, day: number): number {
    return __python_bridge("create_datetime_timestamp", year, month, day, 0, 0, 0);
}

function create_datetime(year: number, month: number, day: number,
                        hour: number, minute: number, second: number): number {
    return __python_bridge("create_datetime_timestamp", year, month, day, hour, minute, second);
}

// Date range functions
function start_of_day(timestamp: number): number {
    return __python_bridge("start_of_day", timestamp);
}

function end_of_day(timestamp: number): number {
    return __python_bridge("end_of_day", timestamp);
}

function start_of_month(timestamp: number): number {
    return __python_bridge("start_of_month", timestamp);
}

function end_of_month(timestamp: number): number {
    return __python_bridge("end_of_month", timestamp);
}

function start_of_year(timestamp: number): number {
    return __python_bridge("start_of_year", timestamp);
}

function end_of_year(timestamp: number): number {
    return __python_bridge("end_of_year", timestamp);
}

// Additional date utilities
function days_in_month(year: number, month: number): number {
    return __python_bridge("days_in_month", year, month);
}

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

// Age calculation
function age_in_years(birth_timestamp: number, current_timestamp: number): number {
    return __python_bridge("calculate_age_years", birth_timestamp, current_timestamp);
}

function age_in_days(birth_timestamp: number, current_timestamp: number): number {
    return days_between(birth_timestamp, current_timestamp);
}

// Date comparison helpers
function is_same_day(timestamp1: number, timestamp2: number): boolean {
    return __python_bridge("is_same_day", timestamp1, timestamp2);
}

function is_same_month(timestamp1: number, timestamp2: number): boolean {
    return get_year(timestamp1) == get_year(timestamp2) &&
           get_month(timestamp1) == get_month(timestamp2);
}

function is_same_year(timestamp1: number, timestamp2: number): boolean {
    return get_year(timestamp1) == get_year(timestamp2);
}

// Business day calculations
function is_business_day(timestamp: number): boolean {
    weekday = get_weekday(timestamp);
    return weekday >= 0 && weekday <= 4; // Monday to Friday
}

function add_business_days(timestamp: number, days: number): number {
    return __python_bridge("add_business_days", timestamp, days);
}

function business_days_between(start_timestamp: number, end_timestamp: number): number {
    return __python_bridge("business_days_between", start_timestamp, end_timestamp);
}