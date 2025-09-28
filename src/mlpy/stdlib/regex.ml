// @description: Regular expression pattern matching with security validation and object-oriented interface
// @capability: execute:regex_operations
// @capability: read:pattern_data
// @version: 2.0.0

/**
 * ML Regex Standard Library
 * Provides regular expression pattern matching with input validation, security checks, and object-oriented API
 */

capability RegexOperations {
    allow execute "regex_operations";
    allow read "pattern_data";
}

// Pattern object constructor - creates object with methods and properties
function create_pattern(pattern_string: string) {
    // Validate pattern for security
    if (!__python_bridge("regex.is_valid", pattern_string)) {
        return null;
    }

    // Compile pattern for performance
    compiled_id = __python_bridge("regex.compile", pattern_string);

    return {
        pattern: pattern_string,
        compiled_id: compiled_id,
        is_compiled: compiled_id != "",

        // Test methods
        test: function(text) {
            if (pattern_obj.is_compiled) {
                return __python_bridge("regex.test_compiled", pattern_obj.compiled_id, text);
            }
            return __python_bridge("regex.test", pattern_obj.pattern, text);
        },

        matches: function(text) {
            return pattern_obj.test(text);
        },

        // Match methods
        match: function(text) {
            if (pattern_obj.is_compiled) {
                return __python_bridge("regex.match_compiled", pattern_obj.compiled_id, text);
            }
            return __python_bridge("regex.match", pattern_obj.pattern, text);
        },

        find_first: function(text) {
            return __python_bridge("regex.find_first", pattern_obj.pattern, text);
        },

        find_all: function(text) {
            return __python_bridge("regex.find_all", pattern_obj.pattern, text);
        },

        find_with_groups: function(text) {
            return __python_bridge("regex.find_with_groups", pattern_obj.pattern, text);
        },

        find_all_with_groups: function(text) {
            return __python_bridge("regex.find_all_with_groups", pattern_obj.pattern, text);
        },

        find_with_positions: function(text) {
            return __python_bridge("regex.find_with_positions", pattern_obj.pattern, text);
        },

        // Replacement methods
        replace: function(text, replacement) {
            return __python_bridge("regex.replace", pattern_obj.pattern, text, replacement);
        },

        replace_all: function(text, replacement) {
            return __python_bridge("regex.replace_all", pattern_obj.pattern, text, replacement);
        },

        replace_with_function: function(text, replacer_func) {
            return __python_bridge("regex.replace_with_function", pattern_obj.pattern, text, replacer_func);
        },

        // Split methods
        split: function(text) {
            return __python_bridge("regex.split", pattern_obj.pattern, text);
        },

        split_with_limit: function(text, max_splits) {
            return __python_bridge("regex.split_with_limit", pattern_obj.pattern, text, max_splits);
        },

        // Count and utility methods
        count_matches: function(text) {
            return __python_bridge("regex.count_matches", pattern_obj.pattern, text);
        },

        is_valid: function() {
            return __python_bridge("regex.is_valid", pattern_obj.pattern);
        },

        // Pattern information
        get_pattern: function() {
            return pattern_obj.pattern;
        },

        get_compiled_id: function() {
            return pattern_obj.compiled_id;
        },

        // String representation
        toString: function() {
            return "Pattern: " + pattern_obj.pattern;
        }
    };
}

// MatchResult object constructor - represents match results with position information
function create_match_result(match_text: string, start_pos: number, end_pos: number, groups: array) {
    return {
        text: match_text,
        start: start_pos,
        end: end_pos,
        groups: groups,
        length: match_text.length,

        // Property getters
        get_text: function() {
            return match_result_obj.text;
        },

        get_start: function() {
            return match_result_obj.start;
        },

        get_end: function() {
            return match_result_obj.end;
        },

        get_length: function() {
            return match_result_obj.length;
        },

        get_groups: function() {
            return match_result_obj.groups;
        },

        // Group access methods
        group: function(index) {
            if (index >= 0 && index < match_result_obj.groups.length) {
                return match_result_obj.groups[index];
            }
            return null;
        },

        group_count: function() {
            return match_result_obj.groups.length;
        },

        has_groups: function() {
            return match_result_obj.groups.length > 0;
        },

        // Utility methods
        substring: function(start_offset, end_offset) {
            actual_start = match_result_obj.start + start_offset;
            actual_end = match_result_obj.start + end_offset;
            return string.substring(match_result_obj.text, actual_start, actual_end);
        },

        // String representation
        toString: function() {
            return "Match: '" + match_result_obj.text + "' at " +
                   string.toString(match_result_obj.start) + "-" + string.toString(match_result_obj.end);
        }
    };
}

// PatternBuilder object constructor - helps build complex patterns
function create_pattern_builder() {
    return {
        pattern_parts: [],
        flags: [],

        // Basic pattern building
        add: function(pattern_part) {
            builder_obj.pattern_parts = safe_append(builder_obj.pattern_parts, pattern_part);
            return builder_obj;
        },

        add_literal: function(text) {
            escaped_text = __python_bridge("regex.escape", text);
            return builder_obj.add(escaped_text);
        },

        add_group: function(pattern_part) {
            return builder_obj.add("(" + pattern_part + ")");
        },

        add_optional: function(pattern_part) {
            return builder_obj.add("(" + pattern_part + ")?");
        },

        add_one_or_more: function(pattern_part) {
            return builder_obj.add("(" + pattern_part + ")+");
        },

        add_zero_or_more: function(pattern_part) {
            return builder_obj.add("(" + pattern_part + ")*");
        },

        // Character classes
        add_any_char: function() {
            return builder_obj.add(".");
        },

        add_word_char: function() {
            return builder_obj.add("\\w");
        },

        add_digit: function() {
            return builder_obj.add("\\d");
        },

        add_whitespace: function() {
            return builder_obj.add("\\s");
        },

        add_word_boundary: function() {
            return builder_obj.add("\\b");
        },

        // Anchors
        add_start_anchor: function() {
            return builder_obj.add("^");
        },

        add_end_anchor: function() {
            return builder_obj.add("$");
        },

        // Quantifiers
        add_exact_count: function(pattern_part, count) {
            return builder_obj.add("(" + pattern_part + "){" + string.toString(count) + "}");
        },

        add_range_count: function(pattern_part, min_count, max_count) {
            return builder_obj.add("(" + pattern_part + "){" + string.toString(min_count) + "," + string.toString(max_count) + "}");
        },

        add_min_count: function(pattern_part, min_count) {
            return builder_obj.add("(" + pattern_part + "){" + string.toString(min_count) + ",}");
        },

        // Alternation
        add_or: function() {
            return builder_obj.add("|");
        },

        add_alternatives: function(alternatives) {
            if (alternatives.length > 0) {
                pattern_part = "(";
                i = 0;
                while (i < alternatives.length) {
                    if (i > 0) {
                        pattern_part = pattern_part + "|";
                    }
                    pattern_part = pattern_part + alternatives[i];
                    i = i + 1;
                }
                pattern_part = pattern_part + ")";
                return builder_obj.add(pattern_part);
            }
            return builder_obj;
        },

        // Character sets
        add_char_set: function(chars) {
            char_set = "[";
            i = 0;
            while (i < chars.length) {
                char_set = char_set + __python_bridge("regex.escape", chars[i]);
                i = i + 1;
            }
            char_set = char_set + "]";
            return builder_obj.add(char_set);
        },

        add_char_range: function(start_char, end_char) {
            escaped_start = __python_bridge("regex.escape", start_char);
            escaped_end = __python_bridge("regex.escape", end_char);
            return builder_obj.add("[" + escaped_start + "-" + escaped_end + "]");
        },

        add_negated_char_set: function(chars) {
            char_set = "[^";
            i = 0;
            while (i < chars.length) {
                char_set = char_set + __python_bridge("regex.escape", chars[i]);
                i = i + 1;
            }
            char_set = char_set + "]";
            return builder_obj.add(char_set);
        },

        // Flags
        case_insensitive: function() {
            builder_obj.flags = safe_append(builder_obj.flags, "i");
            return builder_obj;
        },

        multiline: function() {
            builder_obj.flags = safe_append(builder_obj.flags, "m");
            return builder_obj;
        },

        dotall: function() {
            builder_obj.flags = safe_append(builder_obj.flags, "s");
            return builder_obj;
        },

        // Build final pattern
        build: function() {
            final_pattern = "";
            i = 0;
            while (i < builder_obj.pattern_parts.length) {
                final_pattern = final_pattern + builder_obj.pattern_parts[i];
                i = i + 1;
            }

            // Add flags if any
            if (builder_obj.flags.length > 0) {
                flag_string = "(?";
                j = 0;
                while (j < builder_obj.flags.length) {
                    flag_string = flag_string + builder_obj.flags[j];
                    j = j + 1;
                }
                flag_string = flag_string + ")";
                final_pattern = flag_string + final_pattern;
            }

            return create_pattern(final_pattern);
        },

        // String representation
        toString: function() {
            temp_pattern = "";
            i = 0;
            while (i < builder_obj.pattern_parts.length) {
                temp_pattern = temp_pattern + builder_obj.pattern_parts[i];
                i = i + 1;
            }
            return "PatternBuilder: " + temp_pattern;
        }
    };
}

// Factory functions for creating pattern objects
function compile(pattern_string: string) {
    return create_pattern(pattern_string);
}

function pattern(pattern_string: string) {
    return create_pattern(pattern_string);
}

function builder() {
    return create_pattern_builder();
}

// Common pre-built patterns as objects
function email_pattern() {
    return create_pattern("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$");
}

function url_pattern() {
    return create_pattern("^https?://[^\\s/$.?#].[^\\s]*$");
}

function phone_pattern() {
    return create_pattern("^\\+?[1-9]\\d{1,14}$");
}

function ipv4_pattern() {
    return create_pattern("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$");
}

function ipv6_pattern() {
    return create_pattern("^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::$");
}

function uuid_pattern() {
    return create_pattern("^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$");
}

function hex_color_pattern() {
    return create_pattern("^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$");
}

// Legacy function compatibility (for backward compatibility)
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

function replace(pattern: string, text: string, replacement: string): string {
    return __python_bridge("regex.replace", pattern, text, replacement);
}

function replace_all(pattern: string, text: string, replacement: string): string {
    return __python_bridge("regex.replace_all", pattern, text, replacement);
}

function replace_with_function(pattern: string, text: string, replacer_func): string {
    return __python_bridge("regex.replace_with_function", pattern, text, replacer_func);
}

function split(pattern: string, text: string) {
    return __python_bridge("regex.split", pattern, text);
}

function split_with_limit(pattern: string, text: string, max_splits: number) {
    return __python_bridge("regex.split_with_limit", pattern, text, max_splits);
}

function compile_pattern(pattern: string): string {
    return __python_bridge("regex.compile", pattern);
}

function test_compiled(compiled_pattern: string, text: string): boolean {
    return __python_bridge("regex.test_compiled", compiled_pattern, text);
}

function match_compiled(compiled_pattern: string, text: string) {
    return __python_bridge("regex.match_compiled", compiled_pattern, text);
}

function find_with_groups(pattern: string, text: string) {
    return __python_bridge("regex.find_with_groups", pattern, text);
}

function find_all_with_groups(pattern: string, text: string) {
    return __python_bridge("regex.find_all_with_groups", pattern, text);
}

function find_with_positions(pattern: string, text: string) {
    return __python_bridge("regex.find_with_positions", pattern, text);
}

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
    email_p = email_pattern();
    return email_p.test(text);
}

function is_url(text: string): boolean {
    url_p = url_pattern();
    return url_p.test(text);
}

function is_phone_number(text: string): boolean {
    phone_p = phone_pattern();
    return phone_p.test(text);
}

function is_ipv4(text: string): boolean {
    ipv4_p = ipv4_pattern();
    return ipv4_p.test(text);
}

function is_ipv6(text: string): boolean {
    ipv6_p = ipv6_pattern();
    return ipv6_p.test(text);
}

function is_uuid(text: string): boolean {
    uuid_p = uuid_pattern();
    return uuid_p.test(text);
}

function is_hex_color(text: string): boolean {
    hex_p = hex_color_pattern();
    return hex_p.test(text);
}

// Text extraction helpers
function extract_emails(text: string) {
    email_pattern_str = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}";
    return find_all(email_pattern_str, text);
}

function extract_urls(text: string) {
    url_pattern_str = "https?://[^\\s/$.?#].[^\\s]*";
    return find_all(url_pattern_str, text);
}

function extract_phone_numbers(text: string) {
    phone_pattern_str = "\\+?[1-9]\\d{1,14}";
    return find_all(phone_pattern_str, text);
}

function extract_numbers(text: string) {
    number_pattern_str = "\\b\\d+(?:\\.\\d+)?\\b";
    return find_all(number_pattern_str, text);
}

function extract_words(text: string) {
    word_pattern_str = "\\b[a-zA-Z]+\\b";
    return find_all(word_pattern_str, text);
}

// Text cleaning functions
function remove_html_tags(text: string): string {
    html_pattern_str = "<[^>]*>";
    return replace_all(html_pattern_str, text, "");
}

function remove_extra_whitespace(text: string): string {
    whitespace_pattern_str = "\\s+";
    return replace_all(whitespace_pattern_str, text, " ");
}

function remove_non_alphanumeric(text: string): string {
    non_alnum_pattern_str = "[^a-zA-Z0-9\\s]";
    return replace_all(non_alnum_pattern_str, text, "");
}

function normalize_whitespace(text: string): string {
    // Replace tabs, newlines, etc. with single spaces
    whitespace_pattern_str = "[\\t\\n\\r\\f\\v]+";
    cleaned = replace_all(whitespace_pattern_str, text, " ");
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
    while (i < sql_patterns.length) {
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
    while (i < xss_patterns.length) {
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