"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, get_safe_length

from mlpy.stdlib.string_bridge import string as ml_string

# WARNING: Import 'regex' requires security review
# import regex

from mlpy.stdlib.collections_bridge import collections as ml_collections

def to_string(value):
    if ((value == True) or (value == False)):
        return 'true' if value else 'false'
    else:
        return ml_string.to_string(value)

def safe_upsert(arr, pos, item):
    if (pos < _safe_attr_access(arr, 'length')):
        new_arr = []
        i = 0
        while (i < _safe_attr_access(arr, 'length')):
            if (i == pos):
                new_arr = ml_collections.append(new_arr, item)
            else:
                new_arr = ml_collections.append(new_arr, arr[i])
            i = (i + 1)
        return new_arr
    else:
        return ml_collections.append(arr, item)

def safe_append(arr, item):
    return ml_collections.append(arr, item)

def string_creation_basics():
    print('=== String Creation and Basics ===')
    empty_str = ''
    simple_str = 'Hello, World!'
    single_quote = 'Single quoted string'
    multiline_str = 'This is line 1\\nThis is line 2\\tWith a tab'
    first_name = 'Alice'
    last_name = 'Johnson'
    full_name = (str((str(first_name) + str(' '))) + str(last_name))
    greeting = (str((str('Hello, ') + str(full_name))) + str('!'))
    print((str('Empty string length: ') + str(to_string(ml_string.length(empty_str)))))
    print((str('Simple string: ') + str(simple_str)))
    print((str('Full name: ') + str(full_name)))
    print((str('Greeting: ') + str(greeting)))
    age = 25
    age_str = (str((str('I am ') + str(to_string(age)))) + str(' years old'))
    print((str('Age string: ') + str(age_str)))
    return {'empty': empty_str, 'simple': simple_str, 'full_name': full_name, 'greeting': greeting, 'age_string': age_str}

def string_length_and_access():
    print('\\n=== String Length and Character Access ===')
    text = 'Programming in ML'
    length = ml_string.length(text)
    print((str((str("Text: '") + str(text))) + str("'")))
    print((str('Length: ') + str(to_string(length))))
    if (length > 0):
        first_char = ml_string.char_at(text, 0)
        middle_index = (length / 2)
        middle_char = ml_string.char_at(text, middle_index)
        last_char = ml_string.char_at(text, (length - 1))
        print((str('First character: ') + str(first_char)))
        print((str('Middle character: ') + str(middle_char)))
        print((str('Last character: ') + str(last_char)))
    a_code = ml_string.char_code_at('A', 0)
    z_code = ml_string.char_code_at('z', 0)
    print((str("Character code for 'A': ") + str(to_string(a_code))))
    print((str("Character code for 'z': ") + str(to_string(z_code))))
    from_65 = ml_string.from_char_code(65)
    from_97 = ml_string.from_char_code(97)
    print((str('Character from code 65: ') + str(from_65)))
    print((str('Character from code 97: ') + str(from_97)))
    return {'text': text, 'length': length, 'codes': {'a': a_code, 'z': z_code}, 'chars': {'from_65': from_65, 'from_97': from_97}}

def string_case_operations():
    print('\\n=== String Case Operations ===')
    mixed_case = 'Hello World! This is A Test.'
    upper_case = ml_string.upper(mixed_case)
    lower_case = ml_string.lower(mixed_case)
    capitalized = ml_string.capitalize(mixed_case)
    print((str('Original: ') + str(mixed_case)))
    print((str('Uppercase: ') + str(upper_case)))
    print((str('Lowercase: ') + str(lower_case)))
    print((str('Capitalized: ') + str(capitalized)))
    snake_text = 'hello_world_example'
    camel_text = ml_string.camel_case(snake_text)
    pascal_text = ml_string.pascal_case(snake_text)
    kebab_text = ml_string.kebab_case('HelloWorldExample')
    print('\\nCase Conversion Utilities:')
    print((str('Snake case: ') + str(snake_text)))
    print((str('Camel case: ') + str(camel_text)))
    print((str('Pascal case: ') + str(pascal_text)))
    print((str('Kebab case: ') + str(kebab_text)))
    return {'original': mixed_case, 'upper': upper_case, 'lower': lower_case, 'capitalized': capitalized, 'conversions': {'camel': camel_text, 'pascal': pascal_text, 'kebab': kebab_text}}

def string_search_operations():
    print('\\n=== String Search Operations ===')
    text = 'The quick brown fox jumps over the lazy dog'
    contains_fox = ml_string.contains(text, 'fox')
    contains_cat = ml_string.contains(text, 'cat')
    starts_with_the = ml_string.starts_with(text, 'The')
    ends_with_dog = ml_string.ends_with(text, 'dog')
    print((str('Text: ') + str(text)))
    print((str("Contains 'fox': ") + str(to_string(contains_fox))))
    print((str("Contains 'cat': ") + str(to_string(contains_cat))))
    print((str("Starts with 'The': ") + str(to_string(starts_with_the))))
    print((str("Ends with 'dog': ") + str(to_string(ends_with_dog))))
    fox_position = ml_string.find(text, 'fox')
    the_position = ml_string.find(text, 'the')
    missing_position = ml_string.find(text, 'elephant')
    print((str("Position of 'fox': ") + str(to_string(fox_position))))
    print((str("Position of 'the': ") + str(to_string(the_position))))
    print((str("Position of 'elephant': ") + str(to_string(missing_position))))
    space_count = ml_string.count(text, ' ')
    e_count = ml_string.count(text, 'e')
    print((str('Number of spaces: ') + str(to_string(space_count))))
    print((str("Number of 'e' characters: ") + str(to_string(e_count))))
    return {'text': text, 'search_results': {'contains_fox': contains_fox, 'contains_cat': contains_cat, 'starts_the': starts_with_the, 'ends_dog': ends_with_dog}, 'positions': {'fox': fox_position, 'the': the_position, 'missing': missing_position}, 'counts': {'spaces': space_count, 'e_chars': e_count}}

def string_modification_operations():
    print('\\n=== String Modification Operations ===')
    original = 'Hello, World! Welcome to ML programming.'
    replaced_world = ml_string.replace(original, 'World', 'Universe')
    replaced_all_e = ml_string.replace_all(original, 'e', 'E')
    replaced_spaces = ml_string.replace_all(original, ' ', '_')
    print((str('Original: ') + str(original)))
    print((str("Replace 'World' with 'Universe': ") + str(replaced_world)))
    print((str("Replace all 'e' with 'E': ") + str(replaced_all_e)))
    print((str('Replace spaces with underscores: ') + str(replaced_spaces)))
    padded_text = '   Hello, World!   '
    trimmed = ml_string.trim(padded_text)
    left_trimmed = ml_string.lstrip(padded_text)
    right_trimmed = ml_string.rstrip(padded_text)
    print('\\nTrimming Operations:')
    print((str((str("Padded: '") + str(padded_text))) + str("'")))
    print((str((str("Trimmed: '") + str(trimmed))) + str("'")))
    print((str((str("Left trimmed: '") + str(left_trimmed))) + str("'")))
    print((str((str("Right trimmed: '") + str(right_trimmed))) + str("'")))
    short_text = 'Hi'
    padded_left = ml_string.pad_left(short_text, 10, '*')
    padded_right = ml_string.pad_right(short_text, 10, '-')
    padded_center = ml_string.pad_center(short_text, 10, '=')
    print('\\nPadding Operations:')
    print((str((str("Original: '") + str(short_text))) + str("'")))
    print((str((str("Padded left: '") + str(padded_left))) + str("'")))
    print((str((str("Padded right: '") + str(padded_right))) + str("'")))
    print((str((str("Padded center: '") + str(padded_center))) + str("'")))
    return {'original': original, 'replacements': {'world': replaced_world, 'all_e': replaced_all_e, 'spaces': replaced_spaces}, 'trimming': {'original': padded_text, 'trimmed': trimmed, 'left': left_trimmed, 'right': right_trimmed}, 'padding': {'left': padded_left, 'right': padded_right, 'center': padded_center}}

def string_split_join_operations():
    print('\\n=== String Split and Join Operations ===')
    csv_data = 'apple,banana,cherry,date,elderberry'
    fruits = ml_string.split(csv_data, ',')
    print((str('CSV data: ') + str(csv_data)))
    print((str('Split fruits: ') + str(ml_string.join(', ', fruits))))
    pipe_separated = ml_string.join(' | ', fruits)
    space_separated = ml_string.join(' ', fruits)
    newline_separated = ml_string.join('\\n', fruits)
    print((str('Pipe separated: ') + str(pipe_separated)))
    print((str('Space separated: ') + str(space_separated)))
    print((str('Newline separated:\\n') + str(newline_separated)))
    paragraph = 'This is sentence one. This is sentence two. This is sentence three.'
    sentences = ml_string.split(paragraph, '. ')
    print('\\nSentence splitting:')
    print((str('Paragraph: ') + str(paragraph)))
    print((str('Sentences: ') + str(ml_string.join(' | ', sentences))))
    sentence = 'The quick brown fox'
    words = ml_string.split(sentence, ' ')
    print('\\nWord splitting:')
    print((str('Sentence: ') + str(sentence)))
    print((str('Words: ') + str(ml_string.join(' | ', words))))
    rejoined = ml_string.join('-', words)
    print((str('Rejoined with hyphens: ') + str(rejoined)))
    return {'csv': {'original': csv_data, 'fruits': fruits, 'rejoined': pipe_separated}, 'sentences': {'original': paragraph, 'split': sentences}, 'words': {'original': sentence, 'split': words, 'rejoined': rejoined}}

def string_validation_operations():
    print('\\n=== String Validation Operations ===')
    empty_string = ''
    whitespace_string = '   '
    alpha_string = 'HelloWorld'
    numeric_string = '12345'
    alphanumeric_string = 'Hello123'
    mixed_string = 'Hello, World! 123'
    test_strings = []
    safe_append(test_strings, empty_string)
    safe_append(test_strings, whitespace_string)
    safe_append(test_strings, alpha_string)
    safe_append(test_strings, numeric_string)
    safe_append(test_strings, alphanumeric_string)
    safe_append(test_strings, mixed_string)
    string_names = []
    safe_append(string_names, 'empty')
    safe_append(string_names, 'whitespace')
    safe_append(string_names, 'alpha')
    safe_append(string_names, 'numeric')
    safe_append(string_names, 'alphanumeric')
    safe_append(string_names, 'mixed')
    i = 0
    while (i < _safe_attr_access(test_strings, 'length')):
        test_str = test_strings[i]
        name = string_names[i]
        is_empty = ml_string.is_empty(test_str)
        is_whitespace = ml_string.is_whitespace(test_str)
        is_alpha = ml_string.is_alpha(test_str)
        is_numeric = ml_string.is_numeric(test_str)
        is_alnum = ml_string.is_alphanumeric(test_str)
        print((str((str((str((str("\\nTesting '") + str(name))) + str("': '"))) + str(test_str))) + str("'")))
        print((str('  Empty: ') + str(to_string(is_empty))))
        print((str('  Whitespace: ') + str(to_string(is_whitespace))))
        print((str('  Alpha: ') + str(to_string(is_alpha))))
        print((str('  Numeric: ') + str(to_string(is_numeric))))
        print((str('  Alphanumeric: ') + str(to_string(is_alnum))))
        i = (i + 1)
    return {'test_results': 'Validation tests completed'}

def regex_operations():
    print('\\n=== Regular Expression Operations ===')
    text = 'Contact us at: john@example.com, jane@test.org, or call 555-123-4567'
    emails = _safe_attr_access(regex, 'extract_emails')(text)
    print((str('Text: ') + str(text)))
    print((str('Extracted emails: ') + str(ml_string.join(', ', emails))))
    phone_numbers = _safe_attr_access(regex, 'extract_phone_numbers')(text)
    print((str('Extracted phone numbers: ') + str(ml_string.join(', ', phone_numbers))))
    test_urls = []
    safe_append(test_urls, 'https://www.example.com')
    safe_append(test_urls, 'http://test.org')
    safe_append(test_urls, 'ftp://invalid.url')
    safe_append(test_urls, 'not-a-url')
    print('\\nURL Validation:')
    j = 0
    while (j < _safe_attr_access(test_urls, 'length')):
        url = test_urls[j]
        is_valid_url = _safe_attr_access(regex, 'is_url')(url)
        print((str((str((str("'") + str(url))) + str("' is valid URL: "))) + str(to_string(is_valid_url))))
        j = (j + 1)
    date_text = "Today's date is 2024-03-15"
    date_pattern = '\\\\d{4}-\\\\d{2}-\\\\d{2}'
    found_date = _safe_attr_access(regex, 'find_first')(date_pattern, date_text)
    print('\\nPattern Matching:')
    print((str('Text: ') + str(date_text)))
    print((str('Found date: ') + str(found_date)))
    html_text = 'This is <b>bold</b> and this is <i>italic</i> text.'
    clean_text = _safe_attr_access(regex, 'remove_html_tags')(html_text)
    print('\\nText Cleaning:')
    print((str('HTML text: ') + str(html_text)))
    print((str('Clean text: ') + str(clean_text)))
    return {'emails': emails, 'phones': phone_numbers, 'date': found_date, 'cleaned': clean_text}

def string_building_operations():
    print('\\n=== String Building Operations ===')
    def build_number_string(count):
        result = ''
        i = 1
        while (i <= count):
            if (i == 1):
                result = (result + to_string(i))
            else:
                result = (str((str(result) + str(', '))) + str(to_string(i)))
            i = (i + 1)
        return result
    numbers_str = build_number_string(10)
    print((str('Numbers string: ') + str(numbers_str)))
    def format_person_info(name, age, city):
        return (str((str((str((str((str('Name: ') + str(name))) + str(', Age: '))) + str(to_string(age)))) + str(', City: '))) + str(city))
    person_info = format_person_info('Alice Johnson', 30, 'New York')
    print((str('Person info: ') + str(person_info)))
    separator = ml_string.repeat('=', 50)
    header = ml_string.repeat('-', 20)
    print((str('\\n') + str(separator)))
    print((str((str(header) + str(' FORMATTED OUTPUT '))) + str(header)))
    print(separator)
    def create_table_row(col1, col2, col3):
        padded_col1 = ml_string.pad_right(col1, 15, ' ')
        padded_col2 = ml_string.pad_right(col2, 10, ' ')
        padded_col3 = ml_string.pad_right(col3, 12, ' ')
        return (str((str((str((str((str((str('| ') + str(padded_col1))) + str(' | '))) + str(padded_col2))) + str(' | '))) + str(padded_col3))) + str(' |'))
    table_header = create_table_row('Name', 'Age', 'Department')
    table_separator = ml_string.repeat('-', ml_string.length(table_header))
    print(table_separator)
    print(table_header)
    print(table_separator)
    print(create_table_row('Alice', '30', 'Engineering'))
    print(create_table_row('Bob', '25', 'Marketing'))
    print(create_table_row('Charlie', '35', 'Sales'))
    print(table_separator)
    return {'numbers': numbers_str, 'person': person_info, 'table_demo': 'Table created successfully'}

def type_conversion_operations():
    print('\\n=== Type Conversion Operations ===')
    number_strings = []
    safe_append(number_strings, '123')
    safe_append(number_strings, '45.67')
    safe_append(number_strings, 'invalid')
    safe_append(number_strings, '0')
    print('String to number conversions:')
    i = 0
    while (i < _safe_attr_access(number_strings, 'length')):
        str_val = number_strings[i]
        int_val = ml_string.to_int(str_val)
        float_val = ml_string.to_float(str_val)
        print((str((str((str((str((str("'") + str(str_val))) + str("' -> int: "))) + str(to_string(int_val)))) + str(', float: '))) + str(to_string(float_val))))
        i = (i + 1)
    numbers = []
    safe_append(numbers, 42)
    safe_append(numbers, 3.14159)
    safe_append(numbers, 0)
    safe_append(numbers, 123)
    print('\\nNumber to string conversions:')
    j = 0
    while (j < _safe_attr_access(numbers, 'length')):
        num_val = numbers[j]
        str_val = ml_string.to_string(num_val)
        print((str((str((str(to_string(num_val)) + str(" -> '"))) + str(str_val))) + str("'")))
        j = (j + 1)
    return {'conversion_demo': 'Type conversion tests completed'}

def main():
    print('========================================')
    print('  COMPREHENSIVE STRING OPERATIONS TEST')
    print('========================================')
    results = {}
    results['basics'] = string_creation_basics()
    results['length_access'] = string_length_and_access()
    results['case_ops'] = string_case_operations()
    results['search_ops'] = string_search_operations()
    results['modification'] = string_modification_operations()
    results['split_join'] = string_split_join_operations()
    results['validation'] = string_validation_operations()
    results['regex_ops'] = regex_operations()
    results['building'] = string_building_operations()
    results['type_conversion'] = type_conversion_operations()
    print('\\n========================================')
    print('  ALL STRING TESTS COMPLETED')
    print('========================================')
    return results

main()

# End of generated code