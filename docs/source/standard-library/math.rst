================
math - Mathematics
================

.. module:: math
   :synopsis: Mathematical functions and constants

The ``math`` module provides essential mathematical operations, including basic arithmetic, trigonometry, logarithms, rounding functions, and number theory utilities.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

The math module offers comprehensive mathematical capabilities for ML programs, from simple operations like square roots to advanced functions like logarithms and trigonometry. All functions handle edge cases gracefully and return appropriate error values when needed.

Mathematical Constants
======================

pi
--

The mathematical constant π (pi), approximately 3.14159.

**Value:** ``3.141592653589793``

**Example:**

.. code-block:: ml

   import math;

   circumference = 2 * math.pi * radius;
   area = math.pi * radius * radius;

e
-

The mathematical constant e (Euler's number), approximately 2.71828.

**Value:** ``2.718281828459045``

**Example:**

.. code-block:: ml

   import math;

   // Exponential growth
   result = math.exp(rate * time);

Basic Mathematical Functions
=============================

sqrt(x)
-------

Returns the square root of x.

**Parameters:**

- ``x`` - Number to find the square root of

**Returns:** Square root of x, or 0 if x is negative (error case)

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/01_basic_math.ml
   :language: ml
   :lines: 12-17
   :linenos:

abs(x)
------

Returns the absolute value of x.

**Parameters:**

- ``x`` - Number to get absolute value of

**Returns:** Absolute value of x (always non-negative)

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/01_basic_math.ml
   :language: ml
   :lines: 19-24
   :linenos:

min(a, b)
---------

Returns the smaller of two numbers.

**Parameters:**

- ``a`` - First number
- ``b`` - Second number

**Returns:** The smaller value

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/01_basic_math.ml
   :language: ml
   :lines: 26-30
   :linenos:

max(a, b)
---------

Returns the larger of two numbers.

**Parameters:**

- ``a`` - First number
- ``b`` - Second number

**Returns:** The larger value

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/01_basic_math.ml
   :language: ml
   :lines: 32-36
   :linenos:

pow(base, exponent)
-------------------

Returns base raised to the power of exponent.

**Parameters:**

- ``base`` - The base number
- ``exponent`` - The power to raise to

**Returns:** base^exponent

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/01_basic_math.ml
   :language: ml
   :lines: 38-43
   :linenos:

**Note:** Supports fractional exponents for roots (e.g., ``pow(x, 0.5)`` equals ``sqrt(x)``).

Trigonometric Functions
=======================

All trigonometric functions work with radians. Use ``degToRad()`` and ``radToDeg()`` for angle conversion.

sin(x)
------

Returns the sine of x (x in radians).

**Parameters:**

- ``x`` - Angle in radians

**Returns:** Sine of x, range [-1, 1]

cos(x)
------

Returns the cosine of x (x in radians).

**Parameters:**

- ``x`` - Angle in radians

**Returns:** Cosine of x, range [-1, 1]

tan(x)
------

Returns the tangent of x (x in radians).

**Parameters:**

- ``x`` - Angle in radians

**Returns:** Tangent of x

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/02_trigonometry.ml
   :language: ml
   :lines: 17-24
   :linenos:

Inverse Trigonometric Functions
--------------------------------

asin(x)
^^^^^^^

Returns the arcsine of x in radians.

**Parameters:**

- ``x`` - Value, must be in range [-1, 1]

**Returns:** Angle in radians, range [-π/2, π/2]

acos(x)
^^^^^^^

Returns the arccosine of x in radians.

**Parameters:**

- ``x`` - Value, must be in range [-1, 1]

**Returns:** Angle in radians, range [0, π]

atan(x)
^^^^^^^

Returns the arctangent of x in radians.

**Parameters:**

- ``x`` - Any number

**Returns:** Angle in radians, range [-π/2, π/2]

atan2(y, x)
^^^^^^^^^^^

Returns the angle (in radians) between the positive x-axis and the point (x, y).

**Parameters:**

- ``y`` - Y coordinate
- ``x`` - X coordinate

**Returns:** Angle in radians, range [-π, π]

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/02_trigonometry.ml
   :language: ml
   :lines: 67-83
   :linenos:

**Note:** ``atan2()`` is preferred over ``atan()`` for calculating angles as it handles all quadrants correctly.

Angle Conversion
----------------

degToRad(degrees)
^^^^^^^^^^^^^^^^^

Converts degrees to radians.

**Parameters:**

- ``degrees`` - Angle in degrees

**Returns:** Angle in radians

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/02_trigonometry.ml
   :language: ml
   :lines: 25-37
   :linenos:

radToDeg(radians)
^^^^^^^^^^^^^^^^^

Converts radians to degrees.

**Parameters:**

- ``radians`` - Angle in radians

**Returns:** Angle in degrees

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/02_trigonometry.ml
   :language: ml
   :lines: 39-43
   :linenos:

**Aliases:** ``radians()`` and ``degrees()`` are also available for angle conversion.

Logarithmic and Exponential Functions
======================================

exp(x)
------

Returns e raised to the power of x (e^x).

**Parameters:**

- ``x`` - Exponent

**Returns:** e^x

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/03_logarithms_exponentials.ml
   :language: ml
   :lines: 12-17
   :linenos:

ln(x)
-----

Returns the natural logarithm of x (base e).

**Parameters:**

- ``x`` - Number, must be positive

**Returns:** Natural logarithm of x, or -999 if x ≤ 0 (error case)

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/03_logarithms_exponentials.ml
   :language: ml
   :lines: 19-25
   :linenos:

log(x, base)
------------

Returns the logarithm of x with specified base.

**Parameters:**

- ``x`` - Number, must be positive
- ``base`` - Logarithm base, must be positive and not 1

**Returns:** Logarithm of x with given base, or -999 if invalid inputs

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/03_logarithms_exponentials.ml
   :language: ml
   :lines: 27-32
   :linenos:

**Common bases:**

- ``log(x, 10)`` - Common logarithm (base 10)
- ``log(x, 2)`` - Binary logarithm (base 2)
- Use ``ln(x)`` for natural logarithm (base e)

Rounding and Sign Functions
============================

floor(x)
--------

Returns the largest integer less than or equal to x (rounds down).

**Parameters:**

- ``x`` - Number to round

**Returns:** Largest integer ≤ x

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/04_rounding.ml
   :language: ml
   :lines: 12-18
   :linenos:

ceil(x)
-------

Returns the smallest integer greater than or equal to x (rounds up).

**Parameters:**

- ``x`` - Number to round

**Returns:** Smallest integer ≥ x

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/04_rounding.ml
   :language: ml
   :lines: 20-26
   :linenos:

round(x)
--------

Returns x rounded to the nearest integer.

**Parameters:**

- ``x`` - Number to round

**Returns:** Nearest integer to x

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/04_rounding.ml
   :language: ml
   :lines: 28-34
   :linenos:

**Rounding rule:** Values exactly halfway between integers (like 2.5) round toward positive infinity.

sign(x)
-------

Returns the sign of x.

**Parameters:**

- ``x`` - Any number

**Returns:** 1 if x > 0, -1 if x < 0, 0 if x == 0

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/04_rounding.ml
   :language: ml
   :lines: 36-42
   :linenos:

Number Theory Functions
=======================

factorial(n)
------------

Returns the factorial of n (n!).

**Parameters:**

- ``n`` - Non-negative integer

**Returns:** n! = n × (n-1) × (n-2) × ... × 1

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/05_number_theory.ml
   :language: ml
   :lines: 7-11
   :linenos:

**Note:** ``factorial(0)`` returns 1. Factorials grow very rapidly.

gcd(a, b)
---------

Returns the greatest common divisor of a and b.

**Parameters:**

- ``a`` - First integer
- ``b`` - Second integer

**Returns:** Largest integer that divides both a and b

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/05_number_theory.ml
   :language: ml
   :lines: 13-17
   :linenos:

**Use cases:**

- Simplifying fractions
- Finding coprime numbers (gcd = 1)
- Number theory problems

lcm(a, b)
---------

Returns the least common multiple of a and b.

**Parameters:**

- ``a`` - First integer
- ``b`` - Second integer

**Returns:** Smallest integer divisible by both a and b

**Example:**

.. literalinclude:: ../../ml_snippets/standard-library/math/05_number_theory.ml
   :language: ml
   :lines: 19-23
   :linenos:

**Use cases:**

- Finding common denominators
- Scheduling problems
- Period calculations

Random Number Generation
=========================

random()
--------

Returns a random floating-point number in the range [0, 1).

**Parameters:** None

**Returns:** Random float between 0 (inclusive) and 1 (exclusive)

**Example:**

.. code-block:: ml

   import math;

   // Random number between 0 and 1
   r = math.random();

   // Random integer between 1 and 10
   randomInt = math.floor(math.random() * 10) + 1;

   // Random float between min and max
   randomInRange = min + math.random() * (max - min);

**Note:** For more advanced random number generation (seeding, distributions, etc.), use the ``random`` module instead.

Practical Examples
==================

Distance Calculation
--------------------

Calculate distance between two points using the Pythagorean theorem:

.. literalinclude:: ../../ml_snippets/standard-library/math/01_basic_math.ml
   :language: ml
   :lines: 45-58
   :linenos:

Circle Calculations
-------------------

Calculate circumference and area of a circle:

.. literalinclude:: ../../ml_snippets/standard-library/math/02_trigonometry.ml
   :language: ml
   :lines: 85-99
   :linenos:

Compound Interest
-----------------

Calculate compound interest using exponential functions:

.. literalinclude:: ../../ml_snippets/standard-library/math/03_logarithms_exponentials.ml
   :language: ml
   :lines: 41-57
   :linenos:

Rounding to Decimal Places
---------------------------

Manual implementation of decimal place rounding:

.. literalinclude:: ../../ml_snippets/standard-library/math/04_rounding.ml
   :language: ml
   :lines: 122-136
   :linenos:

Simplifying Fractions
---------------------

Use GCD to simplify fractions to lowest terms:

.. literalinclude:: ../../ml_snippets/standard-library/math/05_number_theory.ml
   :language: ml
   :lines: 56-76
   :linenos:

Comprehensive Statistical Analysis
-----------------------------------

Real-world application combining multiple math functions:

.. literalinclude:: ../../ml_snippets/standard-library/math/06_comprehensive_example.ml
   :language: ml
   :lines: 7-64
   :linenos:

Best Practices
==============

Error Handling
--------------

Some math functions return special error values for invalid inputs:

.. code-block:: ml

   import math;

   // Check for sqrt errors
   result = math.sqrt(-1);  // Returns 0 (error case)

   if (result == 0 && input < 0) {
       console.error("Cannot take square root of negative number");
   }

   // Check for ln/log errors
   result = math.ln(-1);  // Returns -999 (error case)

   if (result == -999) {
       console.error("Logarithm of non-positive number");
   }

**Error values:**

- ``sqrt(x)`` returns 0 for x < 0
- ``ln(x)`` returns -999 for x ≤ 0
- ``log(x, base)`` returns -999 for invalid inputs

Angle Units
-----------

Always be explicit about angle units:

.. code-block:: ml

   import math;

   // CORRECT: Convert degrees to radians
   angleDeg = 45;
   angleRad = math.degToRad(angleDeg);
   result = math.sin(angleRad);

   // WRONG: Using degrees directly
   result = math.sin(45);  // Incorrect - interprets as radians

Precision Considerations
------------------------

Floating-point arithmetic has limitations:

.. code-block:: ml

   import math;

   // Rounding for display
   pi = math.pi;
   displayed = math.round(pi * 100) / 100;  // 3.14

   // Avoid exact floating-point comparisons
   // WRONG: if (value == 0.1)
   // CORRECT: if (math.abs(value - 0.1) < 0.0001)
   epsilon = 0.0001;
   if (math.abs(value - expected) < epsilon) {
       console.log("Values are approximately equal");
   }

Performance
-----------

Some operations are more efficient than others:

.. code-block:: ml

   import math;

   // FASTER: Use pow for simple squares
   square = math.pow(x, 2);

   // SLOWER: Multiple multiplications
   square = x * x * x * x;

   // FASTER: Use sqrt instead of pow(x, 0.5)
   root = math.sqrt(x);

   // SLOWER: Fractional power
   root = math.pow(x, 0.5);

See Also
========

- :doc:`random` - Advanced random number generation with seeding and distributions
- :doc:`collections` - Array manipulation and functional utilities
- Tutorial: :doc:`../user-guide/tutorial` - Basic math operations in ML

Complete Example Programs
==========================

The following complete examples demonstrate various math module capabilities:

**Basic Math Operations:**

.. literalinclude:: ../../ml_snippets/standard-library/math/01_basic_math.ml
   :language: ml
   :linenos:

**Trigonometry:**

.. literalinclude:: ../../ml_snippets/standard-library/math/02_trigonometry.ml
   :language: ml
   :linenos:

**Logarithms and Exponentials:**

.. literalinclude:: ../../ml_snippets/standard-library/math/03_logarithms_exponentials.ml
   :language: ml
   :linenos:

**Rounding Functions:**

.. literalinclude:: ../../ml_snippets/standard-library/math/04_rounding.ml
   :language: ml
   :linenos:

**Number Theory:**

.. literalinclude:: ../../ml_snippets/standard-library/math/05_number_theory.ml
   :language: ml
   :linenos:

**Comprehensive Mathematical Application:**

.. literalinclude:: ../../ml_snippets/standard-library/math/06_comprehensive_example.ml
   :language: ml
   :linenos:
