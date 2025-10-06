# User-Defined Modules & Advanced Import Systems Proposal

**Status:** Draft
**Created:** 2025-10-06
**Author:** mlpy Development Team
**Version:** 1.0
**Priority:** HIGH - Critical for ecosystem growth

## Executive Summary

This proposal documents the current state of mlpy's module system, identifies critical gaps preventing user-defined module imports, and proposes a comprehensive design for advanced import systems including HTTP, database, and custom protocol support.

**Current State:**
- ✅ Complete module resolution infrastructure exists (`ModuleResolver`)
- ✅ Support for user-defined `.ml` modules from filesystem paths
- ❌ **CRITICAL BUG:** Code generator doesn't integrate with resolver, comments out user imports
- ❌ No alternative import systems (HTTP, database, custom protocols)

**Proposed Solution:**
1. **Phase 1:** Fix code generator to enable user module imports (2-3 days)
2. **Phase 2:** Design and implement import protocol abstraction (1-2 weeks)
3. **Phase 3:** Implement HTTP/HTTPS importer with security (2-3 weeks)
4. **Phase 4:** Plugin system for custom importers (1-2 weeks)

---

## Current Module System Architecture

### 1. Module Resolution System (`src/mlpy/ml/resolution/resolver.py`)

**Status:** ✅ **Fully Implemented** (512 lines)

#### Core Components

**ModuleResolver Class:**
- Resolves module imports from multiple sources
- Manages import paths and search strategies
- Integrates with capability system for security
- Provides caching with dependency tracking
- Detects circular dependencies

**Resolution Strategy (in order):**

```python
def resolve_import(self, import_target: list[str], source_file: str | None) -> ModuleInfo:
    """
    Resolution Order:
    1. Check cache (with staleness validation)
    2. ML Standard Library (console, math, datetime, etc.)
    3. User modules from import_paths
    4. Current directory (if allow_current_dir=True)
    5. Python whitelist (math, json, random, etc.)
    6. Raise ImportError if not found
    """
```

**Features:**

1. **Import Path Configuration:**
   - Multiple search directories: `['./lib', './modules', './packages']`
   - Security validation: Only allowed paths accessible
   - Nested module support: `import utils.math` → `utils/math.ml`
   - Package-style modules: `import utils` → `utils/__init__.ml`

2. **Caching System:**
   - File modification time tracking
   - Dependency-based invalidation
   - Circular dependency detection with DFS cycle finding
   - Cache statistics and management

3. **Security Integration:**
   - Capability validation for file access
   - Path restriction enforcement
   - Prevents directory traversal attacks
   - Validates file existence and permissions

4. **Dependency Management:**
   - Extracts imports from AST
   - Builds dependency graph
   - Detects circular dependencies with path reporting
   - Recursive dependency resolution

#### Example Usage

```python
from mlpy.ml.resolution.resolver import ModuleResolver
from mlpy.runtime.capabilities.manager import get_capability_manager

# Create resolver with import paths
resolver = ModuleResolver(
    import_paths=['./lib', './modules', './third_party'],
    capability_manager=get_capability_manager(),
    allow_current_dir=False  # Security: disabled by default
)

# Resolve a user module
try:
    module_info = resolver.resolve_import(['utils', 'math'], source_file='main.ml')
    print(f"Resolved: {module_info.file_path}")
    print(f"Dependencies: {module_info.dependencies}")
except ImportError as e:
    print(f"Import failed: {e}")
```

#### CLI Integration (`src/mlpy/cli/import_config.py`)

**Status:** ✅ **Fully Implemented** (239 lines)

```bash
# Configure import paths via CLI
mlpy run main.ml --import-paths "./lib:./modules:./third_party"

# Allow current directory imports (use with caution)
mlpy run main.ml --import-paths "./lib" --allow-current-dir

# Python compatibility mode
mlpy run main.ml --stdlib-mode python --allow-python-modules "requests,numpy"
```

**Configuration API:**

```python
from mlpy.cli.import_config import ImportConfiguration

config = ImportConfiguration(
    import_paths=['./lib', './modules'],
    allow_current_dir=False,
    stdlib_mode='native',
    python_whitelist=['requests', 'numpy']
)

# Apply globally
config.apply_global_config()

# Get summary
print(config.get_config_summary())
```

### 2. Module Cache System (`src/mlpy/ml/resolution/cache.py`)

**Features:**
- File modification tracking
- Dependency-based invalidation
- LRU eviction policy
- Thread-safe operations
- Cache statistics

**Usage:**
```python
from mlpy.ml.resolution.cache import get_module_cache

cache = get_module_cache()
cache.put(module_path='utils.math', module_info=info, source_code=source)
cached = cache.get_simple('utils.math')
cache.invalidate('utils.math')  # Clear specific module
cache.clear()  # Clear all
```

### 3. Grammar Support (`src/mlpy/ml/grammar/ml.lark`)

**Import Statement Syntax:**

```lark
import_statement: "import" import_target ("as" IDENTIFIER)? ";"
import_target: IDENTIFIER ("." IDENTIFIER)*
```

**Examples:**

```ml
// Simple import
import math;

// Nested module
import utils.math;

// With alias
import utils.math as umath;

// Package import
import mypackage;  // Looks for mypackage/__init__.ml
```

---

## CRITICAL GAP: Code Generator Issue

### Problem Statement

**Location:** `src/mlpy/ml/codegen/python_generator.py` (lines 425-473)

The code generator has a **hardcoded whitelist** of standard library modules and **comments out all unknown imports**, including valid user-defined modules that the `ModuleResolver` can successfully find.

**Current Code:**

```python
def visit_import_statement(self, node: ImportStatement):
    """Generate code for import statement."""
    module_path = ".".join(node.target)

    # Hardcoded stdlib list
    if module_path in [
        "math", "json", "datetime", "random", "collections",
        "console", "string", "array", "functional", "regex",
        "file", "path", "http",
    ]:
        # Generate import for stdlib
        python_module_path = f"mlpy.stdlib.{module_path}_bridge"
        self._emit_line(f"from {python_module_path} import {module_path}", node)
    else:
        # ❌ BUG: Comments out user modules!
        self._emit_line(f"# WARNING: Import '{module_path}' requires security review", node)
        self._emit_line(f"# import {module_path}", node)
```

**Impact:**

```ml
// user_module.ml
function add(a, b) {
    return a + b;
}

// main.ml
import user_module;  // ❌ Will be commented out!

function main() {
    result = user_module.add(5, 3);
    print(result);
}
```

**Generated Python Code:**

```python
# ❌ BROKEN: Import is commented out
# WARNING: Import 'user_module' requires security review
# import user_module

def main():
    result = user_module.add(5, 3)  # NameError: user_module not defined!
    print(result)
```

### Root Cause Analysis

1. **No Integration:** Code generator doesn't call `ModuleResolver`
2. **Static Whitelist:** Hardcoded list can't accommodate user modules
3. **No Module Compilation:** User modules not transpiled to Python
4. **No Import Path Awareness:** Generator doesn't know where to find user modules

---

## Phase 1: Fix User Module Imports (CRITICAL)

### Goal

Enable user-defined `.ml` module imports by integrating `ModuleResolver` into the code generation pipeline.

### Design

#### 1. Code Generator Integration

**Update `python_generator.py`:**

```python
class PythonGenerator:
    def __init__(self, ..., module_resolver: ModuleResolver | None = None):
        # ... existing code ...
        self.module_resolver = module_resolver or get_default_resolver()
        self.compiled_modules: dict[str, str] = {}  # Cache transpiled modules

    def visit_import_statement(self, node: ImportStatement):
        """Generate code for import statement with module resolution."""
        module_path = ".".join(node.target)

        try:
            # Resolve module using resolver
            module_info = self.module_resolver.resolve_import(
                node.target,
                source_file=self.context.source_file
            )

            if module_info.is_stdlib:
                # ML Standard Library
                self._generate_stdlib_import(module_path, node.alias)

            elif module_info.is_python:
                # Python whitelist module
                self._generate_python_import(module_path, node.alias)

            else:
                # User-defined ML module
                self._generate_user_module_import(module_info, node.alias)

        except ImportError as e:
            # Module not found - emit error
            self._emit_line(f"# ERROR: {e}", node)
            self._emit_line(f"raise ImportError('{e}')", node)

    def _generate_user_module_import(self, module_info: ModuleInfo, alias: str | None):
        """Generate import for user-defined ML module."""
        module_path = module_info.module_path

        # Check if module already compiled
        if module_path not in self.compiled_modules:
            # Transpile the user module
            transpiled_code = self._transpile_user_module(module_info)
            self.compiled_modules[module_path] = transpiled_code

            # Emit compiled module as inline module definition
            # OR write to file and import
            self._emit_compiled_module(module_path, transpiled_code)

        # Generate import statement
        if alias:
            self._emit_line(f"import {module_path.replace('.', '_')} as {alias}")
        else:
            self._emit_line(f"import {module_path.replace('.', '_')}")

    def _transpile_user_module(self, module_info: ModuleInfo) -> str:
        """Transpile user module AST to Python code."""
        # Create new generator for the module
        module_generator = PythonGenerator(
            module_resolver=self.module_resolver,
            function_registry=self.function_registry,
            # ... other config ...
        )

        # Generate Python code from module AST
        module_info.ast.accept(module_generator)
        return module_generator.get_code()

    def _emit_compiled_module(self, module_path: str, code: str):
        """Emit compiled module code."""
        # Strategy 1: Inline module (for simple cases)
        module_name = module_path.replace('.', '_')
        self._emit_line(f"# --- Module: {module_path} ---")
        self._emit_line(f"class {module_name}:")
        self._indent()
        for line in code.split('\n'):
            self._emit_line(line)
        self._dedent()
        self._emit_line(f"# --- End Module: {module_path} ---")

        # Strategy 2: Write to file (for complex modules)
        # output_file = f"{module_name}.py"
        # with open(output_file, 'w') as f:
        #     f.write(code)
```

#### 2. Multi-File Output Strategy

**Option A: Single-File Output (Simple)**
- Inline all user modules into main output file
- Works for small projects
- No file management needed

**Option B: Multi-File Output (Scalable)**
- Write each module to separate `.py` file
- Maintain directory structure
- Standard Python import semantics

```python
class MultiFileOutputManager:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.generated_files: dict[str, str] = {}

    def write_module(self, module_path: str, code: str):
        """Write module to appropriate file."""
        # Convert utils.math -> utils/math.py
        parts = module_path.split('.')
        file_path = self.output_dir / Path(*parts[:-1]) / f"{parts[-1]}.py"

        # Create directories
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        file_path.write_text(code, encoding='utf-8')
        self.generated_files[module_path] = str(file_path)

    def create_init_files(self):
        """Create __init__.py files for packages."""
        for module_path in self.generated_files:
            parts = module_path.split('.')
            for i in range(len(parts)):
                package_path = self.output_dir / Path(*parts[:i+1]) / '__init__.py'
                if not package_path.exists():
                    package_path.touch()
```

#### 3. Transpiler Integration

**Update `transpiler.py`:**

```python
class MLTranspiler:
    def transpile_to_python(
        self,
        ml_source: str,
        import_paths: list[str] | None = None,
        allow_current_dir: bool = False,
        output_mode: str = 'single-file',  # or 'multi-file'
        output_dir: str | None = None,
        **kwargs
    ) -> str | dict[str, str]:
        """
        Transpile ML code to Python with module resolution.

        Args:
            ml_source: ML source code
            import_paths: Paths to search for user modules
            allow_current_dir: Allow imports from current directory
            output_mode: 'single-file' or 'multi-file'
            output_dir: Directory for multi-file output

        Returns:
            Single file output (str) or dict of {module_path: code}
        """
        # Create module resolver
        resolver = ModuleResolver(
            import_paths=import_paths or [],
            allow_current_dir=allow_current_dir
        )

        # Create generator with resolver
        generator = PythonGenerator(module_resolver=resolver, ...)

        # Parse and generate
        ast = self.parser.parse(ml_source)
        ast.accept(generator)

        if output_mode == 'single-file':
            return generator.get_code()
        else:
            # Multi-file output
            output_manager = MultiFileOutputManager(output_dir or './output')
            for module_path, code in generator.compiled_modules.items():
                output_manager.write_module(module_path, code)
            output_manager.create_init_files()
            return generator.compiled_modules
```

### Implementation Plan

**Tasks:**

1. **Day 1-2: Code Generator Integration**
   - Add `module_resolver` parameter to `PythonGenerator`
   - Implement `_generate_user_module_import()`
   - Implement `_transpile_user_module()`
   - Add module compilation cache

2. **Day 2-3: Multi-File Output**
   - Implement `MultiFileOutputManager`
   - Update CLI to support `--output-dir` and `--output-mode`
   - Add file writing logic

3. **Day 3: Testing**
   - Create test suite with user modules
   - Test nested imports
   - Test circular dependency handling
   - Test multi-file output

4. **Day 3: Documentation**
   - Update language reference with import examples
   - Document CLI options
   - Add user module tutorial

### Success Criteria

✅ User modules transpile correctly
✅ Nested imports work (`import utils.math`)
✅ Package imports work (`import utils` → `utils/__init__.ml`)
✅ Multi-file output preserves directory structure
✅ Circular dependencies detected and reported
✅ All existing tests still pass

---

## Phase 2: Import Protocol Abstraction

### Goal

Design extensible architecture for alternative import sources (HTTP, database, custom protocols).

### Design

#### 1. Import Protocol Interface

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass
class ImportSource:
    """Metadata about an import source."""
    protocol: str  # 'file', 'http', 'db', 'git', etc.
    location: str  # URL, path, connection string, etc.
    credentials: dict[str, Any] | None = None
    cache_policy: str = 'default'  # 'default', 'no-cache', 'force-cache'
    verify_signature: bool = True

class ImportProtocol(ABC):
    """Abstract base class for import protocols."""

    @property
    @abstractmethod
    def protocol_name(self) -> str:
        """Protocol identifier (e.g., 'http', 'db', 'git')."""
        pass

    @abstractmethod
    def can_resolve(self, module_path: str, source: ImportSource) -> bool:
        """Check if this protocol can resolve the module."""
        pass

    @abstractmethod
    def resolve(self, module_path: str, source: ImportSource) -> ModuleInfo:
        """Resolve and load module from this protocol source."""
        pass

    @abstractmethod
    def validate_access(self, module_path: str, source: ImportSource) -> bool:
        """Validate capability to access this resource."""
        pass

    def get_cache_key(self, module_path: str, source: ImportSource) -> str:
        """Generate cache key for this module."""
        return f"{self.protocol_name}://{source.location}/{module_path}"
```

#### 2. Protocol Manager

```python
class ImportProtocolManager:
    """Manages registered import protocols."""

    def __init__(self):
        self.protocols: dict[str, ImportProtocol] = {}
        self._register_builtin_protocols()

    def register_protocol(self, protocol: ImportProtocol):
        """Register a new import protocol."""
        self.protocols[protocol.protocol_name] = protocol

    def get_protocol(self, protocol_name: str) -> ImportProtocol | None:
        """Get protocol by name."""
        return self.protocols.get(protocol_name)

    def resolve_with_protocol(
        self,
        module_path: str,
        source: ImportSource
    ) -> ModuleInfo:
        """Resolve module using appropriate protocol."""
        protocol = self.get_protocol(source.protocol)
        if not protocol:
            raise ImportError(f"Unknown protocol: {source.protocol}")

        if not protocol.can_resolve(module_path, source):
            raise ImportError(f"Protocol {source.protocol} cannot resolve {module_path}")

        if not protocol.validate_access(module_path, source):
            raise PermissionError(f"Access denied for {module_path} via {source.protocol}")

        return protocol.resolve(module_path, source)

    def _register_builtin_protocols(self):
        """Register built-in protocols."""
        self.register_protocol(FileProtocol())
        # Future: HTTP, database, git protocols
```

#### 3. Enhanced Module Resolver

```python
class ModuleResolverV2:
    """Enhanced module resolver with protocol support."""

    def __init__(
        self,
        import_paths: list[str] | None = None,
        import_sources: list[ImportSource] | None = None,
        protocol_manager: ImportProtocolManager | None = None,
        **kwargs
    ):
        self.import_paths = import_paths or []
        self.import_sources = import_sources or []
        self.protocol_manager = protocol_manager or ImportProtocolManager()
        # ... existing fields ...

    def resolve_import(
        self,
        import_target: list[str],
        source_file: str | None = None
    ) -> ModuleInfo:
        """Resolve import with multi-protocol support."""
        module_path = ".".join(import_target)

        # Try each import source
        for source in self.import_sources:
            try:
                module_info = self.protocol_manager.resolve_with_protocol(
                    module_path, source
                )
                return self._cache_and_return(module_path, module_info)
            except (ImportError, PermissionError):
                continue  # Try next source

        # Fallback to original file-based resolution
        return super().resolve_import(import_target, source_file)
```

#### 4. Extended Import Syntax (Future)

**Grammar Extension:**

```lark
import_statement: "import" import_spec ("as" IDENTIFIER)? ";"

import_spec: simple_import | protocol_import

simple_import: import_target  // Current: import math;

protocol_import: PROTOCOL_PREFIX import_target  // New: import http://cdn.mlpy.org/math;

PROTOCOL_PREFIX: /[a-z]+:\/\//  // Matches "http://", "db://", "git://"
```

**Example Syntax:**

```ml
// Current filesystem import
import utils.math;

// Future: HTTP import
import http://cdn.mlpy.org/stdlib/v2/math;

// Future: Database import
import db://local/custom_modules/crypto;

// Future: Git repository import
import git://github.com/mlpy/stdlib@v2.1.0/advanced_math;

// Future: Import with configuration
import http://private.repo.com/secure_module {
    auth: "bearer_token",
    verify: true,
    cache: "force"
};
```

---

## Phase 3: HTTP/HTTPS Import Protocol

### Goal

Implement secure HTTP(S) module importing with signature verification, caching, and capability integration.

### Design

#### 1. HTTP Protocol Implementation

```python
import hashlib
import requests
from pathlib import Path
from typing import Dict, Any

class HTTPImportProtocol(ImportProtocol):
    """HTTP/HTTPS import protocol with security."""

    def __init__(
        self,
        cache_dir: str = '~/.mlpy/http_cache',
        verify_ssl: bool = True,
        timeout: int = 30,
        signature_required: bool = True
    ):
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.signature_required = signature_required
        self.session = requests.Session()

    @property
    def protocol_name(self) -> str:
        return 'http'

    def can_resolve(self, module_path: str, source: ImportSource) -> bool:
        """Check if module exists at HTTP source."""
        url = self._build_url(module_path, source)
        try:
            response = self.session.head(
                url,
                verify=self.verify_ssl,
                timeout=self.timeout
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def resolve(self, module_path: str, source: ImportSource) -> ModuleInfo:
        """Download and parse module from HTTP source."""
        # Check cache first
        cached = self._check_cache(module_path, source)
        if cached and source.cache_policy != 'no-cache':
            return cached

        # Download module
        ml_source, metadata = self._download_module(module_path, source)

        # Verify signature if required
        if source.verify_signature and self.signature_required:
            self._verify_signature(ml_source, metadata)

        # Parse ML code
        from mlpy.ml.grammar.parser import parse_ml_code
        ast = parse_ml_code(ml_source, f"<http:{source.location}/{module_path}>")

        # Create module info
        module_info = ModuleInfo(
            name=module_path.split('.')[-1],
            module_path=module_path,
            ast=ast,
            source_code=ml_source,
            file_path=None,
            is_stdlib=False,
            is_python=False,
            dependencies=self._extract_dependencies(ast)
        )

        # Cache if not no-cache
        if source.cache_policy != 'no-cache':
            self._cache_module(module_path, source, module_info, ml_source, metadata)

        return module_info

    def validate_access(self, module_path: str, source: ImportSource) -> bool:
        """Validate capability for network access."""
        # Check network.http or network.https capability
        from mlpy.runtime.capabilities.manager import get_capability_manager
        manager = get_capability_manager()

        protocol = 'https' if source.location.startswith('https://') else 'http'
        required_cap = f"network.{protocol}"

        return manager.has_capability(required_cap)

    def _build_url(self, module_path: str, source: ImportSource) -> str:
        """Build full URL for module."""
        base_url = source.location.rstrip('/')
        module_file = module_path.replace('.', '/') + '.ml'
        return f"{base_url}/{module_file}"

    def _download_module(self, module_path: str, source: ImportSource) -> tuple[str, dict]:
        """Download module source and metadata."""
        url = self._build_url(module_path, source)

        # Prepare headers
        headers = {}
        if source.credentials and 'auth_token' in source.credentials:
            headers['Authorization'] = f"Bearer {source.credentials['auth_token']}"

        # Download module
        response = self.session.get(
            url,
            headers=headers,
            verify=self.verify_ssl,
            timeout=self.timeout
        )
        response.raise_for_status()

        ml_source = response.text

        # Download signature file (.sig)
        metadata = {}
        if source.verify_signature:
            sig_url = url + '.sig'
            sig_response = self.session.get(sig_url, verify=self.verify_ssl, timeout=self.timeout)
            if sig_response.status_code == 200:
                metadata['signature'] = sig_response.text
                metadata['signature_algorithm'] = response.headers.get('X-Signature-Algorithm', 'sha256')

        return ml_source, metadata

    def _verify_signature(self, ml_source: str, metadata: dict):
        """Verify module signature."""
        if 'signature' not in metadata:
            raise SecurityError("Module signature not found")

        # Compute hash
        algorithm = metadata.get('signature_algorithm', 'sha256')
        hasher = hashlib.new(algorithm)
        hasher.update(ml_source.encode('utf-8'))
        computed_hash = hasher.hexdigest()

        # Compare with signature
        expected_signature = metadata['signature'].strip()
        if computed_hash != expected_signature:
            raise SecurityError(
                f"Module signature mismatch: expected {expected_signature}, got {computed_hash}"
            )

    def _check_cache(self, module_path: str, source: ImportSource) -> ModuleInfo | None:
        """Check local cache for module."""
        cache_key = self.get_cache_key(module_path, source)
        cache_file = self.cache_dir / f"{hashlib.sha256(cache_key.encode()).hexdigest()}.ml"

        if cache_file.exists():
            # Load cached module
            ml_source = cache_file.read_text(encoding='utf-8')
            from mlpy.ml.grammar.parser import parse_ml_code
            ast = parse_ml_code(ml_source, str(cache_file))

            return ModuleInfo(
                name=module_path.split('.')[-1],
                module_path=module_path,
                ast=ast,
                source_code=ml_source,
                file_path=str(cache_file),
                is_stdlib=False,
                is_python=False
            )

        return None

    def _cache_module(
        self,
        module_path: str,
        source: ImportSource,
        module_info: ModuleInfo,
        ml_source: str,
        metadata: dict
    ):
        """Cache module locally."""
        cache_key = self.get_cache_key(module_path, source)
        cache_file = self.cache_dir / f"{hashlib.sha256(cache_key.encode()).hexdigest()}.ml"

        # Write source
        cache_file.write_text(ml_source, encoding='utf-8')

        # Write metadata
        metadata_file = cache_file.with_suffix('.meta.json')
        import json
        metadata_file.write_text(json.dumps({
            'module_path': module_path,
            'source_url': source.location,
            'cached_at': time.time(),
            'signature': metadata.get('signature'),
            'signature_algorithm': metadata.get('signature_algorithm')
        }), encoding='utf-8')
```

#### 2. Configuration

```python
# In mlpy.json or mlpy.yaml
{
    "import_sources": [
        {
            "protocol": "http",
            "location": "https://cdn.mlpy.org/stdlib/v2",
            "verify_signature": true,
            "cache_policy": "default"
        },
        {
            "protocol": "http",
            "location": "https://private.company.com/ml-modules",
            "credentials": {
                "auth_token": "${MLPY_AUTH_TOKEN}"
            },
            "verify_signature": true,
            "cache_policy": "no-cache"
        }
    ],
    "capabilities": [
        "network.https://cdn.mlpy.org/*",
        "network.https://private.company.com/*"
    ]
}
```

#### 3. CLI Support

```bash
# Add HTTP import source
mlpy run main.ml \
    --import-source "http://cdn.mlpy.org/stdlib/v2" \
    --verify-signatures \
    --cache-dir ~/.mlpy/cache

# Multiple sources
mlpy run main.ml \
    --import-source "http://cdn.mlpy.org/stdlib/v2" \
    --import-source "http://internal.corp.com/modules" \
    --auth-token "${AUTH_TOKEN}"
```

### Security Considerations

1. **Signature Verification:**
   - All HTTP modules require SHA256 signature files
   - Signature mismatch prevents module loading
   - Configurable signature algorithms

2. **Capability Requirements:**
   - `network.http` capability required for HTTP
   - `network.https` capability required for HTTPS
   - Per-domain capabilities for fine-grained control

3. **Content Security:**
   - Downloaded modules go through same security analysis as local modules
   - Malicious code detection before execution
   - Sandbox execution for untrusted sources

4. **Cache Integrity:**
   - Cached modules verified on load
   - Cache invalidation on signature mismatch
   - Configurable cache policies

5. **Transport Security:**
   - HTTPS enforced for production
   - Certificate verification (configurable)
   - TLS 1.2+ required

---

## Phase 4: Plugin System for Custom Importers

### Goal

Enable third-party import protocol implementations through plugin system.

### Design

#### 1. Plugin Discovery

```python
import importlib
import pkgutil
from typing import Type

class ImportPluginRegistry:
    """Registry for import protocol plugins."""

    def __init__(self):
        self.plugins: dict[str, Type[ImportProtocol]] = {}
        self._discover_plugins()

    def _discover_plugins(self):
        """Auto-discover plugins from entry points."""
        try:
            # Use entry points for plugin discovery
            from importlib.metadata import entry_points

            for entry_point in entry_points(group='mlpy.import_protocols'):
                try:
                    protocol_class = entry_point.load()
                    if issubclass(protocol_class, ImportProtocol):
                        self.register_plugin(protocol_class)
                except Exception as e:
                    print(f"Warning: Failed to load plugin {entry_point.name}: {e}")

        except ImportError:
            # Fallback: scan mlpy_plugins namespace package
            self._discover_namespace_plugins()

    def _discover_namespace_plugins(self):
        """Discover plugins from mlpy_plugins namespace."""
        try:
            import mlpy_plugins
            for importer, modname, ispkg in pkgutil.iter_modules(mlpy_plugins.__path__):
                try:
                    module = importlib.import_module(f'mlpy_plugins.{modname}')
                    if hasattr(module, 'get_protocol_class'):
                        protocol_class = module.get_protocol_class()
                        self.register_plugin(protocol_class)
                except Exception:
                    continue
        except ImportError:
            pass  # No plugins installed

    def register_plugin(self, protocol_class: Type[ImportProtocol]):
        """Register a plugin protocol."""
        protocol_instance = protocol_class()
        self.plugins[protocol_instance.protocol_name] = protocol_class
```

#### 2. Plugin Example: Git Protocol

```python
# mlpy_plugins/git_importer.py
from mlpy.ml.resolution.protocols import ImportProtocol, ImportSource, ModuleInfo
import subprocess
import tempfile
from pathlib import Path

class GitImportProtocol(ImportProtocol):
    """Import ML modules from Git repositories."""

    @property
    def protocol_name(self) -> str:
        return 'git'

    def can_resolve(self, module_path: str, source: ImportSource) -> bool:
        """Check if repository is accessible."""
        # Parse git URL: git://github.com/user/repo@branch/module
        repo_url, ref, module_subpath = self._parse_git_url(source.location, module_path)

        # Check if repo exists
        result = subprocess.run(
            ['git', 'ls-remote', repo_url],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0

    def resolve(self, module_path: str, source: ImportSource) -> ModuleInfo:
        """Clone repo and extract module."""
        repo_url, ref, module_subpath = self._parse_git_url(source.location, module_path)

        # Create temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Clone repo with depth=1 for speed
            subprocess.run(
                ['git', 'clone', '--depth=1', '--branch', ref, repo_url, tmpdir],
                check=True,
                capture_output=True
            )

            # Read module file
            module_file = Path(tmpdir) / module_subpath / (module_path.split('.')[-1] + '.ml')
            if not module_file.exists():
                raise ImportError(f"Module {module_path} not found in {repo_url}@{ref}")

            ml_source = module_file.read_text(encoding='utf-8')

            # Parse and return
            from mlpy.ml.grammar.parser import parse_ml_code
            ast = parse_ml_code(ml_source, str(module_file))

            return ModuleInfo(
                name=module_path.split('.')[-1],
                module_path=module_path,
                ast=ast,
                source_code=ml_source,
                file_path=None,
                is_stdlib=False,
                is_python=False
            )

    def validate_access(self, module_path: str, source: ImportSource) -> bool:
        """Require git.clone capability."""
        from mlpy.runtime.capabilities.manager import get_capability_manager
        return get_capability_manager().has_capability('git.clone')

    def _parse_git_url(self, location: str, module_path: str) -> tuple[str, str, str]:
        """Parse git://github.com/user/repo@branch/subpath"""
        # Remove git:// prefix
        url_path = location[6:] if location.startswith('git://') else location

        # Split on @
        if '@' in url_path:
            repo_part, ref_path = url_path.split('@', 1)
            if '/' in ref_path:
                ref, subpath = ref_path.split('/', 1)
            else:
                ref = ref_path
                subpath = ''
        else:
            repo_part = url_path
            ref = 'main'
            subpath = ''

        repo_url = f"https://{repo_part}.git"
        return repo_url, ref, subpath

# Plugin entry point
def get_protocol_class():
    return GitImportProtocol
```

#### 3. Plugin Installation

**setup.py for plugin:**

```python
from setuptools import setup

setup(
    name='mlpy-git-importer',
    version='1.0.0',
    packages=['mlpy_plugins'],
    entry_points={
        'mlpy.import_protocols': [
            'git = mlpy_plugins.git_importer:GitImportProtocol',
        ],
    },
    install_requires=[
        'mlpy>=2.0.0',
    ]
)
```

**Usage:**

```bash
# Install plugin
pip install mlpy-git-importer

# Use in ML code
import git://github.com/mlpy/stdlib@v2.1.0/advanced/crypto;
```

---

## Implementation Roadmap

### Phase 1: Fix User Module Imports (3 days) - CRITICAL

**Priority:** P0 - Blocking ecosystem growth

**Tasks:**
- [ ] Integrate ModuleResolver into PythonGenerator
- [ ] Implement user module transpilation
- [ ] Add multi-file output support
- [ ] Write comprehensive tests
- [ ] Update documentation

**Deliverables:**
- User modules work end-to-end
- CLI supports `--import-paths`
- Multi-file output option available
- 20+ integration tests

### Phase 2: Import Protocol Abstraction (1-2 weeks)

**Priority:** P1 - Foundation for future imports

**Tasks:**
- [ ] Design ImportProtocol interface
- [ ] Implement ImportProtocolManager
- [ ] Update ModuleResolver to use protocols
- [ ] Implement FileProtocol (current behavior)
- [ ] Add protocol configuration system
- [ ] Write protocol tests

**Deliverables:**
- Clean protocol abstraction
- Backwards-compatible with current system
- Plugin architecture ready
- Documentation for protocol API

### Phase 3: HTTP/HTTPS Importer (2-3 weeks)

**Priority:** P1 - Enable centralized module distribution

**Tasks:**
- [ ] Implement HTTPImportProtocol
- [ ] Add signature verification system
- [ ] Implement local caching
- [ ] Add capability integration
- [ ] Implement auth/credentials support
- [ ] Create CDN hosting guide
- [ ] Write HTTP import tests

**Deliverables:**
- Working HTTP(S) imports
- Signature verification
- Local cache with invalidation
- Security documentation
- CDN deployment guide

### Phase 4: Plugin System (1-2 weeks)

**Priority:** P2 - Enable community extensions

**Tasks:**
- [ ] Implement ImportPluginRegistry
- [ ] Add entry point discovery
- [ ] Create plugin template/example
- [ ] Write plugin development guide
- [ ] Implement Git protocol as example
- [ ] Create plugin tests

**Deliverables:**
- Working plugin system
- Git importer plugin
- Plugin development guide
- 2-3 example plugins

---

## Security Considerations

### File System Imports

**Threats:**
- Directory traversal: `import ../../../../etc/passwd`
- Symlink attacks
- TOCTOU race conditions

**Mitigations:**
- Path canonicalization and validation
- Restrict to allowed import paths
- No current directory access by default
- Symlink resolution with bounds checking

### HTTP Imports

**Threats:**
- Man-in-the-middle attacks
- Malicious code injection
- Compromised CDN
- Cache poisoning

**Mitigations:**
- HTTPS enforcement
- Signature verification (SHA256+)
- Certificate validation
- Capability requirements
- Full security analysis before execution

### Plugin System

**Threats:**
- Malicious plugins
- Sandbox escape via plugin
- Capability bypass

**Mitigations:**
- Plugin code review requirement
- Capability enforcement for all protocols
- Plugin signature verification
- Sandboxed plugin loading

---

## Success Metrics

### Phase 1 Success Criteria

- [ ] User can `import mymodule;` and it works
- [ ] Nested imports work: `import utils.math;`
- [ ] Package imports work: `import mypackage;` → `mypackage/__init__.ml`
- [ ] Multi-file output preserves structure
- [ ] Circular dependencies detected
- [ ] 95%+ test coverage for import system
- [ ] Documentation complete

### Phase 2 Success Criteria

- [ ] Protocol abstraction implemented
- [ ] FileProtocol maintains current behavior
- [ ] Protocol registration system works
- [ ] Configuration system integrated
- [ ] All existing tests pass
- [ ] API documentation complete

### Phase 3 Success Criteria

- [ ] HTTP imports work from CDN
- [ ] Signature verification prevents tampering
- [ ] Cache improves performance (>50% speedup on repeated imports)
- [ ] Capabilities enforced correctly
- [ ] Security audit passes
- [ ] CDN deployment guide complete

### Phase 4 Success Criteria

- [ ] Plugins auto-discovered and loaded
- [ ] Git protocol plugin works
- [ ] Plugin development guide published
- [ ] 3rd party plugins installable via pip
- [ ] Plugin security model validated

---

## Documentation Updates Required

### User Documentation

1. **Language Reference - Import System:**
   - Import statement syntax
   - Import resolution order
   - Package imports (`__init__.ml`)
   - Import aliases

2. **CLI Reference:**
   - `--import-paths` option
   - `--allow-current-dir` flag
   - `--import-source` configuration
   - Multi-file output options

3. **Tutorial: Creating Modules:**
   - File structure
   - Module exports (functions, classes)
   - Package organization
   - Best practices

### Integration Guide

1. **Module Development:**
   - Creating reusable modules
   - Dependency management
   - Testing modules
   - Publishing to CDN

2. **Import Protocols:**
   - Protocol interface
   - Implementing custom protocols
   - Plugin development
   - Security considerations

### Developer Guide

1. **Module Resolution Architecture:**
   - Resolution pipeline
   - Caching system
   - Dependency tracking
   - Security integration

2. **Extending Import System:**
   - Writing import protocols
   - Plugin architecture
   - Testing protocols
   - Performance optimization

---

## Conclusion

The ML module system has a solid foundation in `ModuleResolver`, but a critical bug in the code generator prevents user-defined modules from working. Fixing this is a **top priority** (3 days effort) that will unlock ecosystem growth.

The proposed import protocol abstraction provides a clean path to advanced import systems (HTTP, database, Git) while maintaining security and performance. The plugin system enables community extensions without compromising core security.

**Recommended Action:**
1. **Immediate:** Fix code generator (Phase 1) - 3 days
2. **Short-term:** Implement protocol abstraction (Phase 2) - 1-2 weeks
3. **Medium-term:** Build HTTP importer (Phase 3) - 2-3 weeks
4. **Long-term:** Enable plugin ecosystem (Phase 4) - 1-2 weeks

**Total Timeline:** 6-8 weeks for complete implementation

---

**Approval Required:** YES
**Estimated Effort:** 6-8 weeks (1 person)
**Impact:** CRITICAL - Enables ML ecosystem growth and third-party modules
**Risk:** LOW - Well-defined architecture with incremental delivery
