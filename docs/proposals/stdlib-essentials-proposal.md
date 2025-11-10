# ML Standard Library Essentials - Unified Proposal

**Document Type:** Technical Design & Implementation Roadmap
**Status:** Ready for Implementation
**Created:** 2025-11-10
**Authors:** mlpy Development Team

---

## Executive Summary

### Overview

**Current State:** ML has solid foundation modules (file, json, http, math, etc.)
**Gap:** Missing critical utilities needed for 80% of general-purpose programs
**Target State:** Complete standard library covering CLI tools, configuration, logging, data processing, and security
**Feasibility:** ✅ **HIGHLY FEASIBLE** - All leverage existing bridge system

### Modules in This Proposal

1. **`env`** - Environment variable access (configuration, secrets)
2. **`args`** - Command-line argument parsing (CLI tools)
3. **`csv`** - CSV file processing (data import/export)
4. **`log`** - Structured logging (debugging, monitoring)
5. **`crypto`** - Basic cryptography (hashing, UUIDs)

### Why These 5?

**Use Case Coverage:**
- **CLI Tools:** args + log + env (config, debugging, user input)
- **Data Processing:** csv + log (ETL pipelines, data analysis)
- **Web Applications:** env + log + crypto (config, monitoring, security)
- **Automation Scripts:** env + args + log + crypto (DevOps, tooling)

**Impact:** Covers 80% of missing functionality for general-purpose programming

### Effort Estimate

| Module | Complexity | Effort | Priority |
|--------|-----------|--------|----------|
| **env** | Low | 1 day | 🔴 Critical |
| **args** | Medium | 2 days | 🔴 Critical |
| **csv** | Low | 1-2 days | 🔴 Critical |
| **log** | Medium | 1-2 days | 🔴 Critical |
| **crypto** | Low | 1-2 days | 🔴 Critical |

**Total:** ~6-9 days for complete implementation

### Recommendation

**✅ PROCEED** with implementation in priority order: env → crypto → csv → log → args

---

## Table of Contents

1. [Module 1: env - Environment Variables](#module-1-env---environment-variables)
2. [Module 2: args - Command-Line Arguments](#module-2-args---command-line-arguments)
3. [Module 3: csv - CSV File Processing](#module-3-csv---csv-file-processing)
4. [Module 4: log - Structured Logging](#module-4-log---structured-logging)
5. [Module 5: crypto - Basic Cryptography](#module-5-crypto---basic-cryptography)
6. [Security Considerations](#security-considerations)
7. [Testing Strategy](#testing-strategy)
8. [Implementation Roadmap](#implementation-roadmap)
9. [Integration Examples](#integration-examples)

---

## Module 1: env - Environment Variables

### Purpose

Access and manage environment variables for configuration, secrets, and runtime settings.

### API Design

```ml
import env;

// Get environment variable
api_key = env.get("API_KEY");                    // null if not set
api_key = env.get("API_KEY", "default-key");     // With default value

// Get required variable (throws if missing)
db_url = env.require("DATABASE_URL");

// Set environment variable
env.set("DEBUG", "true");

// Check existence
has_token = env.has("AUTH_TOKEN");

// Get all variables as object
all_vars = env.all();  // {PATH: "...", HOME: "...", ...}

// Delete variable
env.delete("TEMP_VAR");

// Get with type conversion
port = env.get_int("PORT", 8080);
debug = env.get_bool("DEBUG", false);
timeout = env.get_float("TIMEOUT", 30.0);

// Common patterns
is_production = env.get("NODE_ENV") == "production";
is_dev = env.get("NODE_ENV", "development") == "development";
```

### Python Implementation

```python
"""Environment variable access module for ML."""

import os
from typing import Any, Optional
from mlpy.stdlib.decorators import ml_module, ml_function


@ml_module(
    name="env",
    description="Environment variable access and management",
    capabilities=["env.read", "env.write"],
    version="1.0.0"
)
class Env:
    """Environment variable operations."""

    @ml_function(description="Get environment variable", capabilities=["env.read"])
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable with optional default.

        Args:
            key: Variable name
            default: Default value if not set

        Returns:
            Variable value or default (None if not set and no default)
        """
        return os.environ.get(key, default)

    @ml_function(description="Get required environment variable", capabilities=["env.read"])
    def require(self, key: str) -> str:
        """Get environment variable or raise error if missing.

        Args:
            key: Variable name

        Returns:
            Variable value

        Raises:
            RuntimeError: If variable not set
        """
        value = os.environ.get(key)
        if value is None:
            raise RuntimeError(f"Required environment variable not set: {key}")
        return value

    @ml_function(description="Set environment variable", capabilities=["env.write"])
    def set(self, key: str, value: str) -> None:
        """Set environment variable.

        Args:
            key: Variable name
            value: Variable value (converted to string)
        """
        os.environ[key] = str(value)

    @ml_function(description="Check if variable exists", capabilities=["env.read"])
    def has(self, key: str) -> bool:
        """Check if environment variable is set."""
        return key in os.environ

    @ml_function(description="Get all environment variables", capabilities=["env.read"])
    def all(self) -> dict[str, str]:
        """Get all environment variables as dictionary."""
        return dict(os.environ)

    @ml_function(description="Delete environment variable", capabilities=["env.write"])
    def delete(self, key: str) -> None:
        """Delete environment variable if it exists."""
        os.environ.pop(key, None)

    @ml_function(description="Get integer environment variable", capabilities=["env.read"])
    def get_int(self, key: str, default: int = 0) -> int:
        """Get environment variable as integer."""
        value = os.environ.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

    @ml_function(description="Get boolean environment variable", capabilities=["env.read"])
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get environment variable as boolean.

        Treats "true", "1", "yes", "on" as True (case-insensitive).
        """
        value = os.environ.get(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")

    @ml_function(description="Get float environment variable", capabilities=["env.read"])
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get environment variable as float."""
        value = os.environ.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            return default
```

### File Structure

```
src/mlpy/stdlib/
├── env_bridge.py              # Main module implementation
└── tests/
    └── test_env_bridge.py     # Unit tests
```

### Security Considerations

**Capabilities:**
- `env.read` - Read environment variables (may expose secrets)
- `env.write` - Modify environment variables (affects process state)

**Risks:**
- Exposing secrets in logs (API keys, passwords)
- Modifying system environment variables

**Mitigations:**
- Require explicit capabilities
- Consider masking sensitive variable names in logs
- Document best practices (use .env files, never commit secrets)

### Use Cases

```ml
// Database configuration
import env;
db_host = env.require("DB_HOST");
db_port = env.get_int("DB_PORT", 5432);
db_name = env.require("DB_NAME");

// Feature flags
enable_cache = env.get_bool("ENABLE_CACHE", true);
max_retries = env.get_int("MAX_RETRIES", 3);

// API configuration
api_key = env.require("API_KEY");
api_url = env.get("API_URL", "https://api.example.com");
```

**Effort:** 1 day
**Files:** 1 bridge module + tests

---

## Module 2: args - Command-Line Arguments

### Purpose

Parse command-line arguments with support for flags, options, positional arguments, and help text.

### API Design

```ml
import args;

// Simple access to raw arguments
all_args = args.all();                    // ["script.ml", "--verbose", "input.txt"]
script_name = args.script();              // "script.ml"
rest = args.rest();                       // ["--verbose", "input.txt"]

// Parse with schema
parser = args.create_parser("My CLI Tool", "Process files and generate output");

// Add flags (boolean)
parser.add_flag("verbose", "v", "Enable verbose output");
parser.add_flag("quiet", "q", "Suppress all output");
parser.add_flag("force", "f", "Force overwrite existing files");

// Add options (key-value)
parser.add_option("output", "o", "Output file path", "output.txt");
parser.add_option("config", "c", "Config file path", null);
parser.add_option("format", null, "Output format: json, xml, csv", "json");

// Add positional arguments
parser.add_positional("input", "Input file to process", true);  // required
parser.add_positional("extra", "Additional files", false);      // optional

// Parse arguments
parsed = parser.parse();

// Access parsed values
if (parsed.has("verbose")) {
    console.log("Verbose mode enabled");
}

output_file = parsed.get("output");           // "output.txt" (default)
config_file = parsed.get("config");           // null (no default)
input_file = parsed.get("input");             // Required positional arg
is_forced = parsed.get_bool("force");         // false

// Get all flags/options
flags = parsed.flags();                       // {verbose: true, force: false}
options = parsed.options();                   // {output: "output.txt", format: "json"}
positionals = parsed.positionals();           // ["input.txt"]

// Generate help text
if (parsed.has("help")) {
    console.log(parser.help());
    // Output:
    // My CLI Tool
    // Process files and generate output
    //
    // Usage: script.ml [options] <input> [extra]
    //
    // Positional Arguments:
    //   input              Input file to process (required)
    //   extra              Additional files (optional)
    //
    // Options:
    //   -v, --verbose      Enable verbose output
    //   -q, --quiet        Suppress all output
    //   -f, --force        Force overwrite existing files
    //   -o, --output PATH  Output file path (default: output.txt)
    //   -c, --config PATH  Config file path
    //   --format FORMAT    Output format: json, xml, csv (default: json)
    //   -h, --help         Show this help message
}

// Validation errors
try {
    parsed = parser.parse();
} except (error) {
    console.log("Error: " + error.message);
    console.log(parser.help());
}
```

### Python Implementation

```python
"""Command-line argument parsing module for ML."""

import sys
from typing import Optional, Any
from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_class
class ArgParser:
    """Command-line argument parser."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.flags = {}       # {name: {short, help, present}}
        self.options = {}     # {name: {short, help, default}}
        self.positionals = [] # [{name, help, required}]
        self._parsed = None

    def add_flag(self, name: str, short: Optional[str], help_text: str):
        """Add boolean flag."""
        self.flags[name] = {
            'short': short,
            'help': help_text
        }

    def add_option(self, name: str, short: Optional[str], help_text: str, default: Any):
        """Add option with value."""
        self.options[name] = {
            'short': short,
            'help': help_text,
            'default': default
        }

    def add_positional(self, name: str, help_text: str, required: bool = False):
        """Add positional argument."""
        self.positionals.append({
            'name': name,
            'help': help_text,
            'required': required
        })

    def parse(self, argv: Optional[list[str]] = None):
        """Parse arguments and return ParsedArgs object."""
        if argv is None:
            argv = sys.argv[1:]  # Skip script name

        result = ParsedArgs()
        positional_values = []
        i = 0

        while i < len(argv):
            arg = argv[i]

            # Long flag (--verbose)
            if arg.startswith('--'):
                name = arg[2:]
                if name in self.flags:
                    result._flags[name] = True
                elif name in self.options:
                    if i + 1 >= len(argv):
                        raise ValueError(f"Option --{name} requires a value")
                    result._options[name] = argv[i + 1]
                    i += 1
                else:
                    raise ValueError(f"Unknown option: {arg}")

            # Short flag (-v or -vf)
            elif arg.startswith('-') and len(arg) > 1:
                shorts = arg[1:]
                for ch in shorts:
                    # Find flag/option by short name
                    found = False
                    for fname, fdata in self.flags.items():
                        if fdata['short'] == ch:
                            result._flags[fname] = True
                            found = True
                            break

                    if not found:
                        for oname, odata in self.options.items():
                            if odata['short'] == ch:
                                if i + 1 >= len(argv):
                                    raise ValueError(f"Option -{ch} requires a value")
                                result._options[oname] = argv[i + 1]
                                i += 1
                                found = True
                                break

                    if not found:
                        raise ValueError(f"Unknown option: -{ch}")

            # Positional argument
            else:
                positional_values.append(arg)

            i += 1

        # Set defaults for options
        for name, data in self.options.items():
            if name not in result._options and data['default'] is not None:
                result._options[name] = data['default']

        # Validate positionals
        for i, pos_def in enumerate(self.positionals):
            if i < len(positional_values):
                result._positionals[pos_def['name']] = positional_values[i]
            elif pos_def['required']:
                raise ValueError(f"Required positional argument missing: {pos_def['name']}")

        self._parsed = result
        return result

    def help(self) -> str:
        """Generate help text."""
        lines = []

        # Header
        if self.name:
            lines.append(self.name)
        if self.description:
            lines.append(self.description)

        # Usage
        usage = "Usage: script.ml [options]"
        for pos in self.positionals:
            if pos['required']:
                usage += f" <{pos['name']}>"
            else:
                usage += f" [{pos['name']}]"
        lines.append("")
        lines.append(usage)

        # Positionals
        if self.positionals:
            lines.append("")
            lines.append("Positional Arguments:")
            for pos in self.positionals:
                req = "(required)" if pos['required'] else "(optional)"
                lines.append(f"  {pos['name']:<18} {pos['help']} {req}")

        # Options
        lines.append("")
        lines.append("Options:")

        for name, data in self.flags.items():
            short = f"-{data['short']}, " if data['short'] else "    "
            lines.append(f"  {short}--{name:<15} {data['help']}")

        for name, data in self.options.items():
            short = f"-{data['short']}, " if data['short'] else "    "
            opt_name = f"--{name} VALUE"
            help_text = data['help']
            if data['default'] is not None:
                help_text += f" (default: {data['default']})"
            lines.append(f"  {short}{opt_name:<15} {help_text}")

        lines.append("  -h, --help         Show this help message")

        return "\n".join(lines)


@ml_class
class ParsedArgs:
    """Parsed command-line arguments."""

    def __init__(self):
        self._flags = {}
        self._options = {}
        self._positionals = {}

    def has(self, name: str) -> bool:
        """Check if flag/option is present."""
        return name in self._flags or name in self._options

    def get(self, name: str, default: Any = None) -> Any:
        """Get option or positional value."""
        if name in self._options:
            return self._options[name]
        if name in self._positionals:
            return self._positionals[name]
        if name in self._flags:
            return self._flags[name]
        return default

    def get_bool(self, name: str) -> bool:
        """Get flag value as boolean."""
        return self._flags.get(name, False)

    def flags(self) -> dict:
        """Get all flags."""
        return dict(self._flags)

    def options(self) -> dict:
        """Get all options."""
        return dict(self._options)

    def positionals(self) -> list:
        """Get all positional values."""
        return list(self._positionals.values())


@ml_module(
    name="args",
    description="Command-line argument parsing",
    capabilities=["args.read"],
    version="1.0.0"
)
class Args:
    """Command-line argument operations."""

    @ml_function(description="Get all command-line arguments", capabilities=["args.read"])
    def all(self) -> list[str]:
        """Get all command-line arguments including script name."""
        return sys.argv

    @ml_function(description="Get script name", capabilities=["args.read"])
    def script(self) -> str:
        """Get script name (first argument)."""
        return sys.argv[0] if sys.argv else ""

    @ml_function(description="Get arguments without script name", capabilities=["args.read"])
    def rest(self) -> list[str]:
        """Get arguments without script name."""
        return sys.argv[1:] if len(sys.argv) > 1 else []

    @ml_function(description="Create argument parser", capabilities=[])
    def create_parser(self, name: str = "", description: str = "") -> ArgParser:
        """Create new argument parser."""
        return ArgParser(name, description)
```

### Use Cases

```ml
// Simple CLI tool
import args;
import file;
import console;

parser = args.create_parser("File Processor", "Process text files");
parser.add_flag("verbose", "v", "Enable verbose output");
parser.add_option("output", "o", "Output directory", ".");
parser.add_positional("input", "Input file", true);

parsed = parser.parse();

if (parsed.get_bool("verbose")) {
    console.log("Processing: " + parsed.get("input"));
}

content = file.read(parsed.get("input"));
// ... process content ...
```

**Effort:** 2 days
**Files:** 1 bridge module + 2 classes + tests

---

## Module 3: csv - CSV File Processing

### Purpose

Read and write CSV files with support for headers, custom delimiters, and type conversion.

### API Design

```ml
import csv;

// Read CSV file (returns array of objects)
data = csv.read("users.csv");
// [
//   {name: "Alice", age: "30", city: "NYC"},
//   {name: "Bob", age: "25", city: "LA"}
// ]

// Read without headers (returns array of arrays)
data = csv.read("data.csv", headers=false);
// [
//   ["Alice", "30", "NYC"],
//   ["Bob", "25", "LA"]
// ]

// Custom delimiter
data = csv.read("data.tsv", delimiter="\t");

// Write CSV file from array of objects
users = [
    {name: "Alice", age: 30, city: "NYC"},
    {name: "Bob", age: 25, city: "LA"}
];
csv.write("output.csv", users);

// Write with custom headers
csv.write("output.csv", users, headers=["Full Name", "Age", "Location"]);

// Write array of arrays
rows = [
    ["Name", "Age", "City"],
    ["Alice", 30, "NYC"],
    ["Bob", 25, "LA"]
];
csv.write("output.csv", rows, headers=false);

// Custom delimiter and quote character
csv.write("output.tsv", data, delimiter="\t", quote="'");

// Advanced: CSV reader for large files (streaming)
reader = csv.create_reader("large.csv");
while (reader.has_next()) {
    row = reader.next();
    console.log(row.name);
}
reader.close();

// Advanced: CSV writer for streaming
writer = csv.create_writer("output.csv", headers=["name", "age"]);
writer.write_row({name: "Alice", age: 30});
writer.write_row({name: "Bob", age: 25});
writer.close();
```

### Python Implementation

```python
"""CSV file processing module for ML."""

import csv as py_csv
from typing import Any, Optional, Union
from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_class
class CSVReader:
    """Streaming CSV reader for large files."""

    def __init__(self, file_path: str, delimiter: str = ',', has_headers: bool = True):
        self.file_path = file_path
        self.delimiter = delimiter
        self.has_headers = has_headers
        self._file = None
        self._reader = None
        self._headers = None
        self._open()

    def _open(self):
        """Open file and initialize reader."""
        self._file = open(self.file_path, 'r', newline='', encoding='utf-8')
        self._reader = py_csv.reader(self._file, delimiter=self.delimiter)

        if self.has_headers:
            self._headers = next(self._reader)

    def has_next(self) -> bool:
        """Check if more rows available."""
        pos = self._file.tell()
        try:
            next(self._reader)
            self._file.seek(pos)
            return True
        except StopIteration:
            return False

    def next(self) -> Union[dict, list]:
        """Read next row."""
        row = next(self._reader)

        if self.has_headers and self._headers:
            return {self._headers[i]: row[i] for i in range(len(row))}
        return row

    def close(self):
        """Close file."""
        if self._file:
            self._file.close()
            self._file = None


@ml_class
class CSVWriter:
    """Streaming CSV writer."""

    def __init__(self, file_path: str, headers: Optional[list] = None,
                 delimiter: str = ',', quote: str = '"'):
        self.file_path = file_path
        self.headers = headers
        self.delimiter = delimiter
        self.quote = quote
        self._file = None
        self._writer = None
        self._open()

    def _open(self):
        """Open file and initialize writer."""
        self._file = open(self.file_path, 'w', newline='', encoding='utf-8')
        self._writer = py_csv.writer(
            self._file,
            delimiter=self.delimiter,
            quotechar=self.quote
        )

        if self.headers:
            self._writer.writerow(self.headers)

    def write_row(self, row: Union[dict, list]):
        """Write single row."""
        if isinstance(row, dict):
            if self.headers:
                row_data = [row.get(h, '') for h in self.headers]
            else:
                row_data = list(row.values())
        else:
            row_data = row

        self._writer.writerow(row_data)

    def close(self):
        """Close file."""
        if self._file:
            self._file.close()
            self._file = None


@ml_module(
    name="csv",
    description="CSV file processing",
    capabilities=["file.read", "file.write"],
    version="1.0.0"
)
class CSV:
    """CSV file operations."""

    @ml_function(description="Read CSV file", capabilities=["file.read"])
    def read(self, file_path: str, delimiter: str = ',',
             headers: bool = True) -> list[Union[dict, list]]:
        """Read CSV file.

        Args:
            file_path: Path to CSV file
            delimiter: Field delimiter (default: ',')
            headers: First row contains headers (default: True)

        Returns:
            List of dictionaries (if headers=True) or list of lists
        """
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = py_csv.reader(f, delimiter=delimiter)

            if headers:
                header_row = next(reader)
                return [
                    {header_row[i]: row[i] for i in range(len(row))}
                    for row in reader
                ]
            else:
                return list(reader)

    @ml_function(description="Write CSV file", capabilities=["file.write"])
    def write(self, file_path: str, data: list,
              delimiter: str = ',', quote: str = '"',
              headers: Optional[list] = None) -> None:
        """Write CSV file.

        Args:
            file_path: Output file path
            data: List of dictionaries or list of lists
            delimiter: Field delimiter (default: ',')
            quote: Quote character (default: '"')
            headers: Custom header names (optional)
        """
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = py_csv.writer(f, delimiter=delimiter, quotechar=quote)

            if not data:
                return

            # Determine if data is list of dicts or list of lists
            is_dict = isinstance(data[0], dict)

            # Write headers
            if is_dict:
                if headers:
                    writer.writerow(headers)
                else:
                    writer.writerow(data[0].keys())
            elif headers:
                writer.writerow(headers)

            # Write rows
            for row in data:
                if is_dict:
                    if headers:
                        row_data = [row.get(h, '') for h in headers]
                    else:
                        row_data = list(row.values())
                else:
                    row_data = row
                writer.writerow(row_data)

    @ml_function(description="Create CSV reader for streaming", capabilities=["file.read"])
    def create_reader(self, file_path: str, delimiter: str = ',',
                     headers: bool = True) -> CSVReader:
        """Create streaming CSV reader for large files."""
        return CSVReader(file_path, delimiter, headers)

    @ml_function(description="Create CSV writer for streaming", capabilities=["file.write"])
    def create_writer(self, file_path: str, headers: Optional[list] = None,
                     delimiter: str = ',', quote: str = '"') -> CSVWriter:
        """Create streaming CSV writer."""
        return CSVWriter(file_path, headers, delimiter, quote)
```

### Use Cases

```ml
// Data import pipeline
import csv;
import console;

// Read CSV
users = csv.read("users.csv");

// Process data
active_users = [];
for (user in users) {
    if (int(user.age) >= 18) {
        active_users.append(user);
    }
}

// Export results
csv.write("active_users.csv", active_users);
console.log("Exported " + str(len(active_users)) + " active users");
```

**Effort:** 1-2 days
**Files:** 1 bridge module + 2 classes + tests

---

## Module 4: log - Structured Logging

### Purpose

Structured logging with levels, formatting, and multiple outputs (console, file).

### API Design

```ml
import log;

// Simple logging
log.info("Application started");
log.warn("Cache miss for key: user_123");
log.error("Database connection failed");
log.debug("Processing item 5 of 100");

// Logging with context data
log.info("User logged in", {user_id: 123, ip: "192.168.1.1"});
log.error("Payment failed", {amount: 99.99, reason: "Insufficient funds"});

// Configure logger
log.set_level("DEBUG");         // DEBUG, INFO, WARN, ERROR
log.set_format("json");         // "text", "json"
log.add_file("app.log");        // Log to file
log.set_timestamp(true);        // Include timestamps

// Create named loggers
db_log = log.create_logger("database");
api_log = log.create_logger("api");

db_log.info("Query executed", {duration: 0.025});
api_log.error("Request failed", {status: 500});

// Log levels
log.debug("Detailed debug info");     // DEBUG level
log.info("Informational message");    // INFO level
log.warn("Warning message");          // WARN level
log.error("Error message");           // ERROR level
log.critical("Critical failure");     // CRITICAL level (always shown)

// Conditional logging
if (log.is_debug()) {
    expensive_data = compute_debug_info();
    log.debug("Debug data", expensive_data);
}

// Format examples:
// TEXT:  [2025-11-10 14:30:22] INFO: Application started
// JSON:  {"timestamp":"2025-11-10T14:30:22Z","level":"INFO","message":"Application started"}
```

### Python Implementation

```python
"""Structured logging module for ML."""

import logging
import json
from datetime import datetime
from typing import Any, Optional
from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


@ml_class
class Logger:
    """Named logger instance."""

    def __init__(self, name: str, level: str = "INFO", format_type: str = "text"):
        self.name = name
        self._logger = logging.getLogger(name)
        self._set_level(level)
        self.format_type = format_type
        self.include_timestamp = True

        # Setup console handler
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(self._get_formatter())
            self._logger.addHandler(handler)

    def _set_level(self, level: str):
        """Set logging level."""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARN": logging.WARNING,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        self._logger.setLevel(level_map.get(level.upper(), logging.INFO))

    def _get_formatter(self):
        """Get log formatter based on format type."""
        if self.format_type == "json":
            return logging.Formatter('%(message)s')
        else:
            return logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

    def _format_message(self, message: str, data: Optional[dict] = None) -> str:
        """Format log message with optional data."""
        if self.format_type == "json":
            log_entry = {
                "message": message,
                "level": self._current_level
            }
            if self.include_timestamp:
                log_entry["timestamp"] = datetime.utcnow().isoformat() + "Z"
            if data:
                log_entry.update(data)
            return json.dumps(log_entry)
        else:
            if data:
                data_str = " | " + " ".join(f"{k}={v}" for k, v in data.items())
                return message + data_str
            return message

    def debug(self, message: str, data: Optional[dict] = None):
        """Log debug message."""
        self._current_level = "DEBUG"
        self._logger.debug(self._format_message(message, data))

    def info(self, message: str, data: Optional[dict] = None):
        """Log info message."""
        self._current_level = "INFO"
        self._logger.info(self._format_message(message, data))

    def warn(self, message: str, data: Optional[dict] = None):
        """Log warning message."""
        self._current_level = "WARN"
        self._logger.warning(self._format_message(message, data))

    def error(self, message: str, data: Optional[dict] = None):
        """Log error message."""
        self._current_level = "ERROR"
        self._logger.error(self._format_message(message, data))

    def critical(self, message: str, data: Optional[dict] = None):
        """Log critical message."""
        self._current_level = "CRITICAL"
        self._logger.critical(self._format_message(message, data))

    def is_debug(self) -> bool:
        """Check if debug logging is enabled."""
        return self._logger.isEnabledFor(logging.DEBUG)

    def set_level(self, level: str):
        """Change logging level."""
        self._set_level(level)

    def add_file(self, file_path: str):
        """Add file output handler."""
        handler = logging.FileHandler(file_path)
        handler.setFormatter(self._get_formatter())
        self._logger.addHandler(handler)

    def set_format(self, format_type: str):
        """Set log format (text or json)."""
        self.format_type = format_type
        for handler in self._logger.handlers:
            handler.setFormatter(self._get_formatter())

    def set_timestamp(self, enabled: bool):
        """Enable/disable timestamps."""
        self.include_timestamp = enabled


@ml_module(
    name="log",
    description="Structured logging with levels and formatting",
    capabilities=["log.write", "file.write"],
    version="1.0.0"
)
class Log:
    """Logging operations."""

    def __init__(self):
        self._default_logger = Logger("default")

    @ml_function(description="Log debug message", capabilities=["log.write"])
    def debug(self, message: str, data: Optional[dict] = None):
        """Log debug level message."""
        self._default_logger.debug(message, data)

    @ml_function(description="Log info message", capabilities=["log.write"])
    def info(self, message: str, data: Optional[dict] = None):
        """Log info level message."""
        self._default_logger.info(message, data)

    @ml_function(description="Log warning message", capabilities=["log.write"])
    def warn(self, message: str, data: Optional[dict] = None):
        """Log warning level message."""
        self._default_logger.warn(message, data)

    @ml_function(description="Log error message", capabilities=["log.write"])
    def error(self, message: str, data: Optional[dict] = None):
        """Log error level message."""
        self._default_logger.error(message, data)

    @ml_function(description="Log critical message", capabilities=["log.write"])
    def critical(self, message: str, data: Optional[dict] = None):
        """Log critical level message."""
        self._default_logger.critical(message, data)

    @ml_function(description="Set log level", capabilities=["log.write"])
    def set_level(self, level: str):
        """Set logging level (DEBUG, INFO, WARN, ERROR)."""
        self._default_logger.set_level(level)

    @ml_function(description="Set log format", capabilities=["log.write"])
    def set_format(self, format_type: str):
        """Set log format (text or json)."""
        self._default_logger.set_format(format_type)

    @ml_function(description="Add file output", capabilities=["log.write", "file.write"])
    def add_file(self, file_path: str):
        """Add file logging output."""
        self._default_logger.add_file(file_path)

    @ml_function(description="Enable/disable timestamps", capabilities=["log.write"])
    def set_timestamp(self, enabled: bool):
        """Enable or disable timestamps in logs."""
        self._default_logger.set_timestamp(enabled)

    @ml_function(description="Check if debug enabled", capabilities=[])
    def is_debug(self) -> bool:
        """Check if debug logging is enabled."""
        return self._default_logger.is_debug()

    @ml_function(description="Create named logger", capabilities=[])
    def create_logger(self, name: str) -> Logger:
        """Create named logger instance."""
        return Logger(name)
```

### Use Cases

```ml
// Web application logging
import log;
import env;

// Configure logging
if (env.get("ENV") == "production") {
    log.set_level("INFO");
    log.set_format("json");
    log.add_file("app.log");
} else {
    log.set_level("DEBUG");
}

// Application code
log.info("Server starting", {port: 8080});

function handle_request(request) {
    log.debug("Request received", {path: request.path, method: request.method});

    try {
        result = process_request(request);
        log.info("Request processed", {status: 200, duration: 0.045});
        return result;
    } except (error) {
        log.error("Request failed", {error: error.message, status: 500});
        throw error;
    }
}
```

**Effort:** 1-2 days
**Files:** 1 bridge module + 1 class + tests

---

## Module 5: crypto - Basic Cryptography

### Purpose

Basic cryptographic operations: hashing (SHA256, MD5), UUID generation, and secure random data.

### API Design

```ml
import crypto;

// Hashing
hash = crypto.sha256("password123");           // SHA-256 hash
hash = crypto.sha1("data");                    // SHA-1 hash
hash = crypto.md5("file contents");            // MD5 hash (checksums only)

// Hash with salt
hash = crypto.sha256("password", salt="random_salt_123");

// Hash file contents
file_hash = crypto.hash_file("document.pdf", algorithm="sha256");

// UUID generation
id = crypto.uuid();                            // UUID v4 (random)
// "a7f3d8e2-4b5c-4d9e-8f7a-6b3c2d1e0f9a"

id = crypto.uuid_from_string("user@example.com");  // UUID v5 (deterministic)

// Secure random data
token = crypto.random_bytes(32);               // 32 random bytes
hex_token = crypto.random_hex(16);             // 32-char hex string
alphanumeric = crypto.random_string(12);       // 12-char string [A-Za-z0-9]

// Random numbers (cryptographically secure)
num = crypto.random_int(1, 100);               // Random int in range
float = crypto.random_float();                 // Random float 0.0-1.0

// Compare hashes securely (timing-attack resistant)
is_valid = crypto.compare_hash(input_hash, stored_hash);

// HMAC (keyed hash for message authentication)
signature = crypto.hmac("message", "secret_key", algorithm="sha256");
is_valid = crypto.verify_hmac("message", signature, "secret_key");
```

### Python Implementation

```python
"""Basic cryptography module for ML."""

import hashlib
import hmac
import secrets
import uuid
from typing import Optional
from mlpy.stdlib.decorators import ml_module, ml_function


@ml_module(
    name="crypto",
    description="Basic cryptographic operations (hashing, UUIDs, secure random)",
    capabilities=["crypto.hash", "crypto.random"],
    version="1.0.0"
)
class Crypto:
    """Cryptographic operations."""

    @ml_function(description="SHA-256 hash", capabilities=["crypto.hash"])
    def sha256(self, data: str, salt: str = "") -> str:
        """Compute SHA-256 hash of string.

        Args:
            data: String to hash
            salt: Optional salt to prepend

        Returns:
            Hex-encoded hash string
        """
        content = (salt + data).encode('utf-8')
        return hashlib.sha256(content).hexdigest()

    @ml_function(description="SHA-1 hash", capabilities=["crypto.hash"])
    def sha1(self, data: str, salt: str = "") -> str:
        """Compute SHA-1 hash of string."""
        content = (salt + data).encode('utf-8')
        return hashlib.sha1(content).hexdigest()

    @ml_function(description="MD5 hash", capabilities=["crypto.hash"])
    def md5(self, data: str, salt: str = "") -> str:
        """Compute MD5 hash of string (use for checksums only, not security)."""
        content = (salt + data).encode('utf-8')
        return hashlib.md5(content).hexdigest()

    @ml_function(description="Hash file contents", capabilities=["crypto.hash", "file.read"])
    def hash_file(self, file_path: str, algorithm: str = "sha256") -> str:
        """Hash entire file contents.

        Args:
            file_path: Path to file
            algorithm: Hash algorithm (sha256, sha1, md5)

        Returns:
            Hex-encoded hash
        """
        hash_func = getattr(hashlib, algorithm)
        hasher = hash_func()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)

        return hasher.hexdigest()

    @ml_function(description="Generate UUID v4", capabilities=["crypto.random"])
    def uuid(self) -> str:
        """Generate random UUID (version 4)."""
        return str(uuid.uuid4())

    @ml_function(description="Generate UUID v5 from string", capabilities=["crypto.hash"])
    def uuid_from_string(self, data: str, namespace: Optional[str] = None) -> str:
        """Generate deterministic UUID from string (version 5).

        Args:
            data: Input string
            namespace: UUID namespace (default: DNS namespace)

        Returns:
            UUID string
        """
        ns = uuid.UUID(namespace) if namespace else uuid.NAMESPACE_DNS
        return str(uuid.uuid5(ns, data))

    @ml_function(description="Generate random bytes", capabilities=["crypto.random"])
    def random_bytes(self, length: int) -> bytes:
        """Generate cryptographically secure random bytes."""
        return secrets.token_bytes(length)

    @ml_function(description="Generate random hex string", capabilities=["crypto.random"])
    def random_hex(self, length: int) -> str:
        """Generate random hex string (2x length characters)."""
        return secrets.token_hex(length)

    @ml_function(description="Generate random alphanumeric string", capabilities=["crypto.random"])
    def random_string(self, length: int) -> str:
        """Generate random alphanumeric string [A-Za-z0-9]."""
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    @ml_function(description="Generate secure random integer", capabilities=["crypto.random"])
    def random_int(self, min_val: int, max_val: int) -> int:
        """Generate cryptographically secure random integer in range [min, max]."""
        return secrets.randbelow(max_val - min_val + 1) + min_val

    @ml_function(description="Generate secure random float", capabilities=["crypto.random"])
    def random_float(self) -> float:
        """Generate cryptographically secure random float in [0.0, 1.0)."""
        return secrets.randbelow(2**32) / 2**32

    @ml_function(description="Compare hashes securely", capabilities=["crypto.hash"])
    def compare_hash(self, hash1: str, hash2: str) -> bool:
        """Compare two hashes using timing-attack resistant comparison.

        Args:
            hash1: First hash
            hash2: Second hash

        Returns:
            True if hashes match
        """
        return hmac.compare_digest(hash1.encode(), hash2.encode())

    @ml_function(description="Generate HMAC signature", capabilities=["crypto.hash"])
    def hmac(self, message: str, key: str, algorithm: str = "sha256") -> str:
        """Generate HMAC signature for message authentication.

        Args:
            message: Message to sign
            key: Secret key
            algorithm: Hash algorithm (sha256, sha1, md5)

        Returns:
            Hex-encoded HMAC signature
        """
        hash_func = getattr(hashlib, algorithm)
        h = hmac.new(key.encode(), message.encode(), hash_func)
        return h.hexdigest()

    @ml_function(description="Verify HMAC signature", capabilities=["crypto.hash"])
    def verify_hmac(self, message: str, signature: str, key: str,
                    algorithm: str = "sha256") -> bool:
        """Verify HMAC signature.

        Args:
            message: Original message
            signature: HMAC signature to verify
            key: Secret key
            algorithm: Hash algorithm

        Returns:
            True if signature is valid
        """
        expected = self.hmac(message, key, algorithm)
        return hmac.compare_digest(signature.encode(), expected.encode())
```

### Use Cases

```ml
// Password hashing (basic - use bcrypt for production)
import crypto;

function hash_password(password) {
    salt = crypto.random_hex(16);
    hash = crypto.sha256(password, salt=salt);
    return salt + ":" + hash;
}

function verify_password(password, stored) {
    parts = stored.split(":");
    salt = parts[0];
    stored_hash = parts[1];
    computed_hash = crypto.sha256(password, salt=salt);
    return crypto.compare_hash(computed_hash, stored_hash);
}

// API token generation
token = crypto.random_hex(32);
console.log("API Token: " + token);

// File integrity check
original_hash = crypto.hash_file("document.pdf");
// ... later ...
current_hash = crypto.hash_file("document.pdf");
if (original_hash == current_hash) {
    console.log("File integrity verified");
}
```

**Effort:** 1-2 days
**Files:** 1 bridge module + tests

---

## Security Considerations

### Capability Requirements

All modules require explicit capabilities:

| Module | Capabilities | Risk Level |
|--------|-------------|-----------|
| **env** | `env.read`, `env.write` | 🟡 Medium (secret exposure) |
| **args** | `args.read` | 🟢 Low |
| **csv** | `file.read`, `file.write` | 🟡 Medium (file access) |
| **log** | `log.write`, `file.write` | 🟢 Low |
| **crypto** | `crypto.hash`, `crypto.random` | 🟢 Low |

### Security Best Practices

**Environment Variables:**
- Never log environment variables directly (may contain secrets)
- Use `.env` files for local development
- Use secure secret management in production
- Document which variables contain sensitive data

**Command-Line Arguments:**
- Never pass secrets via CLI args (visible in process list)
- Validate all user input
- Use `--` to separate flags from positional args

**CSV Processing:**
- Validate file paths to prevent directory traversal
- Set reasonable file size limits
- Sanitize CSV content if displaying in web UI (XSS risk)

**Logging:**
- Mask sensitive data in logs (passwords, tokens, API keys)
- Implement log rotation to prevent disk exhaustion
- Use appropriate log levels (don't log sensitive data at DEBUG level in production)

**Cryptography:**
- This module provides basic crypto only
- For password hashing, recommend bcrypt/argon2 (future module)
- For encryption, recommend dedicated encryption module (future)
- Document limitations clearly

### Capability Hierarchies

```
Root Capabilities:
├── env.read          (read environment variables)
├── env.write         (modify environment variables)
├── args.read         (read command-line arguments)
├── file.read         (required by csv.read)
├── file.write        (required by csv.write, log.add_file)
├── log.write         (write to logs)
├── crypto.hash       (hashing operations)
└── crypto.random     (secure random generation)
```

---

## Capability System Integration

### Current State

**Capability Infrastructure:** mlpy has a complete capability system in place:
- `src/mlpy/runtime/capabilities/manager.py` - Global capability manager
- `src/mlpy/runtime/capabilities/context.py` - Capability contexts with inheritance
- `src/mlpy/runtime/capabilities/tokens.py` - Capability tokens with patterns
- `src/mlpy/stdlib/decorators.py` - Module/function decorators with capability metadata

**Current Status:** Capability validation is **DISABLED by default** (`_CAPABILITY_VALIDATION_ENABLED = False`)
- Decorators capture capability requirements as metadata
- Runtime validation is not yet enforced
- This allows gradual migration and testing

### New Capabilities Introduced

These 5 modules introduce **8 new capability types**:

```python
# New capabilities (need to be registered)
NEW_CAPABILITIES = [
    "env.read",          # Read environment variables
    "env.write",         # Modify environment variables
    "args.read",         # Read command-line arguments
    "log.write",         # Write to logs (console)
    "crypto.hash",       # Cryptographic hashing
    "crypto.random",     # Secure random generation
    # Note: csv uses existing file.read and file.write
]
```

### Capability Declaration in ML Code

**Current Approach (Implicit):**
ML programs currently don't declare capabilities - they're automatically granted based on imported modules.

```ml
// Current: Import automatically grants capabilities
import env;
api_key = env.get("API_KEY");  // Works without declaration
```

**Future Approach (Explicit - Recommended):**
When capability validation is enabled, ML programs should declare required capabilities:

```ml
// Future: Explicit capability declaration (proposed syntax)
// @requires_capability("env.read")
// @requires_capability("file.read")

import env;
import csv;

// Code using env and csv modules
```

### Enforcement Mechanism

**Phase 1: Metadata Collection (Current)**
- ✅ Decorators collect capability requirements
- ✅ Module registry tracks capabilities
- ❌ No runtime enforcement yet

**Phase 2: Opt-in Validation (Recommended Next Step)**
- Enable validation per-module or per-program
- Validate on module import
- Validate on function call
- Clear error messages when capabilities missing

**Phase 3: Mandatory Validation (Future)**
- All programs must declare capabilities
- Sandbox mode enforces strictly
- Production deployment requirement

### Implementation Changes Needed

**No Registration Required!** ✅

The capability system is **extensible by design** - new capability types are introduced simply by using them in decorators. No central registry needed.

**How it works:**
1. Decorators declare capabilities: `@ml_function(capabilities=["env.read"])`
2. Metadata is stored on the function/module
3. When validation is enabled, runtime checks if context has that capability
4. **That's it!** No registration step needed.

**Example - Adding new capabilities:**
```python
@ml_function(description="Get environment variable", capabilities=["env.read"])
def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(key, default)
```

The string `"env.read"` is now a valid capability type - it's registered implicitly by using it.

**Why this is better:**
- ✅ No central registry to update
- ✅ Extensible without core changes
- ✅ Third-party modules can define their own capabilities
- ✅ No risk of forgetting to register

**Enable Validation (Optional)**

For strict mode, enable validation in decorators:

```python
# src/mlpy/stdlib/decorators.py

# Change this flag to enable validation
_CAPABILITY_VALIDATION_ENABLED = True  # Was: False
```

**2. Capability Context Setup (When Validation Enabled)**

When ML program runs with validation, create context with granted capabilities:

```python
from mlpy.runtime.capabilities import CapabilityManager
from mlpy.runtime.capabilities.tokens import create_capability_token

manager = CapabilityManager()
context = manager.create_context("ml_program")

# Grant capabilities based on ML program's imports
env_token = create_capability_token("env.read", resource_patterns=["*"])
context.add_capability(env_token)

csv_read_token = create_capability_token("file.read", resource_patterns=["*.csv"])
context.add_capability(csv_read_token)

log_token = create_capability_token("log.write")
context.add_capability(log_token)

# Execute ML program in this context
# (Context is thread-local, automatically available to called functions)
with context.activate():
    exec(transpiled_code)
```

**3. Function-Level Validation (Already Implemented)**

The decorator system already has validation built-in (currently disabled):

From `src/mlpy/stdlib/decorators.py` (already implemented):

```python
def ml_function(description: str, capabilities: Optional[List[str]] = None, ...):
    def decorator(func: Callable) -> Callable:
        # Attach metadata
        metadata = FunctionMetadata(name=func.__name__, description=description,
                                   capabilities=capabilities, ...)
        func._ml_function_metadata = metadata

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Validation (disabled by default via _CAPABILITY_VALIDATION_ENABLED flag)
            if _CAPABILITY_VALIDATION_ENABLED and metadata.capabilities:
                capability_context = kwargs.pop('_capability_context', None)

                if capability_context is not None:
                    for cap_type in metadata.capabilities:
                        if not capability_context.has_capability(cap_type):
                            raise PermissionError(
                                f"Missing required capability '{cap_type}' for {func.__name__}()"
                            )

            return func(*args, **kwargs)

        wrapper._ml_function_metadata = metadata
        return wrapper

    return decorator
```

**Key Point:** The infrastructure is already there, just disabled by default via the `_CAPABILITY_VALIDATION_ENABLED` flag.

### Integration with Existing Modules

**CSV Module - Reuses Existing Capabilities:**
```python
@ml_module(
    name="csv",
    capabilities=["file.read", "file.write"],  # Existing capabilities
)
```
No new capability types needed - CSV operations are file operations.

**Log Module - Uses Existing + New:**
```python
@ml_module(
    name="log",
    capabilities=["log.write", "file.write"],  # log.write is NEW
)
```
Console logging uses new `log.write`, file logging uses existing `file.write`.

### Security Model

**Capability Granularity:**

```python
# Coarse-grained (module level)
context.grant_capability(CapabilityToken("env.read", "*"))  # All env vars

# Fine-grained (resource patterns)
context.grant_capability(CapabilityToken("env.read", "API_*"))  # Only API_* vars
context.grant_capability(CapabilityToken("env.read", "DB_*"))   # Only DB_* vars

# Specific resources
context.grant_capability(CapabilityToken("file.read", "data/*.csv"))
context.grant_capability(CapabilityToken("file.write", "output/*.csv"))
```

**Least Privilege Principle:**
Grant minimal capabilities needed:

```ml
// ML program only needs to read config
import env;
config = env.get("API_URL");  // Requires: env.read

// Should NOT be able to:
// env.set("API_URL", "evil.com");  // Would require: env.write
```

### Migration Path

**Stage 1: Implementation (This Proposal)**
- ✅ Add 5 new modules with capability decorators
- ✅ Capabilities are documented but not enforced
- ✅ Existing programs work without changes

**Stage 2: Testing & Validation**
- ✅ Enable validation in test suite
- ✅ Verify capability checks work correctly
- ✅ Measure performance impact
- ✅ Gather feedback

**Stage 3: Opt-in Enforcement**
- ✅ Add flag to enable strict mode: `mlpy run --strict-capabilities script.ml`
- ✅ Document capability requirements
- ✅ Provide migration guide

**Stage 4: Default Enforcement (Future)**
- ✅ Enable validation by default
- ✅ Opt-out flag for legacy: `mlpy run --no-capability-check script.ml`
- ✅ Sandbox mode always enforces

### Compatibility Guarantee

**Backward Compatibility:**
- Existing ML programs continue working unchanged
- New modules work without capability system enabled
- Gradual adoption path for capability enforcement

**Forward Compatibility:**
- All new modules include capability metadata
- When validation is enabled, programs get clear error messages
- Documentation shows required capabilities for each function

### Testing Capability Enforcement

**Unit Tests:**
```python
def test_env_read_requires_capability():
    """Test env.get() requires env.read capability."""
    # Enable validation
    _CAPABILITY_VALIDATION_ENABLED = True

    # Create context without capability
    context = CapabilityManager().create_context()

    with context.activate():
        env = Env()

        # Should raise CapabilityError
        with pytest.raises(CapabilityError, match="env.read"):
            env.get("API_KEY")

def test_env_read_with_capability():
    """Test env.get() works with proper capability."""
    _CAPABILITY_VALIDATION_ENABLED = True

    # Create context WITH capability
    context = CapabilityManager().create_context()
    context.grant_capability(CapabilityToken("env.read", "*"))

    with context.activate():
        env = Env()
        result = env.get("PATH")  # Should work
        assert result is not None
```

**Integration Tests:**
Test complete capability chain:
```ml
// test_capabilities.ml
import env;
import csv;
import log;

// This program requires:
// - env.read
// - file.read (for csv.read)
// - log.write

log.info("Starting");
data_file = env.get("DATA_FILE", "data.csv");
data = csv.read(data_file);
log.info("Loaded records", {count: len(data)});
```

### Documentation Requirements

**Module Documentation:**
Each module's docstring must list required capabilities:

```python
"""CSV file processing module.

**Required Capabilities:**
- `file.read` - Read CSV files
- `file.write` - Write CSV files

**Usage:**
```ml
import csv;
data = csv.read("input.csv");  // Requires: file.read
```
"""
```

**Function Documentation:**
Each function must document its capabilities:

```python
@ml_function(description="Read CSV file", capabilities=["file.read"])
def read(self, file_path: str, ...):
    """Read CSV file.

    **Required Capability:** `file.read`

    **Example:**
    ```ml
    data = csv.read("users.csv");
    ```
    """
```

### Summary

**What This Proposal Adds:**
- ✅ 8 new capability types introduced via decorators (no registration needed!)
- ✅ Capability metadata on all modules/functions
- ✅ Foundation for future capability enforcement
- ✅ Extensible system (third-party modules can add their own)

**How Capabilities Work (Simplified):**
1. Decorators declare requirements: `@ml_function(capabilities=["env.read"])`
2. System stores metadata automatically
3. When validation enabled, runtime checks `context.has_capability("env.read")`
4. No central registry - capabilities registered implicitly when declared

**What's NOT Changing (Yet):**
- ❌ Capability validation still disabled by default
- ❌ ML programs don't need to declare capabilities
- ❌ No breaking changes to existing code
- ❌ No central registry to maintain (by design!)

**Why No Registration is Better:**
- ✅ Extensible without core changes
- ✅ Third-party modules define their own capabilities
- ✅ No synchronization between decorator and registry
- ✅ Simpler implementation

**Future Work (Outside This Proposal):**
- Enable capability validation system-wide
- ML syntax for capability declaration
- Fine-grained resource pattern matching
- Capability audit tooling

**Recommendation:**
- Implement all 5 modules with capability decorators
- Keep validation disabled during implementation
- Add capability validation tests (run with flag enabled)
- Document capability requirements thoroughly
- Enable validation in separate future proposal

---

## Documentation Requirements

### Standard Library Documentation

Each module must have comprehensive documentation in `docs/source/standard-library/`:

**File Structure:**
```
docs/source/standard-library/
├── index.rst                    # Standard library overview (update with new modules)
├── env.rst                      # Environment variables module
├── args.rst                     # Command-line arguments module
├── csv.rst                      # CSV file processing module
├── log.rst                      # Structured logging module
└── crypto.rst                   # Basic cryptography module
```

### Documentation Content Requirements

Each module's documentation file must include:

**1. Module Overview**
- Purpose and use cases
- Required capabilities
- Quick start example
- Security considerations

**2. API Reference**
- All functions with signatures
- Parameter descriptions
- Return value descriptions
- Example usage for each function

**3. Common Patterns**
- Typical usage scenarios
- Best practices
- Error handling examples
- Performance considerations

**4. Integration Examples**
- Using module with other standard library modules
- Real-world application examples
- Configuration patterns

**5. Security & Capabilities**
- Detailed capability requirements
- Security best practices
- Common pitfalls to avoid

### Example Documentation Structure (env.rst)

```rst
Environment Variables (env)
===========================

.. module:: env
   :synopsis: Access and manage environment variables

The ``env`` module provides functions for reading and writing environment variables,
essential for configuration management and secret handling in ML applications.

Required Capabilities
--------------------

- ``env.read`` - Read environment variables (may expose secrets)
- ``env.write`` - Modify environment variables (affects process state)

Quick Start
-----------

.. code-block:: ml

   import env;

   // Read environment variable
   api_key = env.get("API_KEY", "default-key");

   // Get required variable (throws if missing)
   db_url = env.require("DATABASE_URL");

   // Type conversion
   port = env.get_int("PORT", 8080);
   debug = env.get_bool("DEBUG", false);

API Reference
-------------

get(key, default)
~~~~~~~~~~~~~~~~~

Get environment variable with optional default value.

**Parameters:**

- ``key`` (string) - Environment variable name
- ``default`` (string, optional) - Default value if not set

**Returns:** string or null

**Example:**

.. code-block:: ml

   api_url = env.get("API_URL", "https://api.example.com");

require(key)
~~~~~~~~~~~~

Get required environment variable or throw error if missing.

**Parameters:**

- ``key`` (string) - Environment variable name

**Returns:** string

**Throws:** RuntimeError if variable not set

**Example:**

.. code-block:: ml

   db_url = env.require("DATABASE_URL");

[Continue with all other functions...]

Common Patterns
---------------

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   import env;

   config = {
       api_url: env.require("API_URL"),
       api_key: env.require("API_KEY"),
       timeout: env.get_int("TIMEOUT", 30),
       debug: env.get_bool("DEBUG", false)
   };

Feature Flags
~~~~~~~~~~~~~

.. code-block:: ml

   enable_cache = env.get_bool("ENABLE_CACHE", true);
   if (enable_cache) {
       // Use caching
   }

Security Considerations
-----------------------

**Never Log Environment Variables:**

Environment variables may contain secrets. Avoid logging them directly:

.. code-block:: ml

   // BAD - Logs all env vars including secrets
   log.info("Environment", env.all());

   // GOOD - Log only specific non-sensitive values
   log.info("Configuration", {api_url: env.get("API_URL")});

**Use .env Files for Development:**

Never commit secrets to version control. Use .env files for local development.

**Production Secret Management:**

Use secure secret management systems in production (AWS Secrets Manager, HashiCorp Vault, etc.).

See Also
--------

- :doc:`log` - Logging module (avoid logging secrets)
- :doc:`crypto` - Cryptography module (for hashing secrets)
```

### Documentation Standards

**Style Guide:**
- Use Sphinx reStructuredText format
- Include code examples for every function
- Highlight security considerations with warnings
- Cross-reference related modules
- Include both simple and complex examples

**Code Example Standards:**
- All examples must be valid ML syntax
- Examples should be self-contained
- Show both success and error cases
- Demonstrate security best practices

**Update Standard Library Index:**

When adding new modules, update `docs/source/standard-library/index.rst`:

```rst
Standard Library Reference
===========================

Core Modules
------------

.. toctree::
   :maxdepth: 2

   builtin
   console
   file
   json
   http
   math
   ...

Essential Utilities
-------------------

.. toctree::
   :maxdepth: 2

   env
   args
   csv
   log
   crypto

[Rest of documentation...]
```

---

## Testing Strategy

### Unit Tests

Each module requires comprehensive unit tests:

**env_bridge.py:**
- ✅ Get/set environment variables
- ✅ Default values
- ✅ Type conversion (int, bool, float)
- ✅ Required variables (error on missing)
- ✅ Has/delete operations

**args_bridge.py:**
- ✅ Parse flags (short and long)
- ✅ Parse options with values
- ✅ Parse positional arguments
- ✅ Validation errors
- ✅ Help text generation
- ✅ Complex combinations

**csv_bridge.py:**
- ✅ Read CSV with headers
- ✅ Read CSV without headers
- ✅ Custom delimiters
- ✅ Write from objects
- ✅ Write from arrays
- ✅ Streaming reader/writer
- ✅ Edge cases (empty files, quoted fields, newlines in data)

**log_bridge.py:**
- ✅ All log levels
- ✅ Log formatting (text, JSON)
- ✅ Named loggers
- ✅ File output
- ✅ Context data
- ✅ Level filtering

**crypto_bridge.py:**
- ✅ Hash functions (SHA256, SHA1, MD5)
- ✅ UUID generation (v4, v5)
- ✅ Random generation (bytes, hex, string, int, float)
- ✅ HMAC operations
- ✅ Secure comparison
- ✅ File hashing

### Integration Tests

**Combined Usage:**
```ml
// Test all 5 modules together
import env;
import args;
import csv;
import log;
import crypto;

// Configure from environment
log_level = env.get("LOG_LEVEL", "INFO");
log.set_level(log_level);

// Parse CLI arguments
parser = args.create_parser("Data Processor");
parser.add_option("input", "i", "Input CSV file", "data.csv");
parser.add_option("output", "o", "Output CSV file", "output.csv");
parsed = parser.parse();

// Read CSV
log.info("Reading input file", {file: parsed.get("input")});
data = csv.read(parsed.get("input"));

// Process with crypto
for (row in data) {
    row.id = crypto.uuid();
    row.hash = crypto.sha256(row.email);
}

// Write output
log.info("Writing output file", {file: parsed.get("output"), count: len(data)});
csv.write(parsed.get("output"), data);

log.info("Processing complete");
```

### End-to-End ML Integration Tests

Each module requires comprehensive end-to-end integration tests in `tests/ml_integration/ml_stdlib/`:

**File Structure:**
```
tests/ml_integration/ml_stdlib/
├── test_env_module.ml              # Environment variables end-to-end tests
├── test_args_module.ml             # Command-line arguments end-to-end tests
├── test_csv_module.ml              # CSV file processing end-to-end tests
├── test_log_module.ml              # Structured logging end-to-end tests
├── test_crypto_module.ml           # Cryptography end-to-end tests
├── test_combined_modules.ml        # Multi-module integration scenarios
├── test_data_pipeline.ml           # Complete ETL pipeline example
└── test_cli_tool.ml                # Full CLI tool example

Supporting test data:
├── fixtures/
│   ├── test_users.csv              # Sample CSV for testing
│   ├── test_large.csv              # Large CSV for performance testing
│   └── test_invalid.csv            # Invalid CSV for error testing
└── README.md                       # Test suite documentation
```

### ML Test Requirements by Module

**test_env_module.ml** - Environment Variables:
```ml
// Test all env module functions end-to-end
import env;
import console;

// Test basic get/set
env.set("TEST_VAR", "test_value");
value = env.get("TEST_VAR");
console.assert(value == "test_value", "env.get() failed");

// Test default values
default_val = env.get("NONEXISTENT", "default");
console.assert(default_val == "default", "env.get() with default failed");

// Test type conversion
env.set("TEST_INT", "42");
env.set("TEST_BOOL", "true");
env.set("TEST_FLOAT", "3.14");

int_val = env.get_int("TEST_INT");
console.assert(int_val == 42, "env.get_int() failed");

bool_val = env.get_bool("TEST_BOOL");
console.assert(bool_val == true, "env.get_bool() failed");

float_val = env.get_float("TEST_FLOAT");
console.assert(float_val == 3.14, "env.get_float() failed");

// Test has()
console.assert(env.has("TEST_VAR") == true, "env.has() failed");
console.assert(env.has("NONEXISTENT") == false, "env.has() failed for missing var");

// Test delete()
env.delete("TEST_VAR");
console.assert(env.has("TEST_VAR") == false, "env.delete() failed");

// Test require() with missing variable (should throw)
try {
    env.require("DEFINITELY_MISSING_VAR");
    console.log("ERROR: env.require() should have thrown");
} except (error) {
    console.log("PASS: env.require() correctly threw error");
}

console.log("All env module tests passed!");
```

**test_args_module.ml** - Command-Line Arguments:
```ml
// Test argument parsing end-to-end
import args;
import console;

// Test parser creation
parser = args.create_parser("Test Tool", "Testing argument parsing");

// Add various argument types
parser.add_flag("verbose", "v", "Verbose output");
parser.add_flag("force", "f", "Force operation");
parser.add_option("output", "o", "Output file", "default.txt");
parser.add_option("format", null, "Output format", "json");
parser.add_positional("input", "Input file", true);

// Test help generation
help_text = parser.help();
console.assert(len(help_text) > 0, "Help text generation failed");
console.log("Help text generated successfully");

// Simulate parsing arguments
// Note: In real tests, we would inject test arguments
// For now, test the API structure
console.log("PASS: args module API validated");
```

**test_csv_module.ml** - CSV File Processing:
```ml
// Test CSV operations end-to-end
import csv;
import console;
import file;

// Create test data
test_data = [
    {name: "Alice", age: 30, city: "NYC"},
    {name: "Bob", age: 25, city: "LA"},
    {name: "Charlie", age: 35, city: "SF"}
];

// Test write
csv.write("test_output.csv", test_data);
console.log("CSV write successful");

// Test read
read_data = csv.read("test_output.csv");
console.assert(len(read_data) == 3, "CSV read count mismatch");
console.assert(read_data[0].name == "Alice", "CSV read data mismatch");
console.log("CSV read successful");

// Test custom delimiter
csv.write("test_tsv.csv", test_data, delimiter="\t");
tsv_data = csv.read("test_tsv.csv", delimiter="\t");
console.assert(len(tsv_data) == 3, "TSV read count mismatch");
console.log("Custom delimiter test passed");

// Test array of arrays
array_data = [
    ["Name", "Age", "City"],
    ["Alice", "30", "NYC"],
    ["Bob", "25", "LA"]
];
csv.write("test_arrays.csv", array_data, headers=false);
array_read = csv.read("test_arrays.csv", headers=false);
console.assert(len(array_read) == 3, "Array CSV read failed");
console.log("Array CSV test passed");

// Cleanup
file.delete("test_output.csv");
file.delete("test_tsv.csv");
file.delete("test_arrays.csv");

console.log("All CSV module tests passed!");
```

**test_log_module.ml** - Structured Logging:
```ml
// Test logging functionality end-to-end
import log;
import console;

// Test all log levels
log.debug("Debug message");
log.info("Info message");
log.warn("Warning message");
log.error("Error message");
log.critical("Critical message");
console.log("PASS: All log levels executed");

// Test logging with context data
log.info("User action", {user_id: 123, action: "login"});
console.log("PASS: Contextual logging executed");

// Test log level configuration
log.set_level("INFO");
console.log("PASS: Log level set");

// Test format configuration
log.set_format("json");
log.info("JSON formatted message");
log.set_format("text");
log.info("Text formatted message");
console.log("PASS: Log format configuration");

// Test named loggers
db_logger = log.create_logger("database");
db_logger.info("Database query", {duration: 0.025});
console.log("PASS: Named logger created");

// Test is_debug()
log.set_level("DEBUG");
console.assert(log.is_debug() == true, "is_debug() failed");
log.set_level("INFO");
console.assert(log.is_debug() == false, "is_debug() failed");
console.log("PASS: is_debug() validation");

console.log("All log module tests passed!");
```

**test_crypto_module.ml** - Cryptography:
```ml
// Test cryptography functions end-to-end
import crypto;
import console;

// Test hashing
sha256_hash = crypto.sha256("test_data");
console.assert(len(sha256_hash) == 64, "SHA-256 hash length incorrect");
console.log("PASS: SHA-256 hashing");

sha1_hash = crypto.sha1("test_data");
console.assert(len(sha1_hash) == 40, "SHA-1 hash length incorrect");
console.log("PASS: SHA-1 hashing");

md5_hash = crypto.md5("test_data");
console.assert(len(md5_hash) == 32, "MD5 hash length incorrect");
console.log("PASS: MD5 hashing");

// Test hashing with salt
salted_hash = crypto.sha256("password", salt="random_salt");
console.assert(len(salted_hash) == 64, "Salted hash failed");
console.log("PASS: Salted hashing");

// Test UUID generation
uuid_val = crypto.uuid();
console.assert(len(uuid_val) == 36, "UUID length incorrect");
console.log("PASS: UUID generation - " + uuid_val);

// Test deterministic UUID
uuid_det = crypto.uuid_from_string("test@example.com");
uuid_det2 = crypto.uuid_from_string("test@example.com");
console.assert(uuid_det == uuid_det2, "Deterministic UUID failed");
console.log("PASS: Deterministic UUID");

// Test random generation
hex_token = crypto.random_hex(16);
console.assert(len(hex_token) == 32, "Random hex length incorrect");
console.log("PASS: Random hex - " + hex_token);

random_str = crypto.random_string(12);
console.assert(len(random_str) == 12, "Random string length incorrect");
console.log("PASS: Random string - " + random_str);

// Test secure random numbers
rand_int = crypto.random_int(1, 100);
console.assert(rand_int >= 1 && rand_int <= 100, "Random int out of range");
console.log("PASS: Random int - " + str(rand_int));

rand_float = crypto.random_float();
console.assert(rand_float >= 0.0 && rand_float < 1.0, "Random float out of range");
console.log("PASS: Random float - " + str(rand_float));

// Test hash comparison
hash1 = crypto.sha256("password123");
hash2 = crypto.sha256("password123");
hash3 = crypto.sha256("different");

console.assert(crypto.compare_hash(hash1, hash2) == true, "Hash comparison failed for equal");
console.assert(crypto.compare_hash(hash1, hash3) == false, "Hash comparison failed for different");
console.log("PASS: Secure hash comparison");

// Test HMAC
signature = crypto.hmac("message", "secret_key");
console.assert(len(signature) == 64, "HMAC signature length incorrect");

is_valid = crypto.verify_hmac("message", signature, "secret_key");
console.assert(is_valid == true, "HMAC verification failed for valid signature");

is_invalid = crypto.verify_hmac("wrong_message", signature, "secret_key");
console.assert(is_invalid == false, "HMAC verification failed for invalid signature");
console.log("PASS: HMAC signature and verification");

console.log("All crypto module tests passed!");
```

**test_combined_modules.ml** - Multi-Module Integration:
```ml
// Test multiple modules working together
import env;
import log;
import csv;
import crypto;
import console;
import file;

// Setup environment configuration
env.set("LOG_LEVEL", "INFO");
env.set("OUTPUT_DIR", "test_output");

// Configure logging from environment
log.set_level(env.get("LOG_LEVEL"));
log.info("Integration test starting");

// Create test data with crypto
users = [
    {
        id: crypto.uuid(),
        email: "alice@example.com",
        email_hash: crypto.sha256("alice@example.com")
    },
    {
        id: crypto.uuid(),
        email: "bob@example.com",
        email_hash: crypto.sha256("bob@example.com")
    }
];

log.info("Generated test data", {count: len(users)});

// Write CSV
output_file = "test_users_combined.csv";
csv.write(output_file, users);
log.info("Wrote CSV file", {file: output_file});

// Read back and verify
read_users = csv.read(output_file);
console.assert(len(read_users) == 2, "User count mismatch");
log.info("Read CSV file", {count: len(read_users)});

// Verify hashes
for (user in read_users) {
    expected_hash = crypto.sha256(user.email);
    console.assert(user.email_hash == expected_hash, "Hash verification failed");
}
log.info("Hash verification complete");

// Cleanup
file.delete(output_file);
log.info("Cleanup complete");

console.log("All combined module tests passed!");
```

**test_data_pipeline.ml** - Complete ETL Pipeline:
```ml
// Complete data processing pipeline example
import env;
import csv;
import log;
import crypto;
import console;
import file;

log.info("ETL Pipeline test starting");

// Extract - Read source data
source_data = [
    {name: "Alice Johnson", email: "alice@example.com", age: "30", ssn: "123-45-6789"},
    {name: "Bob Smith", email: "bob@example.com", age: "25", ssn: "987-65-4321"},
    {name: "Charlie Brown", email: "charlie@example.com", age: "35", ssn: "555-12-3456"}
];

csv.write("pipeline_source.csv", source_data);
extracted = csv.read("pipeline_source.csv");
log.info("Extracted records", {count: len(extracted)});

// Transform - Add IDs, hash sensitive data
transformed = [];
for (row in extracted) {
    transformed_row = {
        id: crypto.uuid(),
        name: row.name,
        email_hash: crypto.sha256(row.email),
        age: int(row.age),
        ssn_hash: crypto.sha256(row.ssn)
    };
    transformed.append(transformed_row);
}
log.info("Transformed records", {count: len(transformed)});

// Load - Write to destination
csv.write("pipeline_output.csv", transformed);
log.info("Loaded records to output");

// Verify
output_data = csv.read("pipeline_output.csv");
console.assert(len(output_data) == 3, "Output count mismatch");
console.assert(len(output_data[0].id) == 36, "UUID format incorrect");
log.info("Pipeline validation complete");

// Cleanup
file.delete("pipeline_source.csv");
file.delete("pipeline_output.csv");

log.info("ETL Pipeline test passed!");
console.log("ETL Pipeline test completed successfully!");
```

### Integration Test Runner

Create `tests/ml_integration/ml_stdlib/README.md`:

```markdown
# Standard Library ML Integration Tests

End-to-end integration tests for mlpy standard library modules.

## Running Tests

Run all stdlib integration tests:
```bash
python tests/ml_test_runner.py --category ml_stdlib --full
```

Run specific module tests:
```bash
mlpy run tests/ml_integration/ml_stdlib/test_env_module.ml
mlpy run tests/ml_integration/ml_stdlib/test_crypto_module.ml
```

## Test Categories

- **test_env_module.ml** - Environment variable operations
- **test_args_module.ml** - Command-line argument parsing
- **test_csv_module.ml** - CSV file reading/writing
- **test_log_module.ml** - Structured logging
- **test_crypto_module.ml** - Cryptographic operations
- **test_combined_modules.ml** - Multi-module integration
- **test_data_pipeline.ml** - Complete ETL pipeline
- **test_cli_tool.ml** - Full CLI tool example

## Success Criteria

✅ All tests must pass the complete ML→Python transpilation pipeline
✅ All assertions must pass
✅ No security threats detected
✅ Proper error handling demonstrated
✅ Performance within acceptable limits

## Test Data

The `fixtures/` directory contains:
- Sample CSV files for testing
- Large datasets for performance validation
- Invalid data for error handling tests
```

### Integration Test Validation

Each ML test file must:

1. **Parse Successfully** - Valid ML syntax, no grammar errors
2. **Pass Security Analysis** - No threats detected
3. **Transpile Successfully** - Generate valid Python code
4. **Execute Successfully** - All assertions pass
5. **Demonstrate Real Usage** - Practical examples of module functionality

### Test Coverage Requirements

**Per Module:**
- ✅ All public API functions tested
- ✅ Error conditions tested (try/except blocks)
- ✅ Edge cases covered
- ✅ Integration with other modules
- ✅ Performance acceptable

**Overall Integration:**
- ✅ Multi-module scenarios
- ✅ Real-world application examples
- ✅ Configuration-driven workflows
- ✅ Error propagation across modules

### Performance Tests

- **csv:** Large file processing (100MB+ files)
- **log:** High-volume logging (1000+ messages/sec)
- **crypto:** Hash performance (1000+ hashes/sec)

### Security Tests

- **env:** Attempt to access without capability
- **csv:** Path traversal attempts
- **log:** Log injection attempts
- **crypto:** Timing attack resistance

---

## Implementation Roadmap

### Phase 1: Foundation (Days 1-2) - ✅ **100% COMPLETE**

**Day 1: env module**
- ✅ **COMPLETE** - Implement `env_bridge.py` (10 functions)
- ✅ **COMPLETE** - Python unit tests (tests/unit/stdlib/test_env_bridge.py - 28 tests, 100% coverage)
- ✅ **COMPLETE** - ML integration test: `test_env_module.ml` (13 tests, passing)
- ✅ **COMPLETE** - Documentation: `docs/source/standard-library/env.rst` (700+ lines)
- ✅ **COMPLETE** - Updated test runner with env.read, env.write capabilities

**Day 2: crypto module**
- ✅ **COMPLETE** - Implement `crypto_bridge.py` (16 functions: hashing, UUID, HMAC, secure random)
- ✅ **COMPLETE** - Python unit tests (tests/unit/stdlib/test_crypto_bridge.py - 42 tests, 100% passing)
- ✅ **COMPLETE** - ML integration test: `test_crypto_module.ml` (20 tests, passing)
- ✅ **COMPLETE** - Documentation: `docs/source/standard-library/crypto.rst` (1000+ lines comprehensive)
- ✅ **COMPLETE** - Updated test runner with crypto.hash, crypto.random capabilities

**Deliverable:** ✅ **PHASE 1 COMPLETE** - env and crypto modules 100% complete with full documentation

**Test Results:** 25/25 stdlib tests passing (100% success rate)

**Lines of Code:**
- Implementation: 350+ lines (env_bridge.py + crypto_bridge.py)
- Unit Tests: 450+ lines (70 tests total)
- ML Integration: 400+ lines (33 end-to-end tests)
- Documentation: 1700+ lines (comprehensive Sphinx docs)

---

### Phase 2: Data Processing (Days 3-4) - ✅ **100% COMPLETE**

**Day 3: csv module**
- ✅ **COMPLETE** - Implement `csv_bridge.py` (8 functions: read, write, read_string, write_string, count_rows, get_headers, append)
- ✅ **COMPLETE** - Python unit tests (tests/unit/stdlib/test_csv_bridge.py - 27 tests, 100% passing)
- ✅ **COMPLETE** - ML integration test: `test_csv_module.ml` (15 tests, passing)
- ✅ **COMPLETE** - Create test fixtures: `fixtures/test_users.csv`
- ✅ **COMPLETE** - Documentation: `docs/source/standard-library/csv.rst` (800+ lines, comprehensive)

**Deliverable:** ✅ csv module 100% complete

**Test Results:** 26/26 stdlib tests passing (100% success rate)

**Lines of Code:**
- Implementation: 300+ lines (csv_bridge.py)
- Unit Tests: 350+ lines (27 tests)
- ML Integration: 180+ lines (15 end-to-end tests)
- Documentation: 800+ lines (comprehensive API reference, patterns, examples)

---

### Phase 3: Observability (Days 5-6) - ✅ **100% COMPLETE**

**Day 5-6: log module**
- ✅ **COMPLETE** - Implement `log_bridge.py` (11 functions: debug, info, warn, error, critical, set_level, set_format, add_file, set_timestamp, is_debug, create_logger)
- ✅ **COMPLETE** - Logger class with text/JSON formatting and named loggers
- ✅ **COMPLETE** - Python unit tests (tests/unit/stdlib/test_log_bridge.py - 30 tests, 100% passing)
- ✅ **COMPLETE** - ML integration test: `test_log_module.ml` (20 tests, passing)
- ✅ **COMPLETE** - Documentation: `docs/source/standard-library/log.rst` (1000+ lines, comprehensive)

**Deliverable:** ✅ log module 100% complete

**Test Results:** 27/27 stdlib tests passing (100% success rate)

**Lines of Code:**
- Implementation: 330+ lines (log_bridge.py with Logger class)
- Unit Tests: 370+ lines (30 tests)
- ML Integration: 160+ lines (20 end-to-end tests)
- Documentation: 1000+ lines (comprehensive API reference, patterns, examples)

---

### Phase 4: CLI Tools (Days 7-9)

**Day 7-9: args**
- ✅ Implement `args_bridge.py`
- ✅ ArgParser and ParsedArgs classes
- ✅ Help text generation
- ✅ Python unit tests (complex argument patterns)
- ✅ ML integration test: `test_args_module.ml`
- ✅ Documentation: `docs/source/standard-library/args.rst`
- ✅ Complete end-to-end test: `test_cli_tool.ml`

**Deliverable:** Complete CLI tool support with full documentation

---

### Phase 5: Integration & Polish (Days 10-11)

**Day 10: Complete Integration**
- ✅ Complete `test_data_pipeline.ml` (full ETL example)
- ✅ Complete `test_cli_tool.ml` (comprehensive CLI tool)
- ✅ Update `test_combined_modules.ml` (all 5 modules)
- ✅ Performance benchmarks for csv and log modules
- ✅ Security validation (capability testing)
- ✅ Create test runner integration for `ml_stdlib` category

**Day 11: Documentation & Polish**
- ✅ Update `docs/source/standard-library/index.rst` with new modules
- ✅ Add "Essential Utilities" section to stdlib index
- ✅ Create `tests/ml_integration/ml_stdlib/README.md`
- ✅ Review all documentation for completeness
- ✅ Update CLAUDE.md with new standard library modules
- ✅ Create implementation summary document

**Deliverable:** Production-ready module suite with enterprise-grade documentation

---

### Timeline Summary

| Phase | Duration | Modules | Deliverables |
|-------|----------|---------|-------------|
| **Phase 1** | 2 days | env, crypto | Implementation + Unit Tests + ML Tests + Docs |
| **Phase 2** | 2 days | csv | Implementation + Unit Tests + ML Tests + Docs |
| **Phase 3** | 2 days | log | Implementation + Unit Tests + ML Tests + Docs |
| **Phase 4** | 3 days | args | Implementation + Unit Tests + ML Tests + Docs |
| **Phase 5** | 2 days | Integration | Complete testing + Documentation finalization |

**Total: 11 days (comprehensive with documentation and testing)**
**Realistic: 8-10 days with focused effort**

### Deliverable Checklist per Module

Each module completion requires:

**Python Implementation:**
- ✅ Bridge module in `src/mlpy/stdlib/`
- ✅ Decorator annotations with capabilities
- ✅ Docstrings for all public functions
- ✅ Type hints throughout

**Python Unit Tests:**
- ✅ Test file in `tests/unit/stdlib/`
- ✅ 95%+ code coverage
- ✅ Edge cases and error conditions tested
- ✅ All public API functions covered

**ML Integration Tests:**
- ✅ End-to-end .ml test file in `tests/ml_integration/ml_stdlib/`
- ✅ Tests all major functions
- ✅ Validates ML→Python transpilation
- ✅ Includes assertions and error handling
- ✅ Demonstrates real-world usage patterns

**Documentation:**
- ✅ Complete .rst file in `docs/source/standard-library/`
- ✅ Module overview and purpose
- ✅ Required capabilities documented
- ✅ API reference for all functions
- ✅ Common patterns and examples
- ✅ Security considerations
- ✅ Integration examples

**Validation:**
- ✅ All Python unit tests pass
- ✅ ML integration test parses successfully
- ✅ ML integration test passes security analysis
- ✅ ML integration test transpiles to valid Python
- ✅ ML integration test executes successfully
- ✅ Documentation builds without errors
- ✅ Code follows style guidelines (Black, Ruff, MyPy)

---

## Integration Examples

### Example 1: CLI Data Processing Tool

```ml
// data-processor.ml - Complete CLI tool using all 5 modules
import env;
import args;
import csv;
import log;
import crypto;

// Configure logging from environment
log_level = env.get("LOG_LEVEL", "INFO");
log.set_level(log_level);

if (env.get_bool("LOG_TO_FILE", false)) {
    log.add_file("processor.log");
}

// Parse command-line arguments
parser = args.create_parser(
    "Data Processor",
    "Process CSV files with hashing and UUID generation"
);

parser.add_option("input", "i", "Input CSV file", null);
parser.add_option("output", "o", "Output CSV file", "output.csv");
parser.add_flag("hash-emails", null, "Hash email addresses");
parser.add_flag("add-ids", null, "Add UUID to each row");
parser.add_option("format", "f", "Log format: text or json", "text");

try {
    parsed = parser.parse();
} except (error) {
    console.log("Error: " + error.message);
    console.log(parser.help());
    return;
}

// Validate required arguments
input_file = parsed.get("input");
if (input_file == null) {
    console.log("Error: --input is required");
    console.log(parser.help());
    return;
}

// Configure log format
log.set_format(parsed.get("format"));

// Process CSV
log.info("Starting data processing", {
    input: input_file,
    output: parsed.get("output")
});

try {
    // Read input
    data = csv.read(input_file);
    log.info("Read input file", {rows: len(data)});

    // Process rows
    processed = 0;
    for (row in data) {
        // Add UUID if requested
        if (parsed.get_bool("add-ids")) {
            row.id = crypto.uuid();
        }

        // Hash emails if requested
        if (parsed.get_bool("hash-emails") && row.email) {
            row.email_hash = crypto.sha256(row.email);
            row.email = "[REDACTED]";
        }

        processed = processed + 1;

        if (processed % 1000 == 0) {
            log.debug("Progress", {processed: processed, total: len(data)});
        }
    }

    // Write output
    csv.write(parsed.get("output"), data);
    log.info("Processing complete", {
        rows: len(data),
        output: parsed.get("output")
    });

} except (error) {
    log.error("Processing failed", {error: error.message});
    throw error;
}
```

**Usage:**
```bash
# Development mode
export LOG_LEVEL=DEBUG
mlpy run data-processor.ml --input users.csv --output processed.csv --hash-emails --add-ids

# Production mode
export LOG_LEVEL=INFO
export LOG_TO_FILE=true
mlpy run data-processor.ml -i users.csv -o processed.csv --hash-emails --format json
```

---

### Example 2: Configuration-Driven Application

```ml
// app.ml - Application with environment-based configuration
import env;
import log;
import crypto;

// Load configuration from environment
config = {
    api_url: env.require("API_URL"),
    api_key: env.require("API_KEY"),
    db_host: env.get("DB_HOST", "localhost"),
    db_port: env.get_int("DB_PORT", 5432),
    db_name: env.require("DB_NAME"),
    cache_enabled: env.get_bool("CACHE_ENABLED", true),
    debug_mode: env.get_bool("DEBUG", false),
    log_level: env.get("LOG_LEVEL", "INFO"),
    max_retries: env.get_int("MAX_RETRIES", 3),
    timeout: env.get_float("TIMEOUT", 30.0)
};

// Configure logging
log.set_level(config.log_level);
if (config.debug_mode) {
    log.set_format("text");
} else {
    log.set_format("json");
    log.add_file("app.log");
}

// Application startup
log.info("Application starting", {
    api_url: config.api_url,
    db_host: config.db_host,
    db_port: config.db_port,
    cache_enabled: config.cache_enabled
});

// Generate session ID
session_id = crypto.uuid();
log.info("Session created", {session_id: session_id});

// Application logic here...
```

**Environment file (.env):**
```bash
API_URL=https://api.example.com
API_KEY=sk_live_abc123xyz
DB_HOST=postgres.example.com
DB_PORT=5432
DB_NAME=production_db
CACHE_ENABLED=true
DEBUG=false
LOG_LEVEL=INFO
MAX_RETRIES=5
TIMEOUT=60.0
```

---

### Example 3: Data ETL Pipeline

```ml
// etl.ml - Extract, Transform, Load pipeline
import csv;
import log;
import crypto;
import env;

// Configure
log.set_level(env.get("LOG_LEVEL", "INFO"));
log.add_file("etl.log");

log.info("ETL Pipeline starting");

// Extract
log.info("Extracting data from source");
source_data = csv.read("raw_data.csv");
log.info("Extracted records", {count: len(source_data)});

// Transform
log.info("Transforming data");
transformed = [];
errors = 0;

for (row in source_data) {
    try {
        // Add unique ID
        row.id = crypto.uuid();

        // Hash sensitive data
        if (row.ssn) {
            row.ssn_hash = crypto.sha256(row.ssn);
            row.ssn = null;  // Remove original
        }

        // Validate and transform
        if (row.age) {
            age = int(row.age);
            if (age < 0 || age > 150) {
                log.warn("Invalid age", {row_id: row.id, age: age});
                errors = errors + 1;
                continue;
            }
        }

        transformed.append(row);

    } except (error) {
        log.error("Transform error", {error: error.message});
        errors = errors + 1;
    }
}

log.info("Transformation complete", {
    success: len(transformed),
    errors: errors
});

// Load
log.info("Loading data to destination");
csv.write("transformed_data.csv", transformed);
log.info("ETL Pipeline complete", {records: len(transformed)});
```

---

## Conclusion

### Summary

This proposal defines 5 essential standard library modules that fill critical gaps in ML's general-purpose programming capabilities:

1. **env** - Configuration and secrets management
2. **args** - CLI tool development
3. **csv** - Data processing and ETL
4. **log** - Debugging and monitoring
5. **crypto** - Security basics

### Impact

**Use Case Coverage:**
- ✅ CLI Tools: Complete support with args + env + log
- ✅ Data Processing: ETL pipelines with csv + log
- ✅ Web Applications: Configuration and logging with env + log + crypto
- ✅ Automation: DevOps scripts with all 5 modules

**Developer Experience:**
- 80% of missing general-purpose functionality covered
- Familiar APIs (inspired by Node.js, Python stdlib)
- Security-first design with capability system
- Comprehensive documentation and examples

### Effort & Timeline

**Total Effort:** 8-11 days (comprehensive with documentation and testing)

**Per Module Breakdown:**
1. **env** (1.5 days) - Implementation + Unit Tests + ML Tests + Documentation
2. **crypto** (1.5 days) - Implementation + Unit Tests + ML Tests + Documentation
3. **csv** (2 days) - Implementation + Classes + Unit Tests + ML Tests + Docs
4. **log** (2 days) - Implementation + Classes + Unit Tests + ML Tests + Docs
5. **args** (3 days) - Implementation + Classes + Unit Tests + ML Tests + Docs (most complex)
6. **Integration** (2 days) - Combined tests + Documentation polish + Validation

**Priority Order:**
1. env (critical for configuration)
2. crypto (security and utility)
3. csv (data processing)
4. log (observability)
5. args (CLI tools - most complex)

### Recommendation

**✅ PROCEED** with implementation following the comprehensive phased roadmap:
- **Phase 1:** env + crypto (foundation) + Documentation + ML Tests
- **Phase 2:** csv (data processing) + Documentation + ML Tests
- **Phase 3:** log (observability) + Documentation + ML Tests
- **Phase 4:** args (CLI tools) + Documentation + ML Tests
- **Phase 5:** Integration, documentation polish, and final validation

**Key Success Criteria:**
- ✅ All 5 modules implemented with Python unit tests (95%+ coverage)
- ✅ All 5 modules have comprehensive ML integration tests in `tests/ml_integration/ml_stdlib/`
- ✅ All 5 modules have complete Sphinx documentation in `docs/source/standard-library/`
- ✅ All ML tests pass through complete transpilation pipeline
- ✅ Security validation passes (capability system tested)
- ✅ Performance benchmarks acceptable

### Next Steps

1. **Approve proposal** - Confirm comprehensive approach with documentation and testing
2. **Setup test infrastructure** - Create `tests/ml_integration/ml_stdlib/` directory
3. **Begin Phase 1** - Implement env and crypto modules with full deliverables
   - Python implementation + unit tests
   - ML integration tests (`test_env_module.ml`, `test_crypto_module.ml`)
   - Complete Sphinx documentation (`env.rst`, `crypto.rst`)
4. **Validate Phase 1** - Ensure all tests pass and docs build successfully
5. **Iterate remaining phases** - Continue with csv, log, args following same pattern
6. **Final integration** - Complete combined tests and documentation index updates

---

**Document Status:** Ready for Implementation with Comprehensive Testing & Documentation
**Last Updated:** 2025-11-10
**Next Action:** Begin Phase 1 implementation (env + crypto modules with full test suite and documentation)
