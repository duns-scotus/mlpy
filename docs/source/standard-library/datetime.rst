datetime - Date and Time Handling
===================================

.. module:: datetime
   :synopsis: Date and time manipulation with OOP interface

The ``datetime`` module provides comprehensive date and time handling through an object-oriented interface. Create datetime objects, perform arithmetic, format dates, and work with time boundaries.

**Import required:**

.. code-block:: ml

   import datetime;

Quick Start
-----------

.. code-block:: ml

   import datetime;

   // Get current datetime
   now = datetime.now();
   console.log(now.year());  // 2025
   console.log(now.month()); // 10
   console.log(now.day());   // 7

   // Create specific datetime
   birthday = datetime.create(1990, 5, 15, 14, 30, 0);

   // Add time
   nextWeek = now.addDays(7);
   later = now.addHours(3).addMinutes(30);

   // Get boundaries
   dayStart = now.startOfDay();    // 00:00:00
   dayEnd = now.endOfDay();        // 23:59:59

Overview
--------

The datetime module provides:

* **DateTimeObject class** - Main datetime type with arithmetic and formatting
* **Factory functions** - ``now()``, ``create()`` for creating datetime objects
* **Date arithmetic** - Add/subtract days, hours, minutes, seconds
* **Time boundaries** - Start/end of day/month operations
* **Component access** - Year, month, day, hour, minute, second, weekday
* **Unix timestamps** - Convert to/from Unix epoch seconds

**Philosophy:** Immutable datetime objects with method chaining for readable date manipulation.

Module Functions
----------------

now()
~~~~~

.. function:: now()

   Get current datetime.

   :returns: DateTimeObject representing current moment

   .. code-block:: ml

      now = datetime.now();
      console.log("Current time: " + str(now.hour()) + ":" + str(now.minute()));

create()
~~~~~~~~

.. function:: create(year, month, day, hour=0, minute=0, second=0)

   Create datetime with specific components.

   :param year: Year (e.g., 2025)
   :param month: Month (1-12)
   :param day: Day of month (1-31)
   :param hour: Hour (0-23, default 0)
   :param minute: Minute (0-59, default 0)
   :param second: Second (0-59, default 0)
   :returns: DateTimeObject

   .. code-block:: ml

      // Just date
      date = datetime.create(2025, 10, 7);

      // Date and time
      meeting = datetime.create(2025, 10, 7, 14, 30, 0);

DateTimeObject Class
--------------------

The main datetime type returned by ``now()`` and ``create()``.

Component Access Methods
~~~~~~~~~~~~~~~~~~~~~~~~~

year()
^^^^^^

.. method:: DateTimeObject.year()

   Get year component.

   :returns: Year as integer (e.g., 2025)

month()
^^^^^^^

.. method:: DateTimeObject.month()

   Get month component.

   :returns: Month as integer (1-12)

day()
^^^^^

.. method:: DateTimeObject.day()

   Get day of month.

   :returns: Day as integer (1-31)

hour()
^^^^^^

.. method:: DateTimeObject.hour()

   Get hour component.

   :returns: Hour as integer (0-23)

minute()
^^^^^^^^

.. method:: DateTimeObject.minute()

   Get minute component.

   :returns: Minute as integer (0-59)

second()
^^^^^^^^

.. method:: DateTimeObject.second()

   Get second component.

   :returns: Second as integer (0-59)

weekday()
^^^^^^^^^

.. method:: DateTimeObject.weekday()

   Get day of week.

   :returns: Integer (0=Monday, 1=Tuesday, ..., 6=Sunday)

   .. code-block:: ml

      dt = datetime.now();
      day = dt.weekday();

      weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday",
                  "Friday", "Saturday", "Sunday"];
      dayName = weekdays[day];
      console.log("Today is " + dayName);

timestamp()
^^^^^^^^^^^

.. method:: DateTimeObject.timestamp()

   Get Unix timestamp (seconds since epoch).

   :returns: Float representing seconds since January 1, 1970 UTC

   .. code-block:: ml

      now = datetime.now();
      ts = now.timestamp();  // e.g., 1728302400.0

      // Useful for comparisons
      earlier = datetime.create(2020, 1, 1);
      later = datetime.create(2025, 1, 1);
      console.log(later.timestamp() > earlier.timestamp());  // true

Arithmetic Methods
~~~~~~~~~~~~~~~~~~

All arithmetic methods return new DateTimeObject instances (immutable).

addDays()
^^^^^^^^^

.. method:: DateTimeObject.addDays(days)

   Add days to datetime.

   :param days: Number of days (can be negative)
   :returns: New DateTimeObject

   .. code-block:: ml

      today = datetime.now();
      tomorrow = today.addDays(1);
      yesterday = today.addDays(-1);
      nextWeek = today.addDays(7);

addHours()
^^^^^^^^^^

.. method:: DateTimeObject.addHours(hours)

   Add hours to datetime.

   :param hours: Number of hours (can be negative)
   :returns: New DateTimeObject

   .. code-block:: ml

      now = datetime.now();
      later = now.addHours(3);
      earlier = now.addHours(-2);

addMinutes()
^^^^^^^^^^^^

.. method:: DateTimeObject.addMinutes(minutes)

   Add minutes to datetime.

   :param minutes: Number of minutes (can be negative)
   :returns: New DateTimeObject

   .. code-block:: ml

      start = datetime.create(2025, 10, 7, 14, 0, 0);
      meetingEnd = start.addMinutes(90);  // 15:30

addSeconds()
^^^^^^^^^^^^

.. method:: DateTimeObject.addSeconds(seconds)

   Add seconds to datetime.

   :param seconds: Number of seconds (can be negative)
   :returns: New DateTimeObject

**Method Chaining:**

.. code-block:: ml

   start = datetime.now();
   future = start.addDays(7).addHours(5).addMinutes(30);
   // 7 days, 5 hours, 30 minutes later

Boundary Methods
~~~~~~~~~~~~~~~~

startOfDay()
^^^^^^^^^^^^

.. method:: DateTimeObject.startOfDay()

   Get datetime at start of day (00:00:00).

   :returns: New DateTimeObject at midnight

   .. code-block:: ml

      now = datetime.create(2025, 10, 7, 14, 30, 45);
      dayStart = now.startOfDay();
      // 2025-10-07 00:00:00

endOfDay()
^^^^^^^^^^

.. method:: DateTimeObject.endOfDay()

   Get datetime at end of day (23:59:59).

   :returns: New DateTimeObject at day end

   .. code-block:: ml

      now = datetime.create(2025, 10, 7, 14, 30, 45);
      dayEnd = now.endOfDay();
      // 2025-10-07 23:59:59

startOfMonth()
^^^^^^^^^^^^^^

.. method:: DateTimeObject.startOfMonth()

   Get datetime at start of month (first day, 00:00:00).

   :returns: New DateTimeObject at month start

   .. code-block:: ml

      now = datetime.create(2025, 10, 15, 14, 30, 0);
      monthStart = now.startOfMonth();
      // 2025-10-01 00:00:00

endOfMonth()
^^^^^^^^^^^^

.. method:: DateTimeObject.endOfMonth()

   Get datetime at end of month (last day, 23:59:59).

   :returns: New DateTimeObject at month end

   .. code-block:: ml

      now = datetime.create(2025, 10, 15, 14, 30, 0);
      monthEnd = now.endOfMonth();
      // 2025-10-31 23:59:59

      // Get days in month
      daysInMonth = monthEnd.day();  // 31

Common Patterns
---------------

Formatting Dates
~~~~~~~~~~~~~~~~

.. code-block:: ml

   dt = datetime.create(2025, 10, 7, 14, 30, 0);

   // ISO-style format
   year = str(dt.year());
   month = str(dt.month());
   day = str(dt.day());

   // Add leading zeros
   if (dt.month() < 10) {
       month = "0" + month;
   }
   if (dt.day() < 10) {
       day = "0" + day;
   }

   formatted = year + "-" + month + "-" + day;
   // "2025-10-07"

Date Comparisons
~~~~~~~~~~~~~~~~

.. code-block:: ml

   dt1 = datetime.create(2025, 10, 7, 12, 0, 0);
   dt2 = datetime.create(2025, 10, 8, 12, 0, 0);

   // Compare using timestamps
   if (dt2.timestamp() > dt1.timestamp()) {
       console.log("dt2 is later");
   }

Calculating Duration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   start = datetime.create(2025, 10, 1, 9, 0, 0);
   end = datetime.create(2025, 10, 1, 17, 0, 0);

   // Duration in seconds
   durationSeconds = end.timestamp() - start.timestamp();

   // Convert to hours
   durationHours = durationSeconds / 3600;
   console.log("Duration: " + str(durationHours) + " hours");

Working Hours Check
~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   dt = datetime.now();
   hour = dt.hour();
   day = dt.weekday();

   // Check if within business hours
   isWeekday = day >= 0 && day <= 4;  // Mon-Fri
   isWorkingHour = hour >= 9 && hour < 17;

   if (isWeekday && isWorkingHour) {
       console.log("Office is open");
   }

Age Calculation
~~~~~~~~~~~~~~~

.. code-block:: ml

   birthdate = datetime.create(1990, 5, 15, 0, 0, 0);
   today = datetime.now();

   age = today.year() - birthdate.year();

   // Adjust if birthday hasn't occurred this year
   if (today.month() < birthdate.month() ||
       (today.month() == birthdate.month() && today.day() < birthdate.day())) {
       age = age - 1;
   }

   console.log("Age: " + str(age));

Event Scheduling
~~~~~~~~~~~~~~~~

.. code-block:: ml

   // Check if time slot is free
   function isAvailable(proposedStart, duration, events) {
       proposedEnd = proposedStart.addMinutes(duration);
       proposedStartTs = proposedStart.timestamp();
       proposedEndTs = proposedEnd.timestamp();

       i = 0;
       while (i < len(events)) {
           event = events[i];
           eventEnd = event.start.addMinutes(event.duration);

           // Check overlap
           if (proposedStartTs < eventEnd.timestamp() &&
               proposedEndTs > event.start.timestamp()) {
               return false;
           }
           i = i + 1;
       }
       return true;
   }

Deadline Tracking
~~~~~~~~~~~~~~~~~

.. code-block:: ml

   now = datetime.now();
   deadline = datetime.create(2025, 10, 15, 17, 0, 0);

   secondsUntil = deadline.timestamp() - now.timestamp();
   hoursUntil = secondsUntil / 3600;
   daysUntil = hoursUntil / 24;

   if (daysUntil < 1) {
       console.log("URGENT: Less than 1 day!");
   } elif (daysUntil < 3) {
       console.log("Soon: " + str(round(daysUntil, 1)) + " days");
   } else {
       console.log("OK: " + str(round(daysUntil, 1)) + " days");
   }

Complete Examples
-----------------

Basic DateTime Operations
~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/datetime/01_basic_datetime.ml
   :language: ml
   :caption: Creating and accessing datetime components

DateTime Arithmetic
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/datetime/02_datetime_arithmetic.ml
   :language: ml
   :caption: Adding and subtracting time

Date Boundaries
~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/datetime/03_date_boundaries.ml
   :language: ml
   :caption: Working with start/end of day/month

Event Management System
~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/datetime/04_comprehensive_example.ml
   :language: ml
   :caption: Complete event scheduling application

Best Practices
--------------

1. **Use Timestamps for Comparisons**

   .. code-block:: ml

      // Good - precise comparison
      if (dt1.timestamp() > dt2.timestamp()) {
          // dt1 is later
      }

      // Avoid - component-wise comparison is error-prone

2. **Method Chaining for Readability**

   .. code-block:: ml

      // Good - clear intent
      deadline = start.addDays(7).addHours(5);

      // Also good but more verbose
      temp = start.addDays(7);
      deadline = temp.addHours(5);

3. **Use Boundaries for Time Ranges**

   .. code-block:: ml

      // Good - clear day range
      dayStart = dt.startOfDay();
      dayEnd = dt.endOfDay();
      range = {start: dayStart.timestamp(), end: dayEnd.timestamp()};

4. **Format with Leading Zeros**

   .. code-block:: ml

      month = str(dt.month());
      if (dt.month() < 10) {
          month = "0" + month;
      }
      // Ensures "05" not "5"

5. **Account for Weekdays**

   .. code-block:: ml

      weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday",
                  "Friday", "Saturday", "Sunday"];
      dayName = weekdays[dt.weekday()];

Limitations
-----------

**No Timezone Support Yet**

The current implementation works with local system time. For UTC or timezone-aware operations, you'll need to manually adjust using ``addHours()``:

.. code-block:: ml

   utcTime = datetime.create(2025, 10, 7, 12, 0, 0);
   estTime = utcTime.addHours(-5);  // EST is UTC-5
   pstTime = utcTime.addHours(-8);  // PST is UTC-8

**No Date Parsing**

The module currently doesn't parse date strings. Use ``create()`` with explicit components:

.. code-block:: ml

   // Cannot do: datetime.parse("2025-10-07")
   // Instead:
   dt = datetime.create(2025, 10, 7);

**Immutable Objects**

DateTimeObject instances are immutable. All arithmetic methods return new objects:

.. code-block:: ml

   dt = datetime.now();
   dt.addDays(1);  // Creates new object, doesn't modify dt

   // Must assign to use result
   tomorrow = dt.addDays(1);

Performance Notes
-----------------

* **Timestamp conversions are fast** - Use for comparisons
* **Component access is lightweight** - year(), month(), etc. are simple property reads
* **Arithmetic creates new objects** - Consider caching results if called repeatedly
* **Boundary methods call replace()** - Efficient but creates new objects

Security Notes
--------------

The datetime module has no capability requirements - it only works with time values, not system operations.

**Safe Operations:**

* All methods are read-only or return new objects
* No file system or network access
* No system time modification

Next Steps
----------

* Use :doc:`builtin` for type conversion with timestamps
* Combine with :doc:`console` for logging with timestamps
* Use :doc:`json` for serializing datetime data

For learning ML basics, see the :doc:`../user-guide/tutorial/index`.
