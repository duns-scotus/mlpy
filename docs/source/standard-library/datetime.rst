===============
DateTime Module
===============

The ``datetime`` module provides comprehensive date and time manipulation capabilities with timezone support, formatting options, and date arithmetic operations.

.. contents:: Contents
   :local:
   :depth: 2

Overview
========

The datetime module offers both ML-native date operations and Python bridge functions for advanced features:

- **Date Creation**: Current time, specific dates, parsing from strings
- **Formatting**: ISO format, custom patterns, localized output
- **Arithmetic**: Add/subtract days, hours, calculate differences
- **Timezone Support**: UTC, local time, timezone conversion
- **Python Bridge**: High-performance implementations for complex operations

Import and Usage
================

.. code-block:: ml

   import datetime;

   // Get current time
   now = datetime.now();
   print("Current time: " + now);

   // Create specific date
   date = datetime.create(2025, 1, 15, 14, 30, 0);

**Note**: This module requires extensive Python bridge implementation. See the source files ``datetime.ml`` and ``datetime_bridge.py`` for complete API documentation.

See Also
========

- :doc:`builtin-functions` - getCurrentTime() function
- :doc:`string` - String formatting operations