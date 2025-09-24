// @description: String manipulation utilities with security validation
// @capability: execute:string_operations
// @version: 1.0.0

/**
 * ML String Standard Library
 * Provides string manipulation functions with input validation
 */

capability StringOperations {
    allow execute "string_operations";
}

// String length function
function length(text: string): number {
    return __python_bridge("len", text);
}

// String case functions
function upper(text: string): string {
    return __python_bridge("str.upper", text);
}

function lower(text: string): string {
    return __python_bridge("str.lower", text);
}

function capitalize(text: string): string {
    return __python_bridge("str.capitalize", text);
}

function title(text: string): string {
    return __python_bridge("str.title", text);
}

// String search functions
function contains(text: string, pattern: string): boolean {
    return __python_bridge("str.__contains__", text, pattern);
}

function starts_with(text: string, prefix: string): boolean {
    return __python_bridge("str.startswith", text, prefix);
}

function ends_with(text: string, suffix: string): boolean {
    return __python_bridge("str.endswith", text, suffix);
}

function find(text: string, pattern: string): number {
    return __python_bridge("str.find", text, pattern);
}

function index_of(text: string, pattern: string): number {
    result = find(text, pattern);
    if (result == -1) {
        return -1; // Not found
    }
    return result;
}

// String modification functions
function replace(text: string, old_pattern: string, new_pattern: string): string {
    return __python_bridge("str.replace", text, old_pattern, new_pattern);
}

function replace_all(text: string, old_pattern: string, new_pattern: string): string {
    return replace(text, old_pattern, new_pattern);
}

function strip(text: string): string {
    return __python_bridge("str.strip", text);
}

function trim(text: string): string {
    return strip(text);
}

function lstrip(text: string): string {
    return __python_bridge("str.lstrip", text);
}

function rstrip(text: string): string {
    return __python_bridge("str.rstrip", text);
}

// String splitting and joining
function split(text: string, delimiter: string) {
    return __python_bridge("str.split", text, delimiter);
}

function join(separator: string, parts) {
    return __python_bridge("str.join", separator, parts);
}

// String validation functions
function is_empty(text: string): boolean {
    return length(text) == 0;
}

function is_whitespace(text: string): boolean {
    return __python_bridge("str.isspace", text);
}

function is_alpha(text: string): boolean {
    return __python_bridge("str.isalpha", text);
}

function is_numeric(text: string): boolean {
    return __python_bridge("str.isnumeric", text);
}

function is_alphanumeric(text: string): boolean {
    return __python_bridge("str.isalnum", text);
}

// String slicing functions
function substring(text: string, start: number, end: number): string {
    return __python_bridge("slice", text, start, end);
}

function left(text: string, count: number): string {
    return substring(text, 0, count);
}

function right(text: string, count: number): string {
    text_length = length(text);
    return substring(text, text_length - count, text_length);
}

// String padding functions
function pad_left(text: string, width: number, fill_char: string): string {
    return __python_bridge("str.rjust", text, width, fill_char);
}

function pad_right(text: string, width: number, fill_char: string): string {
    return __python_bridge("str.ljust", text, width, fill_char);
}

function pad_center(text: string, width: number, fill_char: string): string {
    return __python_bridge("str.center", text, width, fill_char);
}

// String comparison functions
function compare(text1: string, text2: string): number {
    if (text1 == text2) {
        return 0;
    } else if (text1 < text2) {
        return -1;
    } else {
        return 1;
    }
}

function compare_ignore_case(text1: string, text2: string): number {
    return compare(lower(text1), lower(text2));
}

// String encoding functions (safe subset)
function encode_html(text: string): string {
    // Basic HTML encoding for safety
    result = replace(text, "&", "&amp;");
    result = replace(result, "<", "&lt;");
    result = replace(result, ">", "&gt;");
    result = replace(result, "\"", "&quot;");
    result = replace(result, "'", "&#x27;");
    return result;
}

function reverse(text: string): string {
    // Simple character reversal
    return __python_bridge("reverse_string", text);
}