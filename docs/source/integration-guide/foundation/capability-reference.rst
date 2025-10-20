Capability Reference
====================

.. note::
   **Quick Reference:** Complete capability requirements for ML standard library modules.

   **Use This When:** You get ``CapabilityError`` and need to know which capabilities to grant.

----

Overview
--------

This document provides a complete reference of capability requirements for all ML standard library modules.

**What Are Capabilities?**

Capabilities are permission tokens that control access to system resources at runtime. Even when using ``strict_security=False`` for transpilation, runtime capability checking remains active for security.

**How to Use This Reference:**

1. Find your ML module in the tables below
2. Note the required capability token(s)
3. Grant capabilities using ``CapabilityContext``

**Basic Usage:**

.. code-block:: python

   from mlpy.runtime.capabilities import CapabilityContext

   # Grant capabilities before calling ML functions
   with CapabilityContext(['regex.match', 'datetime.now']):
       result = ml_function(data)

----

Standard Library Modules
-------------------------

Complete Capability Reference Table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: ML Standard Library Capability Requirements
   :header-rows: 1
   :widths: 20 25 30 25

   * - ML Module
     - Import Statement
     - Capability Token
     - Security Level
   * - **regex**
     - ``import regex;``
     - ``regex.match``
     - Medium
   * - **datetime**
     - ``import datetime;``
     - ``datetime.now``
     - Low
   * - **file**
     - ``import file;``
     - ``file.read:path`` or ``file.write:path``
     - High
   * - **http**
     - ``import http;``
     - ``http.get:url`` or ``http.post:url``
     - High
   * - **math**
     - ``import math;``
     - *None (built-in)*
     - None
   * - **string**
     - ``import string;``
     - *None (built-in)*
     - None
   * - **console**
     - ``import console;`` (implicit)
     - ``console.log``
     - Low

----

Module-by-Module Reference
---------------------------

regex Module
~~~~~~~~~~~~

**Capability Token:** ``regex.match``

**Operations Requiring Capability:**

.. list-table:: regex Module Operations
   :header-rows: 1
   :widths: 30 50 20

   * - Function
     - Description
     - Example
   * - ``search(pattern, text)``
     - Find first match
     - ``regex.search("@", email)``
   * - ``test(pattern, text)``
     - Test if pattern matches
     - ``regex.test("\\d+", "123")``
   * - ``match(pattern, text)``
     - Match entire string
     - ``regex.match("^\\d+$", "123")``
   * - ``split(pattern, text)``
     - Split by pattern
     - ``regex.split(",", csv)``
   * - ``replace(pattern, repl, text)``
     - Replace matches
     - ``regex.replace("\\s+", " ", text)``
   * - ``extract_emails(text)``
     - Extract email addresses
     - ``regex.extract_emails(content)``
   * - ``extract_phone_numbers(text)``
     - Extract phone numbers
     - ``regex.extract_phone_numbers(content)``
   * - ``is_url(text)``
     - Validate URL
     - ``regex.is_url("https://example.com")``
   * - ``remove_html_tags(html)``
     - Strip HTML tags
     - ``regex.remove_html_tags("<p>Text</p>")``

**Usage Example:**

.. code-block:: ml

   import regex;

   function validate_email(email) {
       // Check for @ symbol
       if (regex.search("@", email) == null) {
           return false;
       }

       // Check for domain
       if (regex.search("\\.", email) == null) {
           return false;
       }

       return true;
   }

.. code-block:: python

   # Python integration with capability
   with CapabilityContext(['regex.match']):
       is_valid = validate_email("user@example.com")

**Security Level:** Medium - Pattern matching can be CPU-intensive

----

datetime Module
~~~~~~~~~~~~~~~

**Capability Token:** ``datetime.now``

**Operations Requiring Capability:**

.. list-table:: datetime Module Operations
   :header-rows: 1
   :widths: 30 50 20

   * - Function
     - Description
     - Example
   * - ``now()``
     - Get current timestamp
     - ``datetime.now()``
   * - ``format(date, fmt)``
     - Format date string
     - ``datetime.format(dt, "%Y-%m-%d")``
   * - ``parse(text)``
     - Parse date string
     - ``datetime.parse("2025-01-20")``
   * - ``add_days(date, days)``
     - Add days to date
     - ``datetime.add_days(dt, 7)``
   * - ``timestamp()``
     - Unix timestamp
     - ``datetime.timestamp()``

**Usage Example:**

.. code-block:: ml

   import datetime;

   function generate_report(data) {
       report = {
           generated_at: datetime.now(),
           data: data,
           expires: datetime.add_days(datetime.now(), 30)
       };

       return report;
   }

.. code-block:: python

   # Python integration with capability
   with CapabilityContext(['datetime.now']):
       report = generate_report(data)

**Security Level:** Low - Time access is generally safe

----

file Module
~~~~~~~~~~~

**Capability Tokens:** ``file.read:path`` and ``file.write:path``

**Path Pattern Syntax:**

.. code-block:: python

   'file.read:/exact/file.txt'      # Exact file path
   'file.read:/data/**'             # All files under /data/ recursively
   'file.read:/config/*.json'       # JSON files in /config/ only
   'file.write:/output/**/*.txt'    # Text files under /output/ recursively

**Operations Requiring Capability:**

.. list-table:: file Module Operations
   :header-rows: 1
   :widths: 30 25 25 20

   * - Function
     - Capability
     - Description
     - Example
   * - ``read(path)``
     - ``file.read:path``
     - Read file contents
     - ``file.read("/data/file.txt")``
   * - ``write(path, content)``
     - ``file.write:path``
     - Write to file
     - ``file.write("/out/data.txt", content)``
   * - ``append(path, content)``
     - ``file.write:path``
     - Append to file
     - ``file.append("/log.txt", entry)``
   * - ``exists(path)``
     - ``file.read:path``
     - Check if file exists
     - ``file.exists("/config.json")``
   * - ``delete(path)``
     - ``file.write:path``
     - Delete file
     - ``file.delete("/temp/cache.txt")``

**Usage Example:**

.. code-block:: ml

   import file;

   function process_data_file(input_path, output_path) {
       // Read input
       content = file.read(input_path);

       // Process
       processed = content.toUpperCase();

       // Write output
       file.write(output_path, processed);

       return true;
   }

.. code-block:: python

   # Python integration with path-specific capabilities
   with CapabilityContext([
       'file.read:/data/**',        # Allow reading from /data/
       'file.write:/output/**'      # Allow writing to /output/
   ]):
       process_data_file("/data/input.txt", "/output/result.txt")

**Security Level:** High - File system access requires careful scoping

**Best Practices:**

1. **Use specific paths:** ``/data/users.json`` over ``/data/**``
2. **Separate read/write:** Grant only needed permissions
3. **Avoid wildcards:** Limit scope to exact directories needed

----

http Module
~~~~~~~~~~~

**Capability Tokens:** ``http.get:url`` and ``http.post:url``

**URL Pattern Syntax:**

.. code-block:: python

   'http.get:https://api.example.com/**'        # All paths under this domain
   'http.get:https://api.example.com/users/*'   # Specific endpoint
   'http.post:https://webhook.site/**'          # POST to webhook service

**Operations Requiring Capability:**

.. list-table:: http Module Operations
   :header-rows: 1
   :widths: 30 25 25 20

   * - Function
     - Capability
     - Description
     - Example
   * - ``get(url)``
     - ``http.get:url``
     - GET request
     - ``http.get("https://api.example.com/data")``
   * - ``post(url, data)``
     - ``http.post:url``
     - POST request
     - ``http.post(url, {key: "value"})``
   * - ``put(url, data)``
     - ``http.put:url``
     - PUT request
     - ``http.put(url, updated)``
   * - ``delete(url)``
     - ``http.delete:url``
     - DELETE request
     - ``http.delete(resource_url)``

**Usage Example:**

.. code-block:: ml

   import http;

   function fetch_user_data(user_id) {
       url = "https://api.example.com/users/" + user_id;

       response = http.get(url);

       if (response.status == 200) {
           return response.data;
       }

       return null;
   }

.. code-block:: python

   # Python integration with URL-specific capabilities
   with CapabilityContext([
       'http.get:https://api.example.com/**'
   ]):
       user_data = fetch_user_data("12345")

**Security Level:** High - Network access requires URL whitelisting

**Best Practices:**

1. **Whitelist specific domains:** Avoid ``**`` wildcards
2. **Use HTTPS:** Prefer secure connections
3. **Limit HTTP methods:** Grant only GET or POST as needed

----

math Module
~~~~~~~~~~~

**Capability Token:** *None (automatically granted)*

**All Operations are Built-in:**

.. list-table:: math Module Operations
   :header-rows: 1
   :widths: 30 50 20

   * - Function
     - Description
     - Example
   * - ``floor(x)``
     - Round down
     - ``math.floor(4.7)`` → ``4``
   * - ``ceil(x)``
     - Round up
     - ``math.ceil(4.2)`` → ``5``
   * - ``round(x)``
     - Round to nearest
     - ``math.round(4.5)`` → ``5``
   * - ``abs(x)``
     - Absolute value
     - ``math.abs(-5)`` → ``5``
   * - ``sqrt(x)``
     - Square root
     - ``math.sqrt(16)`` → ``4``
   * - ``pow(x, y)``
     - Power
     - ``math.pow(2, 3)`` → ``8``
   * - ``min(a, b)``
     - Minimum
     - ``math.min(3, 7)`` → ``3``
   * - ``max(a, b)``
     - Maximum
     - ``math.max(3, 7)`` → ``7``

**Usage Example:**

.. code-block:: ml

   import math;

   function calculate_stats(numbers) {
       sum = 0;
       for (num in numbers) {
           sum = sum + num;
       }

       avg = sum / len(numbers);

       return {
           sum: sum,
           avg: avg,
           rounded_avg: math.round(avg)
       };
   }

.. code-block:: python

   # No CapabilityContext needed - math is built-in
   stats = calculate_stats([10, 20, 30, 40, 50])

**Security Level:** None - Math operations are safe

----

string Module
~~~~~~~~~~~~~

**Capability Token:** *None (automatically granted)*

**All Operations are Built-in:**

.. list-table:: string Module Operations
   :header-rows: 1
   :widths: 30 50 20

   * - Function
     - Description
     - Example
   * - ``toUpperCase(str)``
     - Convert to uppercase
     - ``string.toUpperCase("hello")`` → ``"HELLO"``
   * - ``toLowerCase(str)``
     - Convert to lowercase
     - ``string.toLowerCase("HELLO")`` → ``"hello"``
   * - ``trim(str)``
     - Remove whitespace
     - ``string.trim("  text  ")`` → ``"text"``
   * - ``split(str, delim)``
     - Split into array
     - ``string.split("a,b,c", ",")`` → ``["a", "b", "c"]``
   * - ``join(arr, delim)``
     - Join array
     - ``string.join(["a", "b"], ",")`` → ``"a,b"``
   * - ``replace(str, old, new)``
     - Replace substring
     - ``string.replace("hello", "l", "r")`` → ``"herro"``
   * - ``startsWith(str, prefix)``
     - Check prefix
     - ``string.startsWith("hello", "he")`` → ``true``
   * - ``endsWith(str, suffix)``
     - Check suffix
     - ``string.endsWith("hello", "lo")`` → ``true``
   * - ``camel_case(str)``
     - Convert to camelCase
     - ``string.camel_case("hello world")`` → ``"helloWorld"``
   * - ``pascal_case(str)``
     - Convert to PascalCase
     - ``string.pascal_case("hello world")`` → ``"HelloWorld"``
   * - ``kebab_case(str)``
     - Convert to kebab-case
     - ``string.kebab_case("hello world")`` → ``"hello-world"``

**Usage Example:**

.. code-block:: ml

   import string;

   function normalize_username(username) {
       // Trim whitespace
       trimmed = string.trim(username);

       // Convert to lowercase
       normalized = string.toLowerCase(trimmed);

       return normalized;
   }

.. code-block:: python

   # No CapabilityContext needed - string is built-in
   username = normalize_username("  JohnDoe  ")

**Security Level:** None - String operations are safe

----

console Module
~~~~~~~~~~~~~~

**Capability Token:** ``console.log``

**Operations Requiring Capability:**

.. list-table:: console Module Operations
   :header-rows: 1
   :widths: 40 60

   * - Function
     - Description
   * - ``print(message)``
     - Output to console (if capture is enabled)

**Usage Example:**

.. code-block:: ml

   function process_data(data) {
       print("Processing " + len(data) + " items");

       // Process data...

       print("Processing complete");
       return result;
   }

.. code-block:: python

   # Grant console.log if you want to capture print output
   with CapabilityContext(['console.log']):
       result = process_data(items)

**Security Level:** Low - Console output is generally safe

**Note:** In most integration scenarios, ``print()`` output is captured for logging. Without ``console.log`` capability, print statements are silently ignored.

----

Capability Patterns
-------------------

Common Capability Combinations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Web API Validation:**

.. code-block:: python

   with CapabilityContext(['regex.match']):
       validation_result = validate_user(data)

**Data Processing Pipeline:**

.. code-block:: python

   with CapabilityContext([
       'file.read:/data/**',
       'file.write:/output/**',
       'console.log'
   ]):
       process_data_files()

**Analytics Report Generation:**

.. code-block:: python

   with CapabilityContext([
       'datetime.now',
       'regex.match'
   ]):
       report = generate_analytics_report(users)

**External API Integration:**

.. code-block:: python

   with CapabilityContext([
       'http.get:https://api.example.com/**',
       'http.post:https://webhook.site/**',
       'datetime.now'
   ]):
       sync_external_data()

**File-Based Configuration:**

.. code-block:: python

   with CapabilityContext([
       'file.read:/config/**',
       'regex.match'
   ]):
       config = load_and_validate_config()

Wildcard Patterns
~~~~~~~~~~~~~~~~~

**File Paths:**

.. code-block:: python

   'file.read:/**'                    # ❌ TOO BROAD - All files!
   'file.read:/data/**'               # ✅ GOOD - Specific directory
   'file.read:/config/*.json'         # ✅ BETTER - JSON files only
   'file.read:/config/app.json'       # ✅ BEST - Exact file

**HTTP URLs:**

.. code-block:: python

   'http.get:**'                      # ❌ TOO BROAD - Any URL!
   'http.get:https://**'              # ❌ STILL TOO BROAD
   'http.get:https://api.example.com/**'  # ✅ GOOD - Specific domain
   'http.get:https://api.example.com/v1/users/*'  # ✅ BETTER - Specific endpoint

**Best Practices:**

1. **Start specific, widen only if needed**
2. **Use exact paths for production**
3. **Wildcards for development only**
4. **Document why broad patterns are needed**

----

Security Best Practices
------------------------

Principle of Least Privilege
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Grant only the capabilities absolutely required:

.. code-block:: python

   # ❌ BAD: Overly broad
   with CapabilityContext([
       'file:*:**',
       'http:*:**',
       'regex.match',
       'datetime.now'
   ]):
       simple_validation(data)

   # ✅ GOOD: Only what's needed
   with CapabilityContext(['regex.match']):
       simple_validation(data)

Capability Scoping
~~~~~~~~~~~~~~~~~~

Wrap the narrowest scope possible:

.. code-block:: python

   # ❌ BAD: Long-lived capability context
   with CapabilityContext(['file.read:/data/**']):
       config = load_config()
       process_data(config)
       send_notification()  # Doesn't need file access!

   # ✅ GOOD: Minimal scope
   with CapabilityContext(['file.read:/data/**']):
       config = load_config()

   process_data(config)
   send_notification()

Path Restrictions
~~~~~~~~~~~~~~~~~

Always use path patterns for file and HTTP capabilities:

.. code-block:: python

   # ❌ WRONG: No path pattern
   with CapabilityContext(['file.read']):  # Will fail!
       content = read_file()

   # ✅ CORRECT: Specific path pattern
   with CapabilityContext(['file.read:/config/**']):
       content = read_file()

----

Troubleshooting
---------------

Common Capability Errors
~~~~~~~~~~~~~~~~~~~~~~~~

**Error:** ``CapabilityError: Missing required capability: regex.match``

**Solution:** Add ``'regex.match'`` to CapabilityContext

**Error:** ``CapabilityError: File path not allowed: /etc/passwd``

**Solution:** Check your ``file.read`` path pattern includes this path

**Error:** ``CapabilityError: URL not allowed: https://malicious.com``

**Solution:** Your ``http.get`` pattern doesn't whitelist this domain (this is good if the URL is unexpected!)

Debugging Capability Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # See exactly what capability is missing
   try:
       with CapabilityContext(['regex.match']):
           result = ml_function(data)
   except CapabilityError as e:
       print(f"Missing capability: {e}")
       print(f"Add this to your CapabilityContext: {e.required_capability}")

----

Summary
-------

**Quick Decision Tree:**

1. **ML code uses regex?** → Add ``'regex.match'``
2. **ML code uses datetime?** → Add ``'datetime.now'``
3. **ML code reads files?** → Add ``'file.read:path/pattern'``
4. **ML code writes files?** → Add ``'file.write:path/pattern'``
5. **ML code makes HTTP requests?** → Add ``'http.get:url/pattern'`` or ``'http.post:url/pattern'``
6. **ML code uses math/string?** → No capability needed
7. **ML code uses print()?** → Add ``'console.log'`` if you want output captured

**Remember:**

- ``strict_security=False`` only disables static analysis
- Runtime capabilities are ALWAYS required
- Use path/URL patterns for file and HTTP operations
- Grant minimum necessary capabilities
- Wrap the smallest scope possible

----

**Reference Status:** ✅ Complete | **Last Updated:** January 2026
