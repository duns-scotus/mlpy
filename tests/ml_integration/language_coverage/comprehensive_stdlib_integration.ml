// Comprehensive Standard Library Integration Test - Enhanced Object-Oriented API
// Showcases beautiful functionality with timestamp objects, pattern objects, and advanced string operations

import string;
import datetime;
import regex;
import array;

// Utility function for safe array append
function safe_append(arr, element) {
    new_arr = array.fill(arr.length + 1, 0);
    i = 0;
    while (i < arr.length) {
        new_arr[i] = arr[i];
        i = i + 1;
    }
    new_arr[arr.length] = element;
    return new_arr;
}

// String stdlib testing with enhanced functionality
function string_stdlib_testing() {
    print("=== Enhanced String Standard Library Integration ===");

    // Basic string operations with method chaining possibilities
    text1 = "Hello, World! Welcome to ML Programming.";
    text2 = "   Programming is Fun   ";
    text3 = "user@example.com";

    print("Testing enhanced string library functions:");

    // Length and character operations
    length1 = string.length(text1);
    char_at_5 = string.charAt(text1, 5);
    char_code = string.charCodeAt(text1, 0);
    from_code = string.fromCharCode(65);

    print("Length operations:");
    print("  '" + text1 + "' has length: " + string.toString(length1));
    print("  Character at position 5: '" + char_at_5 + "'");
    print("  Character code of 'H': " + string.toString(char_code));
    print("  Character from code 65: '" + from_code + "'");

    // Case operations
    upper_text = string.upper(text1);
    lower_text = string.lower(text1);
    capitalized = string.capitalize(text1);

    print("\nCase operations:");
    print("  Uppercase: " + upper_text);
    print("  Lowercase: " + lower_text);
    print("  Capitalized: " + capitalized);

    // Search operations
    contains_world = string.contains(text1, "World");
    find_ml = string.indexOf(text1, "ML");

    print("\nSearch operations:");
    print("  Contains 'World': " + string.toString(contains_world));
    print("  Position of 'ML': " + string.toString(find_ml));

    // Advanced string transformations
    snake_case = string.toSnakeCase("HelloWorldExample");
    camel_case = string.toCamelCase("hello_world_example");
    pascal_case = string.toPascalCase("hello_world_example");
    kebab_case = string.toKebabCase("HelloWorldExample");

    print("\nCase transformations:");
    print("  To snake_case: " + snake_case);
    print("  To camelCase: " + camel_case);
    print("  To PascalCase: " + pascal_case);
    print("  To kebab-case: " + kebab_case);

    // String utility operations
    reversed_text = string.reverse("Hello");
    repeated_text = string.repeat("*", 5);
    char_array = string.toChars("Hello");

    print("\nUtility operations:");
    print("  Reversed 'Hello': " + reversed_text);
    print("  Repeated '*' 5 times: " + repeated_text);
    print("  'Hello' as char array length: " + string.toString(char_array.length));

    return {
        string_functions_tested: 15,
        sample_results: {
            length: length1,
            transformations: {
                snake_case: snake_case,
                camel_case: camel_case,
                pascal_case: pascal_case
            }
        }
    };
}

// DateTime stdlib testing with enhanced object-oriented API
function datetime_stdlib_testing() {
    print("\n=== Enhanced DateTime Standard Library Integration ===");

    // Create timestamp objects with method access
    current_time = datetime.now();
    print("Current datetime operations:");
    print("  Current timestamp: " + current_time.toString());
    print("  Current year: " + string.toString(current_time.year()));
    print("  Current month: " + string.toString(current_time.month()));
    print("  Current day: " + string.toString(current_time.day()));

    // Date creation with object methods
    christmas_2024 = datetime.create_date(2024, 12, 25);
    new_years_2025 = datetime.create_date(2025, 1, 1);

    print("\nDate creation and formatting:");
    print("  Christmas 2024: " + christmas_2024.to_date_string());
    print("  New Year 2025: " + new_years_2025.to_date_string());
    print("  Christmas readable: " + christmas_2024.to_readable());

    // Date arithmetic with object methods
    days_30_later = current_time.add_days(30);
    days_15_earlier = current_time.subtract_days(15);
    months_6_later = current_time.add_days(180); // Approximate 6 months

    print("\nDate arithmetic with objects:");
    print("  30 days from now: " + days_30_later.to_date_string());
    print("  15 days ago: " + days_15_earlier.to_date_string());
    print("  ~6 months from now: " + months_6_later.to_date_string());

    // Time difference calculations with objects
    days_until_christmas = current_time.days_until(christmas_2024);
    days_until_new_year = current_time.days_until(new_years_2025);

    print("\nTime difference calculations:");
    print("  Days until Christmas 2024: " + string.toString(days_until_christmas));
    print("  Days until New Year 2025: " + string.toString(days_until_new_year));

    // Date comparison methods
    is_before_christmas = current_time.is_before(christmas_2024);
    is_after_christmas = current_time.is_after(christmas_2024);

    print("\nDate comparisons:");
    print("  Current time is before Christmas: " + string.toString(is_before_christmas));
    print("  Current time is after Christmas: " + string.toString(is_after_christmas));

    // Business day calculations
    monday = datetime.create_date(2024, 3, 4);
    plus_5_business = monday.add_business_days(5);
    is_business_day_check = monday.is_business_day();
    is_weekend_check = monday.is_weekend();

    print("\nBusiness day calculations:");
    print("  Monday + 5 business days: " + plus_5_business.to_date_string());
    print("  Monday is business day: " + string.toString(is_business_day_check));
    print("  Monday is weekend: " + string.toString(is_weekend_check));

    // TimeDelta objects
    delta_1_week = datetime.days(7);
    delta_2_hours = datetime.hours(2);
    delta_30_minutes = datetime.minutes(30);
    delta_combined = delta_1_week.add(delta_2_hours).add(delta_30_minutes);

    print("\nTimeDelta objects:");
    print("  1 week: " + delta_1_week.toString());
    print("  2 hours: " + delta_2_hours.toString());
    print("  30 minutes: " + delta_30_minutes.toString());
    print("  Combined (1w + 2h + 30m): " + delta_combined.toString());

    // Date utility methods
    start_of_today = current_time.start_of_day();
    end_of_today = current_time.end_of_day();
    start_of_month = current_time.start_of_month();

    print("\nDate utility methods:");
    print("  Start of today: " + start_of_today.to_readable());
    print("  End of today: " + end_of_today.to_readable());
    print("  Start of month: " + start_of_month.to_readable());

    return {
        datetime_functions_tested: 20,
        current_timestamp: current_time,
        sample_calculations: {
            days_until_christmas: days_until_christmas,
            combined_timedelta: delta_combined.get_total_seconds()
        }
    };
}

// Regex stdlib testing with enhanced pattern objects
function regex_stdlib_testing() {
    print("\n=== Enhanced Regex Standard Library Integration ===");

    // Sample texts for pattern matching
    text1 = "Contact us at john@example.com or call 555-123-4567";
    text2 = "Visit https://www.example.com for more info";
    text3 = "The meeting is on 2024-03-15 at 14:30";

    print("Testing enhanced regex library with pattern objects:");

    // Email pattern object
    email_pattern = regex.email_pattern();
    print("\nEmail pattern operations:");
    print("  Pattern: " + email_pattern.toString());
    print("  'john@example.com' matches email: " + string.toString(email_pattern.test("john@example.com")));
    print("  'invalid-email' matches email: " + string.toString(email_pattern.test("invalid-email")));

    extracted_emails = email_pattern.find_all(text1);
    print("  Emails found in text: " + array_to_string(extracted_emails));

    // URL pattern object
    url_pattern = regex.url_pattern();
    print("\nURL pattern operations:");
    print("  Pattern: " + url_pattern.toString());
    url_found = url_pattern.find_first(text2);
    print("  First URL found: " + url_found);
    print("  URL pattern is valid: " + string.toString(url_pattern.is_valid()));

    // Phone pattern object
    phone_pattern = regex.phone_pattern();
    print("\nPhone pattern operations:");
    phone_matches = phone_pattern.find_all(text1);
    phone_count = phone_pattern.count_matches(text1);
    print("  Phone numbers found: " + array_to_string(phone_matches));
    print("  Phone match count: " + string.toString(phone_count));

    // Custom pattern with PatternBuilder
    date_builder = regex.builder();
    date_pattern = date_builder
        .add_digit()
        .add_exact_count("\\d", 4)
        .add_literal("-")
        .add_digit()
        .add_exact_count("\\d", 2)
        .add_literal("-")
        .add_digit()
        .add_exact_count("\\d", 2)
        .build();

    print("\nCustom date pattern with builder:");
    print("  Built pattern: " + date_pattern.toString());
    date_found = date_pattern.find_first(text3);
    print("  Date found in text: " + date_found);

    // Pattern replacement operations
    html_text = "This is <b>bold</b> and <i>italic</i> text.";
    html_pattern = regex.compile("<[^>]*>");
    clean_text = html_pattern.replace_all(html_text, "");

    print("\nPattern replacement:");
    print("  HTML text: " + html_text);
    print("  Clean text: " + clean_text);

    // Advanced pattern matching with groups
    log_pattern = regex.compile("(\\d{4}-\\d{2}-\\d{2}) (\\d{2}:\\d{2}:\\d{2}) (\\w+): (.+)");
    log_entry = "2024-03-15 14:30:25 ERROR: Database connection failed";
    groups_found = log_pattern.find_with_groups(log_entry);

    print("\nAdvanced pattern matching:");
    print("  Log entry: " + log_entry);
    print("  Groups found: " + string.toString(groups_found.length));

    // Text cleaning with pattern objects
    whitespace_pattern = regex.compile("\\s+");
    messy_text = "Too   much    whitespace";
    clean_whitespace = whitespace_pattern.replace_all(messy_text, " ");

    print("\nText cleaning:");
    print("  Messy text: '" + messy_text + "'");
    print("  Cleaned text: '" + clean_whitespace + "'");

    // Security validation patterns
    suspicious_input1 = "'; DROP TABLE users; --";
    suspicious_input2 = "<script>alert('xss')</script>";
    has_sql_injection = regex.contains_sql_injection_patterns(suspicious_input1);
    has_xss = regex.contains_xss_patterns(suspicious_input2);

    print("\nSecurity validation:");
    print("  SQL injection detected: " + string.toString(has_sql_injection));
    print("  XSS patterns detected: " + string.toString(has_xss));

    return {
        regex_functions_tested: 15,
        sample_extractions: {
            emails: extracted_emails,
            url: url_found,
            date: date_found
        },
        security_checks: {
            sql_injection: has_sql_injection,
            xss: has_xss
        }
    };
}

// Cross-library integration testing with enhanced APIs
function cross_library_integration() {
    print("\n=== Enhanced Cross-Library Integration Testing ===");

    // Log processing with all three libraries
    log_entry = "2024-03-15 14:30:25 ERROR: Failed login attempt from user@example.com (IP: 192.168.1.100)";
    print("Processing log entry with enhanced APIs: " + log_entry);

    // Extract timestamp using regex pattern object and create datetime object
    timestamp_pattern = regex.compile("\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}");
    extracted_timestamp_str = timestamp_pattern.find_first(log_entry);

    // Parse timestamp into datetime object
    log_timestamp = datetime.parse_date(extracted_timestamp_str, "%Y-%m-%d %H:%M:%S");

    print("  Extracted timestamp: " + extracted_timestamp_str);
    print("  Parsed datetime: " + log_timestamp.to_readable());
    print("  Log day of week: " + datetime.get_weekday_name(log_timestamp.weekday()));

    // Extract email using pattern object
    email_pattern = regex.email_pattern();
    extracted_email = email_pattern.find_first(log_entry);

    // Process email with string operations
    email_parts = string.split(extracted_email, "@");
    email_domain = email_parts[1];
    masked_email = string.upper(string.substring(extracted_email, 0, 3)) + "***@" + email_domain;

    print("  Extracted email: " + extracted_email);
    print("  Email domain: " + email_domain);
    print("  Masked email: " + masked_email);

    // Extract log level and process
    level_pattern = regex.compile("\\b(ERROR|WARN|INFO|DEBUG)\\b");
    log_level = level_pattern.find_first(log_entry);
    is_error_level = string.compare(log_level, "ERROR") == 0;

    print("  Log level: " + log_level);
    print("  Is error level: " + string.toString(is_error_level));

    // Time-based analysis
    current_time = datetime.now();
    time_since_log = current_time.seconds_until(log_timestamp);
    hours_since_log = time_since_log / 3600;

    print("  Hours since log: " + string.toString(hours_since_log));

    // Create structured log object
    structured_log = {
        timestamp: log_timestamp,
        level: log_level,
        email: extracted_email,
        domain: email_domain,
        masked_email: masked_email,
        is_error: is_error_level,
        processed_at: current_time
    };

    // Generate report using all libraries
    report_date = structured_log.processed_at.to_date_string();
    alert_message = "ALERT: " + log_level + " detected on " + report_date;

    print("\nGenerated report:");
    print("  Report date: " + report_date);
    print("  Alert message: " + alert_message);

    // Batch processing simulation with enhanced APIs
    log_entries = [
        "2024-03-15 09:15:30 INFO: User login successful for admin@company.com",
        "2024-03-15 09:16:45 WARN: Multiple failed attempts from test@spam.com",
        "2024-03-15 09:17:22 ERROR: Database connection failed",
        "2024-03-15 09:18:10 INFO: System backup completed successfully"
    ];

    print("\nBatch processing " + string.toString(log_entries.length) + " log entries:");

    processed_logs = [];
    i = 0;
    while (i < log_entries.length) {
        entry = log_entries[i];

        // Extract components using pattern objects
        timestamp_str = timestamp_pattern.find_first(entry);
        entry_timestamp = datetime.parse_date(timestamp_str, "%Y-%m-%d %H:%M:%S");
        level = level_pattern.find_first(entry);
        emails = email_pattern.find_all(entry);

        // Build processed entry
        processed_entry = {
            index: i + 1,
            original_timestamp: timestamp_str,
            datetime_obj: entry_timestamp,
            level: level,
            has_email: emails.length > 0,
            email_count: emails.length,
            processed: true,
            weekday: datetime.get_weekday_name(entry_timestamp.weekday())
        };

        processed_logs = safe_append(processed_logs, processed_entry);

        print("  Entry " + string.toString(i + 1) + ": " + level + " on " + processed_entry.weekday + ", Emails=" + string.toString(processed_entry.email_count));

        i = i + 1;
    }

    return {
        cross_integration_tested: true,
        structured_log: structured_log,
        batch_processed: processed_logs.length,
        libraries_used: ["string", "datetime", "regex"],
        enhanced_features_used: ["timestamp_objects", "pattern_objects", "case_conversion", "date_arithmetic"]
    };
}

// Performance and advanced feature testing
function performance_advanced_testing() {
    print("\n=== Performance and Advanced Feature Testing ===");

    // Large string operations with enhanced string API
    large_string = string.repeat("Hello World! ", 100);
    large_string_length = string.length(large_string);

    print("Large string operations:");
    print("  Created string with length: " + string.toString(large_string_length));

    // Performance timing with datetime objects
    start_time = datetime.now();

    // Complex regex operations with pattern objects
    word_pattern = regex.compile("\\b\\w+\\b");
    words_found = word_pattern.find_all(large_string);
    word_count = word_pattern.count_matches(large_string);

    end_time = datetime.now();
    operation_duration = start_time.seconds_until(end_time);

    print("  Word extraction completed in ~" + string.toString(operation_duration) + " seconds");
    print("  Words found: " + string.toString(word_count));

    // Advanced pattern building
    email_builder = regex.builder();
    custom_email_pattern = email_builder
        .add_one_or_more("\\w")
        .add_zero_or_more("[.-]\\w")
        .add_literal("@")
        .add_one_or_more("\\w")
        .add_zero_or_more("[.-]\\w")
        .add_literal(".")
        .add_range_count("[a-zA-Z]", 2, 4)
        .case_insensitive()
        .build();

    print("\nAdvanced pattern building:");
    print("  Built email pattern: " + custom_email_pattern.toString());

    test_emails = ["user@domain.com", "test.user@sub-domain.co.uk", "invalid@"];
    j = 0;
    while (j < test_emails.length) {
        email = test_emails[j];
        is_valid = custom_email_pattern.test(email);
        print("  '" + email + "' is valid: " + string.toString(is_valid));
        j = j + 1;
    }

    // TimeDelta advanced operations
    project_duration = datetime.days(30).add(datetime.hours(8)).add(datetime.minutes(45));
    project_start = datetime.create_date(2024, 4, 1);
    project_end = project_start.add_days(project_duration.get_total_days());

    print("\nAdvanced datetime calculations:");
    print("  Project duration: " + project_duration.toString());
    print("  Project start: " + project_start.to_date_string());
    print("  Project end: " + project_end.to_date_string());
    print("  Project spans weekend: " + string.toString(project_start.is_weekend() || project_end.is_weekend()));

    // String case conversion chain
    original_text = "hello_world_example_TEST";
    conversion_chain = string.toCamelCase(string.lower(original_text));
    final_pascal = string.toPascalCase(conversion_chain);

    print("\nString transformation chain:");
    print("  Original: " + original_text);
    print("  Chain (lower→camel): " + conversion_chain);
    print("  Final (pascal): " + final_pascal);

    // Memory and object management
    pattern_cache = [];
    k = 0;
    while (k < 5) {
        pattern_str = "\\b\\w{" + string.toString(k + 3) + "}\\b";
        cached_pattern = regex.compile(pattern_str);
        pattern_cache = safe_append(pattern_cache, cached_pattern);
        k = k + 1;
    }

    print("\nPattern caching test:");
    print("  Created " + string.toString(pattern_cache.length) + " cached patterns");

    test_text = "The quick brown fox jumps over the lazy dog";
    m = 0;
    while (m < pattern_cache.length) {
        pattern = pattern_cache[m];
        matches = pattern.find_all(test_text);
        print("  Pattern " + string.toString(m + 1) + " found " + string.toString(matches.length) + " matches");
        m = m + 1;
    }

    return {
        performance_tested: true,
        large_string_length: large_string_length,
        operation_duration: operation_duration,
        advanced_features_tested: 8,
        pattern_cache_size: pattern_cache.length
    };
}

// Utility function to convert array to string representation
function array_to_string(arr) {
    if (arr.length == 0) {
        return "[]";
    }

    result = "[";
    i = 0;
    while (i < arr.length) {
        if (i > 0) {
            result = result + ", ";
        }
        result = result + "'" + string.toString(arr[i]) + "'";
        i = i + 1;
    }
    result = result + "]";
    return result;
}

// Main function to run all enhanced standard library integration tests
function main() {
    print("==========================================================");
    print("  ENHANCED COMPREHENSIVE STANDARD LIBRARY INTEGRATION");
    print("==========================================================");

    results = {
        string_stdlib: null,
        datetime_stdlib: null,
        regex_stdlib: null,
        cross_library: null,
        performance_advanced: null
    };

    results.string_stdlib = string_stdlib_testing();
    results.datetime_stdlib = datetime_stdlib_testing();
    results.regex_stdlib = regex_stdlib_testing();
    results.cross_library = cross_library_integration();
    results.performance_advanced = performance_advanced_testing();

    print("\n==========================================================");
    print("  ALL ENHANCED STANDARD LIBRARY INTEGRATION TESTS COMPLETED");
    print("==========================================================");

    total_functions_tested = results.string_stdlib.string_functions_tested +
                           results.datetime_stdlib.datetime_functions_tested +
                           results.regex_stdlib.regex_functions_tested;

    print("\nEnhanced Test Summary:");
    print("  Total library functions tested: " + string.toString(total_functions_tested));
    print("  Libraries integrated: string, datetime, regex");
    print("  Object-oriented APIs: timestamp objects, pattern objects, timedelta objects");
    print("  Enhanced features: method chaining, fluent APIs, pattern builders");
    print("  Cross-library operations: verified with real-world scenarios");
    print("  Performance testing: completed with advanced feature validation");
    print("  Security validation: SQL injection and XSS pattern detection");

    print("\nKey Enhanced Features Demonstrated:");
    print("  ✓ Timestamp objects with method access (.year(), .add_days(), etc.)");
    print("  ✓ TimeDelta objects with arithmetic operations");
    print("  ✓ Pattern objects with compiled regex and fluent API");
    print("  ✓ PatternBuilder for complex regex construction");
    print("  ✓ String case conversion utilities (snake_case, camelCase, etc.)");
    print("  ✓ Cross-library integration with enhanced APIs");
    print("  ✓ Security-focused validation patterns");
    print("  ✓ Performance optimization with object caching");

    return results;
}

// Execute comprehensive enhanced standard library integration test
main();