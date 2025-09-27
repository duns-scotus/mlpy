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

def main():
    print('Testing Standard Library Modules')
    print('===============================')
    print('\\n--- String Module ---')
    text = '  Hello World  '
    print((str((str("Original: '") + str(text))) + str("'")))
    print((str((str("Trimmed: '") + str(ml_string.trim(text)))) + str("'")))
    print((str('Upper: ') + str(ml_string.upper(text))))
    print((str('Length: ') + str(ml_string.length(text))))
    word = 'programming'
    print((str("Contains 'gram': ") + str(ml_string.contains(word, 'gram'))))
    print((str("Starts with 'prog': ") + str(ml_string.starts_with(word, 'prog'))))
    csv = 'apple,banana,orange'
    fruits = ml_string.split(csv, ',')
    print((str('Split result: ') + str(fruits)))
    print('\\n--- DateTime Module ---')
    current = ml_datetime.now()
    print((str('Current timestamp: ') + str(current)))
    birthday = ml_datetime.create_date(2000, 1, 1)
    print((str('Y2K timestamp: ') + str(birthday)))
    next_week = ml_datetime.add_days(current, 7)
    print((str('Next week: ') + str(next_week)))
    year = ml_datetime.get_year(current)
    month = ml_datetime.get_month(current)
    print((str((str((str('Current year: ') + str(year))) + str(', month: '))) + str(month)))
    is_leap = ml_datetime.is_leap_year(2024)
    print((str('Is 2024 leap year: ') + str(is_leap)))
    print('\\n--- Regex Module ---')
    email = 'test@example.com'
    is_valid = regex['is_email'](email)
    print((str((str((str("'") + str(email))) + str("' is valid email: "))) + str(is_valid)))
    phone_text = 'Call me at 555-123-4567'
    phone_pattern = '\\\\d{3}-\\\\d{3}-\\\\d{4}'
    phone_number = regex['find_first'](phone_pattern, phone_text)
    print((str('Found phone: ') + str(phone_number)))
    message = 'foo bar foo'
    replaced = regex['replace_all']('foo', message, 'baz')
    print((str('Replaced: ') + str(replaced)))
    print((str('URL valid: ') + str(regex['is_url']('https://google.com'))))
    print((str('IPv4 valid: ') + str(regex['is_ipv4']('192.168.1.1'))))
    contact = 'Email: alice@test.com, phone: 555-0123'
    emails = regex['extract_emails'](contact)
    numbers = regex['extract_numbers'](contact)
    print((str('Extracted emails: ') + str(emails)))
    print((str('Extracted numbers: ') + str(numbers)))
    print('\\n--- Test Complete ---')
    print('All modules functioning correctly!')

# End of generated code