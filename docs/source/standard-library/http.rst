====
http
====

.. module:: http
   :synopsis: HTTP client for making web requests with capability-based security

The ``http`` module provides HTTP/HTTPS client functionality with comprehensive request methods, response handling, and fine-grained security controls through capability-based domain restrictions.

Overview
========

The http module enables ML programs to make HTTP requests, handle responses, and work with REST APIs through a clean, secure interface. All network operations require explicit capabilities and support domain/URL pattern restrictions for precise permission management.

Key Features
------------

- **HTTP Methods**: GET, POST, PUT, DELETE, PATCH, HEAD, custom request
- **Response Handling**: Status codes, headers, body parsing, JSON support
- **URL Utilities**: Encoding, decoding, query string handling
- **Security**: Capability-based access with domain/URL patterns
- **Timeouts**: Configurable request timeouts (default: 30s)
- **Size Limits**: Response size limits (default: 10MB)

Security Model
==============

Capability-Based Access
-----------------------

All HTTP operations require explicit capability grants:

.. code-block:: ml

    // Required capabilities:
    network.http      // Make HTTP requests
    network.https     // Make HTTPS requests

    // Domain restrictions:
    network.http:api.example.com          // Specific domain
    network.http:*.example.com            // Subdomain wildcard
    network.http:https://api.example.com/* // URL pattern

URL Validation
--------------

- All URLs validated before requests
- Protocol enforcement (http/https)
- Domain restrictions via capability patterns
- Path pattern matching support

Resource Limits
---------------

- Default timeout: 30 seconds (configurable)
- Maximum response size: 10MB
- Automatic timeout enforcement
- Size limit prevents memory exhaustion

Usage
=====

Import the http module to access HTTP functionality:

.. code-block:: ml

    import http;

    // Simple GET request
    response = http.get("https://api.example.com/data");
    if (response.ok()) {
        data = response.json();
    }

    // POST with JSON
    newItem = {name: "Item", price: 29.99};
    response = http.post("https://api.example.com/items", {
        body: json.stringify(newItem),
        headers: {"Content-Type": "application/json"}
    });

HTTP Request Methods
====================

get
^^^

.. function:: get(url, headers=null, timeout=null)

   Make HTTP GET request.

   :param url: Request URL
   :type url: string
   :param headers: Optional request headers
   :type headers: object
   :param timeout: Request timeout in seconds (default: 30)
   :type timeout: number
   :return: HttpResponse object
   :rtype: HttpResponse
   :capability: network.http or network.https

   **Examples:**

   .. code-block:: ml

       // Simple GET
       response = http.get("https://api.example.com/users");

       // GET with headers
       headers = {
           "Authorization": "Bearer token",
           "Accept": "application/json"
       };
       response = http.get("https://api.example.com/users", headers);

       // GET with timeout
       response = http.get("https://api.example.com/slow-endpoint", null, 60);

       // GET with query parameters
       params = {page: "1", limit: "20"};
       queryStr = http.encodeQuery(params);
       url = "https://api.example.com/users?" + queryStr;
       response = http.get(url);

   **Use Cases:**

   - Fetching data from APIs
   - Reading web resources
   - Checking resource availability
   - Paginated data retrieval

post
^^^^

.. function:: post(url, options=null)

   Make HTTP POST request.

   :param url: Request URL
   :type url: string
   :param options: Request options {body, headers, timeout}
   :type options: object
   :return: HttpResponse object
   :rtype: HttpResponse
   :capability: network.http or network.https

   **Examples:**

   .. code-block:: ml

       // POST with JSON
       newUser = {name: "Alice", email: "alice@example.com"};
       response = http.post("https://api.example.com/users", {
           body: json.stringify(newUser),
           headers: {"Content-Type": "application/json"}
       });

       // POST with form data
       formData = {username: "alice", password: "secret"};
       response = http.post("https://api.example.com/login", {
           body: http.encodeQuery(formData),
           headers: {"Content-Type": "application/x-www-form-urlencoded"}
       });

       // POST with timeout
       response = http.post("https://api.example.com/upload", {
           body: largeData,
           timeout: 120
       });

   **Use Cases:**

   - Creating new resources
   - Submitting forms
   - User authentication
   - File uploads

put
^^^

.. function:: put(url, options=null)

   Make HTTP PUT request for full resource updates.

   :param url: Request URL
   :type url: string
   :param options: Request options {body, headers, timeout}
   :type options: object
   :return: HttpResponse object
   :rtype: HttpResponse
   :capability: network.http or network.https

   **Examples:**

   .. code-block:: ml

       // Update entire resource
       updatedUser = {
           name: "Alice Smith",
           email: "alice@example.com",
           role: "admin"
       };
       response = http.put("https://api.example.com/users/123", {
           body: json.stringify(updatedUser),
           headers: {"Content-Type": "application/json"}
       });

   **Use Cases:**

   - Updating entire resources
   - Replacing resource data
   - Idempotent updates

delete
^^^^^^

.. function:: delete(url, headers=null, timeout=null)

   Make HTTP DELETE request.

   :param url: Request URL
   :type url: string
   :param headers: Optional request headers
   :type headers: object
   :param timeout: Request timeout in seconds
   :type timeout: number
   :return: HttpResponse object
   :rtype: HttpResponse
   :capability: network.http or network.https

   **Examples:**

   .. code-block:: ml

       // Delete resource
       response = http.delete("https://api.example.com/users/123");
       if (response.ok()) {
           console.log("Deleted successfully");
       }

       // Delete with authentication
       headers = {"Authorization": "Bearer token"};
       response = http.delete("https://api.example.com/items/456", headers);

   **Use Cases:**

   - Removing resources
   - Cleanup operations
   - Resource lifecycle management

patch
^^^^^

.. function:: patch(url, options=null)

   Make HTTP PATCH request for partial resource updates.

   :param url: Request URL
   :type url: string
   :param options: Request options {body, headers, timeout}
   :type options: object
   :return: HttpResponse object
   :rtype: HttpResponse
   :capability: network.http or network.https

   **Examples:**

   .. code-block:: ml

       // Partial update
       updates = {status: "completed", priority: "high"};
       response = http.patch("https://api.example.com/tasks/789", {
           body: json.stringify(updates),
           headers: {"Content-Type": "application/json"}
       });

   **Use Cases:**

   - Partial resource updates
   - Status changes
   - Incremental modifications

head
^^^^

.. function:: head(url, headers=null, timeout=null)

   Make HTTP HEAD request (headers only, no body).

   :param url: Request URL
   :type url: string
   :param headers: Optional request headers
   :type headers: object
   :param timeout: Request timeout in seconds
   :type timeout: number
   :return: HttpResponse object (body will be empty)
   :rtype: HttpResponse
   :capability: network.http or network.https

   **Examples:**

   .. code-block:: ml

       // Check resource metadata
       response = http.head("https://example.com/large-file.zip");
       headers = response.headers();
       fileSize = headers["Content-Length"];
       contentType = headers["Content-Type"];
       console.log("File size: " + fileSize);

   **Use Cases:**

   - Checking resource existence
   - Getting file sizes
   - Validating links
   - Cache validation

request
^^^^^^^

.. function:: request(options)

   Make custom HTTP request with full control.

   :param options: Request options {method, url, headers, body, timeout}
   :type options: object
   :return: HttpResponse object
   :rtype: HttpResponse
   :capability: network.http or network.https

   **Examples:**

   .. code-block:: ml

       // Custom request
       response = http.request({
           method: "GET",
           url: "https://api.example.com/data",
           headers: {
               "Authorization": "Bearer token",
               "Accept": "application/json",
               "User-Agent": "MyApp/1.0"
           },
           timeout: 60
       });

       // Custom method
       response = http.request({
           method: "OPTIONS",
           url: "https://api.example.com/resource"
       });

   **Use Cases:**

   - Custom HTTP methods
   - Advanced request configuration
   - Complete control over all parameters

Response Object
===============

HttpResponse
^^^^^^^^^^^^

All HTTP methods return an HttpResponse object with these methods:

status
""""""

.. function:: response.status()

   Get HTTP status code.

   :return: Status code (200, 404, etc.)
   :rtype: number

   **Examples:**

   .. code-block:: ml

       response = http.get(url);
       status = response.status();

       if (status == 200) {
           console.log("Success");
       } elif (status == 404) {
           console.log("Not found");
       }

statusText
""""""""""

.. function:: response.statusText()

   Get status message.

   :return: Status message ("OK", "Not Found", etc.)
   :rtype: string

   **Examples:**

   .. code-block:: ml

       response = http.get(url);
       console.log(str(response.status()) + " " + response.statusText());
       // "404 Not Found"

ok
"""

.. function:: response.ok()

   Check if response status is successful (2xx).

   :return: True if status is 200-299, False otherwise
   :rtype: boolean

   **Examples:**

   .. code-block:: ml

       response = http.get(url);
       if (response.ok()) {
           data = response.json();
           // Process successful response
       } else {
           console.log("Request failed: " + str(response.status()));
       }

body
""""

.. function:: response.body()

   Get response body as string.

   :return: Response body
   :rtype: string

   **Examples:**

   .. code-block:: ml

       response = http.get(url);
       text = response.body();
       console.log("Response: " + text);

text
""""

.. function:: response.text()

   Get response as text (alias for body()).

   :return: Response body
   :rtype: string

json
""""

.. function:: response.json()

   Parse response body as JSON.

   :return: Parsed JSON object
   :raises: ValueError if body is not valid JSON

   **Examples:**

   .. code-block:: ml

       response = http.get("https://api.example.com/users/123");
       if (response.ok()) {
           user = response.json();
           console.log("Name: " + user.name);
           console.log("Email: " + user.email);
       }

headers
"""""""

.. function:: response.headers()

   Get response headers dictionary.

   :return: Headers dictionary
   :rtype: object

   **Examples:**

   .. code-block:: ml

       response = http.get(url);
       headers = response.headers();
       contentType = headers["Content-Type"];
       contentLength = headers["Content-Length"];
       server = headers["Server"];

URL Utilities
=============

encodeURI
^^^^^^^^^

.. function:: encodeURI(text)

   URL encode string (percent encoding).

   :param text: String to encode
   :type text: string
   :return: URL-encoded string
   :rtype: string
   :capability: None required

   **Examples:**

   .. code-block:: ml

       // Encode spaces
       encoded = http.encodeURI("hello world");
       // "hello%20world"

       // Encode special characters
       encoded = http.encodeURI("user@example.com");
       // "user%40example.com"

       // Build search URL
       searchTerm = "machine learning";
       encoded = http.encodeURI(searchTerm);
       url = "https://api.com/search?q=" + encoded;

   **Use Cases:**

   - URL path encoding
   - Search query encoding
   - Building URLs with special characters

decodeURI
^^^^^^^^^

.. function:: decodeURI(text)

   URL decode string (percent decoding).

   :param text: URL-encoded string
   :type text: string
   :return: Decoded string
   :rtype: string
   :capability: None required

   **Examples:**

   .. code-block:: ml

       decoded = http.decodeURI("hello%20world");
       // "hello world"

       decoded = http.decodeURI("user%40example.com");
       // "user@example.com"

   **Use Cases:**

   - Decoding URL parameters
   - Processing encoded URLs
   - Reverse encoding

encodeQuery
^^^^^^^^^^^

.. function:: encodeQuery(params)

   Encode object as URL query string.

   :param params: Parameters dictionary
   :type params: object
   :return: Query string (without leading ?)
   :rtype: string
   :capability: None required

   **Examples:**

   .. code-block:: ml

       // Simple parameters
       params = {name: "John", age: "30"};
       query = http.encodeQuery(params);
       // "name=John&age=30"

       // Build complete URL
       baseUrl = "https://api.example.com/users";
       params = {page: "1", limit: "20"};
       queryStr = http.encodeQuery(params);
       url = baseUrl + "?" + queryStr;
       // "https://api.example.com/users?page=1&limit=20"

   **Use Cases:**

   - Building API URLs
   - Pagination parameters
   - Filter parameters
   - Search queries

parseQuery
^^^^^^^^^^

.. function:: parseQuery(query)

   Parse URL query string to object.

   :param query: Query string (with or without leading ?)
   :type query: string
   :return: Parameters dictionary
   :rtype: object
   :capability: None required

   **Examples:**

   .. code-block:: ml

       // Parse query string
       params = http.parseQuery("name=John&age=30");
       // {name: "John", age: "30"}

       // With leading ?
       params = http.parseQuery("?search=ML&page=2");
       // {search: "ML", page: "2"}

   **Use Cases:**

   - Parsing URL parameters
   - Extracting query values
   - URL analysis

Practical Examples
==================

Simple API Client
-----------------

Basic GET and POST operations:

.. code-block:: ml

    import console;
    import http;
    import json;

    // GET request
    response = http.get("https://api.example.com/users");
    if (response.ok()) {
        users = response.json();
        console.log("Users: " + str(len(users)));
    }

    // POST request
    newUser = {name: "Alice", email: "alice@example.com"};
    response = http.post("https://api.example.com/users", {
        body: json.stringify(newUser),
        headers: {"Content-Type": "application/json"}
    });

    if (response.ok()) {
        created = response.json();
        console.log("Created ID: " + str(created.id));
    }

Authenticated Requests
----------------------

Using bearer token authentication:

.. code-block:: ml

    import http;
    import json;

    // Prepare headers
    authToken = "your_api_token";
    headers = {
        "Authorization": "Bearer " + authToken,
        "Content-Type": "application/json"
    };

    // Authenticated GET
    response = http.get("https://api.example.com/protected", headers);

    // Authenticated POST
    data = {field: "value"};
    response = http.post("https://api.example.com/resource", {
        body: json.stringify(data),
        headers: headers
    });

Pagination
----------

Fetching paginated data:

.. code-block:: ml

    import http;

    function fetchPage(page, limit) {
        params = {page: str(page), limit: str(limit)};
        queryStr = http.encodeQuery(params);
        url = "https://api.example.com/items?" + queryStr;

        return http.get(url);
    }

    // Fetch multiple pages
    page = 1;
    while (page <= 5) {
        response = fetchPage(page, 20);
        if (response.ok()) {
            data = response.json();
            console.log("Page " + str(page) + ": " + str(len(data.items)) + " items");
        }
        page = page + 1;
    }

Error Handling
--------------

Comprehensive error handling:

.. code-block:: ml

    import http;
    import console;

    response = http.get("https://api.example.com/resource");
    status = response.status();

    if (status == 200) {
        data = response.json();
        console.log("Success");
    } elif (status == 404) {
        console.log("Resource not found");
    } elif (status == 401) {
        console.log("Unauthorized - check credentials");
    } elif (status == 429) {
        console.log("Rate limit exceeded");
    } elif (status >= 500) {
        console.log("Server error - try again later");
    } else {
        console.log("Error: " + str(status));
    }

CRUD Operations
---------------

Complete create, read, update, delete workflow:

.. code-block:: ml

    import http;
    import json;

    apiBase = "https://api.example.com";
    headers = {"Content-Type": "application/json"};

    // Create
    newItem = {name: "Item", price: 29.99};
    response = http.post(apiBase + "/items", {
        body: json.stringify(newItem),
        headers: headers
    });
    itemId = response.json().id;

    // Read
    response = http.get(apiBase + "/items/" + str(itemId));
    item = response.json();

    // Update
    item.price = 34.99;
    response = http.put(apiBase + "/items/" + str(itemId), {
        body: json.stringify(item),
        headers: headers
    });

    // Delete
    response = http.delete(apiBase + "/items/" + str(itemId));

Common Patterns
===============

URL Building
------------

Construct URLs with parameters:

.. code-block:: ml

    // Base URL
    baseUrl = "https://api.example.com/search";

    // Add query parameters
    params = {q: "ML", type: "article", limit: "10"};
    queryStr = http.encodeQuery(params);
    fullUrl = baseUrl + "?" + queryStr;

    // Make request
    response = http.get(fullUrl);

Response Validation
-------------------

Check response before processing:

.. code-block:: ml

    response = http.get(url);

    // Check status
    if (!response.ok()) {
        console.log("Request failed: " + str(response.status()));
        return null;
    }

    // Check Content-Type
    headers = response.headers();
    contentType = headers["Content-Type"];

    if (contentType == "application/json") {
        return response.json();
    } else {
        return response.text();
    }

Retry Logic
-----------

Implement request retries:

.. code-block:: ml

    function fetchWithRetry(url, maxRetries) {
        attempt = 0;
        while (attempt < maxRetries) {
            response = http.get(url);

            if (response.ok()) {
                return response;
            }

            // Retry on server errors
            if (response.status() >= 500) {
                attempt = attempt + 1;
                console.log("Retry " + str(attempt) + "/" + str(maxRetries));
            } else {
                // Don't retry client errors
                return response;
            }
        }

        return null;
    }

Best Practices
==============

Request Configuration
---------------------

1. **Set Appropriate Timeouts**: Use longer timeouts for slow endpoints
2. **Include User-Agent**: Identify your application
3. **Use Proper Content-Type**: Match body format
4. **Handle Authentication**: Securely manage tokens

Response Handling
-----------------

1. **Always Check Status**: Use ``response.ok()`` or check status code
2. **Validate Content-Type**: Check before parsing
3. **Handle Errors Gracefully**: Provide meaningful error messages
4. **Parse JSON Safely**: Check status before parsing

Security
--------

1. **Use HTTPS**: Prefer HTTPS over HTTP
2. **Validate URLs**: Ensure URLs are expected domains
3. **Protect Credentials**: Never log or expose tokens
4. **Handle Timeouts**: Set reasonable timeout limits

Performance
-----------

1. **Reuse Connections**: HTTP client handles connection pooling
2. **Batch Requests**: Group related requests when possible
3. **Use HEAD**: Check resources without downloading body
4. **Set Size Limits**: Response size is limited to 10MB

Performance Considerations
==========================

Request Performance
-------------------

- Default timeout: 30 seconds
- Configurable per-request timeouts
- Automatic connection management
- Response size limit: 10MB

Response Parsing
----------------

- ``response.text()`` returns complete body
- ``response.json()`` parses entire body
- Headers available without body parsing
- Status check is instant

Network Efficiency
------------------

- Use HEAD for metadata only
- Compress responses when possible (server-side)
- Batch related requests
- Implement caching strategies

Common HTTP Status Codes
=========================

Success (2xx)
-------------

- **200 OK** - Request succeeded
- **201 Created** - Resource created successfully
- **204 No Content** - Success with no response body

Client Errors (4xx)
-------------------

- **400 Bad Request** - Invalid request syntax
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Authorization failed
- **404 Not Found** - Resource doesn't exist
- **429 Too Many Requests** - Rate limit exceeded

Server Errors (5xx)
-------------------

- **500 Internal Server Error** - Server encountered error
- **502 Bad Gateway** - Invalid upstream response
- **503 Service Unavailable** - Server temporarily unavailable
- **504 Gateway Timeout** - Upstream timeout

See Also
========

- :doc:`json` - JSON parsing for API responses
- :doc:`file` - File operations for caching responses
- :doc:`builtin` - Type checking and conversion functions

.. note::

   All HTTP operations require ``network.http`` or ``network.https`` capabilities. Capabilities can be restricted by domain or URL patterns for fine-grained security control.
