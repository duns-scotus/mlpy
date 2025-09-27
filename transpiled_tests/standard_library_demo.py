"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData

from mlpy.stdlib.string_bridge import string as ml_string

from mlpy.stdlib.datetime_bridge import datetime as ml_datetime

# WARNING: Import 'regex' requires security review
# import regex

def test_string_module():
    print('=== STRING MODULE TESTS ===')
    text = '  Hello, World!  '
    print((str((str("Original: '") + str(text))) + str("'")))
    print((str('Length: ') + str(ml_string.length(text))))
    print((str((str("Trimmed: '") + str(ml_string.trim(text)))) + str("'")))
    print((str('Upper: ') + str(ml_string.upper(text))))
    print((str('Lower: ') + str(ml_string.lower(text))))
    message = 'The quick brown fox jumps over the lazy dog'
    print((str("Contains 'fox': ") + str(ml_string.contains(message, 'fox'))))
    print((str("Starts with 'The': ") + str(ml_string.starts_with(message, 'The'))))
    print((str("Ends with 'dog': ") + str(ml_string.ends_with(message, 'dog'))))
    print((str("Position of 'brown': ") + str(ml_string.find(message, 'brown'))))
    replaced = ml_string.replace(message, 'fox', 'cat')
    print((str('Replaced fox with cat: ') + str(replaced)))
    all_replaced = ml_string.replace_all(message, 'the', 'THE')
    print((str("All 'the' to 'THE': ") + str(all_replaced)))
    csv_data = 'apple,banana,orange,grape'
    fruits = ml_string.split(csv_data, ',')
    print((str('Split CSV: ') + str(fruits)))
    rejoined = ml_string.join(' | ', fruits)
    print((str('Rejoined: ') + str(rejoined)))
    test_text = 'hello_world'
    print((str('Snake case: ') + str(ml_string.snake_case('HelloWorld'))))
    print((str('Camel case: ') + str(ml_string.camel_case('hello_world'))))
    print((str('Pascal case: ') + str(ml_string.pascal_case('hello_world'))))
    print((str('Kebab case: ') + str(ml_string.kebab_case('HelloWorld'))))
    print((str("Is empty '': ") + str(ml_string.is_empty(''))))
    print((str("Is alpha 'Hello': ") + str(ml_string.is_alpha('Hello'))))
    print((str("Is numeric '123': ") + str(ml_string.is_numeric('123'))))
    print((str("Is alphanumeric 'abc123': ") + str(ml_string.is_alphanumeric('abc123'))))
    word = 'Hello'
    print((str('First char: ') + str(ml_string.char_at(word, 0))))
    print((str('Char code: ') + str(ml_string.char_code_at(word, 0))))
    print((str('From char code 65: ') + str(ml_string.from_char_code(65))))
    greeting_template = 'Hello, world! Welcome to ML.'
    print((str('Template demo: ') + str(greeting_template)))

def test_datetime_module():
    print('\\n=== DATETIME MODULE TESTS ===')
    current_timestamp = ml_datetime.now()
    print((str('Current timestamp: ') + str(current_timestamp)))
    current_string = ml_datetime.utcnow()
    print((str('Current UTC string: ') + str(current_string)))
    birthday = ml_datetime.create_date(1990, 12, 25)
    print((str('Birthday timestamp: ') + str(birthday)))
    meeting = ml_datetime.create_datetime(2024, 3, 15, 14, 30, 0)
    print((str('Meeting timestamp: ') + str(meeting)))
    today = ml_datetime.now()
    next_week = ml_datetime.add_days(today, 7)
    print((str('Next week: ') + str(next_week)))
    in_two_hours = ml_datetime.add_hours(today, 2)
    print((str('In two hours: ') + str(in_two_hours)))
    start_date = ml_datetime.create_date(2024, 1, 1)
    end_date = ml_datetime.create_date(2024, 12, 31)
    days_diff = ml_datetime.days_between(start_date, end_date)
    print((str('Days in 2024: ') + str(days_diff)))
    hours_diff = ml_datetime.hours_between(start_date, end_date)
    print((str('Hours in 2024: ') + str(hours_diff)))
    year = ml_datetime.get_year(today)
    month = ml_datetime.get_month(today)
    day = ml_datetime.get_day(today)
    print((str((str((str((str((str('Today: Year=') + str(year))) + str(', Month='))) + str(month))) + str(', Day='))) + str(day)))
    month_name = ml_datetime.get_month_name(month)
    weekday = ml_datetime.get_weekday(today)
    weekday_name = ml_datetime.get_weekday_name(weekday)
    print((str((str((str('Month name: ') + str(month_name))) + str(', Weekday: '))) + str(weekday_name)))
    start_of_day = ml_datetime.start_of_day(today)
    end_of_month = ml_datetime.end_of_month(today)
    print((str('Start of day: ') + str(start_of_day)))
    print((str('End of month: ') + str(end_of_month)))
    is_workday = ml_datetime.is_business_day(today)
    print((str('Is today a business day: ') + str(is_workday)))
    next_business_day = ml_datetime.add_business_days(today, 1)
    print((str('Next business day: ') + str(next_business_day)))
    birth_date = ml_datetime.create_date(1990, 5, 15)
    age = ml_datetime.age_in_years(birth_date, today)
    print((str((str('Age from 1990-05-15: ') + str(age))) + str(' years')))
    is_valid = ml_datetime.is_valid_date(2024, 2, 29)
    print((str('Is 2024-02-29 valid: ') + str(is_valid)))
    is_leap = ml_datetime.is_leap_year(2024)
    print((str('Is 2024 a leap year: ') + str(is_leap)))

def test_regex_module():
    print('\\n=== REGEX MODULE TESTS ===')
    email_pattern = '^[\\\\w._%+-]+@[\\\\w.-]+\\\\.[A-Za-z]{2,}$'
    test_email = 'user@example.com'
    is_valid_email = regex['test'](email_pattern, test_email)
    print((str((str((str("'") + str(test_email))) + str("' is valid email: "))) + str(is_valid_email)))
    text = 'Phone numbers: 123-456-7890, 987-654-3210'
    phone_pattern = '\\\\d{3}-\\\\d{3}-\\\\d{4}'
    first_phone = regex['find_first'](phone_pattern, text)
    all_phones = regex['find_all'](phone_pattern, text)
    print((str('First phone: ') + str(first_phone)))
    print((str('All phones: ') + str(all_phones)))
    message = 'Hello world, hello universe'
    first_replaced = regex['replace']('hello', message, 'hi')
    all_replaced = regex['replace_all']('hello', message, 'hi')
    print((str('First replaced: ') + str(first_replaced)))
    print((str('All replaced: ') + str(all_replaced)))
    csv_data = 'apple,banana,orange,grape'
    fruits = regex['split'](',', csv_data)
    print((str('Split fruits: ') + str(fruits)))
    number_pattern_id = regex['compile_pattern']('\\\\d+')
    has_numbers1 = regex['test_compiled'](number_pattern_id, 'abc 123')
    has_numbers2 = regex['test_compiled'](number_pattern_id, 'no digits')
    print((str("'abc 123' has numbers: ") + str(has_numbers1)))
    print((str("'no digits' has numbers: ") + str(has_numbers2)))
    date_text = 'Date: 2024-03-15'
    date_pattern = '(\\\\d{4})-(\\\\d{2})-(\\\\d{2})'
    date_groups = regex['find_with_groups'](date_pattern, date_text)
    print((str('Date groups: ') + str(date_groups)))
    print((str('Email validation: ') + str(regex['is_email']('user@example.com'))))
    print((str('URL validation: ') + str(regex['is_url']('https://example.com'))))
    print((str('Phone validation: ') + str(regex['is_phone_number']('+1234567890'))))
    print((str('IPv4 validation: ') + str(regex['is_ipv4']('192.168.1.1'))))
    print((str('UUID validation: ') + str(regex['is_uuid']('550e8400-e29b-41d4-a716-446655440000'))))
    print((str('Hex color validation: ') + str(regex['is_hex_color']('#FF5733'))))
    contact_text = 'Contact: user@test.com, phone: +1-555-0123, visit: https://example.com'
    emails = regex['extract_emails'](contact_text)
    phones = regex['extract_phone_numbers'](contact_text)
    urls = regex['extract_urls'](contact_text)
    numbers = regex['extract_numbers'](contact_text)
    print((str('Extracted emails: ') + str(emails)))
    print((str('Extracted phones: ') + str(phones)))
    print((str('Extracted URLs: ') + str(urls)))
    print((str('Extracted numbers: ') + str(numbers)))
    html_text = "Hello <script>alert('xss')</script> <b>world</b>"
    clean_text = regex['remove_html_tags'](html_text)
    print((str((str("HTML removed: '") + str(clean_text))) + str("'")))
    messy_text = 'Too   many    spaces\\t\\nand\\r\\nnewlines'
    normalized = regex['normalize_whitespace'](messy_text)
    print((str((str("Normalized: '") + str(normalized))) + str("'")))
    safe_pattern = '\\\\d+'
    dangerous_pattern = '(a+)+$'
    print((str('Safe pattern valid: ') + str(regex['is_valid_pattern'](safe_pattern))))
    print((str('Dangerous pattern valid: ') + str(regex['is_valid_pattern'](dangerous_pattern))))
    suspicious_sql = "'; DROP TABLE users; --"
    suspicious_js = '<img src=x onerror=alert(1)>'
    print((str('SQL injection detected: ') + str(regex['contains_sql_injection_patterns'](suspicious_sql))))
    print((str('XSS detected: ') + str(regex['contains_xss_patterns'](suspicious_js))))
    literal_text = 'Price: $19.99 (20% off!)'
    escaped = regex['escape_string'](literal_text)
    print((str('Escaped regex: ') + str(escaped)))
    sentence = 'The cat sat on the mat'
    word_count = regex['count_matches']('\\\\bthe\\\\b', sentence)
    print((str("Count of 'the': ") + str(word_count)))

def main():
    print('ML Standard Library Demonstration')
    print('=================================')
    test_string_module()
    test_datetime_module()
    test_regex_module()
    print('\\n=== ALL TESTS COMPLETED ===')
    print('Standard library modules working correctly!')

# End of generated code