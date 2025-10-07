regex - Regular Expression Operations
======================================

.. module:: regex
   :synopsis: Regular expression matching operations

The ``regex`` module provides regular expression matching operations similar to those found in Perl. It allows you to search, match, and manipulate text using powerful pattern matching capabilities.

Quick Start
-----------

.. code-block:: ml

   import console;
   import regex;

   // Simple pattern matching
   text = "The answer is 42";
   match = regex.search('\\d+', text);

   if (match != null) {
       console.log("Found: " + match.group(0));  // "42"
   }

   // Test if pattern matches
   if (regex.test('\\d+', text)) {
       console.log("Text contains numbers");
   }

Module-Level Functions
----------------------

search()
~~~~~~~~

.. function:: search(pattern, text, flags=0)

   Search for the first occurrence of a pattern anywhere in the text.

   :param pattern: Regular expression pattern string
   :param text: Text to search in
   :param flags: Optional regex flags (IGNORECASE, MULTILINE, etc.)
   :returns: Match object if found, null otherwise

   .. code-block:: ml

      import regex;

      text = "Contact: user@example.com";
      match = regex.search('\\w+@\\w+\\.\\w+', text);

      if (match != null) {
          console.log("Email: " + match.group(0));
      }

match()
~~~~~~~

.. function:: match(pattern, text, flags=0)

   Match pattern at the start of the text only.

   :param pattern: Regular expression pattern string
   :param text: Text to match against
   :param flags: Optional regex flags
   :returns: Match object if pattern matches at start, null otherwise

   .. code-block:: ml

      // Matches only if pattern is at the start
      match1 = regex.match('\\d+', "42 is the answer");  // Success
      match2 = regex.match('\\d+', "The answer is 42");  // null

fullmatch()
~~~~~~~~~~~

.. function:: fullmatch(pattern, text, flags=0)

   Match pattern against the entire text. The pattern must match the complete string.

   :param pattern: Regular expression pattern string
   :param text: Text to match against
   :param flags: Optional regex flags
   :returns: Match object if entire text matches, null otherwise

   .. code-block:: ml

      // Must match entire string
      match1 = regex.fullmatch('\\d+', "42");        // Success
      match2 = regex.fullmatch('\\d+', "42 extra");  // null

test()
~~~~~~

.. function:: test(pattern, text, flags=0)

   Quick boolean check if pattern exists in text.

   :param pattern: Regular expression pattern string
   :param text: Text to test
   :param flags: Optional regex flags
   :returns: true if pattern found, false otherwise

   .. code-block:: ml

      if (regex.test('\\d+', text)) {
          console.log("Text contains numbers");
      }

findall()
~~~~~~~~~

.. function:: findall(pattern, text, flags=0)

   Find all non-overlapping matches of pattern in text.

   :param pattern: Regular expression pattern string
   :param text: Text to search in
   :param flags: Optional regex flags
   :returns: Array of matched strings (or arrays of groups if pattern has groups)

   .. code-block:: ml

      text = "I have 5 apples, 3 oranges, and 10 bananas";
      numbers = regex.findall('\\d+', text);
      // numbers = ["5", "3", "10"]

finditer()
~~~~~~~~~~

.. function:: finditer(pattern, text, flags=0)

   Find all matches and return array of Match objects with position information.

   :param pattern: Regular expression pattern string
   :param text: Text to search in
   :param flags: Optional regex flags
   :returns: Array of Match objects

   .. code-block:: ml

      text = "Find 42 and 123 in this text";
      matches = regex.finditer('\\d+', text);

      for (match in matches) {
          console.log(match.group(0) + " at " + str(match.start()));
      }

split()
~~~~~~~

.. function:: split(pattern, text, maxsplit=0, flags=0)

   Split text by occurrences of pattern.

   :param pattern: Regular expression pattern to split on
   :param text: Text to split
   :param maxsplit: Maximum number of splits (0 = unlimited)
   :param flags: Optional regex flags
   :returns: Array of text segments

   .. code-block:: ml

      text = "apple,banana;cherry:date";
      parts = regex.split('[,;:]', text);
      // parts = ["apple", "banana", "cherry", "date"]

sub()
~~~~~

.. function:: sub(pattern, replacement, text, count=0, flags=0)

   Replace occurrences of pattern with replacement text.

   :param pattern: Regular expression pattern to match
   :param replacement: Replacement string (can use \\1, \\2 for backreferences)
   :param text: Text to perform replacement on
   :param count: Maximum replacements (0 = all)
   :param flags: Optional regex flags
   :returns: Modified text

   .. code-block:: ml

      text = "I have 5 apples and 3 oranges";
      result = regex.sub('\\d+', 'X', text);
      // result = "I have X apples and X oranges"

      // With backreferences
      text = "First Last";
      result = regex.sub('(\\w+) (\\w+)', '\\2, \\1', text);
      // result = "Last, First"

subn()
~~~~~~

.. function:: subn(pattern, replacement, text, count=0, flags=0)

   Like sub() but returns object with result and replacement count.

   :param pattern: Regular expression pattern to match
   :param replacement: Replacement string
   :param text: Text to perform replacement on
   :param count: Maximum replacements (0 = all)
   :param flags: Optional regex flags
   :returns: Object with .result (modified text) and .count (replacements made)

   .. code-block:: ml

      result = regex.subn('\\d+', 'X', text);
      console.log("Result: " + result.result);
      console.log("Replacements: " + str(result.count));

escape()
~~~~~~~~

.. function:: escape(text)

   Escape special regex characters in text.

   :param text: Text containing special characters
   :returns: Text with special regex characters escaped

   .. code-block:: ml

      specialChars = "Price: $5.99 (sale!)";
      escaped = regex.escape(specialChars);
      // escaped = "Price:\\ \\$5\\.99\\ \\(sale!\\)"

count()
~~~~~~~

.. function:: count(pattern, text, flags=0)

   Count number of non-overlapping pattern matches.

   :param pattern: Regular expression pattern string
   :param text: Text to search in
   :param flags: Optional regex flags
   :returns: Number of matches

   .. code-block:: ml

      text = "hello world hello universe hello";
      count = regex.count('hello', text);
      // count = 3

isValid()
~~~~~~~~~

.. function:: isValid(pattern)

   Check if a pattern is a valid regular expression.

   :param pattern: Regular expression pattern string
   :returns: true if valid, false otherwise

   .. code-block:: ml

      if (regex.isValid('\\d+')) {
          console.log("Valid pattern");
      }

      if (!regex.isValid('[a-z')) {
          console.log("Invalid pattern - missing closing bracket");
      }

compile()
~~~~~~~~~

.. function:: compile(pattern, flags=0)

   Compile a pattern for efficient reuse.

   :param pattern: Regular expression pattern string
   :param flags: Optional regex flags
   :returns: Pattern object

   .. code-block:: ml

      pattern = regex.compile('\\d+', regex.IGNORECASE());

      // Reuse compiled pattern efficiently
      match1 = pattern.search("Find 42");
      match2 = pattern.search("Also 123");

Pattern Class
-------------

The Pattern class represents a compiled regular expression and provides methods for matching operations.

Methods
~~~~~~~

Pattern.search()
^^^^^^^^^^^^^^^^

.. method:: Pattern.search(text)

   Search for pattern anywhere in text.

   :param text: Text to search in
   :returns: Match object if found, null otherwise

Pattern.match()
^^^^^^^^^^^^^^^

.. method:: Pattern.match(text)

   Match pattern at the start of text.

   :param text: Text to match against
   :returns: Match object if matches at start, null otherwise

Pattern.fullmatch()
^^^^^^^^^^^^^^^^^^^

.. method:: Pattern.fullmatch(text)

   Match pattern against entire text.

   :param text: Text to match against
   :returns: Match object if entire text matches, null otherwise

Pattern.findall()
^^^^^^^^^^^^^^^^^

.. method:: Pattern.findall(text)

   Find all non-overlapping matches in text.

   :param text: Text to search in
   :returns: Array of matched strings or group arrays

Pattern.finditer()
^^^^^^^^^^^^^^^^^^

.. method:: Pattern.finditer(text)

   Find all matches returning Match objects.

   :param text: Text to search in
   :returns: Array of Match objects

Pattern.split()
^^^^^^^^^^^^^^^

.. method:: Pattern.split(text, maxsplit=0)

   Split text by pattern occurrences.

   :param text: Text to split
   :param maxsplit: Maximum splits (0 = unlimited)
   :returns: Array of text segments

Pattern.sub()
^^^^^^^^^^^^^

.. method:: Pattern.sub(replacement, text, count=0)

   Replace pattern matches with replacement.

   :param replacement: Replacement string
   :param text: Text to perform replacement on
   :param count: Maximum replacements (0 = all)
   :returns: Modified text

Pattern.subn()
^^^^^^^^^^^^^^

.. method:: Pattern.subn(replacement, text, count=0)

   Replace matches returning result and count.

   :param replacement: Replacement string
   :param text: Text to perform replacement on
   :param count: Maximum replacements (0 = all)
   :returns: Object with .result and .count

Pattern.test()
^^^^^^^^^^^^^^

.. method:: Pattern.test(text)

   Quick boolean check if pattern matches.

   :param text: Text to test
   :returns: true if pattern found, false otherwise

Pattern Properties
~~~~~~~~~~~~~~~~~~

.. attribute:: Pattern.pattern

   The original pattern string.

.. attribute:: Pattern.flags

   The regex flags used when compiling.

Match Class
-----------

The Match class represents a successful pattern match and provides methods to access match information.

Methods
~~~~~~~

Match.group()
^^^^^^^^^^^^^

.. method:: Match.group(index=0)

   Get matched text by group index.

   :param index: Group index (0 = entire match)
   :returns: Matched text for the group

   .. code-block:: ml

      match = regex.search('(\\d{3})-(\\d{4})', "Call 555-1234");
      match.group(0);  // "555-1234" (entire match)
      match.group(1);  // "555"
      match.group(2);  // "1234"

Match.groupByName()
^^^^^^^^^^^^^^^^^^^

.. method:: Match.groupByName(name)

   Get matched text by named group.

   :param name: Group name
   :returns: Matched text for the named group

   .. code-block:: ml

      pattern = '(?P<area>\\d{3})-(?P<number>\\d{4})';
      match = regex.search(pattern, "Call 555-1234");
      match.groupByName("area");    // "555"
      match.groupByName("number");  // "1234"

Match.groups()
^^^^^^^^^^^^^^

.. method:: Match.groups()

   Get array of all captured groups.

   :returns: Array of matched group strings

   .. code-block:: ml

      match = regex.search('(\\d{3})-(\\d{4})', "555-1234");
      groups = match.groups();  // ["555", "1234"]

Match.groupDict()
^^^^^^^^^^^^^^^^^

.. method:: Match.groupDict()

   Get object mapping named groups to their values.

   :returns: Object with named group mappings

   .. code-block:: ml

      pattern = '(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})';
      match = regex.search(pattern, "2025-10-05");
      dict = match.groupDict();
      // dict = {year: "2025", month: "10", day: "05"}

Match.start()
^^^^^^^^^^^^^

.. method:: Match.start(group=0)

   Get starting position of matched group.

   :param group: Group index (0 = entire match)
   :returns: Start position in original text

Match.end()
^^^^^^^^^^^

.. method:: Match.end(group=0)

   Get ending position of matched group.

   :param group: Group index (0 = entire match)
   :returns: End position in original text

Match.span()
^^^^^^^^^^^^

.. method:: Match.span(group=0)

   Get [start, end] position array for matched group.

   :param group: Group index (0 = entire match)
   :returns: Array [start, end]

   .. code-block:: ml

      match = regex.search('\\d+', "Find 42 here");
      span = match.span();  // [5, 7]

Match.value()
^^^^^^^^^^^^^

.. method:: Match.value()

   Get the matched text (same as group(0)).

   :returns: Matched text

Match Properties
~~~~~~~~~~~~~~~~

.. attribute:: Match.lastindex

   Index of last matched capturing group.

.. attribute:: Match.lastgroup

   Name of last matched capturing group (if named).

Regex Flags
-----------

Flags modify pattern matching behavior. Combine multiple flags with bitwise OR.

IGNORECASE()
~~~~~~~~~~~~

.. function:: IGNORECASE()

   Case-insensitive matching.

   .. code-block:: ml

      match = regex.search('hello', "HELLO WORLD", regex.IGNORECASE());

MULTILINE()
~~~~~~~~~~~

.. function:: MULTILINE()

   Make ^ and $ match line boundaries.

   .. code-block:: ml

      text = "line1\\nline2\\nline3";
      matches = regex.findall('^\\w+', text, regex.MULTILINE());

DOTALL()
~~~~~~~~

.. function:: DOTALL()

   Make . match any character including newlines.

   .. code-block:: ml

      pattern = regex.compile('.*', regex.DOTALL());

VERBOSE()
~~~~~~~~~

.. function:: VERBOSE()

   Allow whitespace and comments in patterns.

ASCII()
~~~~~~~

.. function:: ASCII()

   Make \\w, \\W, \\b, \\B match ASCII only.

UNICODE()
~~~~~~~~~

.. function:: UNICODE()

   Make \\w, \\W, \\b, \\B match Unicode characters.

Capturing Groups
----------------

Numbered Groups
~~~~~~~~~~~~~~~

Use parentheses to capture parts of a match:

.. code-block:: ml

   import regex;

   // Extract phone number parts
   pattern = '(\\d{3})-(\\d{4})';
   match = regex.search(pattern, "Call 555-1234");

   if (match != null) {
       console.log("Area: " + match.group(1));     // "555"
       console.log("Number: " + match.group(2));   // "1234"
   }

Named Groups
~~~~~~~~~~~~

Use ``(?P<name>...)`` syntax for named groups:

.. code-block:: ml

   import regex;

   // Extract date components
   pattern = '(?P<year>\\d{4})-(?P<month>\\d{2})-(?P<day>\\d{2})';
   match = regex.search(pattern, "Date: 2025-10-05");

   if (match != null) {
       console.log("Year: " + match.groupByName("year"));
       console.log("Month: " + match.groupByName("month"));
       console.log("Day: " + match.groupByName("day"));
   }

Practical Examples
------------------

Email Validation
~~~~~~~~~~~~~~~~

.. code-block:: ml

   import console;
   import regex;

   emailPattern = '\\w+@\\w+\\.\\w+';
   emails = [
       "user@example.com",
       "invalid.email",
       "admin@site.org"
   ];

   for (email in emails) {
       if (regex.test(emailPattern, email)) {
           console.log(email + " - valid");
       } else {
           console.log(email + " - invalid");
       }
   }

Log File Parsing
~~~~~~~~~~~~~~~~

.. code-block:: ml

   import console;
   import regex;

   logs = "[ERROR] 10:32:15 - Failed\\n[INFO] 10:32:20 - Started";
   pattern = regex.compile('\\[(\\w+)\\] ([\\d:]+) - (.+)');
   matches = pattern.finditer(logs);

   for (match in matches) {
       level = match.group(1);
       time = match.group(2);
       msg = match.group(3);
       console.log("[" + level + "] " + time + ": " + msg);
   }

URL Extraction
~~~~~~~~~~~~~~

.. code-block:: ml

   import console;
   import regex;

   text = "Visit https://example.com or http://site.org/docs";
   urls = regex.findall('https?://[\\w./]+', text);

   console.log("Found URLs:");
   for (url in urls) {
       console.log("  " + url);
   }

Data Sanitization
~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import console;
   import regex;

   // Redact email addresses
   text = "Contact john@example.com or admin@site.org";
   redacted = regex.sub('\\w+@\\w+\\.\\w+', '[EMAIL REDACTED]', text);
   console.log(redacted);

   // Format phone numbers
   phone = "5551234";
   formatted = regex.sub('(\\d{3})(\\d{4})', '\\1-\\2', phone);
   console.log(formatted);  // "555-1234"

Best Practices
--------------

1. **Compile Patterns for Reuse**

   If you're using the same pattern multiple times, compile it once:

   .. code-block:: ml

      // Good - compile once
      pattern = regex.compile('\\d+');
      match1 = pattern.search(text1);
      match2 = pattern.search(text2);

      // Avoid - recompiling each time
      match1 = regex.search('\\d+', text1);
      match2 = regex.search('\\d+', text2);

2. **Use Raw Strings for Complex Patterns**

   For patterns with many backslashes, the readability is improved with proper escaping:

   .. code-block:: ml

      // Escape backslashes properly
      pattern = '\\d{4}-\\d{2}-\\d{2}';

3. **Check for null Before Using Match**

   Always check if a match was found:

   .. code-block:: ml

      match = regex.search('\\d+', text);
      if (match != null) {
          console.log("Found: " + match.group(0));
      }

4. **Use test() for Boolean Checks**

   When you only need to know if a pattern matches:

   .. code-block:: ml

      if (regex.test('\\d+', text)) {
          console.log("Contains numbers");
      }

5. **Escape Special Characters**

   Use ``escape()`` when matching literal text that might contain special characters:

   .. code-block:: ml

      userInput = "$5.99 (sale!)";
      escaped = regex.escape(userInput);
      pattern = regex.compile(escaped);

Common Patterns
---------------

Here are some commonly used regex patterns:

.. code-block:: ml

   // Email
   '\\w+@\\w+\\.\\w+'

   // Phone (US format)
   '\\d{3}-\\d{3}-\\d{4}'

   // Date (YYYY-MM-DD)
   '\\d{4}-\\d{2}-\\d{2}'

   // URL
   'https?://[\\w./]+'

   // IP Address
   '\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}'

   // Hashtag
   '#\\w+'

   // Hex color
   '#[0-9a-fA-F]{6}'

   // Username (alphanumeric, underscore)
   '\\w+'

   // Integer
   '-?\\d+'

   // Float
   '-?\\d+\\.\\d+'

Complete Examples
-----------------

The following complete examples demonstrate real-world usage of the regex module:

Basic Matching
~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/regex/01_basic_matching.ml
   :language: ml
   :caption: Basic pattern matching operations

Capturing Groups
~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/regex/02_capturing_groups.ml
   :language: ml
   :caption: Using numbered and named capturing groups

Pattern Compilation
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/regex/03_pattern_compilation.ml
   :language: ml
   :caption: Compiling patterns for efficient reuse

Finding Matches
~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/regex/04_finding_matches.ml
   :language: ml
   :caption: Finding multiple matches with findall() and finditer()

Text Manipulation
~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/regex/05_text_manipulation.ml
   :language: ml
   :caption: Text manipulation with split(), sub(), and subn()

Comprehensive Example
~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/regex/06_comprehensive_example.ml
   :language: ml
   :caption: Real-world regex applications
