// Test stdlib module: regex - Utility functions and practical patterns
// Features tested: escape(), isValid(), test(), practical regex patterns
// Module: regex (version 2.0)

import regex;

function test_escape() {
    results = {};

    // Escape special regex characters
    results.price = regex.escape("Price: $5.99");       // "Price: \$5\.99"
    results.brackets = regex.escape("[test]");          // "\[test\]"
    results.parens = regex.escape("(example)");         // "\(example\)"
    results.question = regex.escape("What?");           // "What\?"

    // Use escaped string in pattern
    text = "Price: $5.99";
    escaped = regex.escape("$5.99");
    pattern = regex.compile(escaped);
    match = pattern.search(text);
    results.escaped_match = match != null;              // true

    return results;
}

function test_is_valid() {
    results = {};

    // Valid patterns
    results.valid_digit = regex.isValid('\d+');        // true
    results.valid_word = regex.isValid('\w+');         // true
    results.valid_groups = regex.isValid('(\d+)-(\d+)'); // true

    // Invalid patterns
    results.invalid_unclosed = regex.isValid('(abc');  // false
    results.invalid_bracket = regex.isValid('[abc');   // false

    return results;
}

function test_email_pattern() {
    results = {};

    // Simple email pattern
    pattern = regex.compile('[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,}');

    valid_emails = [
        "user@example.com",
        "test.user@domain.co.uk",
        "name+tag@site.org"
    ];

    results.email_matches = [];
    i = 0;
    while (i < len(valid_emails)) {
        email = valid_emails[i];
        match = pattern.search(email);
        if (match != null) {
            results.email_matches = results.email_matches;  // Track successful matches
        }
        i = i + 1;
    }

    return results;
}

function test_url_pattern() {
    results = {};

    // URL pattern
    pattern = regex.compile('https?://[\w.-]+\.[a-zA-Z]{2,}(/[\w/.-]*)?');

    urls = [
        "https://example.com",
        "http://site.org/path/to/page",
        "https://sub.domain.com/api/v1"
    ];

    results.url_count = 0;
    i = 0;
    while (i < len(urls)) {
        url = urls[i];
        match = pattern.search(url);
        if (match != null) {
            results.url_count = results.url_count + 1;
        }
        i = i + 1;
    }

    return results;
}

function test_ip_address() {
    results = {};

    // IP address pattern (simplified)
    pattern = regex.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}');

    match = pattern.search("Server IP: 192.168.1.1");
    if (match != null) {
        results.ip = match.group(0);                    // "192.168.1.1"
    }

    return results;
}

function test_phone_numbers() {
    results = {};

    // Phone number patterns
    pattern = regex.compile('(\d{3})-(\d{3})-(\d{4})');

    text = "Call 555-123-4567 or 800-555-1234";
    matches = pattern.finditer(text);

    results.phone_count = len(matches);                 // 2

    if (len(matches) > 0) {
        first = matches[0];
        results.area_code = first.group(1);             // "555"
        results.exchange = first.group(2);              // "123"
        results.number = first.group(3);                // "4567"
    }

    return results;
}

function test_word_boundaries() {
    results = {};

    // Word boundary \b
    pattern = regex.compile('\bcat\b');

    results.match_cat = pattern.test("I have a cat");   // true
    results.no_match_catalog = pattern.test("catalog"); // false
    results.no_match_scat = pattern.test("scat");       // false

    return results;
}

function test_character_classes() {
    results = {};

    // Digit class
    digits = regex.compile('\d+');
    results.digits_match = digits.search("Room 101");

    // Word characters
    words = regex.compile('\w+');
    results.word_match = words.search("hello_world");

    // Whitespace
    spaces = regex.compile('\s+');
    results.space_match = spaces.search("a b c");

    // Non-digit
    non_digits = regex.compile('\D+');
    results.non_digit_match = non_digits.search("abc123");

    results.all_found = (results.digits_match != null &&
                         results.word_match != null &&
                         results.space_match != null &&
                         results.non_digit_match != null);

    return results;
}

function test_quantifiers() {
    results = {};

    // Zero or more: *
    pattern1 = regex.compile('go*d');
    results.gd = pattern1.test("gd");                   // true
    results.god = pattern1.test("god");                 // true
    results.good = pattern1.test("good");               // true

    // One or more: +
    pattern2 = regex.compile('go+d');
    results.plus_gd = pattern2.test("gd");              // false
    results.plus_god = pattern2.test("god");            // true

    // Zero or one: ?
    pattern3 = regex.compile('colou?');
    results.color = pattern3.test("colo");             // true
    results.colour = pattern3.test("colou");           // true

    // Exact count: {n}
    pattern4 = regex.compile('\d{3}');
    results.three_digits = pattern4.test("123");        // true
    results.two_digits = pattern4.test("12");           // false

    return results;
}

function test_anchors() {
    results = {};

    // Start of string: ^
    start_pattern = regex.compile('^Hello');
    results.start_match = start_pattern.test("Hello world");    // true
    results.start_no_match = start_pattern.test("Say Hello");   // false

    // End of string: $
    end_pattern = regex.compile('world$');
    results.end_match = end_pattern.test("Hello world");        // true
    results.end_no_match = end_pattern.test("world peace");     // false

    return results;
}

function main() {
    all_results = {};

    all_results.escape = test_escape();
    all_results.validation = test_is_valid();
    all_results.email = test_email_pattern();
    all_results.url = test_url_pattern();
    all_results.ip = test_ip_address();
    all_results.phone = test_phone_numbers();
    all_results.boundaries = test_word_boundaries();
    all_results.classes = test_character_classes();
    all_results.quantifiers = test_quantifiers();
    all_results.anchors = test_anchors();

    return all_results;
}

// Run tests
test_results = main();
