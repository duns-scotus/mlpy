// @description: List and dictionary operations for ML standard library
// @version: 1.0.0

/**
 * ML Collections Standard Library
 * Provides essential list and dictionary operations using only implemented ML features
 */

// =============================================================================
// LIST OPERATIONS
// =============================================================================

// Get length of a list by iterating until null
function length(list) {
    count = 0;
    i = 0;
    while (i >= 0) {
        if (list[i] != null) {
            count = count + 1;
            i = i + 1;
        } else {
            return count;
        }
    }
    return count;
}

// Add element to end of list
function append(list, element) {
    new_list = [];
    len = length(list);

    // Copy existing elements
    i = 0;
    while (i < len) {
        new_list[i] = list[i];
        i = i + 1;
    }

    // Add new element
    new_list[len] = element;
    return new_list;
}

// Add element to beginning of list
function prepend(list, element) {
    new_list = [];
    len = length(list);

    // Add new element first
    new_list[0] = element;

    // Copy existing elements
    i = 0;
    while (i < len) {
        new_list[i + 1] = list[i];
        i = i + 1;
    }

    return new_list;
}

// Remove element at specific index
function removeAt(list, index) {
    len = length(list);

    if (index < 0 || index >= len) {
        return list; // Invalid index, return original
    }

    new_list = [];
    new_index = 0;

    i = 0;
    while (i < len) {
        if (i != index) {
            new_list[new_index] = list[i];
            new_index = new_index + 1;
        }
        i = i + 1;
    }

    return new_list;
}

// Get element at index, return null if out of bounds
function get(list, index) {
    if (index < 0 || index >= length(list)) {
        return null;
    }
    return list[index];
}

// Get first element
function first(list) {
    return get(list, 0);
}

// Get last element
function last(list) {
    len = length(list);
    if (len == 0) {
        return null;
    }
    return list[len - 1];
}

// Check if list contains element
function contains(list, element) {
    len = length(list);
    i = 0;
    while (i < len) {
        if (list[i] == element) {
            return true;
        }
        i = i + 1;
    }
    return false;
}

// Find index of element, return -1 if not found
function indexOf(list, element) {
    len = length(list);
    i = 0;
    while (i < len) {
        if (list[i] == element) {
            return i;
        }
        i = i + 1;
    }
    return -1;
}

// Create a slice of the list
function slice(list, start, end) {
    len = length(list);

    // Handle negative indices and defaults
    if (start < 0) {
        start = 0;
    }
    if (end == null || end > len) {
        end = len;
    }
    if (end <= start) {
        return [];
    }

    new_list = [];
    new_index = 0;

    i = start;
    while (i < end) {
        new_list[new_index] = list[i];
        new_index = new_index + 1;
        i = i + 1;
    }

    return new_list;
}

// Concatenate two lists
function concat(list1, list2) {
    len1 = length(list1);
    len2 = length(list2);
    new_list = [];

    // Copy first list
    i = 0;
    while (i < len1) {
        new_list[i] = list1[i];
        i = i + 1;
    }

    // Copy second list
    i = 0;
    while (i < len2) {
        new_list[len1 + i] = list2[i];
        i = i + 1;
    }

    return new_list;
}

// Reverse a list
function reverse(list) {
    len = length(list);
    new_list = [];

    i = 0;
    while (i < len) {
        new_list[i] = list[len - 1 - i];
        i = i + 1;
    }

    return new_list;
}

// Filter list elements matching predicate
function filter(list, predicate) {
    len = length(list);
    filtered = [];
    filtered_index = 0;

    i = 0;
    while (i < len) {
        element = list[i];
        if (predicate(element)) {
            filtered[filtered_index] = element;
            filtered_index = filtered_index + 1;
        }
        i = i + 1;
    }

    return filtered;
}

// Transform list elements with function
function map(list, transform) {
    len = length(list);
    mapped = [];

    i = 0;
    while (i < len) {
        mapped[i] = transform(list[i]);
        i = i + 1;
    }

    return mapped;
}

// Find first element matching predicate
function find(list, predicate) {
    len = length(list);
    i = 0;
    while (i < len) {
        element = list[i];
        if (predicate(element)) {
            return element;
        }
        i = i + 1;
    }
    return null;
}

// Reduce list to single value
function reduce(list, reducer, initial) {
    len = length(list);
    accumulator = initial;

    i = 0;
    while (i < len) {
        accumulator = reducer(accumulator, list[i]);
        i = i + 1;
    }

    return accumulator;
}

// =============================================================================
// DICTIONARY/OBJECT OPERATIONS
// =============================================================================

// Get all keys from an object (simplified implementation)
function keys(obj) {
    // This is a limitation - we can't easily iterate over object keys in current ML
    // For now, return empty array - would need runtime support
    return [];
}

// Check if object has property
function hasProperty(obj, key) {
    // Use the 'in' operator available in ML
    return key in obj;
}

// Get property value with default
function getProperty(obj, key, defaultValue) {
    if (hasProperty(obj, key)) {
        return obj[key];
    }
    return defaultValue;
}

// Set property value (returns new object)
function setProperty(obj, key, value) {
    // Create new object with all existing properties plus new one
    new_obj = {};

    // Copy existing properties - limitation: we can't iterate keys easily
    // This would need to be implemented with runtime support
    // For now, just set the new property
    new_obj[key] = value;

    return new_obj;
}

// Remove property (returns new object)
function removeProperty(obj, key) {
    new_obj = {};

    // Copy all properties except the one to remove
    // This would need runtime support to iterate keys
    // For now, return original object

    return obj;
}

// Merge two objects (second object properties override first)
function merge(obj1, obj2) {
    merged = {};

    // Copy properties from both objects
    // This would need runtime support for key iteration
    // For now, return obj2 (simplified)

    return obj2;
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

// Check if value is null or undefined
function isEmpty(value) {
    return value == null;
}

// Safe equality check
function equals(a, b) {
    return a == b;
}

// Clone a list (shallow copy)
function cloneList(list) {
    len = length(list);
    clone = [];

    i = 0;
    while (i < len) {
        clone[i] = list[i];
        i = i + 1;
    }

    return clone;
}

// Clone an object (shallow copy)
function cloneObject(obj) {
    clone = {};

    // Copy all properties
    // This would need runtime support for key iteration
    // For now, return empty object

    return clone;
}

// Convert value to string representation
function toString(value) {
    if (value == null) {
        return "null";
    } else if (value == true) {
        return "true";
    } else if (value == false) {
        return "false";
    } else {
        // For numbers and strings, just convert to string
        return "" + value;
    }
}