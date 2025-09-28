============
Math Module
============

The ``math`` module provides mathematical operations and constants with capability-based security. It combines ML-native implementations for basic operations with high-performance Python bridge functions for advanced mathematics.

.. contents:: Contents
   :local:
   :depth: 2

Overview
========

The math module is implemented as a hybrid system:

- **ML Interface**: Defines API and provides basic implementations (``math.ml``)
- **Python Bridge**: High-performance implementations for complex operations (``math_bridge.py``)
- **Security**: Requires ``read:math_constants`` and ``execute:calculations`` capabilities

Import and Usage
=================

.. code-block:: ml

   import math;

   // Use constants
   result = math.pi * radius * radius;

   // Use functions
   hypotenuse = math.sqrt(a*a + b*b);
   angle = math.sin(math.degToRad(30));

Mathematical Constants
======================

.. data:: math.pi

   The mathematical constant π (pi), approximately 3.141592653589793.

   .. code-block:: ml

      circumference = 2 * math.pi * radius;

.. data:: math.e

   The mathematical constant e (Euler's number), approximately 2.718281828459045.

   .. code-block:: ml

      result = math.pow(math.e, x);  // e^x

.. data:: math.tau

   The mathematical constant τ (tau), equal to 2π, approximately 6.283185307179586.

   .. code-block:: ml

      full_circle = math.tau;  // radians in full circle

Basic Functions
===============

.. function:: math.abs(x)

   Return the absolute value of a number.

   :param x: Number to get absolute value of
   :type x: number
   :return: Absolute value of x
   :rtype: number

   .. code-block:: ml

      result = math.abs(-5);    // 5
      result = math.abs(3.14);  // 3.14

.. function:: math.min(a, b)

   Return the smaller of two numbers.

   :param a: First number
   :type a: number
   :param b: Second number
   :type b: number
   :return: The smaller value
   :rtype: number

   .. code-block:: ml

      result = math.min(10, 5);     // 5
      result = math.min(-1, -10);   // -10

.. function:: math.max(a, b)

   Return the larger of two numbers.

   :param a: First number
   :type a: number
   :param b: Second number
   :type b: number
   :return: The larger value
   :rtype: number

   .. code-block:: ml

      result = math.max(10, 5);     // 10
      result = math.max(-1, -10);   // -1

Power and Root Functions
========================

.. function:: math.sqrt(x)

   Return the square root of a number.

   :param x: Number to find square root of (must be non-negative)
   :type x: number
   :return: Square root of x, or 0 if x < 0
   :rtype: number

   **Implementation**: Uses Newton's method in ML, Python's math.sqrt in bridge.

   .. code-block:: ml

      result = math.sqrt(16);   // 4
      result = math.sqrt(2);    // ~1.414
      result = math.sqrt(-1);   // 0 (error case)

.. function:: math.pow(base, exponent)

   Return base raised to the power of exponent.

   :param base: Base number
   :type base: number
   :param exponent: Exponent
   :type exponent: number
   :return: base^exponent
   :rtype: number

   .. code-block:: ml

      result = math.pow(2, 3);    // 8
      result = math.pow(5, 0);    // 1
      result = math.pow(2, 0.5);  // ~1.414 (square root)

.. function:: math.exp(x)

   Return e raised to the power of x.

   :param x: Exponent
   :type x: number
   :return: e^x
   :rtype: number

   .. code-block:: ml

      result = math.exp(1);    // ~2.718 (e)
      result = math.exp(0);    // 1

Logarithmic Functions
=====================

.. function:: math.ln(x)

   Return the natural logarithm of x.

   :param x: Number to find natural log of (must be positive)
   :type x: number
   :return: Natural logarithm of x, or -999 if x <= 0
   :rtype: number

   .. code-block:: ml

      result = math.ln(math.e);  // 1
      result = math.ln(1);       // 0
      result = math.ln(-1);      // -999 (error case)

.. function:: math.log(x, base)

   Return the logarithm of x to the given base.

   :param x: Number to find logarithm of (must be positive)
   :type x: number
   :param base: Base of logarithm (must be positive and != 1)
   :type base: number
   :return: log_base(x), or -999 on error
   :rtype: number

   .. code-block:: ml

      result = math.log(100, 10);  // 2 (log base 10)
      result = math.log(8, 2);     // 3 (log base 2)

Trigonometric Functions
=======================

.. function:: math.sin(x)

   Return the sine of x (x in radians).

   :param x: Angle in radians
   :type x: number
   :return: Sine of x
   :rtype: number

   .. code-block:: ml

      result = math.sin(0);          // 0
      result = math.sin(math.pi/2);  // 1

.. function:: math.cos(x)

   Return the cosine of x (x in radians).

   :param x: Angle in radians
   :type x: number
   :return: Cosine of x
   :rtype: number

   .. code-block:: ml

      result = math.cos(0);          // 1
      result = math.cos(math.pi);    // -1

.. function:: math.tan(x)

   Return the tangent of x (x in radians).

   :param x: Angle in radians
   :type x: number
   :return: Tangent of x
   :rtype: number

   .. code-block:: ml

      result = math.tan(0);          // 0
      result = math.tan(math.pi/4);  // 1

Angle Conversion
================

.. function:: math.degToRad(degrees)

   Convert degrees to radians.

   :param degrees: Angle in degrees
   :type degrees: number
   :return: Angle in radians
   :rtype: number

   .. code-block:: ml

      radians = math.degToRad(180);  // π
      radians = math.degToRad(90);   // π/2

.. function:: math.radToDeg(radians)

   Convert radians to degrees.

   :param radians: Angle in radians
   :type radians: number
   :return: Angle in degrees
   :rtype: number

   .. code-block:: ml

      degrees = math.radToDeg(math.pi);    // 180
      degrees = math.radToDeg(math.pi/2);  // 90

Rounding Functions
==================

.. function:: math.floor(x)

   Return the floor of x (largest integer <= x).

   :param x: Number to floor
   :type x: number
   :return: Floor of x
   :rtype: number

   .. code-block:: ml

      result = math.floor(3.7);   // 3
      result = math.floor(-2.3);  // -3

.. function:: math.ceil(x)

   Return the ceiling of x (smallest integer >= x).

   :param x: Number to ceiling
   :type x: number
   :return: Ceiling of x
   :rtype: number

   .. code-block:: ml

      result = math.ceil(3.2);   // 4
      result = math.ceil(-2.7);  // -2

.. function:: math.round(x)

   Return x rounded to the nearest integer.

   :param x: Number to round
   :type x: number
   :return: Rounded value
   :rtype: number

   .. code-block:: ml

      result = math.round(3.7);   // 4
      result = math.round(3.2);   // 3
      result = math.round(-2.6);  // -3

Additional Functions
====================

.. function:: math.factorial(n)

   Return the factorial of n (n!).

   :param n: Non-negative integer
   :type n: number
   :return: n! (factorial of n)
   :rtype: number

   **Implementation**: Pure ML implementation using iteration.

   .. code-block:: ml

      result = math.factorial(5);  // 120
      result = math.factorial(0);  // 1

.. function:: math.gcd(a, b)

   Return the greatest common divisor of a and b.

   :param a: First integer
   :type a: number
   :param b: Second integer
   :type b: number
   :return: Greatest common divisor
   :rtype: number

   **Implementation**: Uses Euclidean algorithm in ML.

   .. code-block:: ml

      result = math.gcd(48, 18);  // 6
      result = math.gcd(17, 13);  // 1

Security and Capabilities
=========================

The math module requires the following capabilities:

**Required Capabilities:**

- ``read:math_constants`` - Access to mathematical constants
- ``execute:calculations`` - Permission to perform calculations

**Security Features:**

- **Safe Error Handling**: Invalid operations return safe default values instead of throwing exceptions
- **Input Validation**: All functions validate input parameters
- **Capability Enforcement**: All operations checked against granted capabilities

**Error Handling:**

.. code-block:: ml

   // Safe error returns
   result = math.sqrt(-1);    // Returns 0 instead of error
   result = math.ln(-1);      // Returns -999 instead of exception
   result = math.log(0, 10);  // Returns -999 instead of exception

Implementation Details
======================

**Hybrid Architecture:**

The math module uses both ML and Python implementations:

- **Basic operations** (abs, min, max, factorial, gcd): Pure ML implementations
- **Advanced functions** (sin, cos, exp, log): Python bridge for performance
- **Constants**: Defined in both ML and Python for consistency

**Performance:**

- Basic operations: ~0.1ms execution time
- Bridge functions: ~0.05ms with Python optimization
- Constant access: Immediate (no function call overhead)

**Memory Usage:**

- Constants: Loaded once at import time
- Functions: No persistent state, minimal memory footprint
- Caching: Results not cached (functions are pure)

Examples
========

Mathematical Calculations
-------------------------

.. code-block:: ml

   import math;

   // Pythagorean theorem
   function distance(x1, y1, x2, y2) {
       dx = x2 - x1;
       dy = y2 - y1;
       return math.sqrt(dx*dx + dy*dy);
   }

   // Circle area
   function circleArea(radius) {
       return math.pi * radius * radius;
   }

   // Compound interest
   function compoundInterest(principal, rate, time) {
       return principal * math.pow(1 + rate, time);
   }

Trigonometry
------------

.. code-block:: ml

   import math;

   // Convert and calculate
   angle_degrees = 45;
   angle_radians = math.degToRad(angle_degrees);
   sine_value = math.sin(angle_radians);

   print("sin(45°) = " + sine_value);  // ~0.707

Statistics Functions
--------------------

.. code-block:: ml

   import math;

   function mean(numbers) {
       sum = 0;
       for (i = 0; i < numbers.length; i++) {
           sum = sum + numbers[i];
       }
       return sum / numbers.length;
   }

   function standardDeviation(numbers) {
       avg = mean(numbers);
       sumSquaredDiffs = 0;

       for (i = 0; i < numbers.length; i++) {
           diff = numbers[i] - avg;
           sumSquaredDiffs = sumSquaredDiffs + (diff * diff);
       }

       variance = sumSquaredDiffs / numbers.length;
       return math.sqrt(variance);
   }

See Also
========

- :doc:`random` - Random number generation
- :doc:`float` - Floating-point operations
- :doc:`int` - Integer operations
- :doc:`../developer-guide/writing-stdlib-modules` - Creating new modules