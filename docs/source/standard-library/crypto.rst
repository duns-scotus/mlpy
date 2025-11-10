Cryptography (crypto)
=====================

.. module:: crypto
   :synopsis: Basic cryptographic operations (hashing, UUIDs, secure random)

The ``crypto`` module provides basic cryptographic operations including hashing (SHA-256, SHA-1, MD5),
UUID generation, secure random data generation, and HMAC message authentication.

Required Capabilities
--------------------

- ``crypto.hash`` - Cryptographic hashing operations
- ``crypto.random`` - Secure random number generation

.. warning::
   This module provides basic cryptographic primitives. For production systems requiring
   advanced cryptography (encryption, key exchange, digital signatures), use specialized
   cryptographic libraries.

Quick Start
-----------

.. code-block:: ml

   import crypto;

   // Hash data
   password_hash = crypto.sha256("password123");

   // Generate UUID
   user_id = crypto.uuid();

   // Secure random token
   api_token = crypto.random_hex(32);

   // HMAC signature
   signature = crypto.hmac("message", "secret_key");

API Reference
-------------

Hashing Functions
~~~~~~~~~~~~~~~~~

sha256(data, salt)
^^^^^^^^^^^^^^^^^^

Compute SHA-256 cryptographic hash of string.

**Parameters:**

- ``data`` (string) - String to hash
- ``salt`` (string, optional) - Optional salt to prepend (defaults to empty string)

**Returns:** string - Hex-encoded hash (64 characters)

**Capabilities Required:** ``crypto.hash``

**Example:**

.. code-block:: ml

   // Basic hashing
   hash = crypto.sha256("password123");
   console.log(hash);  // 64-character hex string

   // Salted hashing (recommended for passwords)
   salt = crypto.random_hex(16);
   salted_hash = crypto.sha256("password123", salt);

sha1(data, salt)
^^^^^^^^^^^^^^^^

Compute SHA-1 hash of string.

.. note::
   SHA-1 is deprecated for security-critical applications. Use SHA-256 instead.

**Parameters:**

- ``data`` (string) - String to hash
- ``salt`` (string, optional) - Optional salt to prepend

**Returns:** string - Hex-encoded hash (40 characters)

**Capabilities Required:** ``crypto.hash``

**Example:**

.. code-block:: ml

   hash = crypto.sha1("data");
   console.log("SHA-1: " + hash);

md5(data, salt)
^^^^^^^^^^^^^^^

Compute MD5 hash of string.

.. warning::
   MD5 is NOT secure for cryptographic purposes. Use only for checksums and
   non-security applications. For password hashing, use SHA-256.

**Parameters:**

- ``data`` (string) - String to hash
- ``salt`` (string, optional) - Optional salt to prepend

**Returns:** string - Hex-encoded hash (32 characters)

**Capabilities Required:** ``crypto.hash``

**Example:**

.. code-block:: ml

   // Use for checksums, NOT for security
   checksum = crypto.md5("file contents");

hash_file(file_path, algorithm)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hash entire file contents efficiently.

**Parameters:**

- ``file_path`` (string) - Path to file
- ``algorithm`` (string, optional) - Hash algorithm: "sha256", "sha1", "md5" (default: "sha256")

**Returns:** string - Hex-encoded hash

**Capabilities Required:** ``crypto.hash``, ``file.read``

**Example:**

.. code-block:: ml

   import crypto;

   // Hash large file efficiently
   file_hash = crypto.hash_file("document.pdf");
   console.log("File hash: " + file_hash);

   // Verify file integrity
   expected_hash = "abc123...";
   actual_hash = crypto.hash_file("download.zip");
   if (crypto.compare_hash(expected_hash, actual_hash)) {
       console.log("File integrity verified");
   }

UUID Generation
~~~~~~~~~~~~~~~

uuid()
^^^^^^

Generate random UUID version 4.

**Returns:** string - UUID (36 characters with hyphens)

**Capabilities Required:** ``crypto.random``

**Example:**

.. code-block:: ml

   // Generate unique identifiers
   user_id = crypto.uuid();
   session_id = crypto.uuid();
   transaction_id = crypto.uuid();

   console.log(user_id);  // "a7f3d8e2-4b5c-4d9e-8f7a-6b3c2d1e0f9a"

uuid_from_string(data, namespace)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate deterministic UUID version 5 from string.

**Parameters:**

- ``data`` (string) - Input string
- ``namespace`` (string, optional) - UUID namespace (default: DNS namespace)

**Returns:** string - UUID (36 characters with hyphens)

**Capabilities Required:** ``crypto.hash``

**Example:**

.. code-block:: ml

   // Generate deterministic UUIDs
   user_uuid = crypto.uuid_from_string("user@example.com");
   same_uuid = crypto.uuid_from_string("user@example.com");

   // Always produces the same UUID for same input
   console.assert(user_uuid == same_uuid);

Secure Random Generation
~~~~~~~~~~~~~~~~~~~~~~~~~

random_hex(length)
^^^^^^^^^^^^^^^^^^

Generate cryptographically secure random hex string.

**Parameters:**

- ``length`` (integer) - Number of random bytes (output will be 2x characters)

**Returns:** string - Hex-encoded random string

**Capabilities Required:** ``crypto.random``

**Example:**

.. code-block:: ml

   // Generate API tokens
   api_token = crypto.random_hex(32);  // 64-character hex string
   session_token = crypto.random_hex(16);  // 32-character hex string

   console.log("Token: " + api_token);

random_string(length)
^^^^^^^^^^^^^^^^^^^^^

Generate cryptographically secure random alphanumeric string [A-Za-z0-9].

**Parameters:**

- ``length`` (integer) - Number of characters

**Returns:** string - Random alphanumeric string

**Capabilities Required:** ``crypto.random``

**Example:**

.. code-block:: ml

   // Generate passwords
   temp_password = crypto.random_string(12);
   verification_code = crypto.random_string(6);

   console.log("Temp password: " + temp_password);

random_int(min_val, max_val)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate cryptographically secure random integer in range [min, max] (inclusive).

**Parameters:**

- ``min_val`` (integer) - Minimum value (inclusive)
- ``max_val`` (integer) - Maximum value (inclusive)

**Returns:** integer - Random integer in range

**Capabilities Required:** ``crypto.random``

**Example:**

.. code-block:: ml

   // Random selection
   dice_roll = crypto.random_int(1, 6);
   random_index = crypto.random_int(0, len(array) - 1);

   // Cryptographically secure random sampling
   random_user = users[crypto.random_int(0, len(users) - 1)];

random_float()
^^^^^^^^^^^^^^

Generate cryptographically secure random float in [0.0, 1.0).

**Returns:** float - Random float between 0.0 and 1.0

**Capabilities Required:** ``crypto.random``

**Example:**

.. code-block:: ml

   // Random probability
   rand = crypto.random_float();
   if (rand < 0.1) {
       console.log("10% chance event occurred");
   }

   // Weighted selection
   threshold = 0.7;
   if (crypto.random_float() < threshold) {
       select_option_a();
   } else {
       select_option_b();
   }

random_bytes(length)
^^^^^^^^^^^^^^^^^^^^

Generate cryptographically secure random bytes.

**Parameters:**

- ``length`` (integer) - Number of bytes to generate

**Returns:** bytes - Random bytes

**Capabilities Required:** ``crypto.random``

**Example:**

.. code-block:: ml

   // Generate encryption keys (example only)
   key_material = crypto.random_bytes(32);

HMAC Message Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

hmac(message, key, algorithm)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate HMAC signature for message authentication.

**Parameters:**

- ``message`` (string) - Message to sign
- ``key`` (string) - Secret key
- ``algorithm`` (string, optional) - Hash algorithm: "sha256", "sha1", "md5" (default: "sha256")

**Returns:** string - Hex-encoded HMAC signature

**Capabilities Required:** ``crypto.hash``

**Example:**

.. code-block:: ml

   import crypto;

   // Sign message
   message = "user_id=123&amount=100";
   secret_key = "server_secret_key";
   signature = crypto.hmac(message, secret_key);

   // Send message with signature
   send_api_request(message, signature);

verify_hmac(message, signature, key, algorithm)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Verify HMAC signature (timing-attack resistant).

**Parameters:**

- ``message`` (string) - Original message
- ``signature`` (string) - HMAC signature to verify
- ``key`` (string) - Secret key
- ``algorithm`` (string, optional) - Hash algorithm (default: "sha256")

**Returns:** boolean - True if signature is valid

**Capabilities Required:** ``crypto.hash``

**Example:**

.. code-block:: ml

   import crypto;

   // Verify received signature
   received_message = "user_id=123&amount=100";
   received_signature = "abc123...";
   secret_key = "server_secret_key";

   if (crypto.verify_hmac(received_message, received_signature, secret_key)) {
       console.log("Signature valid - message authenticated");
       process_request(received_message);
   } else {
       console.log("Invalid signature - possible tampering");
   }

compare_hash(hash1, hash2)
^^^^^^^^^^^^^^^^^^^^^^^^^^

Compare two hashes using timing-attack resistant comparison.

**Parameters:**

- ``hash1`` (string) - First hash
- ``hash2`` (string) - Second hash

**Returns:** boolean - True if hashes match

**Capabilities Required:** ``crypto.hash``

**Example:**

.. code-block:: ml

   import crypto;

   // Verify password
   stored_hash = get_user_password_hash(user_id);
   input_hash = crypto.sha256(input_password, stored_salt);

   if (crypto.compare_hash(stored_hash, input_hash)) {
       console.log("Password correct");
       login_user();
   } else {
       console.log("Password incorrect");
   }

Common Patterns
---------------

Password Hashing
~~~~~~~~~~~~~~~~

.. warning::
   For production password hashing, use bcrypt, scrypt, or Argon2. This is a basic example.

.. code-block:: ml

   import crypto;

   function hash_password(password) {
       // Generate random salt
       salt = crypto.random_hex(16);

       // Hash password with salt
       hash = crypto.sha256(password, salt);

       // Return both (store both in database)
       return {salt: salt, hash: hash};
   }

   function verify_password(password, stored_salt, stored_hash) {
       // Hash input with stored salt
       input_hash = crypto.sha256(password, stored_salt);

       // Compare using timing-resistant comparison
       return crypto.compare_hash(stored_hash, input_hash);
   }

   // Usage
   credentials = hash_password("user_password_123");
   console.log("Salt: " + credentials.salt);
   console.log("Hash: " + credentials.hash);

   // Later, verify password
   is_valid = verify_password("user_password_123", credentials.salt, credentials.hash);

API Token Generation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;

   function generate_api_token(user_id) {
       // Generate unique token
       token = crypto.random_hex(32);

       // Create token ID
       token_id = crypto.uuid();

       // Generate creation timestamp-based verification
       timestamp = str(datetime.now().timestamp());
       verification = crypto.hmac(token + timestamp, "server_secret");

       return {
           id: token_id,
           token: token,
           user_id: user_id,
           created: timestamp,
           verification: verification
       };
   }

   // Usage
   api_token = generate_api_token(123);
   console.log("API Token: " + api_token.token);
   console.log("Token ID: " + api_token.id);

File Integrity Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;
   import file;

   function verify_file_integrity(file_path, expected_hash) {
       // Compute file hash
       actual_hash = crypto.hash_file(file_path);

       // Compare hashes
       if (crypto.compare_hash(expected_hash, actual_hash)) {
           console.log("File integrity verified");
           return true;
       } else {
           console.error("File corrupted or tampered!");
           return false;
       }
   }

   // Usage - verify downloaded file
   downloaded_file = "package.zip";
   published_hash = "abc123...";  // From official website

   if (verify_file_integrity(downloaded_file, published_hash)) {
       // Safe to use file
       extract_package(downloaded_file);
   }

Secure Session Management
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;
   import datetime;

   function create_session(user_id) {
       // Generate session ID
       session_id = crypto.uuid();

       // Generate session token
       session_token = crypto.random_hex(32);

       // Create expiration
       expires = datetime.now().add_hours(24);

       // Sign session data
       session_data = session_id + "|" + str(user_id) + "|" + str(expires.timestamp());
       signature = crypto.hmac(session_data, "session_secret");

       return {
           id: session_id,
           token: session_token,
           user_id: user_id,
           expires: expires,
           signature: signature
       };
   }

   function validate_session(session) {
       // Verify signature
       session_data = session.id + "|" + str(session.user_id) + "|" + str(session.expires.timestamp());
       is_valid = crypto.verify_hmac(session_data, session.signature, "session_secret");

       if (!is_valid) {
           console.error("Invalid session signature");
           return false;
       }

       // Check expiration
       if (datetime.now() > session.expires) {
           console.log("Session expired");
           return false;
       }

       return true;
   }

Deterministic ID Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;

   // Generate consistent IDs from email addresses
   function get_user_id(email) {
       return crypto.uuid_from_string(email);
   }

   // Same email always produces same ID
   id1 = get_user_id("alice@example.com");
   id2 = get_user_id("alice@example.com");
   console.assert(id1 == id2);

   // Different emails produce different IDs
   id3 = get_user_id("bob@example.com");
   console.assert(id1 != id3);

Security Considerations
-----------------------

Password Hashing Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::
   The SHA-256 examples shown here are for educational purposes. For production
   password hashing, use purpose-built password hashing algorithms:

   - **bcrypt** - Industry standard, well-tested
   - **scrypt** - Memory-hard, resistant to hardware attacks
   - **Argon2** - Winner of Password Hashing Competition

Basic password hashing with SHA-256:

.. code-block:: ml

   import crypto;

   // ❌ BAD - No salt (vulnerable to rainbow tables)
   bad_hash = crypto.sha256("password123");

   // ✅ GOOD - With random salt
   salt = crypto.random_hex(16);
   good_hash = crypto.sha256("password123", salt);
   // Store both salt and hash

   // ✅ BETTER - Use dedicated password hashing (not in basic crypto module)
   // Use bcrypt/scrypt/Argon2 for production

Secure Random vs Regular Random
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Always use ``crypto`` module for security-critical random generation:

.. code-block:: ml

   import crypto;
   import random;

   // ❌ BAD - NOT cryptographically secure
   bad_token = random.random_string(32);

   // ✅ GOOD - Cryptographically secure
   good_token = crypto.random_string(32);

   // ❌ BAD - Predictable
   bad_dice = random.randint(1, 6);

   // ✅ GOOD - Unpredictable
   good_dice = crypto.random_int(1, 6);

Token Storage
~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;
   import env;

   // ❌ BAD - Storing tokens in code
   api_secret = "hardcoded_secret_123";

   // ✅ GOOD - Load from environment
   api_secret = env.require("API_SECRET");

   // ✅ GOOD - Generate and store securely
   new_secret = crypto.random_hex(32);
   env.set("API_SECRET", new_secret);  // Store in secure vault

Timing Attacks
~~~~~~~~~~~~~~

Always use timing-resistant comparison for security-critical checks:

.. code-block:: ml

   import crypto;

   stored_hash = "abc123...";
   input_hash = crypto.sha256(user_input);

   // ❌ BAD - Vulnerable to timing attacks
   if (stored_hash == input_hash) {
       // Timing reveals information
   }

   // ✅ GOOD - Timing-attack resistant
   if (crypto.compare_hash(stored_hash, input_hash)) {
       // Safe comparison
   }

Hash Algorithm Selection
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;

   // ✅ RECOMMENDED - SHA-256 for security
   secure_hash = crypto.sha256("sensitive_data");

   // ⚠️ ACCEPTABLE - SHA-1 for non-security uses
   legacy_hash = crypto.sha1("data");

   // ❌ NOT SECURE - MD5 only for checksums
   checksum = crypto.md5("file_contents");

Integration with Other Modules
-------------------------------

With Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;
   import env;

   // Load secret from environment
   hmac_secret = env.require("HMAC_SECRET");

   // Use for signing
   signature = crypto.hmac("message", hmac_secret);

With HTTP Requests
~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;
   import http;
   import env;

   api_key = env.require("API_KEY");
   api_secret = env.require("API_SECRET");

   // Create request signature
   timestamp = str(datetime.now().timestamp());
   message = "POST" + "/api/users" + timestamp;
   signature = crypto.hmac(message, api_secret);

   headers = {
       "X-API-Key": api_key,
       "X-Signature": signature,
       "X-Timestamp": timestamp
   };

   response = http.post("https://api.example.com/users", {}, headers);

With File Operations
~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;
   import file;
   import json;

   // Verify downloaded file
   download_url = "https://example.com/package.zip";
   checksums_url = "https://example.com/checksums.json";

   // Download checksums
   checksums = json.parse(http.get(checksums_url).body);
   expected_hash = checksums["package.zip"];

   // Download and verify file
   file.download(download_url, "package.zip");
   actual_hash = crypto.hash_file("package.zip");

   if (crypto.compare_hash(expected_hash, actual_hash)) {
       console.log("File verified successfully");
   } else {
       console.error("Checksum mismatch!");
       file.delete("package.zip");
   }

With Database Operations
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;

   function create_user(username, password) {
       // Generate user ID
       user_id = crypto.uuid();

       // Hash password
       salt = crypto.random_hex(16);
       password_hash = crypto.sha256(password, salt);

       // Create user record
       user = {
           id: user_id,
           username: username,
           password_hash: password_hash,
           password_salt: salt,
           api_key: crypto.random_hex(32),
           created_at: datetime.now()
       };

       // Save to database
       db.insert("users", user);

       return user_id;
   }

Performance Considerations
--------------------------

Hashing Performance
~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;

   // Fast - in-memory hashing
   hash = crypto.sha256("data");  // < 1ms

   // Slower - file hashing (depends on file size)
   file_hash = crypto.hash_file("large_file.zip");  // 10-100ms for MB files

   // For large files, consider async processing or progress indicators

Random Generation Performance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;

   // Very fast - < 1ms
   uuid = crypto.uuid();
   token = crypto.random_hex(32);
   number = crypto.random_int(1, 100);

   // Batch generation is efficient
   tokens = [];
   for (i = 0; i < 1000; i = i + 1) {
       tokens.append(crypto.random_hex(16));
   }

Caching Considerations
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;

   // ❌ BAD - Hashing in hot loop
   for (item in large_array) {
       hash = crypto.sha256(item);  // Expensive
       process(hash);
   }

   // ✅ GOOD - Hash once, reuse
   hashes = {};
   for (item in large_array) {
       if (!hashes[item]) {
           hashes[item] = crypto.sha256(item);
       }
       process(hashes[item]);
   }

Error Handling
--------------

File Hashing Errors
~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;
   import file;

   try {
       hash = crypto.hash_file("document.pdf");
       console.log("Hash: " + hash);
   } except (error) {
       console.error("Failed to hash file: " + str(error));
       // Handle missing file or permission error
   }

Invalid Algorithm
~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;

   try {
       // Invalid algorithm name
       hash = crypto.hash_file("file.txt", "invalid_algo");
   } except (error) {
       console.error("Unsupported algorithm");
       // Fall back to default
       hash = crypto.hash_file("file.txt");
   }

See Also
--------

- :doc:`env` - Environment variables (for storing secrets)
- :doc:`file` - File operations (for hash_file)
- :doc:`http` - HTTP client (for API authentication)
- :doc:`random` - Non-cryptographic random (for non-security uses)

Examples
--------

Complete Authentication System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;
   import env;
   import datetime;

   secret_key = env.require("AUTH_SECRET");

   function register_user(username, password, email) {
       // Generate IDs
       user_id = crypto.uuid_from_string(email);
       api_key = crypto.random_hex(32);

       // Hash password
       salt = crypto.random_hex(16);
       password_hash = crypto.sha256(password, salt);

       // Create user
       user = {
           id: user_id,
           username: username,
           email: email,
           password_hash: password_hash,
           password_salt: salt,
           api_key: api_key,
           created_at: datetime.now()
       };

       return user;
   }

   function authenticate_user(username, password, stored_user) {
       // Hash input password with stored salt
       input_hash = crypto.sha256(password, stored_user.password_salt);

       // Timing-resistant comparison
       if (!crypto.compare_hash(stored_user.password_hash, input_hash)) {
           return null;
       }

       // Generate session token
       session_token = crypto.random_hex(32);
       session_data = stored_user.id + "|" + str(datetime.now().timestamp());
       session_signature = crypto.hmac(session_data, secret_key);

       return {
           token: session_token,
           signature: session_signature,
           user_id: stored_user.id
       };
   }

   // Usage
   new_user = register_user("alice", "secure_pass_123", "alice@example.com");
   console.log("User registered: " + new_user.id);

   session = authenticate_user("alice", "secure_pass_123", new_user);
   if (session) {
       console.log("Login successful");
       console.log("Session token: " + session.token);
   }

API Request Signing
~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import crypto;
   import http;
   import json;
   import datetime;

   function sign_api_request(method, path, body, api_key, api_secret) {
       // Create canonical request
       timestamp = str(datetime.now().timestamp());
       body_json = json.stringify(body);
       canonical = method + "\n" + path + "\n" + timestamp + "\n" + body_json;

       // Generate signature
       signature = crypto.hmac(canonical, api_secret);

       // Create headers
       headers = {
           "X-API-Key": api_key,
           "X-Timestamp": timestamp,
           "X-Signature": signature,
           "Content-Type": "application/json"
       };

       return headers;
   }

   // Usage
   api_key = env.require("API_KEY");
   api_secret = env.require("API_SECRET");

   request_body = {user_id: 123, action: "create"};
   headers = sign_api_request("POST", "/api/users", request_body, api_key, api_secret);

   response = http.post("https://api.example.com/users", request_body, headers);
