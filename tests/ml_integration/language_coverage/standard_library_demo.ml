// Standard Library Demo
// Demonstrates string, datetime, and regex modules

import string;
import datetime;
import regex;

// String module demonstrations
function test_string_module() {
    print("=== STRING MODULE TESTS ===");

    // Basic string operations
    text = "  Hello, World!  ";
    print("Original: '" + text + "'");
    print("Length: " + string.length(text));
    print("Trimmed: '" + string.trim(text) + "'");
    print("Upper: " + string.upper(text));
    print("Lower: " + string.lower(text));

    // String search
    message = "The quick brown fox jumps over the lazy dog";
    print("Contains 'fox': " + string.contains(message, "fox"));
    print("Starts with 'The': " + string.starts_with(message, "The"));
    print("Ends with 'dog': " + string.ends_with(message, "dog"));
    print("Position of 'brown': " + string.find(message, "brown"));

    // String modification
    replaced = string.replace(message, "fox", "cat");
    print("Replaced fox with cat: " + replaced);

    all_replaced = string.replace_all(message, "the", "THE");
    print("All 'the' to 'THE': " + all_replaced);

    // String splitting and joining
    csv_data = "apple,banana,orange,grape";
    fruits = string.split(csv_data, ",");
    print("Split CSV: " + fruits);
    rejoined = string.join(" | ", fruits);
    print("Rejoined: " + rejoined);

    // Case conversion utilities
    test_text = "hello_world";
    print("Snake case: " + string.snake_case("HelloWorld"));
    print("Camel case: " + string.camel_case("hello_world"));
    print("Pascal case: " + string.pascal_case("hello_world"));
    print("Kebab case: " + string.kebab_case("HelloWorld"));

    // String validation
    print("Is empty '': " + string.is_empty(""));
    print("Is alpha 'Hello': " + string.is_alpha("Hello"));
    print("Is numeric '123': " + string.is_numeric("123"));
    print("Is alphanumeric 'abc123': " + string.is_alphanumeric("abc123"));

    // Character operations
    word = "Hello";
    print("First char: " + string.char_at(word, 0));
    print("Char code: " + string.char_code_at(word, 0));
    print("From char code 65: " + string.from_char_code(65));

    // String formatting - demonstration with safe template
    greeting_template = "Hello, world! Welcome to ML.";
    print("Template demo: " + greeting_template);
}

// DateTime module demonstrations
function test_datetime_module() {
    print("\n=== DATETIME MODULE TESTS ===");

    // Current time
    current_timestamp = datetime.now();
    print("Current timestamp: " + current_timestamp);

    current_string = datetime.utcnow();
    print("Current UTC string: " + current_string);

    // Date creation
    birthday = datetime.create_date(1990, 12, 25);
    print("Birthday timestamp: " + birthday);

    meeting = datetime.create_datetime(2024, 3, 15, 14, 30, 0);
    print("Meeting timestamp: " + meeting);

    // Date arithmetic
    today = datetime.now();
    next_week = datetime.add_days(today, 7);
    print("Next week: " + next_week);

    in_two_hours = datetime.add_hours(today, 2);
    print("In two hours: " + in_two_hours);

    // Date differences
    start_date = datetime.create_date(2024, 1, 1);
    end_date = datetime.create_date(2024, 12, 31);
    days_diff = datetime.days_between(start_date, end_date);
    print("Days in 2024: " + days_diff);

    hours_diff = datetime.hours_between(start_date, end_date);
    print("Hours in 2024: " + hours_diff);

    // Date components
    year = datetime.get_year(today);
    month = datetime.get_month(today);
    day = datetime.get_day(today);
    print("Today: Year=" + year + ", Month=" + month + ", Day=" + day);

    month_name = datetime.get_month_name(month);
    weekday = datetime.get_weekday(today);
    weekday_name = datetime.get_weekday_name(weekday);
    print("Month name: " + month_name + ", Weekday: " + weekday_name);

    // Date ranges
    start_of_day = datetime.start_of_day(today);
    end_of_month = datetime.end_of_month(today);
    print("Start of day: " + start_of_day);
    print("End of month: " + end_of_month);

    // Business days
    is_workday = datetime.is_business_day(today);
    print("Is today a business day: " + is_workday);

    next_business_day = datetime.add_business_days(today, 1);
    print("Next business day: " + next_business_day);

    // Age calculation
    birth_date = datetime.create_date(1990, 5, 15);
    age = datetime.age_in_years(birth_date, today);
    print("Age from 1990-05-15: " + age + " years");

    // Date validation
    is_valid = datetime.is_valid_date(2024, 2, 29);  // Leap year
    print("Is 2024-02-29 valid: " + is_valid);

    is_leap = datetime.is_leap_year(2024);
    print("Is 2024 a leap year: " + is_leap);
}

// Regex module demonstrations
function test_regex_module() {
    print("\n=== REGEX MODULE TESTS ===");

    // Basic pattern matching
    email_pattern = "^[\\w._%+-]+@[\\w.-]+\\.[A-Za-z]{2,}$";
    test_email = "user@example.com";
    is_valid_email = regex.test(email_pattern, test_email);
    print("'" + test_email + "' is valid email: " + is_valid_email);

    // Finding matches
    text = "Phone numbers: 123-456-7890, 987-654-3210";
    phone_pattern = "\\d{3}-\\d{3}-\\d{4}";
    first_phone = regex.find_first(phone_pattern, text);
    all_phones = regex.find_all(phone_pattern, text);
    print("First phone: " + first_phone);
    print("All phones: " + all_phones);

    // Pattern replacement
    message = "Hello world, hello universe";
    first_replaced = regex.replace("hello", message, "hi");
    all_replaced = regex.replace_all("hello", message, "hi");
    print("First replaced: " + first_replaced);
    print("All replaced: " + all_replaced);

    // Text splitting
    csv_data = "apple,banana,orange,grape";
    fruits = regex.split(",", csv_data);
    print("Split fruits: " + fruits);

    // Compiled patterns (for performance)
    number_pattern_id = regex.compile_pattern("\\d+");
    has_numbers1 = regex.test_compiled(number_pattern_id, "abc 123");
    has_numbers2 = regex.test_compiled(number_pattern_id, "no digits");
    print("'abc 123' has numbers: " + has_numbers1);
    print("'no digits' has numbers: " + has_numbers2);

    // Group matching
    date_text = "Date: 2024-03-15";
    date_pattern = "(\\d{4})-(\\d{2})-(\\d{2})";
    date_groups = regex.find_with_groups(date_pattern, date_text);
    print("Date groups: " + date_groups);

    // Built-in validators
    print("Email validation: " + regex.is_email("user@example.com"));
    print("URL validation: " + regex.is_url("https://example.com"));
    print("Phone validation: " + regex.is_phone_number("+1234567890"));
    print("IPv4 validation: " + regex.is_ipv4("192.168.1.1"));
    print("UUID validation: " + regex.is_uuid("550e8400-e29b-41d4-a716-446655440000"));
    print("Hex color validation: " + regex.is_hex_color("#FF5733"));

    // Text extraction helpers
    contact_text = "Contact: user@test.com, phone: +1-555-0123, visit: https://example.com";
    emails = regex.extract_emails(contact_text);
    phones = regex.extract_phone_numbers(contact_text);
    urls = regex.extract_urls(contact_text);
    numbers = regex.extract_numbers(contact_text);

    print("Extracted emails: " + emails);
    print("Extracted phones: " + phones);
    print("Extracted URLs: " + urls);
    print("Extracted numbers: " + numbers);

    // Text cleaning
    html_text = "Hello <script>alert('xss')</script> <b>world</b>";
    clean_text = regex.remove_html_tags(html_text);
    print("HTML removed: '" + clean_text + "'");

    messy_text = "Too   many    spaces\t\nand\r\nnewlines";
    normalized = regex.normalize_whitespace(messy_text);
    print("Normalized: '" + normalized + "'");

    // Security features
    safe_pattern = "\\d+";
    dangerous_pattern = "(a+)+$";  // ReDoS risk
    print("Safe pattern valid: " + regex.is_valid_pattern(safe_pattern));
    print("Dangerous pattern valid: " + regex.is_valid_pattern(dangerous_pattern));

    // Security pattern detection
    suspicious_sql = "'; DROP TABLE users; --";
    suspicious_js = "<img src=x onerror=alert(1)>";
    print("SQL injection detected: " + regex.contains_sql_injection_patterns(suspicious_sql));
    print("XSS detected: " + regex.contains_xss_patterns(suspicious_js));

    // Utility functions
    literal_text = "Price: $19.99 (20% off!)";
    escaped = regex.escape_string(literal_text);
    print("Escaped regex: " + escaped);

    sentence = "The cat sat on the mat";
    word_count = regex.count_matches("\\bthe\\b", sentence);
    print("Count of 'the': " + word_count);
}

// Run all tests
function main() {
    print("ML Standard Library Demonstration");
    print("=================================");

    test_string_module();
    test_datetime_module();
    test_regex_module();

    print("\n=== ALL TESTS COMPLETED ===");
    print("Standard library modules working correctly!");
}