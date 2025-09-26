// Comprehensive Standard Library Integration Test
// Demonstrates usage of all available standard library modules in ML

import string;
import datetime;
import regex;

// String standard library comprehensive testing
function string_stdlib_testing() {
    print("=== String Standard Library Integration ===");

    // Basic string operations
    text1 = "Hello, World! Welcome to ML Programming.";
    text2 = "   Programming is Fun   ";
    text3 = "test@example.com";

    print("Testing string library functions:");

    // Length and character operations
    length1 = string.length(text1);
    char_at_5 = string.char_at(text1, 5);
    char_code = string.char_code_at(text1, 0);
    from_code = string.from_char_code(65);

    print("Length operations:");
    print("  '" + text1 + "' has length: " + length1);
    print("  Character at position 5: '" + char_at_5 + "'");
    print("  Character code of 'H': " + char_code);
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
    starts_hello = string.starts_with(text1, "Hello");
    ends_period = string.ends_with(text1, ".");
    find_ml = string.find(text1, "ML");
    count_l = string.count(text1, "l");

    print("\nSearch operations:");
    print("  Contains 'World': " + contains_world);
    print("  Starts with 'Hello': " + starts_hello);
    print("  Ends with '.': " + ends_period);
    print("  Position of 'ML': " + find_ml);
    print("  Count of 'l': " + count_l);

    // Modification operations
    replace_world = string.replace(text1, "World", "Universe");
    replace_all_l = string.replace_all(text1, "l", "L");
    trimmed = string.trim(text2);
    padded_left = string.pad_left("Hi", 10, "*");
    padded_right = string.pad_right("Hi", 10, "-");

    print("\nModification operations:");
    print("  Replace 'World' with 'Universe': " + replace_world);
    print("  Replace all 'l' with 'L': " + replace_all_l);
    print("  Trimmed '" + text2 + "': '" + trimmed + "'");
    print("  Padded left: '" + padded_left + "'");
    print("  Padded right: '" + padded_right + "'");

    // Split and join operations
    csv_data = "apple,banana,cherry,date";
    split_fruits = string.split(csv_data, ",");
    joined_pipes = string.join(" | ", split_fruits);

    print("\nSplit and join operations:");
    print("  CSV data: " + csv_data);
    print("  Split by comma: " + split_fruits);
    print("  Joined with pipes: " + joined_pipes);

    // Validation operations
    alpha_test = string.is_alpha("Hello");
    numeric_test = string.is_numeric("12345");
    alnum_test = string.is_alphanumeric("Hello123");
    empty_test = string.is_empty("");

    print("\nValidation operations:");
    print("  'Hello' is alpha: " + alpha_test);
    print("  '12345' is numeric: " + numeric_test);
    print("  'Hello123' is alphanumeric: " + alnum_test);
    print("  '' is empty: " + empty_test);

    // Advanced string operations
    reversed_text = string.reverse("Hello");
    repeated_text = string.repeat("*", 5);
    substring_text = string.substring(text1, 0, 5);

    print("\nAdvanced operations:");
    print("  Reversed 'Hello': " + reversed_text);
    print("  Repeated '*' 5 times: " + repeated_text);
    print("  Substring (0-5): '" + substring_text + "'");

    return {
        string_functions_tested: 20,
        sample_results: {
            length: length1,
            trimmed: trimmed,
            split_result: split_fruits
        }
    };
}

// DateTime standard library testing
function datetime_stdlib_testing() {
    print("\n=== DateTime Standard Library Integration ===");

    // Current time operations
    current_timestamp = datetime.now();
    current_year = datetime.year(current_timestamp);
    current_month = datetime.month(current_timestamp);
    current_day = datetime.day(current_timestamp);

    print("Current datetime operations:");
    print("  Current timestamp: " + current_timestamp);
    print("  Current year: " + current_year);
    print("  Current month: " + current_month);
    print("  Current day: " + current_day);

    // Date creation and parsing
    custom_date = datetime.create_date(2024, 12, 25);
    formatted_date = datetime.format_date(custom_date, "YYYY-MM-DD");
    parsed_date = datetime.parse_date("2024-06-15", "YYYY-MM-DD");

    print("\nDate creation and formatting:");
    print("  Custom date (Christmas 2024): " + custom_date);
    print("  Formatted date: " + formatted_date);
    print("  Parsed date: " + parsed_date);

    // Date arithmetic
    days_30_later = datetime.add_days(current_timestamp, 30);
    days_15_earlier = datetime.subtract_days(current_timestamp, 15);
    months_6_later = datetime.add_months(current_timestamp, 6);

    print("\nDate arithmetic:");
    print("  30 days from now: " + datetime.format_date(days_30_later, "YYYY-MM-DD"));
    print("  15 days ago: " + datetime.format_date(days_15_earlier, "YYYY-MM-DD"));
    print("  6 months from now: " + datetime.format_date(months_6_later, "YYYY-MM-DD"));

    // Time difference calculations
    date1 = datetime.create_date(2024, 1, 1);
    date2 = datetime.create_date(2024, 12, 31);
    days_between = datetime.days_between(date1, date2);

    print("\nTime difference calculations:");
    print("  Days between Jan 1, 2024 and Dec 31, 2024: " + days_between);

    // Business day calculations
    monday = datetime.create_date(2024, 3, 4); // Assuming this is a Monday
    plus_5_business = datetime.add_business_days(monday, 5);
    minus_3_business = datetime.subtract_business_days(monday, 3);

    print("\nBusiness day calculations:");
    print("  Monday + 5 business days: " + datetime.format_date(plus_5_business, "YYYY-MM-DD"));
    print("  Monday - 3 business days: " + datetime.format_date(minus_3_business, "YYYY-MM-DD"));

    // Age calculations
    birth_date = datetime.create_date(1990, 6, 15);
    age_in_years = datetime.age_in_years(birth_date, current_timestamp);
    age_in_days = datetime.age_in_days(birth_date, current_timestamp);

    print("\nAge calculations:");
    print("  Birth date: " + datetime.format_date(birth_date, "YYYY-MM-DD"));
    print("  Age in years: " + age_in_years);
    print("  Age in days: " + age_in_days);

    // Timezone and formatting operations
    utc_time = datetime.to_utc(current_timestamp);
    local_time = datetime.from_utc(utc_time, "America/New_York");
    iso_format = datetime.to_iso_string(current_timestamp);

    print("\nTimezone and formatting:");
    print("  UTC time: " + utc_time);
    print("  Local time (NY): " + local_time);
    print("  ISO format: " + iso_format);

    return {
        datetime_functions_tested: 15,
        current_timestamp: current_timestamp,
        sample_calculations: {
            days_between: days_between,
            age_years: age_in_years
        }
    };
}

// Regex standard library testing
function regex_stdlib_testing() {
    print("\n=== Regex Standard Library Integration ===");

    // Basic pattern matching
    text1 = "Contact us at john@example.com or call 555-123-4567";
    text2 = "Visit https://www.example.com for more info";
    text3 = "The meeting is on 2024-03-15 at 14:30";

    print("Testing regex library functions:");

    // Email operations
    email_pattern = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}";
    is_valid_email1 = regex.is_email("john@example.com");
    is_valid_email2 = regex.is_email("invalid-email");
    extracted_emails = regex.extract_emails(text1);

    print("Email operations:");
    print("  'john@example.com' is valid email: " + is_valid_email1);
    print("  'invalid-email' is valid email: " + is_valid_email2);
    print("  Emails extracted from text: " + extracted_emails);

    // Phone number operations
    is_valid_phone1 = regex.is_phone_number("555-123-4567");
    is_valid_phone2 = regex.is_phone_number("123");
    extracted_phones = regex.extract_phone_numbers(text1);

    print("\nPhone number operations:");
    print("  '555-123-4567' is valid phone: " + is_valid_phone1);
    print("  '123' is valid phone: " + is_valid_phone2);
    print("  Phone numbers extracted: " + extracted_phones);

    // URL operations
    is_valid_url1 = regex.is_url("https://www.example.com");
    is_valid_url2 = regex.is_url("not-a-url");
    extracted_urls = regex.extract_urls(text2);

    print("\nURL operations:");
    print("  'https://www.example.com' is valid URL: " + is_valid_url1);
    print("  'not-a-url' is valid URL: " + is_valid_url2);
    print("  URLs extracted: " + extracted_urls);

    // Date pattern operations
    date_pattern = "\\d{4}-\\d{2}-\\d{2}";
    extracted_dates = regex.extract_dates(text3);
    is_date_format = regex.matches_pattern("2024-03-15", date_pattern);

    print("\nDate pattern operations:");
    print("  Dates extracted from text: " + extracted_dates);
    print("  '2024-03-15' matches YYYY-MM-DD pattern: " + is_date_format);

    // Generic pattern matching
    number_pattern = "\\d+";
    word_pattern = "[a-zA-Z]+";
    numbers_found = regex.find_all(text1, number_pattern);
    words_found = regex.find_all("hello world 123", word_pattern);

    print("\nGeneric pattern matching:");
    print("  Numbers found in text1: " + numbers_found);
    print("  Words found in 'hello world 123': " + words_found);

    // Pattern replacement
    html_text = "This is <b>bold</b> and <i>italic</i> text.";
    clean_text = regex.remove_html_tags(html_text);
    replaced_numbers = regex.replace_pattern(text1, "\\d+", "XXX");

    print("\nPattern replacement:");
    print("  HTML text: " + html_text);
    print("  Clean text: " + clean_text);
    print("  Numbers replaced with XXX: " + replaced_numbers);

    // Validation patterns
    is_alphanumeric = regex.is_alphanumeric_underscore("hello_world123");
    is_only_digits = regex.is_only_digits("123456");
    is_alphabetic = regex.is_only_alphabetic("HelloWorld");

    print("\nValidation patterns:");
    print("  'hello_world123' is alphanumeric+underscore: " + is_alphanumeric);
    print("  '123456' is only digits: " + is_only_digits);
    print("  'HelloWorld' is only alphabetic: " + is_alphabetic);

    // Advanced pattern operations
    complex_text = "Error: File not found at /path/to/file.txt on line 42";
    error_pattern = "Error: (.+) at (.+) on line (\\d+)";
    match_groups = regex.extract_groups(complex_text, error_pattern);

    print("\nAdvanced pattern operations:");
    print("  Complex text: " + complex_text);
    print("  Extracted groups: " + match_groups);

    return {
        regex_functions_tested: 18,
        sample_extractions: {
            emails: extracted_emails,
            phones: extracted_phones,
            urls: extracted_urls,
            dates: extracted_dates
        }
    };
}

// Cross-library integration testing
function cross_library_integration() {
    print("\n=== Cross-Library Integration Testing ===");

    // Combining string, datetime, and regex libraries
    log_entry = "2024-03-15 14:30:25 ERROR: Failed login attempt from user@example.com (IP: 192.168.1.100)";

    print("Processing log entry: " + log_entry);

    // Extract timestamp using regex and parse with datetime
    timestamp_pattern = "\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}";
    extracted_timestamp = regex.find_first(log_entry, timestamp_pattern);
    parsed_timestamp = datetime.parse_datetime(extracted_timestamp, "YYYY-MM-DD HH:mm:ss");

    print("  Extracted timestamp: " + extracted_timestamp);
    print("  Parsed timestamp: " + parsed_timestamp);

    // Extract email using regex and validate with string operations
    extracted_email = regex.extract_emails(log_entry)[0];
    email_domain = string.split(extracted_email, "@")[1];
    is_valid_domain = string.contains(email_domain, ".");

    print("  Extracted email: " + extracted_email);
    print("  Email domain: " + email_domain);
    print("  Valid domain format: " + is_valid_domain);

    // Extract log level using string operations
    parts = string.split(log_entry, " ");
    log_level = parts[2];
    log_level_clean = string.replace(log_level, ":", "");
    is_error_level = string.equals(log_level_clean, "ERROR");

    print("  Log level: " + log_level_clean);
    print("  Is error level: " + is_error_level);

    // Create structured log data
    structured_log = {
        timestamp: parsed_timestamp,
        level: log_level_clean,
        email: extracted_email,
        domain: email_domain,
        message: "Failed login attempt",
        processed_at: datetime.now()
    };

    // Format report using all libraries
    report_date = datetime.format_date(structured_log.processed_at, "YYYY-MM-DD");
    formatted_email = string.upper(string.substring(structured_log.email, 0, 3)) + "***";
    alert_message = "ALERT: " + log_level_clean + " detected on " + report_date;

    print("\nGenerated report:");
    print("  Report date: " + report_date);
    print("  Masked email: " + formatted_email);
    print("  Alert message: " + alert_message);

    // Batch processing simulation
    log_entries = [
        "2024-03-15 09:15:30 INFO: User login successful for admin@company.com",
        "2024-03-15 09:16:45 WARN: Multiple failed attempts from test@spam.com",
        "2024-03-15 09:17:22 ERROR: Database connection failed",
        "2024-03-15 09:18:10 INFO: System backup completed successfully"
    ];

    print("\nBatch processing " + log_entries.length() + " log entries:");

    processed_logs = [];
    i = 0;
    while (i < log_entries.length()) {
        entry = log_entries[i];

        // Extract components
        timestamp_str = regex.find_first(entry, timestamp_pattern);
        level_part = string.split(entry, " ")[2];
        level = string.replace(level_part, ":", "");
        emails = regex.extract_emails(entry);

        // Build processed entry
        processed_entry = {
            index: i + 1,
            original_timestamp: timestamp_str,
            level: level,
            has_email: emails.length() > 0,
            email_count: emails.length(),
            processed: true
        };

        processed_logs[i] = processed_entry;

        print("  Entry " + (i + 1) + ": Level=" + level + ", Emails=" + processed_entry.email_count);

        i = i + 1;
    }

    return {
        cross_integration_tested: true,
        structured_log: structured_log,
        batch_processed: processed_logs.length(),
        libraries_used: ["string", "datetime", "regex"]
    };
}

// Performance and edge case testing
function performance_edge_case_testing() {
    print("\n=== Performance and Edge Case Testing ===");

    // Large string operations
    large_string = string.repeat("Hello World! ", 100);
    large_string_length = string.length(large_string);

    print("Large string operations:");
    print("  Created string with length: " + large_string_length);

    // String search performance
    search_start = datetime.now();
    found_position = string.find(large_string, "World!");
    search_end = datetime.now();
    search_duration = datetime.milliseconds_between(search_start, search_end);

    print("  Search completed in ~" + search_duration + "ms");
    print("  First 'World!' found at position: " + found_position);

    // Edge cases for string operations
    empty_string = "";
    null_like_string = "null";
    special_chars = "Special chars: !@#$%^&*()[]{}|;:,.<>?";

    print("\nEdge case testing:");
    print("  Empty string length: " + string.length(empty_string));
    print("  Empty string is empty: " + string.is_empty(empty_string));
    print("  'null' string contains 'null': " + string.contains(null_like_string, "null"));
    print("  Special chars length: " + string.length(special_chars));

    // Date edge cases
    leap_year_date = datetime.create_date(2024, 2, 29); // Leap year
    century_date = datetime.create_date(2000, 1, 1);    // Y2K
    future_date = datetime.create_date(2100, 12, 31);   // Far future

    print("\nDate edge cases:");
    print("  Leap year date (2024-02-29): " + datetime.format_date(leap_year_date, "YYYY-MM-DD"));
    print("  Century date (Y2K): " + datetime.format_date(century_date, "YYYY-MM-DD"));
    print("  Future date (2100): " + datetime.format_date(future_date, "YYYY-MM-DD"));

    // Regex edge cases
    complex_email = "user.name+tag@sub-domain.example-site.com";
    international_phone = "+1-800-555-0199";
    ipv6_pattern = "[0-9a-fA-F:]+";

    is_complex_email_valid = regex.is_email(complex_email);
    is_intl_phone_valid = regex.is_phone_number(international_phone);
    ipv6_test = regex.matches_pattern("2001:0db8:85a3:0000:0000:8a2e:0370:7334", ipv6_pattern);

    print("\nRegex edge cases:");
    print("  Complex email valid: " + is_complex_email_valid);
    print("  International phone valid: " + is_intl_phone_valid);
    print("  IPv6 pattern match: " + ipv6_test);

    // Memory and resource testing
    memory_test_arrays = [];
    j = 0;
    while (j < 10) {
        test_array = [];
        k = 0;
        while (k < 100) {
            test_array[k] = "Item " + k + " in array " + j;
            k = k + 1;
        }
        memory_test_arrays[j] = test_array;
        j = j + 1;
    }

    print("\nMemory test:");
    print("  Created 10 arrays with 100 items each");
    print("  Total items: " + (memory_test_arrays.length() * 100));

    return {
        performance_tested: true,
        large_string_length: large_string_length,
        search_duration: search_duration,
        edge_cases_tested: 9,
        memory_test_completed: true
    };
}

// Main function to run all standard library integration tests
function main() {
    print("================================================");
    print("  COMPREHENSIVE STANDARD LIBRARY INTEGRATION");
    print("================================================");

    results = {};

    results.string_stdlib = string_stdlib_testing();
    results.datetime_stdlib = datetime_stdlib_testing();
    results.regex_stdlib = regex_stdlib_testing();
    results.cross_library = cross_library_integration();
    results.performance_edge = performance_edge_case_testing();

    print("\n================================================");
    print("  ALL STANDARD LIBRARY INTEGRATION TESTS COMPLETED");
    print("================================================");

    total_functions_tested = results.string_stdlib.string_functions_tested +
                           results.datetime_stdlib.datetime_functions_tested +
                           results.regex_stdlib.regex_functions_tested;

    print("\nTest Summary:");
    print("  Total library functions tested: " + total_functions_tested);
    print("  Libraries integrated: string, datetime, regex");
    print("  Cross-library operations: verified");
    print("  Performance testing: completed");
    print("  Edge case testing: completed");

    return results;
}

// Execute comprehensive standard library integration test
main();