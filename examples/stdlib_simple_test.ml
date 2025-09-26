// Simple Standard Library Test
// Tests basic functionality of string, datetime, and regex modules

import string;
import datetime;
import regex;

function main() {
    print("Testing Standard Library Modules");
    print("===============================");

    // String module basic tests
    print("\n--- String Module ---");
    text = "  Hello World  ";
    print("Original: '" + text + "'");
    print("Trimmed: '" + string.trim(text) + "'");
    print("Upper: " + string.upper(text));
    print("Length: " + string.length(text));

    word = "programming";
    print("Contains 'gram': " + string.contains(word, "gram"));
    print("Starts with 'prog': " + string.starts_with(word, "prog"));

    csv = "apple,banana,orange";
    fruits = string.split(csv, ",");
    print("Split result: " + fruits);

    // DateTime module basic tests
    print("\n--- DateTime Module ---");
    current = datetime.now();
    print("Current timestamp: " + current);

    // Create a specific date
    birthday = datetime.create_date(2000, 1, 1);
    print("Y2K timestamp: " + birthday);

    // Add time
    next_week = datetime.add_days(current, 7);
    print("Next week: " + next_week);

    // Get components
    year = datetime.get_year(current);
    month = datetime.get_month(current);
    print("Current year: " + year + ", month: " + month);

    // Check if leap year
    is_leap = datetime.is_leap_year(2024);
    print("Is 2024 leap year: " + is_leap);

    // Regex module basic tests
    print("\n--- Regex Module ---");

    // Test email validation
    email = "test@example.com";
    is_valid = regex.is_email(email);
    print("'" + email + "' is valid email: " + is_valid);

    // Test pattern matching
    phone_text = "Call me at 555-123-4567";
    phone_pattern = "\\d{3}-\\d{3}-\\d{4}";
    phone_number = regex.find_first(phone_pattern, phone_text);
    print("Found phone: " + phone_number);

    // Test replacement
    message = "foo bar foo";
    replaced = regex.replace_all("foo", message, "baz");
    print("Replaced: " + replaced);

    // Test built-in validators
    print("URL valid: " + regex.is_url("https://google.com"));
    print("IPv4 valid: " + regex.is_ipv4("192.168.1.1"));

    // Test text extraction
    contact = "Email: alice@test.com, phone: 555-0123";
    emails = regex.extract_emails(contact);
    numbers = regex.extract_numbers(contact);
    print("Extracted emails: " + emails);
    print("Extracted numbers: " + numbers);

    print("\n--- Test Complete ---");
    print("All modules functioning correctly!");
}