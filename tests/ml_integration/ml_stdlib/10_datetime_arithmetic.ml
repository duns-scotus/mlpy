// Test stdlib module: datetime - TimeDelta and arithmetic operations
// Features tested: TimeDelta, date/time arithmetic, comparisons
// Module: datetime (version 2.0)

import datetime;

function test_timedelta_creation() {
    results = {};

    // Create timedelta
    delta1 = datetime.createDelta(7, 0, 0, 0);  // 7 days
    results.days = delta1.days();               // 7

    delta2 = datetime.createDelta(0, 5, 30, 0); // 5 hours 30 minutes
    results.seconds = delta2.seconds();         // 19800 (5*3600 + 30*60)

    return results;
}

function test_timedelta_conversions() {
    results = {};

    delta = datetime.createDelta(1, 2, 30, 0);  // 1 day, 2 hours, 30 min

    results.total_seconds = delta.totalSeconds();   // ~95400
    results.total_minutes = delta.totalMinutes();   // ~1590
    results.total_hours = delta.totalHours();       // ~26.5
    results.total_days = delta.totalDays();         // ~1.1

    return results;
}

function test_date_arithmetic() {
    results = {};

    d = datetime.createDate(2025, 10, 1);

    // Add days
    d_plus_7 = d.addDays(7);
    results.add_day = d_plus_7.day();           // 8
    results.add_month = d_plus_7.month();       // 10

    // Subtract days
    d_minus_5 = d.subtractDays(5);
    results.sub_day = d_minus_5.day();          // 26
    results.sub_month = d_minus_5.month();      // 9

    // Difference between dates
    d1 = datetime.createDate(2025, 10, 10);
    d2 = datetime.createDate(2025, 10, 1);
    diff = d1.diff(d2);
    results.diff_days = diff;                   // 9

    return results;
}

function test_datetime_arithmetic() {
    results = {};

    dt = datetime.create(2025, 10, 5, 12, 0, 0);
    delta = datetime.createDelta(1, 3, 0, 0);   // 1 day, 3 hours

    // Add timedelta
    dt_plus = dt.add(delta);
    results.plus_day = dt_plus.day();           // 6
    results.plus_hour = dt_plus.hour();         // 15

    // Subtract timedelta
    dt_minus = dt.subtract(delta);
    results.minus_day = dt_minus.day();         // 4
    results.minus_hour = dt_minus.hour();       // 9

    return results;
}

function test_datetime_diff() {
    results = {};

    dt1 = datetime.create(2025, 10, 10, 14, 0, 0);
    dt2 = datetime.create(2025, 10, 5, 12, 0, 0);

    diff = dt1.diff(dt2);
    results.diff_days = diff.days();            // 5
    results.diff_seconds = diff.seconds();      // 7200 (2 hours)

    return results;
}

function test_datetime_comparison() {
    results = {};

    dt1 = datetime.create(2025, 10, 5, 12, 0, 0);
    dt2 = datetime.create(2025, 10, 10, 12, 0, 0);

    results.is_before = dt1.isBefore(dt2);      // true
    results.is_after = dt1.isAfter(dt2);        // false
    results.is_same = dt1.isSame(dt1);          // true

    return results;
}

function test_timedelta_arithmetic() {
    results = {};

    delta1 = datetime.createDelta(5, 0, 0, 0);  // 5 days
    delta2 = datetime.createDelta(3, 0, 0, 0);  // 3 days

    // Add deltas
    sum = delta1.add(delta2);
    results.sum_days = sum.days();              // 8

    // Subtract deltas
    diff = delta1.subtract(delta2);
    results.diff_days = diff.days();            // 2

    // Multiply delta
    doubled = delta1.multiply(2.0);
    results.double_days = doubled.days();       // 10

    return results;
}

function test_timedelta_properties() {
    results = {};

    // Positive delta
    delta_pos = datetime.createDelta(5, 0, 0, 0);
    results.is_neg_pos = delta_pos.isNegative(); // false

    // Negative delta (created via subtraction)
    dt1 = datetime.create(2025, 10, 1, 0, 0, 0);
    dt2 = datetime.create(2025, 10, 10, 0, 0, 0);
    delta_neg = dt1.diff(dt2);
    results.is_neg_true = delta_neg.isNegative(); // true

    // Absolute value
    delta_abs = delta_neg.abs();
    results.abs_days = delta_abs.days();        // 9

    return results;
}

function main() {
    all_results = {};

    all_results.creation = test_timedelta_creation();
    all_results.conversions = test_timedelta_conversions();
    all_results.date_math = test_date_arithmetic();
    all_results.datetime_math = test_datetime_arithmetic();
    all_results.datetime_diff = test_datetime_diff();
    all_results.comparison = test_datetime_comparison();
    all_results.delta_math = test_timedelta_arithmetic();
    all_results.properties = test_timedelta_properties();

    return all_results;
}

// Run tests
test_results = main();
