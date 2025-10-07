=================
Working with Data
=================

Most programs work with collections of data. ML provides arrays and objects for organizing and processing information.

.. contents::
   :local:
   :depth: 2

Array Operations
================

Arrays store ordered collections of values.

Creating Arrays
---------------

Create empty arrays or initialize them with values:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-14-array-operations.transcript
   :language: text
   :lines: 7-14

Combining Arrays
----------------

Use the ``+`` operator to concatenate arrays:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-14-array-operations.transcript
   :language: text
   :lines: 16-23

This creates a new array containing all elements from both arrays.

Adding Elements
---------------

Build arrays incrementally using concatenation:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-14-array-operations.transcript
   :language: text
   :lines: 25-34

.. important::
   Arrays do not auto-extend with index assignment. Always use ``arr = arr + [value]`` to add elements, or use the ``append()`` function.

Working with Array Length
-------------------------

Get the number of elements with ``len()``:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-14-array-operations.transcript
   :language: text
   :lines: 36-40

Array Techniques
================

Transforming Arrays
-------------------

Create new arrays by transforming each element:

.. code-block:: ml

    function multiplyBy(arr, factor) {
        output = [];
        for (value in arr) {
            output = output + [value * factor];
        }
        return output;
    }

    numbers = [1, 2, 3, 4, 5];
    doubled = multiplyBy(numbers, 2);  // [2, 4, 6, 8, 10]

Filtering Arrays
----------------

Select elements matching criteria:

.. code-block:: ml

    function filterGreaterThan(arr, threshold) {
        filtered = [];
        for (value in arr) {
            if (value > threshold) {
                filtered = filtered + [value];
            }
        }
        return filtered;
    }

    values = [5, 15, 8, 23, 12, 30, 7];
    aboveTen = filterGreaterThan(values, 10);  // [15, 23, 12, 30]

Searching Arrays
----------------

Find specific elements:

.. code-block:: ml

    function findFirstMatch(arr, target) {
        for (value in arr) {
            if (value == target) {
                return value;
            }
        }
        return -1;  // Not found
    }

Complete Array Example
----------------------

Here's a program demonstrating array techniques:

.. literalinclude:: ../../../ml_snippets/tutorial/13_array_techniques.ml
   :language: ml

This shows:

* **Combining**: Concatenating multiple arrays
* **Building**: Creating arrays incrementally
* **Transforming**: Applying operations to each element
* **Filtering**: Selecting elements by condition
* **Searching**: Finding specific values
* **Partitioning**: Splitting arrays into groups

Object Operations
=================

Objects store key-value pairs. Access properties using dot notation.

Creating Objects
----------------

Define objects with property-value pairs:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-15-object-operations.transcript
   :language: text
   :lines: 7-13

Modifying Properties
--------------------

Change property values with assignment:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-15-object-operations.transcript
   :language: text
   :lines: 15-22

Adding Properties
-----------------

Add new properties to existing objects:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-15-object-operations.transcript
   :language: text
   :lines: 24-32

Nested Objects
--------------

Objects can contain other objects:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-15-object-operations.transcript
   :language: text
   :lines: 34-42

Access nested properties by chaining dot notation: ``user.address.city``

Object Techniques
=================

Objects in Functions
--------------------

Pass objects to functions as parameters:

.. code-block:: ml

    function describeProduct(prod) {
        description = prod.name + " costs $" + str(prod.price);
        return description;
    }

    item = {name: "Laptop", price: 999.99};
    console.log(describeProduct(item));

Functions that Create Objects
------------------------------

Return objects from functions:

.. code-block:: ml

    function createUser(username, email) {
        return {
            name: username,
            email: email,
            active: true
        };
    }

    user = createUser("alice", "alice@example.com");
    console.log(user.name);  // "alice"

This pattern helps organize related data.

Complete Object Example
-----------------------

Here's a program demonstrating object techniques:

.. literalinclude:: ../../../ml_snippets/tutorial/14_object_techniques.ml
   :language: ml

Nested Data Structures
======================

Real programs often combine arrays and objects.

Arrays of Objects
-----------------

Store multiple records as objects in an array:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-16-nested-data.transcript
   :language: text
   :lines: 7-15

This pattern is common for lists of records, users, products, or any collection of related data.

Objects with Arrays
-------------------

Objects can have array properties:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-16-nested-data.transcript
   :language: text
   :lines: 17-25

Use this when objects have multiple values for a property (scores, tags, items).

Complex Nesting
---------------

Combine multiple levels of nesting:

.. literalinclude:: ../../../repl_snippets/tutorial/tutorial-16-nested-data.transcript
   :language: text
   :lines: 27-37

Navigate nested structures by chaining array indices and property access.

Data Processing Patterns
========================

Processing Arrays of Objects
-----------------------------

Iterate over records and access properties:

.. code-block:: ml

    students = [
        {name: "Alice", grade: 85},
        {name: "Bob", grade: 92},
        {name: "Carol", grade: 78}
    ];

    for (student in students) {
        console.log(student.name + ": " + str(student.grade));
    }

Filtering by Property
---------------------

Select objects matching criteria:

.. code-block:: ml

    function getHighScorers(studentList, threshold) {
        highScorers = [];
        for (student in studentList) {
            if (student.grade >= threshold) {
                highScorers = highScorers + [student];
            }
        }
        return highScorers;
    }

    topStudents = getHighScorers(students, 90);

Calculating Statistics
----------------------

Aggregate data from object properties:

.. code-block:: ml

    function calculateAverageGrade(studentList) {
        total = 0;
        for (student in studentList) {
            total = total + student.grade;
        }
        return total / len(studentList);
    }

    average = calculateAverageGrade(students);

Grouping Data
-------------

Organize objects by property values:

.. code-block:: ml

    function groupBySubject(studentList) {
        mathStudents = [];
        scienceStudents = [];
        for (student in studentList) {
            if (student.subject == "Math") {
                mathStudents = mathStudents + [student];
            } else {
                scienceStudents = scienceStudents + [student];
            }
        }
        return {
            math: mathStudents,
            science: scienceStudents
        };
    }

Complete Data Processing Example
=================================

Here's a program showing practical data processing:

.. literalinclude:: ../../../ml_snippets/tutorial/15_data_processing.ml
   :language: ml

This demonstrates:

* **Arrays of objects**: Student records, course information
* **Filtering**: Finding high scorers by grade
* **Aggregation**: Calculating averages and totals
* **Grouping**: Organizing students by subject
* **Nested access**: Working with courses in departments
* **Search**: Finding specific items in collections

Common Patterns
===============

Collection Pattern
------------------

Store related items together:

.. code-block:: ml

    products = [
        {id: 1, name: "Widget", price: 29.99, inStock: true},
        {id: 2, name: "Gadget", price: 49.99, inStock: false},
        {id: 3, name: "Gizmo", price: 19.99, inStock: true}
    ];

Lookup Pattern
--------------

Find items by property:

.. code-block:: ml

    function findById(items, targetId) {
        for (item in items) {
            if (item.id == targetId) {
                return item;
            }
        }
        return {id: -1, name: "Not found"};
    }

    product = findById(products, 2);

Accumulation Pattern
--------------------

Sum values across a collection:

.. code-block:: ml

    function totalPrice(items) {
        total = 0;
        for (item in items) {
            total = total + item.price;
        }
        return total;
    }

    cost = totalPrice(products);

Transformation Pattern
----------------------

Convert one collection to another:

.. code-block:: ml

    function getNames(items) {
        names = [];
        for (item in items) {
            names = names + [item.name];
        }
        return names;
    }

    productNames = getNames(products);

Best Practices
==============

**Array Building**: Always use ``arr = arr + [value]`` or ``append(arr, value)`` to add elements. Index assignment doesn't work on empty arrays.

**Consistent Structure**: Keep objects in an array with the same properties. This makes processing predictable.

**Meaningful Names**: Use descriptive variable names: ``students``, ``products``, ``userProfiles``.

**Small Functions**: Break complex data processing into smaller functions that do one thing.

**Null Checks**: When searching, return a sensible default if not found (like ``-1`` or an empty object).

**Immutability**: Consider creating new arrays instead of modifying existing ones. This makes code easier to reason about.

**Documentation**: Complex data structures benefit from comments explaining their shape and purpose.

Summary
=======

You now understand:

* Array operations (creating, combining, adding elements)
* Array techniques (transforming, filtering, searching)
* Object operations (creating, modifying, nesting)
* Nested data structures (arrays of objects, objects with arrays)
* Data processing patterns (filtering, aggregating, grouping)

These techniques form the foundation for working with real-world data in ML programs. Practice combining arrays and objects to model the data your programs need.

Tutorial Complete
=================

You've completed the ML tutorial! You've learned:

* **Getting Started**: REPL basics, variables, simple programs
* **Basic Syntax**: Data types, operators, collections
* **Control Flow**: Loops, conditionals, break/continue
* **Functions**: Definition, parameters, return values, patterns
* **Working with Data**: Arrays, objects, nested structures, processing

Next, explore the language reference for complete syntax details, or the standard library documentation for built-in modules and functions.
