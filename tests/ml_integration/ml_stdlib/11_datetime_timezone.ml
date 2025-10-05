// Test stdlib module: datetime - Timezone support
// Features tested: TimeZone, UTC, timezone-aware datetime
// Module: datetime (version 2.0)

import datetime;

function test_utc_timezone() {
    results = {};

    // Get UTC timezone
    utc = datetime.utc();
    results.has_utc = utc != null;

    // Create UTC datetime
    dt_utc = datetime.now(utc);
    results.has_year = dt_utc.year() > 2020;

    return results;
}

function test_custom_timezone() {
    results = {};

    // Create timezone: UTC+9 (Tokyo)
    tokyo = datetime.createTimeZone(9, 0, "JST");
    results.has_tokyo = tokyo != null;

    // Create timezone: UTC-5 (New York)
    ny = datetime.createTimeZone(-5, 0, "EST");
    results.has_ny = ny != null;

    // Create timezone: UTC+5:30 (India)
    india = datetime.createTimeZone(5, 30, "IST");
    results.has_india = india != null;

    return results;
}

function test_timezone_aware_datetime() {
    results = {};

    // Create datetime with timezone
    utc = datetime.utc();
    dt = datetime.now(utc);

    results.has_datetime = dt != null;
    results.has_components = dt.year() > 2020;

    return results;
}

function main() {
    all_results = {};

    all_results.utc = test_utc_timezone();
    all_results.custom = test_custom_timezone();
    all_results.aware = test_timezone_aware_datetime();

    return all_results;
}

// Run tests
test_results = main();
