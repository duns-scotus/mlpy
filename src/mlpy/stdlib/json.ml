// @description: JSON encoding and decoding with security validation
// @capability: read:json_data
// @capability: write:json_data
// @version: 1.0.0

/**
 * ML JSON Standard Library
 * Provides safe JSON operations with input validation
 */

capability JSONOperations {
    allow read "json_data";
    allow write "json_data";
}

// JSON serialization function
function dumps(obj): string {
    // Serialize object to JSON string with Python bridge
    return __python_bridge("json.dumps", obj);
}

function dumps_pretty(obj): string {
    // Serialize object to JSON string with pretty formatting
    return __python_bridge("json.dumps", obj, true, null, 4);
}

// JSON deserialization function
function loads(json_string: string) {
    // Parse JSON string to object with Python bridge
    return __python_bridge("json.loads", json_string);
}

// Safe JSON parsing with validation
function safe_loads(json_string: string, max_depth: number) {
    // Validate input before parsing
    if (max_depth > 100) {
        // Prevent deeply nested JSON attacks
        max_depth = 100;
    }

    // TODO: Add depth validation in bridge function
    return loads(json_string);
}

// Utility functions for JSON validation
function is_valid_json(json_string: string): boolean {
    try {
        loads(json_string);
        return true;
    } except {
        return false;
    }
}

// JSON type checking functions
function is_json_object(obj): boolean {
    return typeof(obj) == "object" && obj != null && !is_array(obj);
}

function is_json_array(obj): boolean {
    return is_array(obj);
}

function is_json_string(obj): boolean {
    return typeof(obj) == "string";
}

function is_json_number(obj): boolean {
    return typeof(obj) == "number";
}

function is_json_boolean(obj): boolean {
    return typeof(obj) == "boolean";
}

function is_json_null(obj): boolean {
    return obj == null;
}

// Helper function to check if object is an array
function is_array(obj): boolean {
    // This would need to be implemented based on ML's type system
    return false; // Placeholder
}