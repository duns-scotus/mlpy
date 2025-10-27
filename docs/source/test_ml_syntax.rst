ML Syntax Highlighting Test
=============================

This document tests all improvements to the ML Pygments lexer.

Keywords and Control Flow
--------------------------

Test that all actual keywords are highlighted correctly.

.. code-block:: ml

    // Control flow keywords
    if (condition) {
        return value;
    } elif (other) {
        break;
    } else {
        continue;
    }

    // Loop keywords
    while (running) {
        for (item in collection) {
            // process
        }
    }

    // Exception handling
    try {
        throw { message: "error" };
    } except (e) {
        print(e);
    } finally {
        cleanup();
    }

Comments Test
-------------

**CRITICAL TEST**: Comments should be solid gray with NO internal highlighting.

.. code-block:: ml

    // This comment should be GRAY with NO highlighting of:
    // function, return, if, else, true, false, "strings"

    /*
       Multi-line comment should also be GRAY
       Keywords like function, if, while should NOT highlight
       Strings like "test" should NOT be yellow
       Numbers like 42 should NOT be purple
    */

    function test() {
        // Normal code here should highlight
        return true;
    }

Builtins and Stdlib
-------------------

Test complete 45-function builtin highlighting (cyan, bold).

.. code-block:: ml

    // Type conversion builtins (6 functions) - CYAN
    print(typeof(value));
    x = int("42");
    y = float(3.14);
    z = str(true);
    b = bool(1);
    is_num = isinstance(x, "number");

    // Collection builtins (8 functions) - CYAN
    arr = range(10);
    total = sum(arr);
    size = len(arr);
    for (item in enumerate(arr)) {
        print(item);
    }
    k = keys({a: 1, b: 2});
    v = values({a: 1, b: 2});
    s = sorted([3, 1, 2]);
    pairs = zip([1, 2], ["a", "b"]);

    // Math builtins (4 functions) - CYAN
    absolute = abs(-5);
    minimum = min(1, 2, 3);
    maximum = max(1, 2, 3);
    rounded = round(3.14159, 2);

    // Introspection builtins (6 functions) - CYAN
    help(print);
    m = methods("string");
    mods = modules();
    avail = available_modules();
    exists = has_module("math");
    info = module_info("math");

    // Capability builtins (3 functions) - CYAN
    can_read = hasCapability("file.read");
    caps = getCapabilities();
    cap_info = getCapabilityInfo("file.read");

    // Dynamic introspection (4 functions) - CYAN
    has = hasattr(obj, "prop");
    val = getattr(obj, "prop", null);
    result = call(func, arg1, arg2);
    is_func = callable(func);

    // Iteration builtins (5 functions) - CYAN
    it = iter([1, 2, 3]);
    first = next(it);
    rev = reversed([1, 2, 3]);
    all_true = all([true, true]);
    any_true = any([false, true]);

    // Conversion builtins (7 functions) - CYAN
    char = chr(65);
    code = ord("A");
    hexval = hex(255);
    binval = bin(10);
    octval = oct(8);
    reprval = repr(obj);
    formatted = format(3.14, ".2f");

    // Stdlib modules (require import) - YELLOW
    import console;
    import json;
    import math;
    import datetime;
    import functional;
    import regex;
    import string;
    import collections;
    import file;
    import http;
    import path;
    import random;

    console.log("Hello");
    data = json.parse(text);
    result = math.sqrt(16);

Operators
---------

All operators should be highlighted in pink.

.. code-block:: ml

    // Arithmetic operators (PINK)
    x = 10 + 5 - 3 * 2 / 4 % 2;
    floor_div = 10 // 3;

    // Comparison operators (PINK)
    if (x > 5 && y < 10 || z == 0) {
        equal = a == b;
        not_equal = a != b;
        less = a < b;
        greater = a > b;
        less_eq = a <= b;
        greater_eq = a >= b;
    }

    // Logical operators (PINK)
    and_result = true && false;
    or_result = true || false;
    not_result = !true;

    // Ternary operator (PINK)
    result = condition ? valueIfTrue : valueIfFalse;

    // Arrow function operator (PINK)
    add = fn(x, y) => x + y;

    // Unary operators (PINK)
    negative = -x;
    inverted = !flag;

Functions and Variables
-----------------------

Functions should be green, variables white.

.. code-block:: ml

    // Function definition (function keyword PURPLE, name GREEN)
    function calculateSum(a, b) {
        return a + b;
    }

    // Function call (GREEN)
    result = calculateSum(5, 10);

    // Arrow function (fn keyword PURPLE, => PINK)
    add = fn(x, y) => x + y;
    multiply = fn(a, b) => a * b;

    // Variables (WHITE)
    myVariable = 42;
    another_var = "test";
    data = [1, 2, 3];

Member Access
-------------

Object properties should be italic white, method calls green.

.. code-block:: ml

    // Object property access (property in ITALIC WHITE)
    obj.property = value;
    result = data.field.nested;

    // Method calls (GREEN)
    console.log("message");
    arr.push(item);
    str.upper();

Braces and Parentheses
----------------------

Braces should be bold pink, parentheses pink.

.. code-block:: ml

    // Braces (PINK, bold)
    object = { key: "value", count: 42 };

    // Brackets (PINK, bold)
    array = [1, 2, 3, 4, 5];

    // Parentheses (PINK)
    result = func(arg1, arg2, arg3);

    if (condition) {
        process();
    }

Capability Declarations
-----------------------

Capability blocks should have special highlighting with orange names.

.. code-block:: ml

    // Complete capability block (special highlighting)
    capability FileAccess {
        resource "data/*.json";
        allow read "config.json";
        allow write "output/*.txt";
        allow execute "scripts/*";
    }

    capability NetworkAccess {
        resource "https://api.example.com/*";
        allow network "api.example.com";
    }

    // Function using capability
    function loadData() {
        // Implementation
    }

Boolean Literals and Keywords
------------------------------

Boolean values should be highlighted as keyword constants (purple, bold).

.. code-block:: ml

    // Boolean literals (PURPLE, bold)
    is_valid = true;
    is_error = false;
    empty = null;
    undef = undefined;

    // Should be distinct from variables
    true_value = true;  // true is keyword
    myTrue = false;     // myTrue is variable, false is keyword

Numbers
-------

All number formats should be purple.

.. code-block:: ml

    // Integers (PURPLE)
    count = 42;
    negative = -100;

    // Floats (PURPLE)
    pi = 3.14159;
    temperature = -273.15;

    // Scientific notation (PURPLE)
    avogadro = 6.022e23;
    planck = 6.626e-34;
    large = 1.5e6;

Strings
-------

All string types should be yellow.

.. code-block:: ml

    // Double quotes (YELLOW)
    message = "Hello, World!";

    // Single quotes (YELLOW)
    char = 'x';
    name = 'Alice';

    // Escaped characters (YELLOW)
    path = "C:\\Users\\Documents";
    quote = "He said \"hello\"";

Complete Real-World Example
----------------------------

Comprehensive example showing all features together.

.. code-block:: ml

    // Security-first data processing program
    import json;
    import console;
    import file;

    capability DataAccess {
        resource "data/*.json";
        allow read "data/input.json";
        allow write "data/output.json";
    }

    function processData(filename) {
        // Load and parse data
        raw = file.read(filename);
        data = json.parse(raw);

        // Process each item
        results = [];
        for (item in data) {
            // Transform with ternary
            value = item.valid ? item.value : 0;

            // Apply calculation
            processed = value * 2 + 10;
            results.push(processed);
        }

        // Calculate statistics using builtins
        total = sum(results);
        average = total / len(results);
        minimum = min(results);
        maximum = max(results);

        // Log results
        console.log("Processed " + str(len(results)) + " items");
        console.log("Average: " + str(average));
        console.log("Range: " + str(minimum) + " to " + str(maximum));

        return results;
    }

    // Execute with error handling
    try {
        output = processData("data/input.json");
        file.write("data/output.json", json.stringify(output));
        console.log("Processing complete!");
    } except (e) {
        console.error("Processing failed: " + e.message);
    } finally {
        console.log("Cleanup complete");
    }

Advanced Features Test
----------------------

Test advanced language constructs.

.. code-block:: ml

    // Nested function calls and member access
    result = math.sqrt(abs(min(array.filter(fn(x) => x > 0))));

    // Complex conditionals
    if (hasCapability("file.read") && file.exists(path)) {
        data = file.read(path);
    } elif (hasCapability("network.http")) {
        data = http.get(url);
    } else {
        console.error("No access method available");
    }

    // Chained operations
    processed = data
        .filter(fn(x) => typeof(x) == "number")
        .map(fn(x) => x * 2)
        .reduce(fn(acc, x) => acc + x, 0);

    // Multiple capability checks
    caps = getCapabilities();
    for (cap in caps) {
        info = getCapabilityInfo(cap);
        console.log("Capability: " + cap);
        console.log("  Available: " + str(info.available));
    }

Expected Visual Results
-----------------------

After building the documentation, you should see:

**Keywords (Purple, Bold):**
  if, elif, else, while, for, break, continue, return, function, fn,
  import, from, as, try, except, finally, throw, capability, resource,
  allow, nonlocal

**Boolean Literals (Purple, Bold):**
  true, false, null, undefined

**Builtins (Cyan, Bold):**
  All 45 functions: int, float, str, bool, typeof, isinstance, len, range,
  enumerate, keys, values, sorted, sum, zip, print, input, abs, min, max,
  round, help, methods, modules, available_modules, has_module, module_info,
  hasCapability, getCapabilities, getCapabilityInfo, hasattr, getattr, call,
  callable, iter, next, reversed, all, any, chr, ord, hex, bin, oct, repr, format

**Stdlib Modules (Yellow):**
  console, json, math, datetime, functional, regex, string, collections,
  file, http, path, random

**Functions (Green):**
  Function definitions and calls

**Variables (White):**
  All other identifiers

**Operators (Pink):**
  +, -, *, /, %, ==, !=, <, >, <=, >=, &&, ||, !, =>, ?, :, =

**Strings (Yellow):**
  "double quotes", 'single quotes'

**Numbers (Purple):**
  42, 3.14, 6.022e23

**Comments (Gray, Italic):**
  // single-line
  /* multi-line */

**Braces (Pink, Bold):**
  { }

**Brackets (Pink, Bold):**
  [ ]

**Parentheses (Pink):**
  ( )
