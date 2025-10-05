// Test stdlib module: datetime - Date, Time, and DateTime objects
// Features tested: Date, Time, DateTime factory methods and component access
// Module: datetime (version 2.0)

import datetime;

function test_date_objects() {
    results = {};

    // Create date
    d = datetime.createDate(2025, 10, 5);
    results.year = d.year();            // 2025
    results.month = d.month();          // 10
    results.day = d.day();              // 5
    results.weekday = d.weekday();      // 0-6
    results.is_weekend = d.isWeekend(); // true or false

    // Today
    today = datetime.today();
    results.has_today = today.year() > 2020;

    return results;
}

function test_time_objects() {
    results = {};

    // Create time
    t = datetime.createTime(14, 30, 45, 0);
    results.hour = t.hour();            // 14
    results.minute = t.minute();        // 30
    results.second = t.second();        // 45

    return results;
}

function test_datetime_objects() {
    results = {};

    // Create datetime
    dt = datetime.create(2025, 10, 5, 14, 30, 0);
    results.year = dt.year();           // 2025
    results.month = dt.month();         // 10
    results.day = dt.day();             // 5
    results.hour = dt.hour();           // 14
    results.minute = dt.minute();       // 30
    results.second = dt.second();       // 0

    // Extract date and time
    d = dt.date();
    t = dt.time();
    results.date_year = d.year();       // 2025
    results.time_hour = t.hour();       // 14

    return results;
}

function test_datetime_now() {
    results = {};

    // Current datetime
    now = datetime.now();
    results.has_year = now.year() > 2020;
    results.has_month = now.month() >= 1 && now.month() <= 12;
    results.has_day = now.day() >= 1 && now.day() <= 31;

    return results;
}

function test_formatting() {
    results = {};

    // Date formatting
    d = datetime.createDate(2025, 10, 5);
    results.date_iso = d.toISOString();     // "2025-10-05"

    // DateTime formatting
    dt = datetime.create(2025, 10, 5, 14, 30, 0);
    results.dt_iso = dt.toISOString();      // Contains date and time

    return results;
}

function test_parse_iso() {
    results = {};

    // Parse ISO string
    dt = datetime.parseISO("2025-10-05T14:30:00");
    results.year = dt.year();               // 2025
    results.month = dt.month();             // 10
    results.day = dt.day();                 // 5
    results.hour = dt.hour();               // 14
    results.minute = dt.minute();           // 30

    return results;
}

function test_utilities() {
    results = {};

    // Days in month
    results.days_jan = datetime.daysInMonth(2025, 1);   // 31
    results.days_feb = datetime.daysInMonth(2025, 2);   // 28
    results.days_feb_leap = datetime.daysInMonth(2024, 2); // 29

    // Leap year
    results.leap_2024 = datetime.isLeapYear(2024);      // true
    results.leap_2025 = datetime.isLeapYear(2025);      // false

    return results;
}

function main() {
    all_results = {};

    all_results.date = test_date_objects();
    all_results.time = test_time_objects();
    all_results.datetime = test_datetime_objects();
    all_results.now = test_datetime_now();
    all_results.formatting = test_formatting();
    all_results.parsing = test_parse_iso();
    all_results.utilities = test_utilities();

    return all_results;
}

// Run tests
test_results = main();
