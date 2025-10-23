collections - List Operations
==============================

.. module:: collections
   :synopsis: Functional list operations and utilities

The ``collections`` module provides a comprehensive set of functional list operations. All functions are pure - they return new lists without modifying the originals, enabling safe and predictable data transformations.

Philosophy: Functional List Processing
---------------------------------------

The collections module embodies functional programming principles:

- **Immutability**: All operations return new lists, never modifying originals
- **Pure Functions**: No side effects, same inputs always produce same outputs
- **Composability**: Operations can be chained together for complex transformations
- **Data Pipelines**: Build sophisticated data processing workflows step by step

This approach leads to safer, more maintainable code with predictable behavior.

Basic Operations
----------------

length()
~~~~~~~~

.. code-block:: ml

   length(list) -> number

Returns the number of elements in a list.

**Parameters:**

- ``list``: The list to measure

**Returns:** The number of elements

**Example:**

.. code-block:: ml

   import collections;

   numbers = [10, 20, 30];
   count = collections.length(numbers);
   // Result: 3

append()
~~~~~~~~

.. code-block:: ml

   append(list, element) -> list

Returns a new list with element added to the end.

**Parameters:**

- ``list``: The original list
- ``element``: The element to add

**Returns:** New list with element appended

**Example:**

.. code-block:: ml

   import collections;

   numbers = [10, 20, 30];
   withFour = collections.append(numbers, 40);
   // Result: [10, 20, 30, 40]
   // Original unchanged: [10, 20, 30]

prepend()
~~~~~~~~~

.. code-block:: ml

   prepend(list, element) -> list

Returns a new list with element added to the beginning.

**Parameters:**

- ``list``: The original list
- ``element``: The element to add

**Returns:** New list with element prepended

**Example:**

.. code-block:: ml

   import collections;

   numbers = [10, 20, 30];
   withZero = collections.prepend(numbers, 0);
   // Result: [0, 10, 20, 30]

concat()
~~~~~~~~

.. code-block:: ml

   concat(list1, list2) -> list

Returns a new list combining two lists.

**Parameters:**

- ``list1``: First list
- ``list2``: Second list

**Returns:** New list containing all elements from both lists

**Example:**

.. code-block:: ml

   import collections;

   first = [1, 2, 3];
   second = [4, 5, 6];
   combined = collections.concat(first, second);
   // Result: [1, 2, 3, 4, 5, 6]

get()
~~~~~

.. code-block:: ml

   get(list, index) -> element | null

Safely retrieves element at index, returning null if out of bounds.

**Parameters:**

- ``list``: The list to access
- ``index``: Zero-based index

**Returns:** Element at index, or null if index is invalid

**Example:**

.. code-block:: ml

   import collections;

   numbers = [10, 20, 30];
   second = collections.get(numbers, 1);      // 20
   missing = collections.get(numbers, 10);    // null

first()
~~~~~~~

.. code-block:: ml

   first(list) -> element

Returns the first element of a list.

**Parameters:**

- ``list``: The list

**Returns:** First element

**Example:**

.. code-block:: ml

   import collections;

   numbers = [10, 20, 30];
   firstNum = collections.first(numbers);
   // Result: 10

last()
~~~~~~

.. code-block:: ml

   last(list) -> element

Returns the last element of a list.

**Parameters:**

- ``list``: The list

**Returns:** Last element

**Example:**

.. code-block:: ml

   import collections;

   numbers = [10, 20, 30];
   lastNum = collections.last(numbers);
   // Result: 30

isEmpty()
~~~~~~~~~

.. code-block:: ml

   isEmpty(list) -> boolean

Checks if a list is empty.

**Parameters:**

- ``list``: The list to check

**Returns:** true if list is empty, false otherwise

**Example:**

.. code-block:: ml

   import collections;

   empty = [];
   numbers = [1, 2, 3];

   collections.isEmpty(empty);      // true
   collections.isEmpty(numbers);    // false

Functional Operations
---------------------

map()
~~~~~

.. code-block:: ml

   map(list, fn) -> list

Transforms each element using a function.

**Parameters:**

- ``list``: The list to transform
- ``fn``: Function taking one element, returning transformed value

**Returns:** New list with transformed elements

**Example:**

.. code-block:: ml

   import collections;

   function double(n) {
       return n * 2;
   }

   numbers = [1, 2, 3, 4, 5];
   doubled = collections.map(numbers, double);
   // Result: [2, 4, 6, 8, 10]

filter()
~~~~~~~~

.. code-block:: ml

   filter(list, predicate) -> list

Selects elements matching a condition.

**Parameters:**

- ``list``: The list to filter
- ``predicate``: Function taking one element, returning boolean

**Returns:** New list containing only matching elements

**Example:**

.. code-block:: ml

   import collections;

   function isEven(n) {
       return n % 2 == 0;
   }

   numbers = [1, 2, 3, 4, 5, 6];
   evens = collections.filter(numbers, isEven);
   // Result: [2, 4, 6]

reduce()
~~~~~~~~

.. code-block:: ml

   reduce(list, fn, initial) -> value

Aggregates list to a single value.

**Parameters:**

- ``list``: The list to reduce
- ``fn``: Function taking (accumulator, element), returning new accumulator
- ``initial``: Initial accumulator value

**Returns:** Final accumulated value

**Example:**

.. code-block:: ml

   import collections;

   function add(acc, n) {
       return acc + n;
   }

   numbers = [1, 2, 3, 4, 5];
   sum = collections.reduce(numbers, add, 0);
   // Result: 15

find()
~~~~~~

.. code-block:: ml

   find(list, predicate) -> element | null

Finds first element matching condition.

**Parameters:**

- ``list``: The list to search
- ``predicate``: Function taking one element, returning boolean

**Returns:** First matching element, or null if none found

**Example:**

.. code-block:: ml

   import collections;

   function greaterThanFive(n) {
       return n > 5;
   }

   numbers = [1, 3, 6, 8, 2];
   firstLarge = collections.find(numbers, greaterThanFive);
   // Result: 6

every()
~~~~~~~

.. code-block:: ml

   every(list, predicate) -> boolean

Checks if all elements match condition.

**Parameters:**

- ``list``: The list to check
- ``predicate``: Function taking one element, returning boolean

**Returns:** true if all elements match, false otherwise

**Example:**

.. code-block:: ml

   import collections;

   function isPositive(n) {
       return n > 0;
   }

   numbers = [1, 2, 3, 4, 5];
   allPositive = collections.every(numbers, isPositive);
   // Result: true

some()
~~~~~~

.. code-block:: ml

   some(list, predicate) -> boolean

Checks if any element matches condition.

**Parameters:**

- ``list``: The list to check
- ``predicate``: Function taking one element, returning boolean

**Returns:** true if at least one element matches, false otherwise

**Example:**

.. code-block:: ml

   import collections;

   function isEven(n) {
       return n % 2 == 0;
   }

   numbers = [1, 3, 5, 6, 7];
   hasEven = collections.some(numbers, isEven);
   // Result: true

List Manipulation
-----------------

slice()
~~~~~~~

.. code-block:: ml

   slice(list, start, end) -> list

Extracts a portion of a list.

**Parameters:**

- ``list``: The list to slice
- ``start``: Starting index (inclusive)
- ``end``: Ending index (exclusive), or null for end of list

**Returns:** New list containing the slice

**Example:**

.. code-block:: ml

   import collections;

   numbers = [10, 20, 30, 40, 50];
   firstThree = collections.slice(numbers, 0, 3);
   // Result: [10, 20, 30]

   fromTwo = collections.slice(numbers, 2, null);
   // Result: [30, 40, 50]

reverse()
~~~~~~~~~

.. code-block:: ml

   reverse(list) -> list

Returns a new list with elements in reverse order.

**Parameters:**

- ``list``: The list to reverse

**Returns:** New list with reversed order

**Example:**

.. code-block:: ml

   import collections;

   numbers = [1, 2, 3, 4, 5];
   reversed = collections.reverse(numbers);
   // Result: [5, 4, 3, 2, 1]
   // Original unchanged: [1, 2, 3, 4, 5]

unique()
~~~~~~~~

.. code-block:: ml

   unique(list) -> list

Returns a new list with duplicate elements removed.

**Parameters:**

- ``list``: The list

**Returns:** New list with unique elements only

**Example:**

.. code-block:: ml

   import collections;

   withDupes = [1, 2, 2, 3, 1, 4, 3];
   uniqueVals = collections.unique(withDupes);
   // Result: [1, 2, 3, 4]

flatten()
~~~~~~~~~

.. code-block:: ml

   flatten(list) -> list

Flattens nested lists by one level.

**Parameters:**

- ``list``: List containing nested lists

**Returns:** New list with one level of nesting removed

**Example:**

.. code-block:: ml

   import collections;

   nested = [[1, 2], [3, 4], [5, 6]];
   flat = collections.flatten(nested);
   // Result: [1, 2, 3, 4, 5, 6]

sort()
~~~~~~

.. code-block:: ml

   sort(list) -> list

Returns a new sorted list.

**Parameters:**

- ``list``: The list to sort

**Returns:** New list sorted in ascending order

**Example:**

.. code-block:: ml

   import collections;

   unsorted = [3, 1, 4, 1, 5, 9];
   sorted = collections.sort(unsorted);
   // Result: [1, 1, 3, 4, 5, 9]

sortBy()
~~~~~~~~

.. code-block:: ml

   sortBy(list, keyFn) -> list

Returns a new list sorted by a key function.

**Parameters:**

- ``list``: The list to sort
- ``keyFn``: Function extracting sort key from each element

**Returns:** New list sorted by key function

**Example:**

.. code-block:: ml

   import collections;

   words = ["elephant", "cat", "dog", "butterfly"];

   function byLength(word) {
       return len(word);
   }

   byLen = collections.sortBy(words, byLength);
   // Result: ["cat", "dog", "elephant", "butterfly"]

take()
~~~~~~

.. code-block:: ml

   take(list, n) -> list

Returns first n elements.

**Parameters:**

- ``list``: The list
- ``n``: Number of elements to take

**Returns:** New list with first n elements

**Example:**

.. code-block:: ml

   import collections;

   numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
   firstFive = collections.take(numbers, 5);
   // Result: [1, 2, 3, 4, 5]

drop()
~~~~~~

.. code-block:: ml

   drop(list, n) -> list

Returns list with first n elements removed.

**Parameters:**

- ``list``: The list
- ``n``: Number of elements to drop

**Returns:** New list without first n elements

**Example:**

.. code-block:: ml

   import collections;

   numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
   afterFive = collections.drop(numbers, 5);
   // Result: [6, 7, 8, 9, 10]

chunk()
~~~~~~~

.. code-block:: ml

   chunk(list, size) -> list

Splits list into chunks of specified size.

**Parameters:**

- ``list``: The list to chunk
- ``size``: Size of each chunk

**Returns:** List of lists, each containing up to size elements

**Example:**

.. code-block:: ml

   import collections;

   numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9];
   chunks = collections.chunk(numbers, 3);
   // Result: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

zip()
~~~~~

.. code-block:: ml

   zip(list1, list2) -> list

Combines two lists into pairs.

**Parameters:**

- ``list1``: First list
- ``list2``: Second list

**Returns:** List of two-element lists pairing corresponding elements

**Example:**

.. code-block:: ml

   import collections;

   names = ["Alice", "Bob", "Charlie"];
   ages = [25, 30, 35];
   pairs = collections.zip(names, ages);
   // Result: [["Alice", 25], ["Bob", 30], ["Charlie", 35]]

Searching and Testing
---------------------

contains()
~~~~~~~~~~

.. code-block:: ml

   contains(list, element) -> boolean

Checks if list contains element.

**Parameters:**

- ``list``: The list to search
- ``element``: Element to find

**Returns:** true if element is in list, false otherwise

**Example:**

.. code-block:: ml

   import collections;

   numbers = [10, 20, 30, 40];
   hasThirty = collections.contains(numbers, 30);    // true
   hasFifty = collections.contains(numbers, 50);     // false

indexOf()
~~~~~~~~~

.. code-block:: ml

   indexOf(list, element) -> number

Finds the index of an element.

**Parameters:**

- ``list``: The list to search
- ``element``: Element to find

**Returns:** Zero-based index of element, or -1 if not found

**Example:**

.. code-block:: ml

   import collections;

   numbers = [10, 20, 30, 40];
   index = collections.indexOf(numbers, 30);     // 2
   notFound = collections.indexOf(numbers, 50);  // -1

removeAt()
~~~~~~~~~~

.. code-block:: ml

   removeAt(list, index) -> list

Returns new list with element at index removed.

**Parameters:**

- ``list``: The list
- ``index``: Index of element to remove

**Returns:** New list without element at index

**Example:**

.. code-block:: ml

   import collections;

   numbers = [10, 20, 30, 40, 50];
   withoutThird = collections.removeAt(numbers, 2);
   // Result: [10, 20, 40, 50]

Chaining Operations
-------------------

The collections module shines when operations are chained together to build data processing pipelines.

**Example: Filter, Sort, Take Top 3**

.. code-block:: ml

   import collections;

   scores = [78, 92, 85, 67, 95, 73, 88, 91];

   // Filter passing scores
   function isPassing(score) {
       return score >= 70;
   }
   passing = collections.filter(scores, isPassing);

   // Sort in ascending order
   sorted = collections.sort(passing);

   // Reverse for descending
   descending = collections.reverse(sorted);

   // Take top 3
   topThree = collections.take(descending, 3);
   // Result: [95, 92, 91]

**Example: Map, Filter, Reduce**

.. code-block:: ml

   import collections;

   numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

   // Filter evens
   function isEven(n) {
       return n % 2 == 0;
   }
   evens = collections.filter(numbers, isEven);

   // Double each
   function double(n) {
       return n * 2;
   }
   doubled = collections.map(evens, double);

   // Sum all
   function add(acc, n) {
       return acc + n;
   }
   sum = collections.reduce(doubled, add, 0);
   // Result: 60

Practical Examples
------------------

Data Cleaning Pipeline
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/collections/03_list_manipulation.ml
   :language: ml
   :lines: 107-121
   :caption: Remove duplicates and analyze data

Pagination System
~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/collections/03_list_manipulation.ml
   :language: ml
   :lines: 124-131
   :caption: Implement pagination with drop and take

Student Analytics
~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/collections/04_comprehensive_example.ml
   :language: ml
   :lines: 27-47
   :caption: Complete analytics pipeline

Performance Considerations
--------------------------

**Pure Functions Benefits:**

- Predictable behavior - same inputs always produce same outputs
- Thread-safe - no shared mutable state
- Testable - easy to verify correctness
- Composable - operations can be safely combined

**Memory Efficiency:**

- Operations create new lists, original data is preserved
- For large datasets, consider breaking into chunks
- Use ``take()`` and ``drop()`` for working with subsets

**Common Patterns:**

.. code-block:: ml

   // Good: Build pipeline step by step
   filtered = collections.filter(data, predicate);
   sorted = collections.sort(filtered);
   result = collections.take(sorted, 10);

   // Good: Process in chunks for large datasets
   chunks = collections.chunk(largeData, 100);

   // Good: Reuse functions
   function isValid(item) { return item.score > 0; }
   validItems = collections.filter(data, isValid);

See Also
--------

- :doc:`builtin` - Core list operations (len, range)
- :doc:`functional` - Advanced functional programming utilities
- :doc:`datetime` - Working with time-based data

Complete Examples
-----------------

See the following complete examples demonstrating the collections module:

- ``docs/ml_snippets/standard-library/collections/01_basic_operations.ml`` - Basic list operations
- ``docs/ml_snippets/standard-library/collections/02_functional_operations.ml`` - Map, filter, reduce patterns
- ``docs/ml_snippets/standard-library/collections/03_list_manipulation.ml`` - Slice, reverse, sort operations
- ``docs/ml_snippets/standard-library/collections/04_comprehensive_example.ml`` - Complete student analytics system
