// @description: Functional programming utilities with higher-order functions
// @capability: execute:functional_operations
// @capability: read:function_data
// @version: 1.0.0

/**
 * ML Functional Programming Standard Library
 * Provides comprehensive functional programming operations
 * Inspired by Ramda, Lodash/FP, and Haskell
 */

capability FunctionalOperations {
    allow execute "functional_operations";
    allow read "function_data";
}

// =============================================================================
// CORE HIGHER-ORDER FUNCTIONS
// =============================================================================

// Map: Transform each element of a list
function map(fn, list) {
    result = [];
    i = 0;
    while (i < length(list)) {
        transformed = fn(list[i]);
        result = append(result, transformed);
        i = i + 1;
    }
    return result;
}

// Filter: Select elements that match a predicate
function filter(predicate, list) {
    result = [];
    i = 0;
    while (i < length(list)) {
        element = list[i];
        if (predicate(element)) {
            result = append(result, element);
        }
        i = i + 1;
    }
    return result;
}

// Reduce: Accumulate list elements into a single value
function reduce(reducer, initial, list) {
    accumulator = initial;
    i = 0;
    while (i < length(list)) {
        accumulator = reducer(accumulator, list[i]);
        i = i + 1;
    }
    return accumulator;
}

// ReduceRight: Reduce from right to left
function reduceRight(reducer, initial, list) {
    accumulator = initial;
    i = length(list) - 1;
    while (i >= 0) {
        accumulator = reducer(accumulator, list[i]);
        i = i - 1;
    }
    return accumulator;
}

// ForEach: Execute a function for each element (side effects)
function forEach(fn, list) {
    i = 0;
    while (i < length(list)) {
        fn(list[i]);
        i = i + 1;
    }
    return list; // Return original list for chaining
}

// =============================================================================
// SEARCH AND SELECTION FUNCTIONS
// =============================================================================

// Find: Get the first element that matches predicate
function find(predicate, list) {
    i = 0;
    while (i < length(list)) {
        element = list[i];
        if (predicate(element)) {
            return element;
        }
        i = i + 1;
    }
    return null; // Not found
}

// FindIndex: Get the index of first element that matches predicate
function findIndex(predicate, list) {
    i = 0;
    while (i < length(list)) {
        if (predicate(list[i])) {
            return i;
        }
        i = i + 1;
    }
    return -1; // Not found
}

// Some: Check if any element matches predicate
function some(predicate, list) {
    i = 0;
    while (i < length(list)) {
        if (predicate(list[i])) {
            return true;
        }
        i = i + 1;
    }
    return false;
}

// Every: Check if all elements match predicate
function every(predicate, list) {
    i = 0;
    while (i < length(list)) {
        if (!predicate(list[i])) {
            return false;
        }
        i = i + 1;
    }
    return true;
}

// None: Check if no elements match predicate
function none(predicate, list) {
    return !some(predicate, list);
}

// =============================================================================
// FUNCTION COMPOSITION AND UTILITIES
// =============================================================================

// Identity: Return input unchanged
function identity(x) {
    return x;
}

// Constant: Return a function that always returns the same value
function constant(value) {
    return function(x) {
        return value;
    };
}

// Compose: Right-to-left function composition f(g(x))
function compose(f, g) {
    return function(x) {
        return f(g(x));
    };
}

// Pipe: Left-to-right function composition g(f(x))
function pipe(f, g) {
    return function(x) {
        return g(f(x));
    };
}

// Flip: Flip the order of the first two arguments
function flip(fn) {
    return function(a, b) {
        return fn(b, a);
    };
}

// Negate: Logical negation of a predicate function
function negate(predicate) {
    return function(x) {
        return !predicate(x);
    };
}

// =============================================================================
// PARTIAL APPLICATION AND CURRYING
// =============================================================================

// Partial: Partially apply arguments to a function
function partial(fn, ...args) {
    return function(...remainingArgs) {
        return fn(...args, ...remainingArgs);
    };
}

// Curry2: Curry a 2-argument function
function curry2(fn) {
    return function(a) {
        return function(b) {
            return fn(a, b);
        };
    };
}

// Curry3: Curry a 3-argument function
function curry3(fn) {
    return function(a) {
        return function(b) {
            return function(c) {
                return fn(a, b, c);
            };
        };
    };
}

// =============================================================================
// LIST PROCESSING FUNCTIONS
// =============================================================================

// FlatMap: Map and then flatten the results
function flatMap(fn, list) {
    mapped = map(fn, list);
    return flatten(mapped);
}

// Flatten: Flatten a nested array one level deep
function flatten(nestedList) {
    result = [];
    i = 0;
    while (i < length(nestedList)) {
        element = nestedList[i];
        if (isArray(element)) {
            // Flatten one level
            j = 0;
            while (j < length(element)) {
                result = append(result, element[j]);
                j = j + 1;
            }
        } else {
            result = append(result, element);
        }
        i = i + 1;
    }
    return result;
}

// Zip: Combine two arrays into pairs
function zip(list1, list2) {
    result = [];
    minLength = min(length(list1), length(list2));
    i = 0;
    while (i < minLength) {
        pair = [list1[i], list2[i]];
        result = append(result, pair);
        i = i + 1;
    }
    return result;
}

// ZipWith: Zip two arrays with a combining function
function zipWith(fn, list1, list2) {
    result = [];
    minLength = min(length(list1), length(list2));
    i = 0;
    while (i < minLength) {
        combined = fn(list1[i], list2[i]);
        result = append(result, combined);
        i = i + 1;
    }
    return result;
}

// Unzip: Separate an array of pairs into two arrays
function unzip(pairList) {
    first = [];
    second = [];
    i = 0;
    while (i < length(pairList)) {
        pair = pairList[i];
        if (length(pair) >= 2) {
            first = append(first, pair[0]);
            second = append(second, pair[1]);
        }
        i = i + 1;
    }
    return [first, second];
}

// =============================================================================
// DATA TRANSFORMATION FUNCTIONS
// =============================================================================

// Partition: Split list into two based on predicate
function partition(predicate, list) {
    truthy = [];
    falsy = [];
    i = 0;
    while (i < length(list)) {
        element = list[i];
        if (predicate(element)) {
            truthy = append(truthy, element);
        } else {
            falsy = append(falsy, element);
        }
        i = i + 1;
    }
    return [truthy, falsy];
}

// GroupBy: Group elements by a key function
function groupBy(keyFn, list) {
    groups = {};
    i = 0;
    while (i < length(list)) {
        element = list[i];
        key = keyFn(element);

        if (key in groups) {
            groups[key] = append(groups[key], element);
        } else {
            groups[key] = [element];
        }
        i = i + 1;
    }
    return groups;
}

// Unique: Remove duplicate elements
function unique(list) {
    seen = {};
    result = [];
    i = 0;
    while (i < length(list)) {
        element = list[i];
        elementStr = toString(element);

        if (!(elementStr in seen)) {
            seen[elementStr] = true;
            result = append(result, element);
        }
        i = i + 1;
    }
    return result;
}

// UniqueBy: Remove duplicates based on a key function
function uniqueBy(keyFn, list) {
    seen = {};
    result = [];
    i = 0;
    while (i < length(list)) {
        element = list[i];
        key = toString(keyFn(element));

        if (!(key in seen)) {
            seen[key] = true;
            result = append(result, element);
        }
        i = i + 1;
    }
    return result;
}

// =============================================================================
// LIST SLICING AND MANIPULATION
// =============================================================================

// Take: Take the first n elements
function take(n, list) {
    if (n <= 0) {
        return [];
    }

    result = [];
    maxIndex = min(n, length(list));
    i = 0;
    while (i < maxIndex) {
        result = append(result, list[i]);
        i = i + 1;
    }
    return result;
}

// Drop: Skip the first n elements
function drop(n, list) {
    if (n <= 0) {
        return list;
    }

    result = [];
    i = n;
    while (i < length(list)) {
        result = append(result, list[i]);
        i = i + 1;
    }
    return result;
}

// TakeWhile: Take elements while predicate is true
function takeWhile(predicate, list) {
    result = [];
    i = 0;
    while (i < length(list) && predicate(list[i])) {
        result = append(result, list[i]);
        i = i + 1;
    }
    return result;
}

// DropWhile: Drop elements while predicate is true
function dropWhile(predicate, list) {
    i = 0;
    // Find first element where predicate is false
    while (i < length(list) && predicate(list[i])) {
        i = i + 1;
    }

    // Return rest of list
    result = [];
    while (i < length(list)) {
        result = append(result, list[i]);
        i = i + 1;
    }
    return result;
}

// =============================================================================
// CONDITIONAL FUNCTIONS
// =============================================================================

// IfElse: Conditional function application
function ifElse(predicate, thenFn, elseFn) {
    return function(x) {
        if (predicate(x)) {
            return thenFn(x);
        } else {
            return elseFn(x);
        }
    };
}

// When: Apply function only if condition is true
function when(predicate, fn) {
    return function(x) {
        if (predicate(x)) {
            return fn(x);
        } else {
            return x;
        }
    };
}

// Unless: Apply function only if condition is false
function unless(predicate, fn) {
    return when(negate(predicate), fn);
}

// Cond: Multi-condition case-like function
function cond(conditionPairs) {
    return function(x) {
        i = 0;
        while (i < length(conditionPairs)) {
            pair = conditionPairs[i];
            predicate = pair[0];
            action = pair[1];

            if (predicate(x)) {
                return action(x);
            }
            i = i + 1;
        }
        return x; // Default case
    };
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

// Range: Create a list of numbers
function range(start, end, step) {
    if (step == null) {
        step = 1;
    }

    result = [];
    current = start;

    if (step > 0) {
        while (current < end) {
            result = append(result, current);
            current = current + step;
        }
    } else if (step < 0) {
        while (current > end) {
            result = append(result, current);
            current = current + step;
        }
    }

    return result;
}

// Repeat: Create a list with repeated value
function repeat(value, count) {
    result = [];
    i = 0;
    while (i < count) {
        result = append(result, value);
        i = i + 1;
    }
    return result;
}

// Times: Execute a function n times and collect results
function times(fn, count) {
    result = [];
    i = 0;
    while (i < count) {
        result = append(result, fn(i));
        i = i + 1;
    }
    return result;
}

// =============================================================================
// HELPER FUNCTIONS (would be implemented by runtime)
// =============================================================================

// These functions would need to be implemented by the ML runtime
// or bridged to Python implementations

function length(list) {
    // Return length of array/list
    return __python_bridge("len", list);
}

function append(list, element) {
    // Add element to end of list
    return __python_bridge("list_append", list, element);
}

function isArray(value) {
    // Check if value is an array
    return __python_bridge("isinstance", value, "list");
}

function toString(value) {
    // Convert value to string representation
    return __python_bridge("str", value);
}

function min(a, b) {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

function max(a, b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

// =============================================================================
// ADVANCED FUNCTIONAL UTILITIES
// =============================================================================

// Memoize: Cache function results for performance
function memoize(fn) {
    cache = {};
    return function(x) {
        key = toString(x);
        if (key in cache) {
            return cache[key];
        } else {
            result = fn(x);
            cache[key] = result;
            return result;
        }
    };
}

// Trampoline: Handle tail-call optimization manually
function trampoline(fn) {
    return function(...args) {
        result = fn(...args);
        while (typeof result == "function") {
            result = result();
        }
        return result;
    };
}

// Y Combinator: Enable recursion in pure functional style
function Y(f) {
    return function(x) {
        return f(Y(f))(x);
    };
}

// =============================================================================
// FUNCTION COMPOSITION HELPERS
// =============================================================================

// ComposeAll: Compose multiple functions right-to-left
function composeAll(functions) {
    return reduce(compose, identity, functions);
}

// PipeAll: Compose multiple functions left-to-right
function pipeAll(functions) {
    return reduce(pipe, identity, functions);
}

// Juxt: Apply multiple functions to same input and return array of results
function juxt(functions) {
    return function(x) {
        return map(function(fn) { return fn(x); }, functions);
    };
}