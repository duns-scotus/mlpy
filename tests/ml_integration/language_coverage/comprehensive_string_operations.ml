// Comprehensive String Operations Test
// Demonstrates all aspects of string manipulation in ML with standard library

import string;
import regex;

// String creation and basic operations
function string_creation_basics() {
    print("=== String Creation and Basics ===");

    // Different ways to create strings
    empty_str = "";
    simple_str = "Hello, World!";
    single_quote = 'Single quoted string';
    multiline_str = "This is line 1\nThis is line 2\tWith a tab";

    // String concatenation
    first_name = "Alice";
    last_name = "Johnson";
    full_name = first_name + " " + last_name;
    greeting = "Hello, " + full_name + "!";

    print("Empty string length: " + string.length(empty_str));
    print("Simple string: " + simple_str);
    print("Full name: " + full_name);
    print("Greeting: " + greeting);

    // String with numbers
    age = 25;
    age_str = "I am " + age + " years old";
    print("Age string: " + age_str);

    return {
        empty: empty_str,
        simple: simple_str,
        full_name: full_name,
        greeting: greeting,
        age_string: age_str
    };
}

// String length and character access
function string_length_and_access() {
    print("\n=== String Length and Character Access ===");

    text = "Programming in ML";
    length = string.length(text);

    print("Text: '" + text + "'");
    print("Length: " + length);

    // Character access (if supported by standard library)
    if (length > 0) {
        first_char = string.char_at(text, 0);
        middle_char = string.char_at(text, length / 2);
        last_char = string.char_at(text, length - 1);

        print("First character: " + first_char);
        print("Middle character: " + middle_char);
        print("Last character: " + last_char);
    }

    // Character codes
    a_code = string.char_code_at("A", 0);
    z_code = string.char_code_at("z", 0);
    print("Character code for 'A': " + a_code);
    print("Character code for 'z': " + z_code);

    // From character codes
    from_65 = string.from_char_code(65);
    from_97 = string.from_char_code(97);
    print("Character from code 65: " + from_65);
    print("Character from code 97: " + from_97);

    return {
        text: text,
        length: length,
        codes: {a: a_code, z: z_code},
        chars: {from_65: from_65, from_97: from_97}
    };
}

// Case conversion operations
function string_case_operations() {
    print("\n=== String Case Operations ===");

    mixed_case = "Hello World! This is A Test.";

    upper_case = string.upper(mixed_case);
    lower_case = string.lower(mixed_case);
    capitalized = string.capitalize(mixed_case);

    print("Original: " + mixed_case);
    print("Uppercase: " + upper_case);
    print("Lowercase: " + lower_case);
    print("Capitalized: " + capitalized);

    // Case conversion utilities
    snake_text = "hello_world_example";
    camel_text = string.camel_case(snake_text);
    pascal_text = string.pascal_case(snake_text);
    kebab_text = string.kebab_case("HelloWorldExample");

    print("\nCase Conversion Utilities:");
    print("Snake case: " + snake_text);
    print("Camel case: " + camel_text);
    print("Pascal case: " + pascal_text);
    print("Kebab case: " + kebab_text);

    return {
        original: mixed_case,
        upper: upper_case,
        lower: lower_case,
        capitalized: capitalized,
        conversions: {
            camel: camel_text,
            pascal: pascal_text,
            kebab: kebab_text
        }
    };
}

// String search and find operations
function string_search_operations() {
    print("\n=== String Search Operations ===");

    text = "The quick brown fox jumps over the lazy dog";

    // Basic search
    contains_fox = string.contains(text, "fox");
    contains_cat = string.contains(text, "cat");
    starts_with_the = string.starts_with(text, "The");
    ends_with_dog = string.ends_with(text, "dog");

    print("Text: " + text);
    print("Contains 'fox': " + contains_fox);
    print("Contains 'cat': " + contains_cat);
    print("Starts with 'The': " + starts_with_the);
    print("Ends with 'dog': " + ends_with_dog);

    // Find positions
    fox_position = string.find(text, "fox");
    the_position = string.find(text, "the");
    missing_position = string.find(text, "elephant");

    print("Position of 'fox': " + fox_position);
    print("Position of 'the': " + the_position);
    print("Position of 'elephant': " + missing_position);

    // Count occurrences
    space_count = string.count(text, " ");
    e_count = string.count(text, "e");

    print("Number of spaces: " + space_count);
    print("Number of 'e' characters: " + e_count);

    return {
        text: text,
        search_results: {
            contains_fox: contains_fox,
            contains_cat: contains_cat,
            starts_the: starts_with_the,
            ends_dog: ends_with_dog
        },
        positions: {
            fox: fox_position,
            the: the_position,
            missing: missing_position
        },
        counts: {
            spaces: space_count,
            e_chars: e_count
        }
    };
}

// String modification operations
function string_modification_operations() {
    print("\n=== String Modification Operations ===");

    original = "Hello, World! Welcome to ML programming.";

    // Replace operations
    replaced_world = string.replace(original, "World", "Universe");
    replaced_all_e = string.replace_all(original, "e", "E");
    replaced_spaces = string.replace_all(original, " ", "_");

    print("Original: " + original);
    print("Replace 'World' with 'Universe': " + replaced_world);
    print("Replace all 'e' with 'E': " + replaced_all_e);
    print("Replace spaces with underscores: " + replaced_spaces);

    // Trimming operations
    padded_text = "   Hello, World!   ";
    trimmed = string.trim(padded_text);
    left_trimmed = string.lstrip(padded_text);
    right_trimmed = string.rstrip(padded_text);

    print("\nTrimming Operations:");
    print("Padded: '" + padded_text + "'");
    print("Trimmed: '" + trimmed + "'");
    print("Left trimmed: '" + left_trimmed + "'");
    print("Right trimmed: '" + right_trimmed + "'");

    // Padding operations
    short_text = "Hi";
    padded_left = string.pad_left(short_text, 10, "*");
    padded_right = string.pad_right(short_text, 10, "-");
    padded_center = string.pad_center(short_text, 10, "=");

    print("\nPadding Operations:");
    print("Original: '" + short_text + "'");
    print("Padded left: '" + padded_left + "'");
    print("Padded right: '" + padded_right + "'");
    print("Padded center: '" + padded_center + "'");

    return {
        original: original,
        replacements: {
            world: replaced_world,
            all_e: replaced_all_e,
            spaces: replaced_spaces
        },
        trimming: {
            original: padded_text,
            trimmed: trimmed,
            left: left_trimmed,
            right: right_trimmed
        },
        padding: {
            left: padded_left,
            right: padded_right,
            center: padded_center
        }
    };
}

// String splitting and joining
function string_split_join_operations() {
    print("\n=== String Split and Join Operations ===");

    // CSV data example
    csv_data = "apple,banana,cherry,date,elderberry";
    fruits = string.split(csv_data, ",");

    print("CSV data: " + csv_data);
    print("Split fruits: " + fruits);

    // Rejoin with different separator
    pipe_separated = string.join(" | ", fruits);
    space_separated = string.join(" ", fruits);
    newline_separated = string.join("\n", fruits);

    print("Pipe separated: " + pipe_separated);
    print("Space separated: " + space_separated);
    print("Newline separated:\n" + newline_separated);

    // Split sentences
    paragraph = "This is sentence one. This is sentence two. This is sentence three.";
    sentences = string.split(paragraph, ". ");

    print("\nSentence splitting:");
    print("Paragraph: " + paragraph);
    print("Sentences: " + sentences);

    // Split words
    sentence = "The quick brown fox";
    words = string.split(sentence, " ");

    print("\nWord splitting:");
    print("Sentence: " + sentence);
    print("Words: " + words);

    // Join words back
    rejoined = string.join("-", words);
    print("Rejoined with hyphens: " + rejoined);

    return {
        csv: {
            original: csv_data,
            fruits: fruits,
            rejoined: pipe_separated
        },
        sentences: {
            original: paragraph,
            split: sentences
        },
        words: {
            original: sentence,
            split: words,
            rejoined: rejoined
        }
    };
}

// String validation functions
function string_validation_operations() {
    print("\n=== String Validation Operations ===");

    // Test various string types
    empty_string = "";
    whitespace_string = "   ";
    alpha_string = "HelloWorld";
    numeric_string = "12345";
    alphanumeric_string = "Hello123";
    mixed_string = "Hello, World! 123";

    test_strings = [
        empty_string,
        whitespace_string,
        alpha_string,
        numeric_string,
        alphanumeric_string,
        mixed_string
    ];

    string_names = [
        "empty",
        "whitespace",
        "alpha",
        "numeric",
        "alphanumeric",
        "mixed"
    ];

    i = 0;
    while (i < test_strings.length()) {
        test_str = test_strings[i];
        name = string_names[i];

        is_empty = string.is_empty(test_str);
        is_whitespace = string.is_whitespace(test_str);
        is_alpha = string.is_alpha(test_str);
        is_numeric = string.is_numeric(test_str);
        is_alnum = string.is_alphanumeric(test_str);

        print("\nTesting '" + name + "': '" + test_str + "'");
        print("  Empty: " + is_empty);
        print("  Whitespace: " + is_whitespace);
        print("  Alpha: " + is_alpha);
        print("  Numeric: " + is_numeric);
        print("  Alphanumeric: " + is_alnum);

        i = i + 1;
    }

    return {
        test_results: "Validation tests completed"
    };
}

// Regular expression operations
function regex_operations() {
    print("\n=== Regular Expression Operations ===");

    text = "Contact us at: john@example.com, jane@test.org, or call 555-123-4567";

    // Email validation and extraction
    email_pattern = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}";
    emails = regex.extract_emails(text);

    print("Text: " + text);
    print("Extracted emails: " + emails);

    // Phone number extraction
    phone_numbers = regex.extract_phone_numbers(text);
    print("Extracted phone numbers: " + phone_numbers);

    // URL validation
    test_urls = [
        "https://www.example.com",
        "http://test.org",
        "ftp://invalid.url",
        "not-a-url"
    ];

    print("\nURL Validation:");
    j = 0;
    while (j < test_urls.length()) {
        url = test_urls[j];
        is_valid_url = regex.is_url(url);
        print("'" + url + "' is valid URL: " + is_valid_url);
        j = j + 1;
    }

    // Pattern matching
    date_text = "Today's date is 2024-03-15";
    date_pattern = "\\d{4}-\\d{2}-\\d{2}";
    found_date = regex.find_first(date_pattern, date_text);

    print("\nPattern Matching:");
    print("Text: " + date_text);
    print("Found date: " + found_date);

    // Text cleaning
    html_text = "This is <b>bold</b> and this is <i>italic</i> text.";
    clean_text = regex.remove_html_tags(html_text);

    print("\nText Cleaning:");
    print("HTML text: " + html_text);
    print("Clean text: " + clean_text);

    return {
        emails: emails,
        phones: phone_numbers,
        date: found_date,
        cleaned: clean_text
    };
}

// String building and formatting
function string_building_operations() {
    print("\n=== String Building Operations ===");

    // Building strings with loops
    function build_number_string(count) {
        result = "";
        i = 1;
        while (i <= count) {
            if (i == 1) {
                result = result + i;
            } else {
                result = result + ", " + i;
            }
            i = i + 1;
        }
        return result;
    }

    numbers_str = build_number_string(10);
    print("Numbers string: " + numbers_str);

    // Building formatted strings
    function format_person_info(name, age, city) {
        return "Name: " + name + ", Age: " + age + ", City: " + city;
    }

    person_info = format_person_info("Alice Johnson", 30, "New York");
    print("Person info: " + person_info);

    // String repetition
    separator = string.repeat("=", 50);
    header = string.repeat("-", 20);

    print("\n" + separator);
    print(header + " FORMATTED OUTPUT " + header);
    print(separator);

    // Building tables
    function create_table_row(col1, col2, col3) {
        padded_col1 = string.pad_right(col1, 15, " ");
        padded_col2 = string.pad_right(col2, 10, " ");
        padded_col3 = string.pad_right(col3, 12, " ");
        return "| " + padded_col1 + " | " + padded_col2 + " | " + padded_col3 + " |";
    }

    table_header = create_table_row("Name", "Age", "Department");
    table_separator = string.repeat("-", string.length(table_header));

    print(table_separator);
    print(table_header);
    print(table_separator);
    print(create_table_row("Alice", "30", "Engineering"));
    print(create_table_row("Bob", "25", "Marketing"));
    print(create_table_row("Charlie", "35", "Sales"));
    print(table_separator);

    return {
        numbers: numbers_str,
        person: person_info,
        table_demo: "Table created successfully"
    };
}

// Main test runner
function main() {
    print("========================================");
    print("  COMPREHENSIVE STRING OPERATIONS TEST");
    print("========================================");

    results = {};

    results.basics = string_creation_basics();
    results.length_access = string_length_and_access();
    results.case_ops = string_case_operations();
    results.search_ops = string_search_operations();
    results.modification = string_modification_operations();
    results.split_join = string_split_join_operations();
    results.validation = string_validation_operations();
    results.regex_ops = regex_operations();
    results.building = string_building_operations();

    print("\n========================================");
    print("  ALL STRING TESTS COMPLETED");
    print("========================================");

    return results;
}

// Execute all string tests
main();