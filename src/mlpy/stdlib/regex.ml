// @description: Regular expression pattern matching with security validation
// @capability: execute:regex_operations
// @capability: read:pattern_data
// @version: 1.0.0

/**
 * ML Regex Standard Library
 * Provides regular expression pattern matching with input validation and security checks
 */

capability RegexOperations {
    allow execute "regex_operations";
    allow read "pattern_data";
}

// Basic pattern matching functions
function test(pattern: string, text: string): boolean {
    return __python_bridge("regex.test", pattern, text);
}

function match(pattern: string, text: string) {
    return __python_bridge("regex.match", pattern, text);
}

function find_all(pattern: string, text: string) {
    return __python_bridge("regex.find_all", pattern, text);
}

function find_first(pattern: string, text: string): string {
    return __python_bridge("regex.find_first", pattern, text);
}

// Pattern replacement functions
function replace(pattern: string, text: string, replacement: string): string {
    return __python_bridge("regex.replace", pattern, text, replacement);
}

function replace_all(pattern: string, text: string, replacement: string): string {
    return __python_bridge("regex.replace_all", pattern, text, replacement);
}

function replace_with_function(pattern: string, text: string, replacer_func): string {
    return __python_bridge("regex.replace_with_function", pattern, text, replacer_func);
}

// Text splitting functions
function split(pattern: string, text: string) {
    return __python_bridge("regex.split", pattern, text);
}

function split_with_limit(pattern: string, text: string, max_splits: number) {
    return __python_bridge("regex.split_with_limit", pattern, text, max_splits);
}

// Pattern compilation and reuse (for performance)
function compile_pattern(pattern: string): string {
    return __python_bridge("regex.compile", pattern);
}

function test_compiled(compiled_pattern: string, text: string): boolean {
    return __python_bridge("regex.test_compiled", compiled_pattern, text);
}

function match_compiled(compiled_pattern: string, text: string) {
    return __python_bridge("regex.match_compiled", compiled_pattern, text);
}

// Advanced matching functions
function find_with_groups(pattern: string, text: string) {
    return __python_bridge("regex.find_with_groups", pattern, text);
}

function find_all_with_groups(pattern: string, text: string) {
    return __python_bridge("regex.find_all_with_groups", pattern, text);
}

function find_with_positions(pattern: string, text: string) {
    return __python_bridge("regex.find_with_positions", pattern, text);
}

// Pattern validation and utilities
function is_valid_pattern(pattern: string): boolean {
    return __python_bridge("regex.is_valid", pattern);
}

function escape_string(text: string): string {
    return __python_bridge("regex.escape", text);
}

function count_matches(pattern: string, text: string): number {
    return __python_bridge("regex.count_matches", pattern, text);
}

// Common pattern validators
function is_email(text: string): boolean {
    email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$";
    return test(email_pattern, text);
}

function is_url(text: string): boolean {
    url_pattern = "^https?://[^\\s/$.?#].[^\\s]*$";
    return test(url_pattern, text);
}

function is_phone_number(text: string): boolean {
    phone_pattern = "^\\+?[1-9]\\d{1,14}$";
    return test(phone_pattern, text);
}

function is_ipv4(text: string): boolean {
    ipv4_pattern = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$";
    return test(ipv4_pattern, text);
}

function is_ipv6(text: string): boolean {
    ipv6_pattern = "^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::$";
    return test(ipv6_pattern, text);
}

function is_uuid(text: string): boolean {
    uuid_pattern = "^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$";
    return test(uuid_pattern, text);
}

function is_hex_color(text: string): boolean {
    hex_color_pattern = "^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$";
    return test(hex_color_pattern, text);
}

// Text extraction helpers
function extract_emails(text: string) {
    email_pattern = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}";
    return find_all(email_pattern, text);
}

function extract_urls(text: string) {
    url_pattern = "https?://[^\\s/$.?#].[^\\s]*";
    return find_all(url_pattern, text);
}

function extract_phone_numbers(text: string) {
    phone_pattern = "\\+?[1-9]\\d{1,14}";
    return find_all(phone_pattern, text);
}

function extract_numbers(text: string) {
    number_pattern = "\\b\\d+(?:\\.\\d+)?\\b";
    return find_all(number_pattern, text);
}

function extract_words(text: string) {
    word_pattern = "\\b[a-zA-Z]+\\b";
    return find_all(word_pattern, text);
}

// Text cleaning functions
function remove_html_tags(text: string): string {
    html_pattern = "<[^>]*>";
    return replace_all(html_pattern, text, "");
}

function remove_extra_whitespace(text: string): string {
    whitespace_pattern = "\\s+";
    return replace_all(whitespace_pattern, text, " ");
}

function remove_non_alphanumeric(text: string): string {
    non_alnum_pattern = "[^a-zA-Z0-9\\s]";
    return replace_all(non_alnum_pattern, text, "");
}

function normalize_whitespace(text: string): string {
    // Replace tabs, newlines, etc. with single spaces
    whitespace_pattern = "[\\t\\n\\r\\f\\v]+";
    cleaned = replace_all(whitespace_pattern, text, " ");
    return remove_extra_whitespace(cleaned);
}

// Pattern building utilities
function create_word_boundary_pattern(word: string): string {
    escaped_word = escape_string(word);
    return "\\b" + escaped_word + "\\b";
}

function create_case_insensitive_pattern(pattern: string): string {
    return "(?i)" + pattern;
}

function create_multiline_pattern(pattern: string): string {
    return "(?m)" + pattern;
}

function create_dotall_pattern(pattern: string): string {
    return "(?s)" + pattern;
}

// Security-focused validation patterns
function contains_sql_injection_patterns(text: string): boolean {
    // Basic SQL injection detection
    sql_patterns = [
        "';.*--",
        "\\bunion\\b.*\\bselect\\b",
        "\\bdrop\\b.*\\btable\\b",
        "\\bexec\\b.*\\(",
        "\\/\\*.*\\*\\/"
    ];

    i = 0;
    while (i < sql_patterns.length()) {
        if (test(sql_patterns[i], text)) {
            return true;
        }
        i = i + 1;
    }
    return false;
}

function contains_xss_patterns(text: string): boolean {
    // Basic XSS detection
    xss_patterns = [
        "<script.*?>",
        "javascript:",
        "on\\w+\\s*=",
        "<iframe.*?>"
    ];

    i = 0;
    while (i < xss_patterns.length()) {
        if (test(xss_patterns[i], text)) {
            return true;
        }
        i = i + 1;
    }
    return false;
}

function sanitize_for_regex(text: string): string {
    // Escape characters that have special meaning in regex
    return escape_string(text);
}