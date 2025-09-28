==================
Collections Module
==================

The ``collections`` module provides essential list and dictionary operations for data structure manipulation. It offers pure ML implementations for core operations and Python bridge functions for advanced features.

.. contents:: Contents
   :local:
   :depth: 2

Overview
========

The collections module implements fundamental data structure operations:

- **List Operations**: append, prepend, length, indexing, searching
- **Dictionary Operations**: key/value manipulation, merging, iteration
- **Pure ML Implementation**: Most functions implemented directly in ML
- **Python Bridge**: Advanced operations use Python for performance
- **Immutable Operations**: Functions return new collections, preserving originals

Import and Usage
================

.. code-block:: ml

   import collections;

   // List operations
   list = [1, 2, 3];
   new_list = collections.append(list, 4);  // [1, 2, 3, 4]
   length = collections.length(list);       // 3

   // Dictionary operations
   dict = {name: "Alice", age: 30};
   keys = collections.keys(dict);           // ["name", "age"]

List Operations
===============

.. function:: collections.length(list)

   Get the length of a list by iterating until null.

   :param list: List to measure
   :type list: array
   :return: Number of elements in list
   :rtype: number

   **Implementation**: Pure ML using iteration.

   .. code-block:: ml

      length = collections.length([1, 2, 3]);     // 3
      length = collections.length([]);            // 0
      length = collections.length(["a", "b"]);    // 2

.. function:: collections.append(list, element)

   Add element to the end of a list (returns new list).

   :param list: Source list
   :type list: array
   :param element: Element to add
   :type element: any
   :return: New list with element appended
   :rtype: array

   .. code-block:: ml

      new_list = collections.append([1, 2], 3);        // [1, 2, 3]
      new_list = collections.append([], "first");      // ["first"]
      new_list = collections.append(["a"], "b");       // ["a", "b"]

.. function:: collections.prepend(list, element)

   Add element to the beginning of a list (returns new list).

   :param list: Source list
   :type list: array
   :param element: Element to add
   :type element: any
   :return: New list with element prepended
   :rtype: array

   .. code-block:: ml

      new_list = collections.prepend([2, 3], 1);       // [1, 2, 3]
      new_list = collections.prepend([], "first");     // ["first"]

.. function:: collections.get(list, index)

   Get element at specific index (safe indexing).

   :param list: Source list
   :type list: array
   :param index: Index position (0-based)
   :type index: number
   :return: Element at index, or null if out of bounds
   :rtype: any

   .. code-block:: ml

      element = collections.get([1, 2, 3], 0);     // 1
      element = collections.get([1, 2, 3], 2);     // 3
      element = collections.get([1, 2, 3], 10);    // null (out of bounds)

.. function:: collections.contains(list, element)

   Check if list contains a specific element.

   :param list: List to search
   :type list: array
   :param element: Element to find
   :type element: any
   :return: True if element found, false otherwise
   :rtype: boolean

   .. code-block:: ml

      found = collections.contains([1, 2, 3], 2);      // true
      found = collections.contains([1, 2, 3], 5);      // false
      found = collections.contains(["a", "b"], "a");   // true

.. function:: collections.indexOf(list, element)

   Find the index of the first occurrence of an element.

   :param list: List to search
   :type list: array
   :param element: Element to find
   :type element: any
   :return: Index of element, or -1 if not found
   :rtype: number

   .. code-block:: ml

      index = collections.indexOf([1, 2, 3], 2);       // 1
      index = collections.indexOf([1, 2, 3], 5);       // -1
      index = collections.indexOf(["a", "b"], "b");    // 1

List Transformation
===================

.. function:: collections.reverse(list)

   Reverse the order of elements in a list.

   :param list: List to reverse
   :type list: array
   :return: New list with elements in reverse order
   :rtype: array

   .. code-block:: ml

      reversed = collections.reverse([1, 2, 3]);       // [3, 2, 1]
      reversed = collections.reverse(["a", "b"]);      // ["b", "a"]

.. function:: collections.slice(list, start, end)

   Extract a portion of a list.

   :param list: Source list
   :type list: array
   :param start: Start index (inclusive)
   :type start: number
   :param end: End index (exclusive)
   :type end: number
   :return: New list containing slice
   :rtype: array

   .. code-block:: ml

      slice = collections.slice([1, 2, 3, 4], 1, 3);   // [2, 3]
      slice = collections.slice([1, 2, 3, 4], 0, 2);   // [1, 2]

.. function:: collections.concat(list1, list2)

   Concatenate two lists.

   :param list1: First list
   :type list1: array
   :param list2: Second list
   :type list2: array
   :return: New list containing elements from both lists
   :rtype: array

   .. code-block:: ml

      combined = collections.concat([1, 2], [3, 4]);   // [1, 2, 3, 4]
      combined = collections.concat([], [1, 2]);       // [1, 2]

Dictionary Operations
=====================

.. function:: collections.keys(dict)

   Get all keys from a dictionary.

   :param dict: Dictionary to extract keys from
   :type dict: object
   :return: Array of keys
   :rtype: array

   .. code-block:: ml

      keys = collections.keys({name: "Alice", age: 30});
      // ["name", "age"]

.. function:: collections.values(dict)

   Get all values from a dictionary.

   :param dict: Dictionary to extract values from
   :type dict: object
   :return: Array of values
   :rtype: array

   .. code-block:: ml

      values = collections.values({name: "Alice", age: 30});
      // ["Alice", 30]

.. function:: collections.hasKey(dict, key)

   Check if dictionary contains a specific key.

   :param dict: Dictionary to check
   :type dict: object
   :param key: Key to look for
   :type key: string
   :return: True if key exists, false otherwise
   :rtype: boolean

   .. code-block:: ml

      exists = collections.hasKey({name: "Alice"}, "name");  // true
      exists = collections.hasKey({name: "Alice"}, "age");   // false

.. function:: collections.merge(dict1, dict2)

   Merge two dictionaries (second dictionary takes precedence).

   :param dict1: First dictionary
   :type dict1: object
   :param dict2: Second dictionary (overwrites conflicts)
   :type dict2: object
   :return: New merged dictionary
   :rtype: object

   .. code-block:: ml

      dict1 = {name: "Alice", age: 30};
      dict2 = {age: 31, city: "New York"};
      merged = collections.merge(dict1, dict2);
      // {name: "Alice", age: 31, city: "New York"}

Advanced Operations
===================

.. function:: collections.filter(list, predicate)

   Filter list elements using a predicate function.

   :param list: List to filter
   :type list: array
   :param predicate: Function that returns true/false for each element
   :type predicate: function
   :return: New list containing only elements where predicate returns true
   :rtype: array

   .. code-block:: ml

      // Filter even numbers
      function isEven(x) {
          return x % 2 == 0;
      }

      evens = collections.filter([1, 2, 3, 4], isEven);  // [2, 4]

.. function:: collections.map(list, transform)

   Transform each element in a list using a function.

   :param list: List to transform
   :type list: array
   :param transform: Function to apply to each element
   :type transform: function
   :return: New list with transformed elements
   :rtype: array

   .. code-block:: ml

      // Double each number
      function double(x) {
          return x * 2;
      }

      doubled = collections.map([1, 2, 3], double);  // [2, 4, 6]

.. function:: collections.reduce(list, reducer, initial)

   Reduce list to a single value using a reducer function.

   :param list: List to reduce
   :type list: array
   :param reducer: Function that takes accumulator and current value
   :type reducer: function
   :param initial: Initial accumulator value
   :type initial: any
   :return: Final accumulated value
   :rtype: any

   .. code-block:: ml

      // Sum all numbers
      function add(acc, curr) {
          return acc + curr;
      }

      sum = collections.reduce([1, 2, 3, 4], add, 0);  // 10

Set Operations
==============

.. function:: collections.unique(list)

   Remove duplicate elements from a list.

   :param list: List that may contain duplicates
   :type list: array
   :return: New list with unique elements only
   :rtype: array

   .. code-block:: ml

      unique = collections.unique([1, 2, 2, 3, 1]);    // [1, 2, 3]
      unique = collections.unique(["a", "b", "a"]);    // ["a", "b"]

.. function:: collections.intersection(list1, list2)

   Find elements that exist in both lists.

   :param list1: First list
   :type list1: array
   :param list2: Second list
   :type list2: array
   :return: New list containing common elements
   :rtype: array

   .. code-block:: ml

      common = collections.intersection([1, 2, 3], [2, 3, 4]);  // [2, 3]

.. function:: collections.union(list1, list2)

   Combine two lists removing duplicates.

   :param list1: First list
   :type list1: array
   :param list2: Second list
   :type list2: array
   :return: New list containing all unique elements
   :rtype: array

   .. code-block:: ml

      combined = collections.union([1, 2], [2, 3]);    // [1, 2, 3]

Sorting Operations
==================

.. function:: collections.sort(list)

   Sort list elements in ascending order.

   :param list: List to sort
   :type list: array
   :return: New sorted list
   :rtype: array

   .. code-block:: ml

      sorted = collections.sort([3, 1, 4, 1, 5]);      // [1, 1, 3, 4, 5]
      sorted = collections.sort(["c", "a", "b"]);      // ["a", "b", "c"]

.. function:: collections.sortBy(list, keyFunc)

   Sort list elements using a key function.

   :param list: List to sort
   :type list: array
   :param keyFunc: Function that returns sort key for each element
   :type keyFunc: function
   :return: New sorted list
   :rtype: array

   .. code-block:: ml

      // Sort by string length
      function getLength(str) {
          return str.length;
      }

      sorted = collections.sortBy(["hello", "hi", "world"], getLength);
      // ["hi", "hello", "world"]

Security and Performance
========================

**Security Features:**

- **Immutable Operations**: Original collections never modified
- **Safe Indexing**: Out-of-bounds access returns safe values (null, -1)
- **Input Validation**: All functions validate input parameters
- **No Code Injection**: All operations are safe from injection attacks

**Performance Characteristics:**

- **Basic Operations** (length, get, contains): O(n) in pure ML
- **List Building** (append, prepend): O(n) due to copying
- **Dictionary Operations**: O(1) for most operations via Python bridge
- **Advanced Operations** (sort, filter, map): O(n log n) or O(n) depending on operation

**Memory Usage:**

- Immutable operations create new collections
- Large collections may benefit from streaming operations
- Python bridge functions optimized for memory efficiency

Implementation Details
======================

**Pure ML vs Python Bridge:**

- **Pure ML**: Basic list operations (length, append, prepend, get)
- **Python Bridge**: Dictionary operations, sorting, advanced transformations
- **Hybrid**: Some operations use ML logic with Python optimization

**Error Handling:**

.. code-block:: ml

   // Safe operations return sensible defaults
   element = collections.get([], 0);           // null (empty list)
   index = collections.indexOf([1, 2], 5);     // -1 (not found)
   keys = collections.keys({});                // [] (empty array)

Examples
========

Data Processing Pipeline
-----------------------

.. code-block:: ml

   import collections;

   function processUsers(users) {
       // Filter active users
       active = collections.filter(users, function(user) {
           return user.active == true;
       });

       // Extract user names
       names = collections.map(active, function(user) {
           return user.name;
       });

       // Sort alphabetically
       return collections.sort(names);
   }

   users = [
       {name: "Alice", active: true},
       {name: "Bob", active: false},
       {name: "Charlie", active: true}
   ];

   result = processUsers(users);  // ["Alice", "Charlie"]

List Utilities
--------------

.. code-block:: ml

   import collections;

   function createRange(start, end) {
       result = [];
       for (i = start; i < end; i++) {
           result = collections.append(result, i);
       }
       return result;
   }

   function sum(numbers) {
       return collections.reduce(numbers, function(acc, curr) {
           return acc + curr;
       }, 0);
   }

   numbers = createRange(1, 6);  // [1, 2, 3, 4, 5]
   total = sum(numbers);         // 15

Dictionary Operations
--------------------

.. code-block:: ml

   import collections;

   function mergeConfigs(default, user) {
       // Start with defaults
       config = default;

       // Apply user overrides
       config = collections.merge(config, user);

       // Ensure required keys exist
       if (!collections.hasKey(config, "version")) {
           config = collections.merge(config, {version: "1.0"});
       }

       return config;
   }

   default = {theme: "light", debug: false};
   user = {theme: "dark", verbose: true};
   config = mergeConfigs(default, user);
   // {theme: "dark", debug: false, verbose: true, version: "1.0"}

See Also
========

- :doc:`functional` - Functional programming utilities
- :doc:`array` - Array-specific operations
- :doc:`string` - String manipulation
- :doc:`../developer-guide/writing-stdlib-modules` - Creating new modules