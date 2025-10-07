functional - Functional Programming
====================================

.. module:: functional
   :synopsis: Comprehensive functional programming utilities

The ``functional`` module provides a complete toolkit for functional programming in ML. It includes function composition, higher-order functions, and advanced FP patterns that enable elegant, declarative code.

Philosophy: Functional Programming
-----------------------------------

Functional programming emphasizes:

- **Pure Functions**: Same inputs always produce same outputs
- **Composition**: Building complex operations from simple functions
- **Immutability**: Data transformations return new values
- **Declarative Style**: Describing what to compute, not how

This module brings functional programming power to ML, enabling readable, maintainable, and testable code.

Function Composition
--------------------

compose()
~~~~~~~~~

.. code-block:: ml

   compose(f, g, ...) -> function

Compose functions right to left. Result applies functions in reverse order.

**Parameters:**

- ``...functions``: Functions to compose

**Returns:** Composed function

**Example:**

.. code-block:: ml

   import functional;

   function addTen(x) { return x + 10; }
   function double(x) { return x * 2; }
   function square(x) { return x * x; }

   // Executes: square(double(addTen(5)))
   combined = functional.compose(square, double, addTen);
   result = combined(5);  // 900

pipe()
~~~~~~

.. code-block:: ml

   pipe(f, g, ...) -> function

Pipe functions left to right. Result applies functions in order.

**Parameters:**

- ``...functions``: Functions to pipe

**Returns:** Piped function

**Example:**

.. code-block:: ml

   import functional;

   // Executes: square(double(addTen(5)))
   piped = functional.pipe(addTen, double, square);
   result = piped(5);  // 900

curry()
~~~~~~~

.. code-block:: ml

   curry(func, arity) -> function

Curry a function to enable partial application.

**Parameters:**

- ``func``: Function to curry
- ``arity``: Number of arguments (optional, auto-detected)

**Returns:** Curried function

**Example:**

.. code-block:: ml

   import functional;

   function add(a, b, c) {
       return a + b + c;
   }

   addCurried = functional.curry(add, 3);
   addFive = addCurried(5);
   addFiveAndThree = addFive(3);
   result = addFiveAndThree(2);  // 10

curry2()
~~~~~~~~

.. code-block:: ml

   curry2(func) -> function

Curry a function with exactly 2 arguments.

**Parameters:**

- ``func``: Two-argument function

**Returns:** Curried function

**Example:**

.. code-block:: ml

   import functional;

   function add(a, b) {
       return a + b;
   }

   addCurried = functional.curry2(add);
   addFive = addCurried(5);
   result = addFive(10);  // 15

partial()
~~~~~~~~~

.. code-block:: ml

   partial(func, ...args) -> function

Partially apply arguments to function.

**Parameters:**

- ``func``: Function to partially apply
- ``...args``: Arguments to pre-fill

**Returns:** Partially applied function

**Example:**

.. code-block:: ml

   import functional;

   function multiply(a, b, c) {
       return a * b * c;
   }

   multiplyBy6 = functional.partial(multiply, 2, 3);
   result = multiplyBy6(4);  // 24

Higher-Order Functions
----------------------

map()
~~~~~

.. code-block:: ml

   map(func, iterable) -> list

Transform each element using function.

**Parameters:**

- ``func``: Transform function
- ``iterable``: List to transform

**Returns:** New list with transformed elements

**Example:**

.. code-block:: ml

   import functional;

   function double(x) {
       return x * 2;
   }

   numbers = [1, 2, 3, 4, 5];
   doubled = functional.map(double, numbers);
   // Result: [2, 4, 6, 8, 10]

filter()
~~~~~~~~

.. code-block:: ml

   filter(predicate, iterable) -> list

Select elements matching condition.

**Parameters:**

- ``predicate``: Test function returning boolean
- ``iterable``: List to filter

**Returns:** New list with matching elements

**Example:**

.. code-block:: ml

   import functional;

   function isEven(x) {
       return x % 2 == 0;
   }

   numbers = [1, 2, 3, 4, 5, 6];
   evens = functional.filter(isEven, numbers);
   // Result: [2, 4, 6]

reduce()
~~~~~~~~

.. code-block:: ml

   reduce(func, iterable, initial) -> value

Aggregate list to single value.

**Parameters:**

- ``func``: Reducer function taking (accumulator, element)
- ``iterable``: List to reduce
- ``initial``: Initial accumulator value (optional)

**Returns:** Final accumulated value

**Example:**

.. code-block:: ml

   import functional;

   function add(acc, x) {
       return acc + x;
   }

   numbers = [1, 2, 3, 4, 5];
   sum = functional.reduce(add, numbers, 0);
   // Result: 15

find()
~~~~~~

.. code-block:: ml

   find(predicate, iterable) -> element | null

Find first element matching condition.

**Parameters:**

- ``predicate``: Test function
- ``iterable``: List to search

**Returns:** First matching element, or null

**Example:**

.. code-block:: ml

   import functional;

   function greaterThanSeven(x) {
       return x > 7;
   }

   numbers = [1, 3, 6, 8, 2];
   result = functional.find(greaterThanSeven, numbers);
   // Result: 8

every()
~~~~~~~

.. code-block:: ml

   every(predicate, iterable) -> boolean

Check if all elements match condition.

**Parameters:**

- ``predicate``: Test function
- ``iterable``: List to check

**Returns:** true if all match, false otherwise

**Example:**

.. code-block:: ml

   import functional;

   function isPositive(x) {
       return x > 0;
   }

   numbers = [1, 2, 3, 4, 5];
   allPositive = functional.every(isPositive, numbers);
   // Result: true

some()
~~~~~~

.. code-block:: ml

   some(predicate, iterable) -> boolean

Check if any element matches condition.

**Parameters:**

- ``predicate``: Test function
- ``iterable``: List to check

**Returns:** true if at least one matches, false otherwise

**Example:**

.. code-block:: ml

   import functional;

   function isEven(x) {
       return x % 2 == 0;
   }

   numbers = [1, 3, 5, 6, 7];
   hasEven = functional.some(isEven, numbers);
   // Result: true

forEach()
~~~~~~~~~

.. code-block:: ml

   forEach(func, iterable) -> void

Execute function for each element.

**Parameters:**

- ``func``: Function to execute
- ``iterable``: List to process

**Example:**

.. code-block:: ml

   import functional;
   import console;

   function printDouble(x) {
       console.log(str(x * 2));
   }

   numbers = [1, 2, 3];
   functional.forEach(printDouble, numbers);
   // Prints: 2, 4, 6

List Operations
---------------

range()
~~~~~~~

.. code-block:: ml

   range(start, end, step) -> list

Generate sequence of numbers.

**Parameters:**

- ``start``: Start value (or end if end is null)
- ``end``: End value (optional)
- ``step``: Step size (default 1)

**Returns:** List of numbers

**Example:**

.. code-block:: ml

   import functional;

   nums = functional.range(10);           // [0..9]
   range5to15 = functional.range(5, 15);  // [5..14]
   stepped = functional.range(0, 20, 3);  // [0, 3, 6, 9, 12, 15, 18]

take()
~~~~~~

.. code-block:: ml

   take(n, iterable) -> list

Take first n elements.

**Parameters:**

- ``n``: Number of elements to take
- ``iterable``: List to take from

**Returns:** List with first n elements

**Example:**

.. code-block:: ml

   import functional;

   numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
   firstFive = functional.take(5, numbers);
   // Result: [1, 2, 3, 4, 5]

drop()
~~~~~~

.. code-block:: ml

   drop(n, iterable) -> list

Drop first n elements.

**Parameters:**

- ``n``: Number of elements to drop
- ``iterable``: List to drop from

**Returns:** List without first n elements

**Example:**

.. code-block:: ml

   import functional;

   numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
   afterFive = functional.drop(5, numbers);
   // Result: [6, 7, 8, 9, 10]

chunk()
~~~~~~~

.. code-block:: ml

   chunk(size, iterable) -> list

Split list into groups of size.

**Parameters:**

- ``size``: Chunk size
- ``iterable``: List to chunk

**Returns:** List of chunks

**Example:**

.. code-block:: ml

   import functional;

   numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9];
   chunks = functional.chunk(3, numbers);
   // Result: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

flatten()
~~~~~~~~~

.. code-block:: ml

   flatten(nested_list) -> list

Flatten nested list by one level.

**Parameters:**

- ``nested_list``: Nested list to flatten

**Returns:** Flattened list

**Example:**

.. code-block:: ml

   import functional;

   nested = [[1, 2], [3, 4], [5, 6]];
   flat = functional.flatten(nested);
   // Result: [1, 2, 3, 4, 5, 6]

reverse()
~~~~~~~~~

.. code-block:: ml

   reverse(iterable) -> list

Reverse list order.

**Parameters:**

- ``iterable``: List to reverse

**Returns:** Reversed list

**Example:**

.. code-block:: ml

   import functional;

   numbers = [1, 2, 3, 4, 5];
   reversed = functional.reverse(numbers);
   // Result: [5, 4, 3, 2, 1]

unique()
~~~~~~~~

.. code-block:: ml

   unique(iterable) -> list

Get unique elements preserving order.

**Parameters:**

- ``iterable``: List to deduplicate

**Returns:** List of unique elements

**Example:**

.. code-block:: ml

   import functional;

   withDupes = [1, 2, 2, 3, 1, 4, 3];
   uniqueVals = functional.unique(withDupes);
   // Result: [1, 2, 3, 4]

repeat()
~~~~~~~~

.. code-block:: ml

   repeat(value, times) -> list

Repeat value n times.

**Parameters:**

- ``value``: Value to repeat
- ``times``: Number of repetitions

**Returns:** List of repeated values

**Example:**

.. code-block:: ml

   import functional;

   zeros = functional.repeat(0, 5);
   // Result: [0, 0, 0, 0, 0]

zip()
~~~~~

.. code-block:: ml

   zip(...iterables) -> list

Zip iterables into tuples.

**Parameters:**

- ``...iterables``: Lists to zip

**Returns:** List of tuples

**Example:**

.. code-block:: ml

   import functional;

   names = ["Alice", "Bob", "Charlie"];
   ages = [25, 30, 35];
   pairs = functional.zip(names, ages);
   // Result: [["Alice", 25], ["Bob", 30], ["Charlie", 35]]

zipWith()
~~~~~~~~~

.. code-block:: ml

   zipWith(combiner, iterable1, iterable2) -> list

Zip with custom combiner function.

**Parameters:**

- ``combiner``: Function to combine pairs
- ``iterable1``: First list
- ``iterable2``: Second list

**Returns:** List of combined values

**Example:**

.. code-block:: ml

   import functional;

   function add(a, b) {
       return a + b;
   }

   list1 = [1, 2, 3, 4];
   list2 = [10, 20, 30, 40];
   sums = functional.zipWith(add, list1, list2);
   // Result: [11, 22, 33, 44]

groupBy()
~~~~~~~~~

.. code-block:: ml

   groupBy(key_func, iterable) -> object

Group elements by key function.

**Parameters:**

- ``key_func``: Function extracting group key
- ``iterable``: List to group

**Returns:** Object mapping keys to element lists

**Example:**

.. code-block:: ml

   import functional;

   items = [
       {type: "fruit", name: "apple"},
       {type: "vegetable", name: "carrot"},
       {type: "fruit", name: "banana"}
   ];

   function getType(item) {
       return item.type;
   }

   grouped = functional.groupBy(getType, items);
   // Result: {fruit: [...], vegetable: [...]}

Advanced Patterns
-----------------

partition()
~~~~~~~~~~~

.. code-block:: ml

   partition(predicate, iterable) -> list

Partition list into matching and non-matching.

**Parameters:**

- ``predicate``: Test function
- ``iterable``: List to partition

**Returns:** List containing [matching, non-matching]

**Example:**

.. code-block:: ml

   import functional;

   function isEven(x) {
       return x % 2 == 0;
   }

   numbers = [1, 2, 3, 4, 5, 6];
   parts = functional.partition(isEven, numbers);
   // Result: [[2, 4, 6], [1, 3, 5]]

ifElse()
~~~~~~~~

.. code-block:: ml

   ifElse(predicate, true_fn, false_fn) -> function

Create conditional function.

**Parameters:**

- ``predicate``: Condition function
- ``true_fn``: Function if true
- ``false_fn``: Function if false

**Returns:** Conditional function

**Example:**

.. code-block:: ml

   import functional;

   function isPositive(x) { return x > 0; }
   function double(x) { return x * 2; }
   function negate(x) { return -x; }

   process = functional.ifElse(isPositive, double, negate);
   result1 = process(5);   // 10
   result2 = process(-3);  // 3

cond()
~~~~~~

.. code-block:: ml

   cond(conditions) -> function

Multi-condition function (like switch/case).

**Parameters:**

- ``conditions``: List of [predicate, action] pairs

**Returns:** Function applying first matching action

**Example:**

.. code-block:: ml

   import functional;

   function isSmall(x) { return x < 10; }
   function isMedium(x) { return x >= 10 && x < 100; }
   function isLarge(x) { return x >= 100; }

   function small(x) { return "small"; }
   function medium(x) { return "medium"; }
   function large(x) { return "large"; }

   categorize = functional.cond([
       [isSmall, small],
       [isMedium, medium],
       [isLarge, large]
   ]);

   result = categorize(50);  // "medium"

takeWhile()
~~~~~~~~~~~

.. code-block:: ml

   takeWhile(predicate, iterable) -> list

Take elements while predicate is true.

**Parameters:**

- ``predicate``: Test function
- ``iterable``: List to take from

**Returns:** Elements until predicate fails

**Example:**

.. code-block:: ml

   import functional;

   function lessThan50(x) {
       return x < 50;
   }

   numbers = [10, 20, 30, 40, 50, 60];
   result = functional.takeWhile(lessThan50, numbers);
   // Result: [10, 20, 30, 40]

times()
~~~~~~~

.. code-block:: ml

   times(n, func) -> list

Execute function n times with index.

**Parameters:**

- ``n``: Number of times
- ``func``: Function receiving index

**Returns:** List of results

**Example:**

.. code-block:: ml

   import functional;

   function square(i) {
       return i * i;
   }

   squares = functional.times(5, square);
   // Result: [0, 1, 4, 9, 16]

juxt()
~~~~~~

.. code-block:: ml

   juxt(functions) -> function

Apply multiple functions to same input.

**Parameters:**

- ``functions``: List of functions to apply

**Returns:** Function returning list of all results

**Example:**

.. code-block:: ml

   import functional;

   function addTen(x) { return x + 10; }
   function double(x) { return x * 2; }
   function square(x) { return x * x; }

   applyAll = functional.juxt([addTen, double, square]);
   results = applyAll(5);
   // Result: [15, 10, 25]

Utility Functions
-----------------

identity()
~~~~~~~~~~

.. code-block:: ml

   identity(x) -> x

Identity function - returns input unchanged.

**Parameters:**

- ``x``: Value to return

**Returns:** Same value

**Example:**

.. code-block:: ml

   import functional;

   value = functional.identity(42);  // 42

constant()
~~~~~~~~~~

.. code-block:: ml

   constant(value) -> function

Create function that always returns value.

**Parameters:**

- ``value``: Value to return

**Returns:** Constant function

**Example:**

.. code-block:: ml

   import functional;

   alwaysZero = functional.constant(0);
   result1 = alwaysZero();  // 0
   result2 = alwaysZero();  // 0

memoize()
~~~~~~~~~

.. code-block:: ml

   memoize(func) -> function

Memoize function results for performance.

**Parameters:**

- ``func``: Function to memoize

**Returns:** Memoized function with caching

**Example:**

.. code-block:: ml

   import functional;

   function expensiveCalc(n) {
       // Expensive computation
       return n * n * n;
   }

   memoized = functional.memoize(expensiveCalc);
   result1 = memoized(10);  // Computes
   result2 = memoized(10);  // Cached

Chaining Patterns
-----------------

Functional programming shines when operations are chained together.

**Pipeline Pattern:**

.. code-block:: ml

   import functional;

   numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

   // Filter evens -> double -> sum
   function isEven(x) { return x % 2 == 0; }
   function double(x) { return x * 2; }
   function add(a, b) { return a + b; }

   evens = functional.filter(isEven, numbers);
   doubled = functional.map(double, evens);
   sum = functional.reduce(add, doubled, 0);
   // Result: 60

**Composition Pattern:**

.. code-block:: ml

   import functional;

   function addTen(x) { return x + 10; }
   function double(x) { return x * 2; }
   function square(x) { return x * x; }

   // Build complex transformation
   transform = functional.pipe(addTen, double, square);

   // Apply to many values
   numbers = [1, 2, 3, 4, 5];
   results = functional.map(transform, numbers);

Practical Examples
------------------

Data Processing Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/functional/02_higher_order_functions.ml
   :language: ml
   :lines: 157-189
   :caption: Complete data transformation pipeline

Statistical Analysis
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/functional/04_advanced_patterns.ml
   :language: ml
   :lines: 242-276
   :caption: Statistical functions with juxt

E-commerce Order Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/functional/05_comprehensive_example.ml
   :language: ml
   :lines: 35-65
   :caption: Order processing with functional patterns

Performance Considerations
--------------------------

**Composition Benefits:**

- Reusable transformation pipelines
- Easier testing of individual functions
- Clear data flow

**When to Use:**

- Data transformation pipelines
- Event processing
- Statistical computations
- Complex business logic

**Performance Tips:**

.. code-block:: ml

   // Good: Reuse composed functions
   transform = functional.pipe(clean, validate, process);
   results = functional.map(transform, data);

   // Good: Use memoization for expensive pure functions
   memoized = functional.memoize(expensiveCalc);

   // Good: Partition for conditional processing
   parts = functional.partition(needsProcessing, items);

See Also
--------

- :doc:`collections` - List operations and utilities
- :doc:`builtin` - Core language functions

Complete Examples
-----------------

See the following complete examples:

- ``docs/ml_snippets/standard-library/functional/01_composition.ml`` - Composition and currying
- ``docs/ml_snippets/standard-library/functional/02_higher_order_functions.ml`` - Map, filter, reduce patterns
- ``docs/ml_snippets/standard-library/functional/03_list_operations.ml`` - List manipulation
- ``docs/ml_snippets/standard-library/functional/04_advanced_patterns.ml`` - Advanced FP patterns
- ``docs/ml_snippets/standard-library/functional/05_comprehensive_example.ml`` - Complete order processing system
