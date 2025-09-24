# ML Module Support Implementation Plan

## Executive Summary
Create a comprehensive module import system for ML with two components:
1. **User .ml Module Import** - File system-based imports with strict security controls
2. **ML Standard Library** - Native ML modules wrapping Python stdlib with capability integration

## Current State Analysis

### Existing Infrastructure ✅
- Complete import grammar: `import module.submodule as alias;`
- AST nodes: ImportStatement with target/alias support
- Security analysis: Dangerous module blocking (os, sys, subprocess, etc.)
- Python code generation: Whitelisted modules (math, json, datetime, random)
- Member function calls: `math.sqrt(25)` working via enhanced grammar
- CLI foundation: Ready for new import path options

### Current Limitations 🚨
- No user .ml file import capability
- No ML Standard Library modules
- No file system access controls for imports
- No CLI configuration for import paths
- Hard-coded Python module whitelist

## Architecture Design

### 1. User .ml Module Import System
- **Import Resolution**: Search order: `import_paths` → current directory → built-in modules
- **Security Model**: Empty import paths by default, CLI configuration required
- **File Access**: Capability-based file system access with pattern validation
- **Caching**: Compiled module cache with dependency tracking

### 2. ML Standard Library Modules
- **Native ML Modules**: Replace Python imports with capability-aware ML modules
- **Registration System**: Dynamic module discovery and loading
- **Security Integration**: Each function call validated through capability system
- **Python Interop**: Seamless bridging to safe Python stdlib functions

### 3. CLI Integration
- `--import-paths`: Colon-separated search paths (empty default)
- `--allow-python-modules`: Override Python module whitelist
- `--stdlib-mode`: Choose between "native" (ML modules) or "python" (whitelisted)

## Implementation Plan

### Phase 1: File System Import Foundation
1. **Module Resolution Engine** (`src/mlpy/ml/resolution/`)
   - Path resolution with security validation
   - Circular dependency detection
   - Module caching system
2. **Enhanced Security Analysis**
   - File access capability validation
   - Import path security auditing
3. **CLI Options**
   - `--import-paths` implementation
   - Configuration validation

### Phase 2: ML Standard Library
1. **Module Registry** (`src/mlpy/stdlib/`)
   - Dynamic module discovery
   - Capability requirement registration
   - Python function bridging
2. **Core Modules**
   - `math.ml`: Mathematical operations with capability checks
   - `json.ml`: JSON handling with sanitization
   - `string.ml`: String manipulation utilities
   - `datetime.ml`: Date/time operations
3. **Capability Integration**
   - Function-level capability requirements
   - Runtime validation and enforcement

### Phase 3: Integration & Testing
1. **End-to-End Testing**
   - User module import scenarios
   - Standard library functionality
   - Security boundary validation
2. **Performance Optimization**
   - Import caching optimization
   - Capability validation caching
3. **Documentation**
   - Module authoring guide
   - Security best practices

## Security Strategy: Capability-First Approach

### Recommendation: Native ML Standard Library
**Chosen approach**: Native ML modules with capability integration over Python whitelisting

**Rationale**:
- **Fine-grained Control**: Each function can specify exact capabilities needed
- **Security Transparency**: Clear capability requirements vs. opaque Python modules
- **Consistency**: Uniform security model across all operations
- **Extensibility**: Easy to add new secure operations without Python dependencies

### Module Security Model
```ml
// math.ml - Native ML Standard Library Module
capability MathOperations {
    allow read "constants";
    allow execute "calculations";
}

function sqrt(value: number): number {
    // Capability automatically validated
    return __python_bridge("math.sqrt", value);
}
```

### Import Path Security
- **Default**: Empty import paths = no file system access
- **Configuration**: CLI `--import-paths` required for user modules
- **Validation**: All paths validated through capability system
- **Sandboxing**: Imported code executed in same security boundary

## Implementation Details

### Module Resolution Algorithm
1. **Parse Import Statement**: Extract module path and alias
2. **Security Validation**: Check import paths against capabilities
3. **Module Search**:
   - Check ML Standard Library registry
   - Search configured import paths
   - Search current directory (if allowed)
   - Check Python whitelist (compatibility mode)
4. **Load & Cache**: Parse, analyze, and cache resolved module
5. **Dependency Tracking**: Record dependencies for cache invalidation

### File System Integration
```python
# Module resolver with capability integration
class ModuleResolver:
    def __init__(self, import_paths: list[str], capability_manager):
        self.import_paths = import_paths
        self.capability_manager = capability_manager
        self.module_cache = {}

    def resolve_import(self, import_target: list[str]) -> ModuleInfo:
        # Validate file access capability
        # Search configured paths
        # Load and parse .ml file
        # Return compiled module info
```

### Standard Library Registry
```python
# ML Standard Library registration system
class StandardLibraryRegistry:
    def __init__(self):
        self.modules = {}
        self.capabilities = {}

    def register_module(self, name: str, module_path: str, required_capabilities: list[str]):
        # Register ML standard library module
        # Associate with capability requirements
```

## Implementation Files

### New Components
- `src/mlpy/ml/resolution/resolver.py` - Module resolution engine
- `src/mlpy/ml/resolution/cache.py` - Import caching system
- `src/mlpy/ml/resolution/__init__.py` - Resolution package
- `src/mlpy/stdlib/` - ML Standard Library modules directory
- `src/mlpy/stdlib/registry.py` - Module registration system
- `src/mlpy/stdlib/math.ml` - Math standard library module
- `src/mlpy/stdlib/json.ml` - JSON standard library module
- `src/mlpy/stdlib/string.ml` - String standard library module
- `src/mlpy/stdlib/datetime.ml` - DateTime standard library module
- `src/mlpy/cli/import_config.py` - CLI import configuration

### Modified Components
- `src/mlpy/cli/app.py` - Add import path CLI options
- `src/mlpy/ml/analysis/security_analyzer.py` - File access validation
- `src/mlpy/ml/codegen/python_generator.py` - Module import generation
- `src/mlpy/ml/transpiler.py` - Module resolution integration

## Testing Strategy

### Unit Tests
- Module resolution logic
- Cache management
- Capability validation
- Standard library registration

### Integration Tests
- End-to-end import scenarios
- User module importing
- Standard library functionality
- Security boundary validation

### Security Tests
- Import path validation
- Capability enforcement
- Malicious module detection
- File system access controls

### Performance Tests
- Import resolution speed (<10ms target)
- Cache hit rates (>95% target)
- Memory usage optimization
- Concurrent import handling

## Success Metrics
- ✅ User can import .ml modules from configured paths
- ✅ ML Standard Library provides math, json, string, datetime functionality
- ✅ All module operations validated through capability system
- ✅ Zero security vulnerabilities in import system
- ✅ <10ms import resolution performance
- ✅ 100% compatibility with existing ML code

## CLI Usage Examples

### Basic Usage
```bash
# Import user modules from specific paths
mlpy run app.ml --import-paths "./modules:./lib"

# Use native ML standard library
mlpy run app.ml --stdlib-mode native

# Allow additional Python modules (compatibility)
mlpy run app.ml --allow-python-modules "urllib,hashlib"
```

### Security Configuration
```bash
# Strict mode with no file system access
mlpy run app.ml  # Default: empty import paths

# Sandbox with specific module access
mlpy run app.ml --import-paths "./safe-modules" --strict
```

## Module Development Guide

### Creating ML Standard Library Modules
```ml
// Example: string.ml
capability StringOperations {
    allow read "string_constants";
    allow execute "string_processing";
}

function uppercase(text: string): string {
    return __python_bridge("str.upper", text);
}

function contains(text: string, pattern: string): boolean {
    return __python_bridge("str.__contains__", text, pattern);
}
```

### User Module Structure
```ml
// Example: user module utils.ml
import math;

function calculateDistance(x1: number, y1: number, x2: number, y2: number): number {
    dx = x2 - x1;
    dy = y2 - y1;
    return math.sqrt(dx * dx + dy * dy);
}
```

## Migration Strategy

### Phase 1: Backward Compatibility
- Maintain existing Python module imports
- Add ML Standard Library alongside
- CLI flag to choose mode

### Phase 2: Native Preference
- Default to ML Standard Library modules
- Python modules as fallback
- Deprecation warnings for Python imports

### Phase 3: Pure ML Standard Library
- Complete migration to native modules
- Remove Python import compatibility
- Full capability integration

This implementation plan provides a comprehensive, security-first module system that enables both user module development and safe standard library access while maintaining ML's zero-trust security model.