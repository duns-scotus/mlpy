# ML Standard Library: SQLite3 Database Support

**Document Type:** Technical Design & Implementation Roadmap
**Status:** Ready for Implementation
**Created:** 2025-11-10
**Authors:** mlpy Development Team

---

## Executive Summary

### Overview

**Current State:** ML has file I/O and JSON support but no database capabilities
**Gap:** No way to store structured data, query efficiently, or maintain data integrity
**Target State:** Production-ready SQLite3 support with security-first design
**Feasibility:** ✅ **HIGHLY FEASIBLE** - Python's sqlite3 module is robust and well-tested

### Why SQLite3?

**Perfect for ML Programs:**
- ✅ **Zero Configuration** - No server setup, just a file
- ✅ **Embedded Database** - Runs in-process, no network overhead
- ✅ **Single File** - Easy to backup, version, distribute
- ✅ **ACID Compliance** - Full transaction support
- ✅ **Production Ready** - Used by iOS, Android, browsers, millions of apps
- ✅ **SQL Standard** - Industry-standard query language
- ✅ **Small Footprint** - ~600KB library, minimal overhead

**Common Use Cases:**
- Data-driven applications (analytics, reporting)
- Configuration storage (beyond simple key-value)
- Local caching and offline-first apps
- Testing (mock production databases)
- Educational projects (learn SQL in ML)
- Embedded systems and IoT devices

### Key Features

**Core Functionality:**
- Database creation and connection management
- Execute SQL queries (SELECT, INSERT, UPDATE, DELETE)
- Parameterized queries (SQL injection prevention)
- Transaction support (BEGIN, COMMIT, ROLLBACK)
- Schema management (CREATE TABLE, ALTER TABLE)
- Type conversion (ML ↔ SQLite)
- Connection pooling (performance)
- Error handling with meaningful messages

**Security:**
- Capability-based access control
- SQL injection prevention (parameterized queries only)
- Path validation (prevent directory traversal)
- Resource limits (max connections, query timeout)
- Read-only mode option

### Effort Estimate

| Component | Complexity | Effort | Priority |
|-----------|-----------|--------|----------|
| **Core API** | Medium | 2 days | 🔴 Critical |
| **Connection Pool** | Medium | 1 day | 🟡 High |
| **Transaction Support** | Low | 0.5 days | 🔴 Critical |
| **Type Conversion** | Low | 0.5 days | 🔴 Critical |
| **Error Handling** | Low | 0.5 days | 🔴 Critical |
| **Testing** | Medium | 1 day | 🔴 Critical |
| **Documentation** | Low | 0.5 days | 🟡 High |

**Total:** 5-6 days for complete, production-ready implementation

### Recommendation

**✅ PROCEED** with implementation as high-priority standard library module

---

## Table of Contents

1. [API Design](#api-design)
2. [Python Implementation](#python-implementation)
3. [Security Considerations](#security-considerations)
4. [Type Conversion System](#type-conversion-system)
5. [Connection Management](#connection-management)
6. [Transaction Support](#transaction-support)
7. [Error Handling](#error-handling)
8. [Testing Strategy](#testing-strategy)
9. [Integration Examples](#integration-examples)
10. [Performance Considerations](#performance-considerations)
11. [Migration from Other Databases](#migration-from-other-databases)

---

## API Design

### Basic Operations

```ml
import sqlite;

// Open/create database
db = sqlite.connect("myapp.db");

// Create table
db.execute("
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
");

// Insert data (parameterized - safe from SQL injection)
db.execute(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    ["Alice", "alice@example.com", 30]
);

// Query data (returns array of objects)
users = db.query("SELECT * FROM users WHERE age > ?", [25]);
// [
//   {id: 1, name: "Alice", email: "alice@example.com", age: 30, created_at: "2025-11-10 14:30:00"},
//   {id: 2, name: "Bob", email: "bob@example.com", age: 28, created_at: "2025-11-10 14:31:00"}
// ]

// Query single row
user = db.query_one("SELECT * FROM users WHERE id = ?", [1]);
// {id: 1, name: "Alice", email: "alice@example.com", age: 30, created_at: "2025-11-10 14:30:00"}

// Query single value
count = db.query_scalar("SELECT COUNT(*) FROM users");
// 2

// Update data
db.execute("UPDATE users SET age = ? WHERE id = ?", [31, 1]);

// Delete data
db.execute("DELETE FROM users WHERE id = ?", [1]);

// Close connection
db.close();
```

### Transaction Support

```ml
import sqlite;

db = sqlite.connect("store.db");

// Automatic transaction (recommended)
try {
    db.begin_transaction();

    // Multiple operations in transaction
    db.execute("INSERT INTO orders (customer_id, total) VALUES (?, ?)", [123, 99.99]);
    order_id = db.last_insert_id();

    db.execute("INSERT INTO order_items (order_id, product_id, qty) VALUES (?, ?, ?)",
               [order_id, 456, 2]);
    db.execute("UPDATE inventory SET quantity = quantity - ? WHERE id = ?", [2, 456]);

    db.commit();
    console.log("Order placed successfully");

} except (error) {
    db.rollback();
    console.log("Order failed, rolling back: " + error.message);
}

// Alternative: Manual transaction control
db.execute("BEGIN TRANSACTION");
db.execute("INSERT INTO users (name) VALUES (?)", ["Test"]);
db.execute("COMMIT");
```

### Batch Operations

```ml
import sqlite;

db = sqlite.connect("data.db");

// Insert many rows efficiently
users = [
    ["Alice", "alice@example.com"],
    ["Bob", "bob@example.com"],
    ["Charlie", "charlie@example.com"]
];

db.execute_many("INSERT INTO users (name, email) VALUES (?, ?)", users);
console.log("Inserted " + str(len(users)) + " users");

// Batch queries (returns iterator for large datasets)
for (row in db.query_iter("SELECT * FROM large_table")) {
    process(row);
    // Processes one row at a time, memory-efficient
}
```

### Schema Management

```ml
import sqlite;

db = sqlite.connect("myapp.db");

// Check if table exists
if (!db.table_exists("users")) {
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)");
}

// Get table info
columns = db.get_table_info("users");
// [
//   {name: "id", type: "INTEGER", notnull: 0, dflt_value: null, pk: 1},
//   {name: "name", type: "TEXT", notnull: 0, dflt_value: null, pk: 0}
// ]

// List all tables
tables = db.list_tables();
// ["users", "orders", "products"]

// Check if column exists
if (!db.column_exists("users", "email")) {
    db.execute("ALTER TABLE users ADD COLUMN email TEXT");
}

// Drop table
db.execute("DROP TABLE IF EXISTS temp_data");
```

### Connection Options

```ml
import sqlite;

// Basic connection
db = sqlite.connect("app.db");

// Read-only mode (security)
db = sqlite.connect("app.db", readonly=true);

// In-memory database (testing, caching)
db = sqlite.connect(":memory:");

// Custom timeout (default 5 seconds)
db = sqlite.connect("app.db", timeout=10.0);

// Enable foreign keys (not enabled by default in SQLite)
db = sqlite.connect("app.db", foreign_keys=true);

// Custom connection string
db = sqlite.connect("file:data.db?mode=ro&cache=shared");
```

### Advanced Features

```ml
import sqlite;

db = sqlite.connect("app.db");

// Get last inserted ID
db.execute("INSERT INTO users (name) VALUES (?)", ["Alice"]);
user_id = db.last_insert_id();

// Get number of affected rows
db.execute("UPDATE users SET active = 1 WHERE age > ?", [18]);
affected = db.affected_rows();
console.log("Updated " + str(affected) + " rows");

// Check if query would return results (efficient)
exists = db.exists("SELECT 1 FROM users WHERE email = ?", ["test@example.com"]);

// Vacuum database (reclaim space)
db.execute("VACUUM");

// Enable Write-Ahead Logging (better concurrency)
db.execute("PRAGMA journal_mode=WAL");

// Get database size
size = db.get_size();
console.log("Database size: " + str(size) + " bytes");
```

### Connection Pooling

```ml
import sqlite;

// Create connection pool (shared across requests)
pool = sqlite.create_pool("app.db", max_connections=5);

// Get connection from pool
db = pool.get_connection();

// Use connection
users = db.query("SELECT * FROM users");

// Return to pool (automatic if used with 'with' syntax - future feature)
pool.release_connection(db);

// Alternative: Callback pattern
pool.with_connection(fn(db) => {
    users = db.query("SELECT * FROM users");
    return users;
});

// Close all connections in pool
pool.close_all();
```

---

## Python Implementation

### Core Database Class

```python
"""SQLite3 database support for ML."""

import sqlite3
import threading
from pathlib import Path
from typing import Any, Optional, Union, Iterator
from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_class
class Database:
    """SQLite database connection wrapper."""

    def __init__(
        self,
        database: str,
        readonly: bool = False,
        timeout: float = 5.0,
        foreign_keys: bool = False,
    ):
        """Initialize database connection.

        Args:
            database: Database file path or ":memory:"
            readonly: Open in read-only mode
            timeout: Connection timeout in seconds
            foreign_keys: Enable foreign key constraints
        """
        self.database = database
        self.readonly = readonly
        self.timeout = timeout
        self.foreign_keys = foreign_keys
        self._connection = None
        self._connect()

    def _connect(self):
        """Establish database connection."""
        if self.readonly:
            # Read-only mode
            uri = f"file:{self.database}?mode=ro"
            self._connection = sqlite3.connect(uri, uri=True, timeout=self.timeout)
        else:
            self._connection = sqlite3.connect(
                self.database,
                timeout=self.timeout,
                check_same_thread=False  # Allow multi-threaded access
            )

        # Enable dictionary cursor (column names in results)
        self._connection.row_factory = sqlite3.Row

        # Enable foreign keys if requested
        if self.foreign_keys:
            self._connection.execute("PRAGMA foreign_keys = ON")

    def execute(self, sql: str, params: Optional[list] = None) -> int:
        """Execute SQL statement (requires db.write capability).

        Args:
            sql: SQL statement
            params: Query parameters (prevents SQL injection)

        Returns:
            Number of affected rows

        Raises:
            sqlite3.Error: If query fails
            PermissionError: If db.write capability missing

        Note: This method should be decorated with @ml_function when exposed to ML:
            @ml_function(capabilities=["db.write"])
        """
        params = params or []
        cursor = self._connection.execute(sql, params)
        self._connection.commit()
        return cursor.rowcount

    def execute_many(self, sql: str, params_list: list[list]) -> int:
        """Execute SQL statement with multiple parameter sets.

        Args:
            sql: SQL statement
            params_list: List of parameter lists

        Returns:
            Total number of affected rows
        """
        cursor = self._connection.executemany(sql, params_list)
        self._connection.commit()
        return cursor.rowcount

    def query(self, sql: str, params: Optional[list] = None) -> list[dict]:
        """Execute query and return all results (requires db.read capability).

        Args:
            sql: SQL query
            params: Query parameters

        Returns:
            List of dictionaries (one per row)

        Raises:
            PermissionError: If db.read capability missing

        Note: This method should be decorated with @ml_function when exposed to ML:
            @ml_function(capabilities=["db.read"])
        """
        params = params or []
        cursor = self._connection.execute(sql, params)
        rows = cursor.fetchall()

        # Convert Row objects to dictionaries
        return [dict(row) for row in rows]

    def query_one(self, sql: str, params: Optional[list] = None) -> Optional[dict]:
        """Execute query and return first result.

        Args:
            sql: SQL query
            params: Query parameters

        Returns:
            Dictionary or None if no results
        """
        params = params or []
        cursor = self._connection.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def query_scalar(self, sql: str, params: Optional[list] = None) -> Any:
        """Execute query and return single value.

        Args:
            sql: SQL query
            params: Query parameters

        Returns:
            First column of first row, or None
        """
        params = params or []
        cursor = self._connection.execute(sql, params)
        row = cursor.fetchone()
        return row[0] if row else None

    def query_iter(self, sql: str, params: Optional[list] = None) -> Iterator[dict]:
        """Execute query and return iterator (memory efficient).

        Args:
            sql: SQL query
            params: Query parameters

        Yields:
            Dictionary for each row
        """
        params = params or []
        cursor = self._connection.execute(sql, params)

        for row in cursor:
            yield dict(row)

    def begin_transaction(self):
        """Begin transaction."""
        self._connection.execute("BEGIN TRANSACTION")

    def commit(self):
        """Commit transaction."""
        self._connection.commit()

    def rollback(self):
        """Rollback transaction."""
        self._connection.rollback()

    def last_insert_id(self) -> int:
        """Get last inserted row ID."""
        return self._connection.execute("SELECT last_insert_rowid()").fetchone()[0]

    def affected_rows(self) -> int:
        """Get number of rows affected by last operation."""
        return self._connection.total_changes

    def exists(self, sql: str, params: Optional[list] = None) -> bool:
        """Check if query returns any results.

        Args:
            sql: SQL query (should use SELECT 1 for efficiency)
            params: Query parameters

        Returns:
            True if results exist
        """
        result = self.query_one(sql, params)
        return result is not None

    def table_exists(self, table_name: str) -> bool:
        """Check if table exists."""
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        return self.exists(sql, [table_name])

    def column_exists(self, table_name: str, column_name: str) -> bool:
        """Check if column exists in table."""
        info = self.get_table_info(table_name)
        return any(col['name'] == column_name for col in info)

    def list_tables(self) -> list[str]:
        """List all tables in database."""
        sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        results = self.query(sql)
        return [row['name'] for row in results]

    def get_table_info(self, table_name: str) -> list[dict]:
        """Get table schema information.

        Returns:
            List of column info dictionaries
        """
        sql = f"PRAGMA table_info({table_name})"
        return self.query(sql)

    def get_size(self) -> int:
        """Get database file size in bytes."""
        if self.database == ":memory:":
            return 0

        try:
            return Path(self.database).stat().st_size
        except:
            return 0

    def close(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if exc_type:
            self.rollback()
        self.close()


@ml_class
class ConnectionPool:
    """Connection pool for database connections."""

    def __init__(
        self,
        database: str,
        max_connections: int = 5,
        readonly: bool = False,
        timeout: float = 5.0,
    ):
        """Initialize connection pool.

        Args:
            database: Database file path
            max_connections: Maximum connections in pool
            readonly: Open connections in read-only mode
            timeout: Connection timeout
        """
        self.database = database
        self.max_connections = max_connections
        self.readonly = readonly
        self.timeout = timeout

        self._pool: list[Database] = []
        self._in_use: set[Database] = set()
        self._lock = threading.Lock()

    def get_connection(self) -> Database:
        """Get connection from pool.

        Returns:
            Database connection

        Raises:
            RuntimeError: If pool is exhausted
        """
        with self._lock:
            # Try to reuse existing connection
            if self._pool:
                conn = self._pool.pop()
                self._in_use.add(conn)
                return conn

            # Create new connection if under limit
            if len(self._in_use) < self.max_connections:
                conn = Database(
                    self.database,
                    readonly=self.readonly,
                    timeout=self.timeout
                )
                self._in_use.add(conn)
                return conn

            raise RuntimeError(f"Connection pool exhausted (max: {self.max_connections})")

    def release_connection(self, conn: Database):
        """Return connection to pool."""
        with self._lock:
            if conn in self._in_use:
                self._in_use.remove(conn)
                self._pool.append(conn)

    def with_connection(self, callback):
        """Execute callback with connection from pool.

        Args:
            callback: Function that takes Database as argument

        Returns:
            Result of callback
        """
        conn = self.get_connection()
        try:
            return callback(conn)
        finally:
            self.release_connection(conn)

    def close_all(self):
        """Close all connections in pool."""
        with self._lock:
            for conn in self._pool:
                conn.close()
            for conn in self._in_use:
                conn.close()

            self._pool.clear()
            self._in_use.clear()


@ml_module(
    name="sqlite",
    description="SQLite3 database support with security and connection pooling",
    capabilities=["db.read", "db.write", "file.read", "file.write"],
    version="1.0.0"
)
class SQLite:
    """SQLite database operations."""

    @ml_function(
        description="Connect to SQLite database",
        capabilities=["file.read"]  # Only file access for opening
    )
    def connect(
        self,
        database: str,
        readonly: bool = False,
        timeout: float = 5.0,
        foreign_keys: bool = False
    ) -> Database:
        """Connect to SQLite database.

        Args:
            database: Database file path or ":memory:"
            readonly: Open in read-only mode
            timeout: Connection timeout in seconds
            foreign_keys: Enable foreign key constraints

        Returns:
            Database connection object

        Example:
            ```ml
            db = sqlite.connect("app.db");
            users = db.query("SELECT * FROM users");
            db.close();
            ```
        """
        return Database(database, readonly, timeout, foreign_keys)

    @ml_function(
        description="Create connection pool",
        capabilities=["file.read"]  # File access only for pool creation
    )
    def create_pool(
        self,
        database: str,
        max_connections: int = 5,
        readonly: bool = False,
        timeout: float = 5.0
    ) -> ConnectionPool:
        """Create connection pool for database.

        Args:
            database: Database file path
            max_connections: Maximum connections in pool
            readonly: Open in read-only mode
            timeout: Connection timeout

        Returns:
            Connection pool object

        Example:
            ```ml
            pool = sqlite.create_pool("app.db", max_connections=10);
            db = pool.get_connection();
            // ... use db ...
            pool.release_connection(db);
            ```
        """
        return ConnectionPool(database, max_connections, readonly, timeout)
```

### File Structure

```
src/mlpy/stdlib/
├── sqlite_bridge.py           # Main module implementation
└── tests/
    └── test_sqlite_bridge.py  # Comprehensive unit tests
```

---

## Security Considerations

### Capability Requirements (Two-Layer Model)

**Layer 1: File Access (Reuses Existing Capabilities)**
- `file.read` - Open/read database files
- `file.write` - Create/modify database files

**Layer 2: Database Operations (New Capabilities)**
- `db.read` - Execute SELECT queries
- `db.write` - Execute INSERT/UPDATE/DELETE/CREATE/DROP queries

**Why Two Layers?**

This separation allows fine-grained control:

```ml
// Example 1: Read-only access to specific database
// Requires: file.read:/data/reports.db + db.read
db = sqlite.connect("/data/reports.db", readonly=true);
data = db.query("SELECT * FROM sales");  // ✅ Allowed

// Example 2: Read database, but can't write
// Requires: file.read:/data/app.db + file.write:/data/app.db + db.read
db = sqlite.connect("/data/app.db");     // ✅ Can open
users = db.query("SELECT * FROM users"); // ✅ Can read
db.execute("DELETE FROM users");         // ❌ Blocked (needs db.write)

// Example 3: Full access
// Requires: file.read:/data/app.db + file.write:/data/app.db + db.read + db.write
db = sqlite.connect("/data/app.db");
db.execute("INSERT INTO users VALUES (?, ?)", ["Alice", 30]);  // ✅ Allowed
```

**Risk Assessment:**

| Operation | Capabilities Required | Risk Level | Mitigation |
|-----------|---------------------|-----------|-----------|
| **Open database** | `file.read` | 🟡 Medium | Path validation |
| **Create database** | `file.write` | 🟡 Medium | Path validation |
| **SELECT queries** | `db.read` | 🟢 Low | Read-only, no side effects |
| **INSERT/UPDATE/DELETE** | `db.write` | 🟡 Medium | Can modify data |
| **CREATE/DROP TABLE** | `db.write` | 🟡 Medium | Schema changes |
| **VACUUM/ANALYZE** | `db.write` | 🟢 Low | Optimization only |
| **SQL Injection** | N/A | 🔴 High | Parameterized queries ONLY |

### SQL Injection Prevention

**CRITICAL: All queries MUST use parameterized queries.**

**Safe (✅):**
```ml
// Parameterized query - SAFE
user_id = 123;
user = db.query_one("SELECT * FROM users WHERE id = ?", [user_id]);

// Multiple parameters - SAFE
name = "Alice";
age = 30;
db.execute("INSERT INTO users (name, age) VALUES (?, ?)", [name, age]);
```

**UNSAFE (❌ - NEVER DO THIS):**
```ml
// String concatenation - VULNERABLE TO SQL INJECTION
user_id = 123;
user = db.query_one("SELECT * FROM users WHERE id = " + str(user_id));  // DANGEROUS!

// String interpolation - VULNERABLE
name = "Alice";
db.execute("INSERT INTO users (name) VALUES ('" + name + "')");  // DANGEROUS!
```

**Implementation Enforcement:**
- `execute()` and `query()` methods REQUIRE params argument
- No string concatenation allowed in SQL
- Validation in bridge code (reject queries with user data in SQL string)
- Clear error messages when unsafe patterns detected

### Path Validation

**Database File Path Security (Enforced by file.read/file.write):**

Path validation is handled by the existing file capability system:

```python
@ml_function(capabilities=["file.read"])
def connect(self, database: str, readonly: bool = False, ...):
    """Connect to database with path validation via file.read capability."""

    # Allow in-memory databases (no file access needed)
    if database == ":memory:":
        return Database(database, readonly, ...)

    # File capability system handles path validation
    # If context has capability: CapabilityToken("file.read", ["*.db"])
    # Then only *.db files are accessible

    # Additional validation (belt and suspenders)
    path = Path(database).resolve()

    # Prevent directory traversal
    if ".." in str(path):
        raise SecurityError("Path traversal not allowed")

    # The actual file access check happens when opening the file
    # If file.read capability doesn't cover this path, connection fails
    return Database(str(path), readonly, ...)
```

**How File Capabilities Control Database Access:**

```python
# Example 1: Restrict to specific database
token = create_capability_token("file.read", resource_patterns=["/data/app.db"])
# Can only open /data/app.db

# Example 2: Restrict to directory
token = create_capability_token("file.read", resource_patterns=["/data/*.db"])
# Can open any .db file in /data/

# Example 3: Read-only access
read_token = create_capability_token("file.read", resource_patterns=["*.db"])
# Has file.read but NOT file.write
# Can open database but db.execute() will fail (needs file.write for modifications)
```

### Read-Only Mode

**Use read-only mode for untrusted queries:**

```ml
// Open in read-only mode
db = sqlite.connect("production.db", readonly=true);

// All writes will fail
try {
    db.execute("DELETE FROM users");  // Throws error
} except (error) {
    console.log("Write blocked: " + error.message);
}

// Reads work fine
users = db.query("SELECT * FROM users");
```

### Resource Limits

**Prevent resource exhaustion:**

```python
class Database:
    # Query timeout (prevent infinite queries)
    MAX_QUERY_TIME = 30.0  # seconds

    # Result set size limit (prevent memory exhaustion)
    MAX_RESULTS = 100000  # rows

    # Connection timeout
    DEFAULT_TIMEOUT = 5.0  # seconds

    def query(self, sql: str, params: Optional[list] = None):
        """Query with resource limits."""
        # Set query timeout
        self._connection.set_trace_callback(self._check_timeout)

        # Execute query
        cursor = self._connection.execute(sql, params)

        # Limit result set size
        rows = cursor.fetchmany(self.MAX_RESULTS)

        if len(rows) == self.MAX_RESULTS:
            raise RuntimeError(f"Query exceeded max results: {self.MAX_RESULTS}")

        return [dict(row) for row in rows]
```

### Capability Hierarchy

**Two-Layer Architecture:**

```
Database Operations (Layer 2)
├── db.read (SELECT, PRAGMA read-only, EXPLAIN)
└── db.write (INSERT, UPDATE, DELETE, CREATE/DROP TABLE, ALTER TABLE, VACUUM)

Database File Access (Layer 1)
├── file.read (open existing database, required for all operations)
└── file.write (create/modify database file, required for db.write operations)
```

**Capability Combinations:**

| Use Case | Required Capabilities | Example |
|----------|---------------------|---------|
| **Read-only queries** | `file.read` + `db.read` | Reports, analytics |
| **Full database access** | `file.read` + `file.write` + `db.read` + `db.write` | Application database |
| **Create new database** | `file.write` + `db.write` | Initialize new DB |
| **Schema introspection** | `file.read` + `db.read` | List tables, get schema |
| **Read-only file mode** | `file.read` + `db.read` | Production data (safe queries) |

**Security Principle: Least Privilege**

Always grant minimal capabilities:

```ml
// Bad: Grant everything
// capabilities=["file.read", "file.write", "db.read", "db.write"]

// Good: Grant only what's needed
// For reporting: capabilities=["file.read", "db.read"]
// For admin: capabilities=["file.read", "file.write", "db.read", "db.write"]
```

---

## Type Conversion System

### ML ↔ SQLite Type Mapping

**SQLite → ML:**
| SQLite Type | Python Type | ML Value | Notes |
|------------|-------------|----------|-------|
| `NULL` | None | `null` | Null values |
| `INTEGER` | int | number | 64-bit integers |
| `REAL` | float | number | Floating point |
| `TEXT` | str | string | UTF-8 text |
| `BLOB` | bytes | (future) | Binary data |

**ML → SQLite:**
| ML Type | SQLite Type | Example |
|---------|-------------|---------|
| `null` | NULL | `null` |
| `number` (int) | INTEGER | `42` |
| `number` (float) | REAL | `3.14` |
| `string` | TEXT | `"hello"` |
| `boolean` | INTEGER | `1` (true), `0` (false) |
| `array` | TEXT (JSON) | `"[1,2,3]"` |
| `object` | TEXT (JSON) | `"{\"a\":1}"` |

### Boolean Handling

```ml
// Insert boolean (converts to 0/1)
db.execute("INSERT INTO users (name, active) VALUES (?, ?)", ["Alice", true]);

// Query boolean (converts 0/1 to false/true)
user = db.query_one("SELECT * FROM users WHERE id = ?", [1]);
if (user.active) {  // true
    console.log("User is active");
}
```

### Array/Object Handling

```ml
import json;

// Store array as JSON
tags = ["admin", "moderator", "user"];
db.execute("INSERT INTO users (name, tags) VALUES (?, ?)",
           ["Alice", json.stringify(tags)]);

// Retrieve and parse
user = db.query_one("SELECT * FROM users WHERE id = ?", [1]);
tags = json.parse(user.tags);
console.log(tags[0]);  // "admin"

// Alternative: Use JSON1 extension (if available)
db.execute("CREATE TABLE users (name TEXT, tags JSON)");
db.execute("INSERT INTO users (name, tags) VALUES (?, json(?))",
           ["Alice", json.stringify(tags)]);
```

### Timestamp Handling

```ml
import datetime;

// Insert timestamp
now = datetime.now();
db.execute("INSERT INTO logs (message, created_at) VALUES (?, ?)",
           ["Event occurred", now.format()]);

// Query with timestamp
logs = db.query("SELECT * FROM logs WHERE created_at > ?", ["2025-01-01 00:00:00"]);

// SQLite's built-in timestamp functions
db.execute("INSERT INTO logs (message, created_at) VALUES (?, CURRENT_TIMESTAMP)",
           ["Event"]);
```

---

## Connection Management

### Single Connection Pattern

```ml
import sqlite;

// Simple: One connection per operation
db = sqlite.connect("app.db");
users = db.query("SELECT * FROM users");
db.close();
```

### Connection Reuse Pattern

```ml
import sqlite;

// Reuse connection across operations
db = sqlite.connect("app.db");

// Multiple operations
db.execute("INSERT INTO users (name) VALUES (?)", ["Alice"]);
db.execute("INSERT INTO users (name) VALUES (?)", ["Bob"]);
users = db.query("SELECT * FROM users");

// Close when done
db.close();
```

### Connection Pool Pattern (High Performance)

```ml
import sqlite;

// Create pool once (at application startup)
pool = sqlite.create_pool("app.db", max_connections=10);

// Request handler (can run concurrently)
function handle_request(request_id) {
    db = pool.get_connection();

    try {
        // Use connection
        users = db.query("SELECT * FROM users WHERE active = 1");
        return users;
    } finally {
        // Always return to pool
        pool.release_connection(db);
    }
}

// Process many requests concurrently
for (i in range(100)) {
    handle_request(i);
}

// Cleanup on shutdown
pool.close_all();
```

### Thread Safety

**SQLite3 in Python:**
- ✅ Thread-safe by default
- ✅ Multiple readers can access simultaneously
- ✅ Single writer (write operations are serialized)
- ⚠️ One connection per thread (or use connection pool)

**ML Bridge Approach:**
```python
# Allow connection sharing across threads
self._connection = sqlite3.connect(
    self.database,
    check_same_thread=False  # Allow multi-threaded access
)
```

---

## Transaction Support

### Automatic Transaction Pattern (Recommended)

```ml
import sqlite;

db = sqlite.connect("store.db");

// Automatic transaction management
try {
    db.begin_transaction();

    // All or nothing
    db.execute("INSERT INTO orders (customer_id, total) VALUES (?, ?)", [123, 99.99]);
    order_id = db.last_insert_id();

    db.execute("INSERT INTO order_items (order_id, product_id) VALUES (?, ?)",
               [order_id, 456]);

    db.commit();
    console.log("Transaction successful");

} except (error) {
    db.rollback();
    console.log("Transaction failed: " + error.message);
}
```

### Manual Transaction Pattern

```ml
// Manual control
db.execute("BEGIN TRANSACTION");

db.execute("UPDATE accounts SET balance = balance - 100 WHERE id = ?", [1]);
db.execute("UPDATE accounts SET balance = balance + 100 WHERE id = ?", [2]);

db.execute("COMMIT");
```

### Savepoints (Nested Transactions)

```ml
db.begin_transaction();

db.execute("INSERT INTO logs (message) VALUES (?)", ["Start"]);

// Create savepoint
db.execute("SAVEPOINT sp1");

try {
    db.execute("INSERT INTO logs (message) VALUES (?)", ["Critical operation"]);
    // ... more operations ...

} except (error) {
    // Rollback to savepoint only
    db.execute("ROLLBACK TO sp1");
}

// Commit main transaction
db.commit();
```

### Transaction Isolation

**SQLite Isolation Levels:**
- Default: **SERIALIZABLE** (highest isolation)
- Alternative: **READ UNCOMMITTED** (via PRAGMA)

```ml
// Enable read uncommitted (lower isolation, better concurrency)
db.execute("PRAGMA read_uncommitted = 1");
```

---

## Error Handling

### Error Types

```python
"""SQLite error types and handling."""

from sqlite3 import (
    Error,              # Base error
    IntegrityError,     # Constraint violation
    OperationalError,   # Database locked, disk full, etc.
    ProgrammingError,   # SQL syntax error
    DatabaseError,      # General database error
)
```

### ML Error Handling Patterns

```ml
import sqlite;

db = sqlite.connect("app.db");

// Handle constraint violations
try {
    db.execute("INSERT INTO users (id, email) VALUES (?, ?)", [1, "test@example.com"]);
} except (error) {
    if (error.type == "IntegrityError") {
        console.log("Duplicate entry or constraint violation");
    }
}

// Handle locked database
try {
    db.execute("UPDATE users SET name = ? WHERE id = ?", ["Alice", 1]);
} except (error) {
    if (error.type == "OperationalError" && error.message.contains("locked")) {
        console.log("Database is locked, retry later");
        // Implement retry logic
    }
}

// Handle SQL syntax errors
try {
    db.execute("SELCT * FROM users");  // Typo
} except (error) {
    if (error.type == "ProgrammingError") {
        console.log("SQL syntax error: " + error.message);
    }
}
```

### Retry Logic for Locked Database

```ml
function execute_with_retry(db, sql, params, max_retries=3) {
    retries = 0;

    while (retries < max_retries) {
        try {
            return db.execute(sql, params);
        } except (error) {
            if (error.type == "OperationalError" && retries < max_retries - 1) {
                retries = retries + 1;
                console.log("Database locked, retry " + str(retries));
                // Wait before retry (exponential backoff)
                sleep(0.1 * (2 ** retries));
            } else {
                throw error;
            }
        }
    }
}
```

---

## Testing Strategy

### Capability Tests

**Two-Layer Capability Model Tests:**

```python
def test_db_read_requires_capability():
    """Test db.query() requires db.read capability."""
    from mlpy.stdlib.decorators import _CAPABILITY_VALIDATION_ENABLED
    from mlpy.runtime.capabilities import CapabilityManager
    from mlpy.runtime.capabilities.tokens import create_capability_token

    # Enable validation for this test
    _CAPABILITY_VALIDATION_ENABLED = True

    try:
        sqlite_module = SQLite()
        db = sqlite_module.connect(":memory:")

        # Create test table
        db.execute("CREATE TABLE test (id INTEGER, name TEXT)")

        # Create context without db.read capability
        context = CapabilityManager().create_context()

        with context.activate():
            # Should raise PermissionError
            with pytest.raises(PermissionError, match="db.read"):
                db.query("SELECT * FROM test")
    finally:
        _CAPABILITY_VALIDATION_ENABLED = False

def test_db_write_requires_capability():
    """Test db.execute() requires db.write capability."""
    _CAPABILITY_VALIDATION_ENABLED = True

    try:
        sqlite_module = SQLite()
        db = sqlite_module.connect(":memory:")

        # Create context with db.read but NOT db.write
        context = CapabilityManager().create_context()
        read_token = create_capability_token("db.read")
        context.add_capability(read_token)

        with context.activate():
            # SELECT should work (has db.read)
            db.query("SELECT 1")

            # INSERT should fail (missing db.write)
            with pytest.raises(PermissionError, match="db.write"):
                db.execute("CREATE TABLE test (id INTEGER)")
    finally:
        _CAPABILITY_VALIDATION_ENABLED = False

def test_file_path_restrictions():
    """Test file.read capability restricts database paths."""
    _CAPABILITY_VALIDATION_ENABLED = True

    try:
        # Create context with restricted file access
        context = CapabilityManager().create_context()
        file_token = create_capability_token("file.read", resource_patterns=["/data/*.db"])
        db_token = create_capability_token("db.read")
        context.add_capability(file_token)
        context.add_capability(db_token)

        with context.activate():
            sqlite_module = SQLite()

            # Should work - matches pattern
            db1 = sqlite_module.connect("/data/app.db")

            # Should fail - doesn't match pattern
            with pytest.raises(PermissionError):
                db2 = sqlite_module.connect("/tmp/other.db")
    finally:
        _CAPABILITY_VALIDATION_ENABLED = False
```

### Unit Tests

**Core Functionality:**
```python
def test_connect_and_query():
    """Test database connection and basic query."""
    sqlite = SQLite()
    db = sqlite.connect(":memory:")

    # Create table
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")

    # Insert data
    db.execute("INSERT INTO users (name) VALUES (?)", ["Alice"])

    # Query data
    users = db.query("SELECT * FROM users")
    assert len(users) == 1
    assert users[0]['name'] == "Alice"

    db.close()

def test_parameterized_queries():
    """Test SQL injection prevention."""
    db = SQLite().connect(":memory:")
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")

    # Safe parameterized query
    name = "Alice'; DROP TABLE users; --"  # Malicious input
    db.execute("INSERT INTO users (name) VALUES (?)", [name])

    # Table should still exist and contain the literal string
    users = db.query("SELECT * FROM users")
    assert len(users) == 1
    assert users[0]['name'] == "Alice'; DROP TABLE users; --"

def test_transactions():
    """Test transaction commit and rollback."""
    db = SQLite().connect(":memory:")
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")

    # Successful transaction
    db.begin_transaction()
    db.execute("INSERT INTO users (name) VALUES (?)", ["Alice"])
    db.commit()

    assert len(db.query("SELECT * FROM users")) == 1

    # Rolled back transaction
    db.begin_transaction()
    db.execute("INSERT INTO users (name) VALUES (?)", ["Bob"])
    db.rollback()

    assert len(db.query("SELECT * FROM users")) == 1  # Still 1, Bob not added

def test_connection_pool():
    """Test connection pooling."""
    sqlite = SQLite()
    pool = sqlite.create_pool(":memory:", max_connections=3)

    # Get connections
    db1 = pool.get_connection()
    db2 = pool.get_connection()
    db3 = pool.get_connection()

    # Pool should be exhausted
    with pytest.raises(RuntimeError, match="pool exhausted"):
        pool.get_connection()

    # Release and reuse
    pool.release_connection(db1)
    db4 = pool.get_connection()  # Should work now

    pool.close_all()

def test_readonly_mode():
    """Test read-only database access."""
    # Create and populate database
    db = SQLite().connect("test.db")
    db.execute("CREATE TABLE users (name TEXT)")
    db.execute("INSERT INTO users VALUES (?)", ["Alice"])
    db.close()

    # Open in read-only mode
    db_ro = SQLite().connect("test.db", readonly=True)

    # Reads should work
    users = db_ro.query("SELECT * FROM users")
    assert len(users) == 1

    # Writes should fail
    with pytest.raises(sqlite3.OperationalError, match="readonly"):
        db_ro.execute("INSERT INTO users VALUES (?)", ["Bob"])

    db_ro.close()
```

### Integration Tests

**Complete Application Flow:**
```ml
// test_sqlite_integration.ml
import sqlite;
import console;

// Setup test database
db = sqlite.connect(":memory:");

db.execute("
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER DEFAULT 0
    )
");

// Populate test data
products = [
    ["Widget", 9.99, 100],
    ["Gadget", 19.99, 50],
    ["Gizmo", 29.99, 25]
];

db.execute_many("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", products);

// Test queries
all_products = db.query("SELECT * FROM products ORDER BY price");
console.log("Total products: " + str(len(all_products)));

// Test aggregation
total_value = db.query_scalar("SELECT SUM(price * stock) FROM products");
console.log("Total inventory value: $" + str(total_value));

// Test transaction
try {
    db.begin_transaction();

    // Simulate order
    db.execute("UPDATE products SET stock = stock - 10 WHERE name = ?", ["Widget"]);
    new_stock = db.query_scalar("SELECT stock FROM products WHERE name = ?", ["Widget"]);

    if (new_stock < 0) {
        throw "Insufficient stock";
    }

    db.commit();
    console.log("Order processed successfully");

} except (error) {
    db.rollback();
    console.log("Order failed: " + error);
}

db.close();
console.log("Integration test complete");
```

### Performance Tests

```python
def test_bulk_insert_performance():
    """Test large batch insert performance."""
    db = SQLite().connect(":memory:")
    db.execute("CREATE TABLE data (id INTEGER PRIMARY KEY, value TEXT)")

    import time

    # Generate test data
    rows = [["value_" + str(i)] for i in range(10000)]

    # Measure insert time
    start = time.time()
    db.execute_many("INSERT INTO data (value) VALUES (?)", rows)
    elapsed = time.time() - start

    # Should be fast (< 1 second for 10k rows)
    assert elapsed < 1.0
    assert len(db.query("SELECT * FROM data")) == 10000

def test_query_performance():
    """Test query performance with indexes."""
    db = SQLite().connect(":memory:")
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT)")

    # Insert test data
    rows = [[f"user{i}@example.com"] for i in range(1000)]
    db.execute_many("INSERT INTO users (email) VALUES (?)", rows)

    # Query without index
    import time
    start = time.time()
    db.query("SELECT * FROM users WHERE email = ?", ["user500@example.com"])
    no_index_time = time.time() - start

    # Create index
    db.execute("CREATE INDEX idx_email ON users(email)")

    # Query with index
    start = time.time()
    db.query("SELECT * FROM users WHERE email = ?", ["user500@example.com"])
    with_index_time = time.time() - start

    # Index should improve performance
    assert with_index_time < no_index_time
```

---

## Integration Examples

### Example 1: Task Management App

```ml
// tasks.ml - Simple task management application
import sqlite;
import console;

// Initialize database
db = sqlite.connect("tasks.db");

// Create schema
if (!db.table_exists("tasks")) {
    db.execute("
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            priority INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    ");
    console.log("Database initialized");
}

// Add task
function add_task(title, description, priority) {
    db.execute(
        "INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)",
        [title, description, priority]
    );
    console.log("Task added: " + title);
}

// List pending tasks
function list_tasks(status) {
    tasks = db.query(
        "SELECT * FROM tasks WHERE status = ? ORDER BY priority DESC, created_at",
        [status]
    );

    console.log("Tasks (" + status + "):");
    for (task in tasks) {
        console.log("  [" + str(task.id) + "] " + task.title + " (Priority: " + str(task.priority) + ")");
    }
}

// Complete task
function complete_task(task_id) {
    db.execute(
        "UPDATE tasks SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = ?",
        [task_id]
    );
    console.log("Task completed: " + str(task_id));
}

// Usage
add_task("Write proposal", "Complete SQLite proposal document", 1);
add_task("Review code", "Code review for PR #123", 2);
add_task("Deploy", "Deploy to production", 1);

list_tasks("pending");

complete_task(1);

list_tasks("completed");

db.close();
```

### Example 2: Analytics Dashboard

```ml
// analytics.ml - Data analytics with SQLite
import sqlite;
import csv;
import console;

// Import CSV data into SQLite
function import_csv_to_sqlite(csv_file, table_name) {
    // Read CSV
    data = csv.read(csv_file);

    // Create database
    db = sqlite.connect("analytics.db");

    // Create table from CSV headers
    if (len(data) > 0) {
        first_row = data[0];
        columns = [];
        for (key in Object.keys(first_row)) {
            columns.append(key + " TEXT");
        }

        create_sql = "CREATE TABLE IF NOT EXISTS " + table_name + " (" + columns.join(", ") + ")";
        db.execute(create_sql);

        // Insert data
        keys = Object.keys(first_row);
        placeholders = [];
        for (i in range(len(keys))) {
            placeholders.append("?");
        }

        insert_sql = "INSERT INTO " + table_name + " VALUES (" + placeholders.join(", ") + ")";

        rows = [];
        for (row in data) {
            values = [];
            for (key in keys) {
                values.append(row[key]);
            }
            rows.append(values);
        }

        db.execute_many(insert_sql, rows);
        console.log("Imported " + str(len(rows)) + " rows into " + table_name);
    }

    return db;
}

// Analyze data
function analyze_sales(db) {
    // Total sales
    total = db.query_scalar("SELECT SUM(CAST(amount AS REAL)) FROM sales");
    console.log("Total sales: $" + str(total));

    // Sales by product
    by_product = db.query("
        SELECT product, COUNT(*) as count, SUM(CAST(amount AS REAL)) as total
        FROM sales
        GROUP BY product
        ORDER BY total DESC
    ");

    console.log("\nSales by product:");
    for (row in by_product) {
        console.log("  " + row.product + ": " + str(row.count) + " orders, $" + str(row.total));
    }

    // Top customers
    top_customers = db.query("
        SELECT customer, COUNT(*) as orders, SUM(CAST(amount AS REAL)) as total
        FROM sales
        GROUP BY customer
        ORDER BY total DESC
        LIMIT 5
    ");

    console.log("\nTop 5 customers:");
    for (row in top_customers) {
        console.log("  " + row.customer + ": " + str(row.orders) + " orders, $" + str(row.total));
    }
}

// Import and analyze
db = import_csv_to_sqlite("sales_data.csv", "sales");
analyze_sales(db);
db.close();
```

### Example 3: User Authentication System

```ml
// auth.ml - User authentication with SQLite
import sqlite;
import crypto;
import console;

// Initialize auth database
db = sqlite.connect("auth.db");

db.execute("
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )
");

// Register user
function register_user(username, password) {
    // Check if user exists
    if (db.exists("SELECT 1 FROM users WHERE username = ?", [username])) {
        console.log("Error: Username already exists");
        return false;
    }

    // Generate salt and hash password
    salt = crypto.random_hex(16);
    password_hash = crypto.sha256(password, salt=salt);

    // Insert user
    db.execute(
        "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
        [username, password_hash, salt]
    );

    console.log("User registered: " + username);
    return true;
}

// Login user
function login_user(username, password) {
    // Get user record
    user = db.query_one("SELECT * FROM users WHERE username = ?", [username]);

    if (user == null) {
        console.log("Error: User not found");
        return false;
    }

    // Verify password
    password_hash = crypto.sha256(password, salt=user.salt);

    if (!crypto.compare_hash(password_hash, user.password_hash)) {
        console.log("Error: Invalid password");
        return false;
    }

    // Update last login
    db.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", [user.id]);

    console.log("Login successful: " + username);
    return true;
}

// Usage
register_user("alice", "secure_password_123");
register_user("bob", "another_password_456");

login_user("alice", "wrong_password");  // Fails
login_user("alice", "secure_password_123");  // Success

db.close();
```

---

## Performance Considerations

### Optimization Techniques

**1. Use Indexes**
```ml
// Create indexes for frequently queried columns
db.execute("CREATE INDEX idx_user_email ON users(email)");
db.execute("CREATE INDEX idx_order_customer ON orders(customer_id)");

// Compound indexes for multi-column queries
db.execute("CREATE INDEX idx_order_status_date ON orders(status, created_at)");
```

**2. Batch Operations**
```ml
// BAD: Individual inserts (slow)
for (user in users) {
    db.execute("INSERT INTO users (name) VALUES (?)", [user.name]);
}

// GOOD: Batch insert (fast)
db.execute_many("INSERT INTO users (name) VALUES (?)",
                users.map(fn(u) => [u.name]));
```

**3. Transaction Batching**
```ml
// BAD: Auto-commit for each insert
for (i in range(1000)) {
    db.execute("INSERT INTO data (value) VALUES (?)", [i]);
}

// GOOD: Single transaction for batch
db.begin_transaction();
for (i in range(1000)) {
    db.execute("INSERT INTO data (value) VALUES (?)", [i]);
}
db.commit();
```

**4. Query Optimization**
```ml
// Use EXPLAIN QUERY PLAN to analyze queries
plan = db.query("EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = ?", ["test@example.com"]);
console.log(plan);

// Optimize with covering indexes
db.execute("CREATE INDEX idx_user_covering ON users(email, name, id)");
```

**5. Write-Ahead Logging (WAL)**
```ml
// Enable WAL mode for better concurrency
db.execute("PRAGMA journal_mode=WAL");

// WAL benefits:
// - Readers don't block writers
// - Writers don't block readers
// - Faster for most operations
```

### Benchmarking Results (Expected)

| Operation | Rows | Time | Notes |
|-----------|------|------|-------|
| **Batch Insert** | 10,000 | ~500ms | With transaction |
| **Single Inserts** | 10,000 | ~20s | Without transaction |
| **Indexed Query** | 1M rows | <5ms | With proper index |
| **Full Table Scan** | 1M rows | ~2s | Without index |
| **JOIN Query** | 100K rows | ~50ms | With indexes |
| **Aggregate Query** | 100K rows | ~100ms | SUM, COUNT, AVG |

### Memory Management

```ml
// Use query_iter() for large result sets
db = sqlite.connect("large.db");

// BAD: Load all rows into memory
all_rows = db.query("SELECT * FROM huge_table");  // May cause OOM

// GOOD: Stream rows one at a time
for (row in db.query_iter("SELECT * FROM huge_table")) {
    process_row(row);
    // Only one row in memory at a time
}
```

---

## Migration from Other Databases

### From PostgreSQL/MySQL

**Common Differences:**
```ml
// PostgreSQL/MySQL: SERIAL type
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT);

// SQLite equivalent
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);

// PostgreSQL: RETURNING clause
INSERT INTO users (name) VALUES ('Alice') RETURNING id;

// SQLite equivalent
INSERT INTO users (name) VALUES ('Alice');
id = db.last_insert_id();

// PostgreSQL: BOOLEAN type
CREATE TABLE users (name TEXT, active BOOLEAN);

// SQLite equivalent (use INTEGER)
CREATE TABLE users (name TEXT, active INTEGER);  // 0 = false, 1 = true
```

### From MongoDB/NoSQL

**Document Storage in SQLite:**
```ml
import json;

// Store documents as JSON
db.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, data TEXT)");

doc = {
    name: "Alice",
    age: 30,
    tags: ["admin", "user"]
};

db.execute("INSERT INTO documents (data) VALUES (?)", [json.stringify(doc)]);

// Query and parse
result = db.query_one("SELECT * FROM documents WHERE id = ?", [1]);
doc = json.parse(result.data);
console.log(doc.name);  // "Alice"

// Alternative: JSON1 extension
db.execute("SELECT json_extract(data, '$.name') FROM documents WHERE id = ?", [1]);
```

---

## Conclusion

### Summary

This proposal defines comprehensive SQLite3 database support for ML:

**Core Capabilities:**
- ✅ Full SQL query support with parameterized queries
- ✅ Transaction management (ACID compliance)
- ✅ Connection pooling for performance
- ✅ Type conversion between ML and SQLite
- ✅ Security-first design (SQL injection prevention)
- ✅ Rich error handling
- ✅ Schema introspection

**Security Features:**
- ✅ Capability-based access control (`db.read`, `db.write`)
- ✅ Parameterized queries prevent SQL injection
- ✅ Read-only mode for untrusted code
- ✅ Path validation prevents directory traversal
- ✅ Resource limits prevent denial of service

**Performance:**
- ✅ Connection pooling for concurrent access
- ✅ Batch operations for bulk inserts
- ✅ Iterator pattern for large result sets
- ✅ WAL mode for better concurrency
- ✅ Index support for query optimization

### Implementation Effort

**Total:** 5-6 days

| Phase | Duration | Tasks |
|-------|----------|-------|
| **Day 1-2** | 2 days | Core API (connect, execute, query methods) |
| **Day 3** | 1 day | Connection pool + transaction support |
| **Day 4** | 1 day | Type conversion + error handling |
| **Day 5** | 1 day | Comprehensive testing |
| **Day 6** | 0.5-1 day | Documentation + examples |

### Use Cases Unlocked

**Data-Driven Applications:**
- Analytics dashboards
- Reporting systems
- Data processing pipelines

**Application Development:**
- User authentication systems
- Content management systems
- Task/project management apps
- Configuration storage

**Development & Testing:**
- Mock databases for testing
- Local development environments
- Prototyping and POCs

**Education:**
- Learn SQL in ML language
- Database design teaching
- Data modeling exercises

### Next Steps

1. **Approve proposal** - Confirm approach and API design
2. **Implement core module** - Database class with basic operations
3. **Add connection pool** - Performance optimization
4. **Comprehensive testing** - Unit + integration + performance
5. **Documentation** - API docs + usage examples
6. **Integration** - Update standard library registry

---

**Document Status:** Ready for Implementation
**Last Updated:** 2025-11-10
**Next Action:** Begin implementation of core Database class
