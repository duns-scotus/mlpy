# Standard Library I/O Capabilities Documentation

## Overview

The ML standard library I/O modules (`file`, `path`, `http`) implement fine-grained capability-based security. This document explains how to configure and restrict access using capability patterns.

## Capability System Basics

### Simple Capabilities

Grant broad access to entire module capabilities:

```ml
// Grant all file read operations
capabilities: ["file.read"]

// Grant all file write operations
capabilities: ["file.write"]

// Grant all HTTP requests
capabilities: ["network.http", "network.https"]
```

### Fine-Grained Path Restrictions

Restrict file/path operations to specific directories or patterns:

```ml
// Read files only in /data directory
capabilities: ["file.read:/data/*"]

// Write files only to /output and /tmp
capabilities: ["file.write:/output/*", "file.write:/tmp/*"]

// Delete only temporary files
capabilities: ["file.delete:/tmp/*"]

// Create directories only under /projects
capabilities: ["path.write:/projects/*"]
```

### Fine-Grained Network Restrictions

Restrict HTTP requests to specific domains or URL patterns:

```ml
// Allow only specific API domain
capabilities: ["network.https:api.example.com"]

// Allow all subdomains of example.com
capabilities: ["network.https:*.example.com"]

// Allow specific URL path patterns
capabilities: ["network.https:api.example.com/v1/*"]

// Allow multiple specific domains
capabilities: [
    "network.https:api.example.com",
    "network.https:cdn.example.com"
]
```

## File Module Capabilities

### file.read

**Description:** Read file contents

**Pattern Syntax:**
- `file.read` - Read any file
- `file.read:/path/to/dir/*` - Read files in specific directory
- `file.read:/data/**/*.txt` - Read .txt files recursively in /data
- `file.read:~/.config/*` - Read files in user config directory

**Example Usage:**

```ml
import file;

// Requires: file.read
content = file.read("/data/config.json");

// Requires: file.read:/data/*
lines = file.readLines("/data/log.txt");

// Requires: file.read
binary = file.readBytes("/images/photo.jpg");
```

**Security Considerations:**
- Path traversal is prevented (../ resolved before capability check)
- Symlinks are resolved to canonical paths
- Capability check happens after path canonicalization

### file.write

**Description:** Write or create files

**Pattern Syntax:**
- `file.write` - Write to any location
- `file.write:/output/*` - Write only to /output directory
- `file.write:/tmp/*` - Write only to temporary directory
- `file.write:**/results/*.json` - Write .json files anywhere under results/

**Example Usage:**

```ml
import file;

// Requires: file.write
file.write("/output/data.txt", "Hello World");

// Requires: file.write:/output/*
file.writeLines("/output/log.txt", ["line 1", "line 2"]);

// Requires: file.write (creates parent directories)
file.writeBytes("/output/subdir/image.png", binary_data);
```

**Security Considerations:**
- Parent directories are created automatically if missing
- Overwrites existing files without warning
- Use file.append for safer incremental writes

### file.append

**Description:** Append to existing files

**Pattern Syntax:**
- `file.append` - Append to any file
- `file.append:/logs/*` - Append only to log files
- `file.append:**/*.log` - Append to .log files anywhere

**Example Usage:**

```ml
import file;

// Requires: file.append:/logs/*
file.append("/logs/application.log", timestamp + " - " + message + "\n");
```

### file.delete

**Description:** Delete files (not directories)

**Pattern Syntax:**
- `file.delete` - Delete any file
- `file.delete:/tmp/*` - Delete only temporary files
- `file.delete:**/cache/*` - Delete cache files anywhere

**Example Usage:**

```ml
import file;

// Requires: file.delete:/tmp/*
if (file.exists("/tmp/temp.dat")) {
    file.delete("/tmp/temp.dat");
}
```

**Security Considerations:**
- Only deletes files, not directories (use path.removeDir for directories)
- No confirmation or recovery
- Returns false if file doesn't exist (no error)

### file.copy and file.move

**Description:** Copy or move files

**Capabilities Required:**
- `file.copy` requires: `file.read` (source) + `file.write` (destination)
- `file.move` requires: `file.read` + `file.write` + `file.delete`

**Example Usage:**

```ml
import file;

// Requires: file.read:/data/* AND file.write:/backup/*
file.copy("/data/important.txt", "/backup/important.txt");

// Requires: file.read + file.write + file.delete
file.move("/tmp/upload.dat", "/data/processed.dat");
```

## Path Module Capabilities

### path.read

**Description:** List directories, walk filesystem

**Pattern Syntax:**
- `path.read` - Read any directory structure
- `path.read:/data/*` - List only /data directory
- `path.read:/projects/**` - Walk /projects recursively

**Example Usage:**

```ml
import path;

// Requires: path.read:/data/*
files = path.listDir("/data");

// Requires: path.read
txt_files = path.glob("/data/**/*.txt");

// Requires: path.read:/projects/**
all_files = path.walk("/projects", 3);  // Max depth 3
```

**Security Considerations:**
- Returns only file/directory names or relative paths
- Does not expose file contents (use file.read for that)
- Glob patterns are powerful but capability-restricted

### path.write

**Description:** Create or remove directories

**Pattern Syntax:**
- `path.write` - Create/remove any directory
- `path.write:/output/*` - Manage only /output subdirectories
- `path.write:/tmp/**` - Manage /tmp directory tree

**Example Usage:**

```ml
import path;

// Requires: path.write:/output/*
path.createDir("/output/results");

// Requires: path.write
path.createDir("/a/b/c/d", true);  // Creates all parents

// Requires: path.write:/tmp/*
path.removeDir("/tmp/empty");  // Only if empty

// Requires: path.write:/tmp/* (DANGEROUS)
path.removeDirRecursive("/tmp/data");  // Deletes everything
```

**Security Considerations:**
- `removeDir` only removes empty directories
- `removeDirRecursive` is DANGEROUS - removes all contents
- Parent directories created by default (no error if exists)

### No Capability Required

Many path operations are pure path manipulation and require no capabilities:

```ml
import path;

// Pure path operations (no capabilities)
full_path = path.join("dir", "file.txt");
dir = path.dirname("/path/to/file");
name = path.basename("/path/to/file.txt");
ext = path.extname("file.txt");
abs = path.absolute("../relative/path");
norm = path.normalize("/path/./to/../file");

// Metadata operations (no capabilities)
exists = path.exists("/some/path");
is_file = path.isFile("/data/file.txt");
is_dir = path.isDirectory("/data");

// System paths (no capabilities)
current = path.cwd();
home = path.home();
temp = path.tempDir();
```

## HTTP Module Capabilities

### network.http / network.https

**Description:** Make HTTP/HTTPS requests

**Pattern Syntax:**
- `network.http` - HTTP requests to any domain
- `network.https` - HTTPS requests to any domain
- `network.https:api.example.com` - Only specific domain
- `network.https:*.example.com` - Domain and all subdomains
- `network.https:api.example.com/v1/*` - Specific URL path pattern

**Example Usage:**

```ml
import http;

// Requires: network.https:api.github.com
response = http.get("https://api.github.com/users/octocat");

// Requires: network.https:api.example.com
response = http.post("https://api.example.com/items", {
    body: json.stringify({name: "Item"}),
    headers: {"Content-Type": "application/json"}
});

// Requires: network.https (any domain)
response = http.request({
    method: "PUT",
    url: "https://api.service.com/resource/123",
    headers: {"Authorization": "Bearer " + token},
    body: data
});
```

**Security Considerations:**
- Default timeout: 30 seconds (prevents hanging)
- Maximum response size: 10MB (prevents memory exhaustion)
- User-Agent automatically set if not provided
- Error responses (4xx, 5xx) return HttpResponse (not exceptions)

### URL Encoding (No Capability Required)

```ml
import http;

// Pure string operations (no capabilities)
encoded = http.encodeURI("hello world");  // "hello%20world"
decoded = http.decodeURI("hello%20world"); // "hello world"

query_string = http.encodeQuery({name: "John", age: 30});
// "name=John&age=30"

params = http.parseQuery("name=John&age=30");
// {name: "John", age: "30"}
```

## Capability Configuration Examples

### Example 1: Data Processing Application

**Scenario:** Process data files from /input, write results to /output, no network

```python
capabilities = [
    "file.read:/input/*",        # Read input files
    "file.write:/output/*",       # Write output files
    "path.read:/input/*",         # List input directory
    "path.write:/output/*",       # Create output subdirectories
]
```

### Example 2: Web Scraper

**Scenario:** Fetch data from specific APIs, save to /data, log to /logs

```python
capabilities = [
    "network.https:api.github.com",     # GitHub API
    "network.https:api.reddit.com",     # Reddit API
    "file.write:/data/*",                # Save scraped data
    "file.append:/logs/*.log",           # Append to logs
    "path.write:/data/*",                # Create data subdirectories
]
```

### Example 3: Log Analyzer

**Scenario:** Read logs from multiple sources, generate reports

```python
capabilities = [
    "file.read:/var/log/**/*.log",      # Read system logs
    "file.read:/app/logs/*",             # Read application logs
    "file.write:/reports/*",             # Write analysis reports
    "path.read:/var/log/**",             # Walk log directories
    "path.write:/reports/*",             # Create report directories
]
```

### Example 4: API Integration Service

**Scenario:** Call external APIs, cache responses, no local file writes

```python
capabilities = [
    "network.https:*.example.com",      # Example.com services
    "network.https:api.stripe.com",     # Payment API
    "file.read:/config/*",               # Read config files only
    "file.write:/tmp/cache/*",           # Cache in temp directory
]
```

### Example 5: Backup Utility

**Scenario:** Read source files, write to backup location, delete old backups

```python
capabilities = [
    "file.read:/home/user/**",          # Read all user files
    "file.write:/backup/**",             # Write to backup location
    "file.delete:/backup/old/*",         # Delete old backups
    "path.read:/home/user/**",           # Walk user directories
    "path.write:/backup/**",             # Create backup structure
]
```

## Advanced Patterns

### Wildcard Patterns

**Single wildcard `*`** - Matches any characters except path separator:
```python
"file.read:/data/*.txt"           # Files in /data only, not subdirs
"network.https:api.*.example.com" # api.sub.example.com, not api.example.com
```

**Recursive wildcard `**`** - Matches any characters including path separator:
```python
"file.read:/data/**/*.json"       # All .json files under /data recursively
"path.read:/projects/**"          # All subdirectories of /projects
```

**Character sets `[abc]`** - Matches any character in set:
```python
"file.read:/logs/app[123].log"    # app1.log, app2.log, app3.log
"file.write:/data/file[0-9].txt"  # file0.txt through file9.txt
```

### Combining Patterns

Multiple patterns = OR logic (any match grants access):

```python
capabilities = [
    "file.read:/data/*.json",      # JSON in /data
    "file.read:/config/*.json",    # OR JSON in /config
    "file.read:/backup/**/*.json", # OR JSON anywhere in /backup
]
```

### Deny Patterns (Future)

Future enhancement - explicit deny overrides allow:

```python
capabilities = [
    "file.read:/data/**",          # Read all of /data
    "!file.read:/data/secrets/*",  # EXCEPT secrets directory
]
```

## Implementation Notes

### Path Canonicalization

All paths are canonicalized before capability checks:

1. `~` expanded to user home directory
2. Relative paths converted to absolute
3. `.` and `..` resolved
4. Symlinks resolved (or rejected)
5. Normalized to OS path format

**Example:**
```ml
// User requests: file.read("../data/./file.txt")
// Canonicalized to: /home/user/project/data/file.txt
// Capability checked: "file.read:/home/user/project/data/*"
```

### Security Best Practices

1. **Principle of Least Privilege:** Grant minimal capabilities needed
2. **Specific Over General:** Use path patterns instead of broad access
3. **Separate Read/Write:** Don't grant write when only read needed
4. **Time-Limited Tokens:** Use capability tokens with expiration
5. **Audit Logging:** Log all file/network operations for review
6. **Test Restrictions:** Verify capability patterns work as expected

### Performance Considerations

- Capability checks are fast (pattern matching, not I/O)
- Path canonicalization adds minimal overhead
- HTTP timeouts prevent resource exhaustion
- Response size limits prevent memory issues

## Testing Capabilities

### Verify Restrictions Work

```ml
import file;

// Should succeed (within capability)
content = file.read("/data/allowed.txt");

// Should fail (outside capability)
try {
    content = file.read("/etc/passwd");  // CapabilityError
} catch (err) {
    console.log("Correctly blocked: " + err);
}
```

### Test Capability Patterns

```python
# Test configuration
test_capabilities = [
    "file.read:/data/*",
    "file.write:/output/*",
    "network.https:api.example.com"
]

# Run ML code with test capabilities
# Verify expected operations succeed/fail
```

## Future Enhancements

1. **Deny Patterns:** Explicit deny rules (`!pattern`)
2. **Time-Based Capabilities:** Expiring capability tokens
3. **Rate Limiting:** Limit requests per minute/hour
4. **Quota Management:** Maximum bytes read/written
5. **Audit Trails:** Automatic logging of all capability checks
6. **Dynamic Capabilities:** Runtime capability elevation (with confirmation)

## Related Documentation

- [Capability System Architecture](../architecture/capabilities.md)
- [Security Model](../security/model.md)
- [Standard Library Reference](../reference/stdlib.md)
