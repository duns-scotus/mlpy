"""Python bridge implementation for ML builtin module.

The builtin module provides core functions that are always available in ML code
without requiring explicit import. These functions cover:
- Type conversion (int, float, str, bool)
- Type checking (typeof, isinstance)
- Collections (len, range)
- I/O (print, input)
- Introspection (help, methods, modules)
- Math utilities (abs, min, max, round)

These functions are auto-imported by the code generator and available globally.
"""

from typing import Any, Callable
from mlpy.stdlib.decorators import ml_module, ml_function, _MODULE_REGISTRY


@ml_module(
    name="builtin",
    description="Core builtin functions always available without import",
    capabilities=[],  # Builtin functions don't require capabilities
    version="1.0.0"
)
class Builtin:
    """Builtin module providing core ML functions.

    This module is auto-imported and provides essential functionality
    that should be available in all ML programs.
    """

    # =====================================================================
    # Type Conversion Functions
    # =====================================================================

    @ml_function(description="Convert value to integer", capabilities=[])
    def int(self, value: Any) -> int:
        """Convert value to integer with ML-compatible semantics.

        Args:
            value: Value to convert (bool, str, float, int)

        Returns:
            Integer representation of value

        Raises:
            ValueError: If value cannot be converted to integer

        Examples:
            int(3.14) => 3
            int("42") => 42
            int(true) => 1
            int(false) => 0
            int("invalid") => raises ValueError
        """
        # Handle boolean explicitly (before int check)
        if isinstance(value, bool):
            return 1 if value else 0

        # Handle numeric types
        if isinstance(value, (int, float)):
            return int(value)

        # Handle strings
        if isinstance(value, str):
            # Try float first (handles "3.14" -> 3)
            try:
                return int(float(value))
            except ValueError:
                # Try direct int conversion
                return int(value)  # Will raise ValueError if invalid

        # Default conversion attempt (will raise ValueError/TypeError if invalid)
        return int(value)

    @ml_function(description="Convert value to float", capabilities=[])
    def float(self, value: Any) -> float:
        """Convert value to float with ML-compatible semantics.

        Args:
            value: Value to convert (bool, str, int, float)

        Returns:
            Float representation of value

        Raises:
            ValueError: If value cannot be converted to float

        Examples:
            float(42) => 42.0
            float("3.14") => 3.14
            float(true) => 1.0
            float(false) => 0.0
            float("invalid") => raises ValueError
        """
        # Handle boolean explicitly (before float check)
        if isinstance(value, bool):
            return 1.0 if value else 0.0

        # Handle numeric types
        if isinstance(value, (int, float)):
            return float(value)

        # Handle strings and other types (will raise ValueError if invalid)
        return float(value)

    @ml_function(description="Convert value to string", capabilities=[])
    def str(self, value: Any) -> str:
        """Convert value to string with ML-compatible boolean formatting.

        Args:
            value: Value to convert

        Returns:
            String representation of value

        Examples:
            str(42) => "42"
            str(3.14) => "3.14"
            str(true) => "true"  (NOT "True")
            str(false) => "false"  (NOT "False")
        """
        # ML uses lowercase true/false
        if isinstance(value, bool):
            return "true" if value else "false"

        return str(value)

    @ml_function(description="Convert value to boolean", capabilities=[])
    def bool(self, value: Any) -> bool:
        """Convert value to boolean with ML-compatible semantics.

        Args:
            value: Value to convert

        Returns:
            Boolean representation of value

        Examples:
            bool(1) => true
            bool(0) => false
            bool("") => false
            bool("hello") => true
        """
        return bool(value)

    # =====================================================================
    # Type Checking Functions
    # =====================================================================

    @ml_function(description="Get type of value with class metadata awareness", capabilities=[])
    def typeof(self, value: Any) -> str:
        """Get type of value with @ml_class metadata integration.

        This function recognizes decorated classes from Phase 1-3 and returns
        their ML class names instead of generic "object".

        Args:
            value: Value to check type of

        Returns:
            Type name: "boolean", "number", "string", "array", "object",
                      "function", or custom class name (e.g., "Pattern", "DateTimeObject")

        Examples:
            typeof(true) => "boolean"
            typeof(42) => "number"
            typeof("hello") => "string"
            typeof([1,2,3]) => "array"
            typeof({a: 1}) => "object"
            typeof(pattern) => "Pattern"  (if Pattern is @ml_class decorated)
        """
        # Check for @ml_class metadata (from Phase 1-3)
        if hasattr(type(value), '_ml_class_metadata'):
            return type(value)._ml_class_metadata.name

        # Standard type detection
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        elif callable(value):
            return "function"
        else:
            return "unknown"

    @ml_function(description="Check if value is instance of type", capabilities=[])
    def isinstance(self, value: Any, type_name: str) -> bool:
        """Check if value is instance of given type name.

        Supports both primitive types and custom @ml_class decorated classes.

        Args:
            value: Value to check
            type_name: Type name to check against

        Returns:
            True if value is of given type

        Examples:
            isinstance(42, "number") => true
            isinstance("hello", "string") => true
            isinstance(pattern, "Pattern") => true
        """
        actual_type = self.typeof(value)
        return actual_type == type_name

    # =====================================================================
    # Collection Functions
    # =====================================================================

    @ml_function(description="Get length of collection", capabilities=[])
    def len(self, collection: Any) -> int:
        """Get length of string, array, or object.

        Args:
            collection: String, array, or object to measure

        Returns:
            Length/size of collection, or 0 if not a collection

        Examples:
            len("hello") => 5
            len([1,2,3]) => 3
            len({a:1, b:2}) => 2
        """
        try:
            return len(collection)
        except TypeError:
            return 0

    @ml_function(description="Generate range of numbers", capabilities=[])
    def range(self, *args) -> list:
        """Generate range of numbers.

        Args:
            start: Start value (or stop if only one arg)
            stop: Stop value (exclusive)
            step: Step size (default 1)

        Returns:
            List of numbers in range

        Examples:
            range(5) => [0, 1, 2, 3, 4]
            range(1, 5) => [1, 2, 3, 4]
            range(0, 10, 2) => [0, 2, 4, 6, 8]
        """
        return list(range(*args))

    @ml_function(description="Enumerate array with indices", capabilities=[])
    def enumerate(self, array: list, start: int = 0) -> list:
        """Enumerate array returning (index, value) pairs.

        Args:
            array: Array to enumerate
            start: Starting index (default 0)

        Returns:
            List of (index, value) tuples

        Examples:
            enumerate(['a', 'b', 'c']) => [(0, 'a'), (1, 'b'), (2, 'c')]
        """
        return list(enumerate(array, start))

    # =====================================================================
    # I/O Functions
    # =====================================================================

    @ml_function(description="Print value to console", capabilities=[])
    def print(self, *values: Any) -> None:
        """Print values to console.

        Args:
            *values: Values to print

        Examples:
            print("Hello", "World") => prints "Hello World"
        """
        # Use ML-compatible boolean formatting
        formatted = []
        for val in values:
            if isinstance(val, bool):
                formatted.append("true" if val else "false")
            else:
                formatted.append(str(val))

        print(*formatted)

    @ml_function(description="Read input from console", capabilities=[])
    def input(self, prompt: str = "") -> str:
        """Read string input from console.

        Args:
            prompt: Prompt to display

        Returns:
            User input as string

        Examples:
            name = input("Enter name: ")
        """
        return input(prompt)

    # =====================================================================
    # Introspection Functions
    # =====================================================================

    @ml_function(description="Get help for function or module", capabilities=[])
    def help(self, target: Any) -> str:
        """Show documentation for function, method, or module.

        Includes capability requirements if the function has metadata.

        Args:
            target: Function, method, or module to get help for

        Returns:
            Documentation string with capabilities info if available

        Examples:
            help(string.upper) => "Convert string to uppercase\nCapabilities: None required"
            help(file.read) => "Read file contents from path\nRequires: file.read"
            help(console) => "Console output and logging module"
        """
        description = None
        capabilities = None

        # Check for @ml_function metadata
        if hasattr(target, '_ml_function_metadata'):
            metadata = target._ml_function_metadata
            description = metadata.description if metadata.description else 'No description available'
            capabilities = metadata.capabilities

        # Check for @ml_module metadata
        elif hasattr(target, '_ml_module_metadata'):
            metadata = target._ml_module_metadata
            description = metadata.description if metadata.description else 'No description available'
            capabilities = metadata.capabilities

        # Check for @ml_class metadata
        elif hasattr(type(target), '_ml_class_metadata'):
            metadata = type(target)._ml_class_metadata
            description = metadata.description if metadata.description else 'No description available'
            capabilities = metadata.capabilities

        # Fallback to docstring
        elif hasattr(target, '__doc__') and target.__doc__:
            description = target.__doc__.strip()

        else:
            return f"No help available for {target}"

        # Add capability information
        if capabilities is not None:
            if capabilities and len(capabilities) > 0:
                cap_str = ", ".join(capabilities)
                description += f"\nRequires: {cap_str}"
            else:
                description += "\nCapabilities: None required"

        return description

    @ml_function(description="List all methods available on value", capabilities=[])
    def methods(self, value: Any) -> list:
        """List all available methods for a value type.

        Args:
            value: Value to get methods for

        Returns:
            List of method names

        Examples:
            methods("hello") => ["upper", "lower", "split", ...]
            methods([1,2,3]) => ["map", "filter", "push", ...]
        """
        # This would integrate with SafeAttributeRegistry
        # For now, return basic implementation
        type_name = self.typeof(value)

        # Get all non-private attributes
        methods = [attr for attr in dir(value) if not attr.startswith('_')]
        return sorted(methods)

    @ml_function(description="List all imported modules", capabilities=[])
    def modules(self) -> list:
        """List all currently imported modules.

        Returns:
            List of module names

        Examples:
            modules() => ["console", "math", "regex", "datetime"]
        """
        return sorted(list(_MODULE_REGISTRY.keys()))

    @ml_function(description="List all available modules (including unimported)", capabilities=[])
    def available_modules(self, module_type: str = None) -> list:
        """List all available ML modules (both imported and discovered).

        This includes:
        - Standard library modules (auto-discovered from *_bridge.py files)
        - Extension modules (from configured extension paths)
        - ML source modules (from configured ML module paths)
        - Already imported modules

        Args:
            module_type: Optional filter - "python_bridge", "ml_source", or None for all

        Returns:
            Sorted list of all available module names

        Examples:
            available_modules() => ["collections", "console", "datetime", "file",
                                     "functional", "http", "json", "math", "path",
                                     "random", "regex", "user_modules.sorting", ...]
            available_modules("python_bridge") => ["console", "datetime", "json", "math", ...]
            available_modules("ml_source") => ["user_modules.sorting", "utils", ...]
        """
        from mlpy.stdlib.module_registry import get_registry, ModuleType

        registry = get_registry()

        if module_type is None:
            # Return all modules
            return sorted(list(registry.get_all_module_names()))

        # Filter by type
        try:
            type_enum = ModuleType(module_type)
            modules = registry.get_all_modules(include_type=type_enum)
            return sorted(modules.keys())
        except (ValueError, AttributeError):
            # Invalid module_type - return all modules
            return sorted(list(registry.get_all_module_names()))

    @ml_function(description="Check if module is available", capabilities=[])
    def has_module(self, module_name: str) -> bool:
        """Check if a module is available for import.

        Args:
            module_name: Name of module to check

        Returns:
            True if module can be imported, False otherwise

        Examples:
            has_module("math") => true
            has_module("nonexistent") => false
        """
        from mlpy.stdlib.module_registry import get_registry

        registry = get_registry()
        return registry.is_available(module_name)

    @ml_function(description="Get module metadata and information", capabilities=[])
    def module_info(self, module_name: str) -> dict:
        """Get detailed information about a module (Python bridge or ML source).

        Returns metadata including:
        - name: Module name
        - type: Module type ("python_bridge", "ml_source", or "builtin")
        - file_path: Path to source file
        - loaded: Whether module is currently loaded
        - reload_count: Number of times module has been reloaded

        For ML modules additionally includes:
        - transpiled_path: Path to transpiled Python file
        - needs_recompilation: Whether source has changed since last transpilation
        - source_modified: Last modification timestamp of source file

        For Python bridge modules additionally includes:
        - functions: List of available function names

        For all modules (if performance tracking enabled):
        - load_time_ms: Time taken to load/transpile the module

        Args:
            module_name: Name of module to get info for

        Returns:
            Dictionary with module metadata, or None if module not found

        Examples:
            info = module_info("math")
            print(info["type"])         => "python_bridge"
            print(info["functions"])    => ["sqrt", "pow", "sin", "cos", ...]

            info = module_info("user_modules.sorting")
            print(info["type"])                 => "ml_source"
            print(info["needs_recompilation"])  => false
        """
        from mlpy.stdlib.module_registry import get_registry

        registry = get_registry()

        # Query unified registry (handles both Python bridges and ML modules)
        return registry.get_module_info(module_name)

    # =====================================================================
    # Capability Introspection Functions
    # =====================================================================

    @ml_function(description="Check if specific capability is available", capabilities=[])
    def hasCapability(self, name: str) -> bool:
        """Check if a specific capability is available in current execution context.

        This function allows ML programs to query their security permissions before
        attempting operations. Enables defensive programming and graceful degradation.

        Args:
            name: Capability type string (e.g., "file.read", "network.http", "gui.create")

        Returns:
            True if capability is available and valid, False otherwise

        Examples:
            // Check before attempting file operation
            if (hasCapability("file.read")) {
                content = file.read("data.txt");
            } else {
                print("File reading not permitted");
            }

            // Check multiple capabilities
            if (hasCapability("file.read") && hasCapability("file.write")) {
                processFiles();
            }

            // Feature detection
            hasNetwork = hasCapability("network.http");
            if (hasNetwork) {
                syncWithServer();
            }
        """
        from mlpy.runtime.whitelist_validator import get_current_capability_context

        context = get_current_capability_context()
        if not context:
            return False

        return context.has_capability(name, check_parents=True)

    @ml_function(description="Get list of all available capabilities", capabilities=[])
    def getCapabilities(self) -> list:
        """Get list of all available capability types in current execution context.

        Returns all capabilities granted to this execution context, including
        capabilities inherited from parent contexts.

        Returns:
            List of capability type strings, or empty list if no context/capabilities

        Examples:
            // List all capabilities
            caps = getCapabilities();
            print("Available capabilities:");
            for (cap in caps) {
                print("  - " + cap);
            }

            // Check if any file operations allowed
            caps = getCapabilities();
            hasAnyFileAccess = false;
            for (cap in caps) {
                if (cap == "file.read" || cap == "file.write") {
                    hasAnyFileAccess = true;
                }
            }

            // Debug: Print execution environment
            print("Running with capabilities: " + str(getCapabilities()));
        """
        from mlpy.runtime.whitelist_validator import get_current_capability_context

        context = get_current_capability_context()
        if not context:
            return []

        # Get all capabilities (including inherited from parents)
        all_caps = context.get_all_capabilities(include_parents=True)
        return sorted(all_caps.keys())

    @ml_function(description="Get detailed information about a capability", capabilities=[])
    def getCapabilityInfo(self, name: str) -> dict:
        """Get detailed information about a specific capability.

        Returns comprehensive information about capability constraints, usage limits,
        and current status. Returns null if capability is not available.

        Args:
            name: Capability type string (e.g., "file.read", "network.http")

        Returns:
            Dictionary with capability details, or None if capability not available.

            Dictionary structure:
            {
                "type": "file.read",              // Capability type
                "available": true,                 // Is currently valid?
                "patterns": ["*.txt", "data/*"],  // Resource patterns (or None)
                "operations": ["read"],            // Allowed operations (or None)
                "expires_at": null,                // Expiration time (or None)
                "usage_count": 5,                  // Times capability has been used
                "max_usage": null                  // Max usage limit (or None)
            }

        Examples:
            // Get detailed info
            info = getCapabilityInfo("file.read");
            if (info != null) {
                print("File read capability:");
                print("  Patterns: " + str(info.patterns));
                print("  Usage: " + str(info.usage_count) + " times");
            }

            // Check resource pattern restrictions
            info = getCapabilityInfo("file.read");
            if (info != null && info.patterns != null) {
                print("Can only read files matching: " + str(info.patterns));
            }

            // Check usage limits
            info = getCapabilityInfo("network.http");
            if (info != null && info.max_usage != null) {
                remaining = info.max_usage - info.usage_count;
                print("HTTP requests remaining: " + str(remaining));
            }
        """
        from mlpy.runtime.whitelist_validator import get_current_capability_context

        context = get_current_capability_context()
        if not context:
            return None

        # Get capability token (unchecked to include expired tokens for introspection)
        token = context.get_capability_token_unchecked(name)
        if not token:
            return None

        # Build info object
        info = {
            'type': token.capability_type,
            'available': token.is_valid(),
            'usage_count': token.usage_count,
        }

        # Add constraint details if available
        if token.constraints:
            info['patterns'] = token.constraints.resource_patterns if token.constraints.resource_patterns else None
            info['operations'] = list(token.constraints.allowed_operations) if token.constraints.allowed_operations else None
            info['max_usage'] = token.constraints.max_usage_count
            info['expires_at'] = token.constraints.expires_at.isoformat() if token.constraints.expires_at else None
        else:
            info['patterns'] = None
            info['operations'] = None
            info['max_usage'] = None
            info['expires_at'] = None

        return info

    @ml_function(description="Get list of capabilities required by function", capabilities=[])
    def requiredCapabilities(self, func: Callable) -> list:
        """Get list of capabilities required by a function.

        Inspects function metadata to determine what capabilities it needs.
        Returns empty list if function requires no capabilities or has no metadata.

        Args:
            func: Function or callable to inspect

        Returns:
            List of capability type strings (e.g., ["file.read", "network.http"])
            Empty list if no capabilities required

        Examples:
            import file;

            // Check file.read requirements
            caps = requiredCapabilities(file.read);
            print(caps);  // ["file.read"]

            // Check if we can call it
            canCall = true;
            for (cap in caps) {
                if (!hasCapability(cap)) {
                    print("Missing: " + cap);
                    canCall = false;
                }
            }

            if (canCall) {
                content = file.read("data.txt");
            }

            // Check builtin (no requirements)
            caps = requiredCapabilities(print);
            print(caps);  // []

            // Utility function for checking callability
            function canExecute(fn) {
                required = requiredCapabilities(fn);
                for (cap in required) {
                    if (!hasCapability(cap)) {
                        return false;
                    }
                }
                return true;
            }
        """
        # Check for @ml_function metadata
        if hasattr(func, '_ml_function_metadata'):
            metadata = func._ml_function_metadata
            return list(metadata.capabilities) if metadata.capabilities else []

        # Check for @ml_class metadata on methods
        if hasattr(func, '__self__'):
            obj = func.__self__
            if hasattr(type(obj), '_ml_class_metadata'):
                class_meta = type(obj)._ml_class_metadata
                method_name = func.__name__
                if method_name in class_meta.methods:
                    method_meta = class_meta.methods[method_name]
                    return list(method_meta.capabilities) if method_meta.capabilities else []

        # No metadata or no capabilities
        return []

    # =====================================================================
    # Dynamic Introspection Functions (Secure)
    # =====================================================================

    @ml_function(description="Check if object has safe attribute", capabilities=[])
    def hasattr(self, obj: Any, name: str) -> bool:
        """Check if object has safe attribute.

        Only returns True for attributes in SafeAttributeRegistry whitelist.
        ALL dunder attributes return False for security.

        Args:
            obj: Object to check
            name: Attribute name

        Returns:
            True if object has safe attribute, False otherwise

        Security:
            - Blocks ALL dunder attributes (__class__, __dict__, etc.)
            - Only whitelisted safe attributes return True
            - Dangerous attributes always return False

        Examples:
            hasattr("hello", "upper") => true
            hasattr("hello", "__class__") => false (blocked)
            hasattr([1,2,3], "append") => true
            hasattr([1,2,3], "__dict__") => false (blocked)
        """
        from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry

        # Block ALL dunder attributes immediately
        if name.startswith('_'):
            return False

        registry = get_safe_registry()
        return registry.is_safe_attribute_name(obj, name) and hasattr(obj, name)

    @ml_function(description="Get safe attribute from object", capabilities=[])
    def getattr(self, obj: Any, name: str, default: Any = None) -> Any:
        """Get safe attribute from object.

        Only allows access to attributes in SafeAttributeRegistry whitelist.
        Dangerous attributes return the default value.

        Args:
            obj: Object to get attribute from
            name: Attribute name
            default: Default value if attribute not found or unsafe

        Returns:
            Attribute value if safe, default otherwise

        Security:
            - Routes ALL access through SafeAttributeRegistry
            - Blocks __class__, __globals__, __dict__, etc.
            - Only whitelisted safe attributes accessible
            - No access to object internals

        Examples:
            getattr("hello", "upper") => <method 'upper'>
            getattr("hello", "__class__", "BLOCKED") => "BLOCKED"
            getattr(obj, "missing", 42) => 42
        """
        from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry

        # Block ALL dunder attributes immediately
        if name.startswith('_'):
            return default

        registry = get_safe_registry()

        try:
            return registry.safe_attr_access(obj, name)
        except (AttributeError, Exception):
            return default

    @ml_function(description="Call function dynamically with arguments", capabilities=[])
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Call function dynamically with arguments.

        SECURITY: Uses safe_call to validate function before execution.
        This prevents execution of non-whitelisted functions passed as arguments.

        Args:
            func: Callable to invoke
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Result of function call

        Raises:
            TypeError: If func is not callable
            SecurityError: If func is not whitelisted
            CapabilityError: If required capabilities not available

        Examples:
            call(math.abs, -5) => 5
            call(string.upper, "hello") => "HELLO"
            call(eval, "code") => SecurityError (BLOCKED!)

        Security:
            Prevents these attacks:
            - call(eval, "malicious") - Blocked
            - call(open, "secrets.txt") - Blocked
            - call(__import__, "os") - Blocked
        """
        # Import here to avoid circular dependency at module load time
        from mlpy.runtime.whitelist_validator import safe_call

        # Delegate to safe_call for validation and execution
        return safe_call(func, *args, **kwargs)

    # =====================================================================
    # Math Utility Functions
    # =====================================================================

    @ml_function(description="Get absolute value", capabilities=[])
    def abs(self, value: float) -> float:
        """Get absolute value of number.

        Args:
            value: Number to get absolute value of

        Returns:
            Absolute value

        Examples:
            abs(-5) => 5
            abs(3.14) => 3.14
        """
        return abs(value)

    @ml_function(description="Get minimum value", capabilities=[])
    def min(self, *values) -> Any:
        """Get minimum value from arguments.

        Args:
            *values: Values to compare (or single array)

        Returns:
            Minimum value

        Examples:
            min(1, 2, 3) => 1
            min([5, 2, 8]) => 2
        """
        # Handle single array argument
        if len(values) == 1 and isinstance(values[0], list):
            return min(values[0]) if values[0] else None
        return min(values) if values else None

    @ml_function(description="Get maximum value", capabilities=[])
    def max(self, *values) -> Any:
        """Get maximum value from arguments.

        Args:
            *values: Values to compare (or single array)

        Returns:
            Maximum value

        Examples:
            max(1, 2, 3) => 3
            max([5, 2, 8]) => 8
        """
        # Handle single array argument
        if len(values) == 1 and isinstance(values[0], list):
            return max(values[0]) if values[0] else None
        return max(values) if values else None

    @ml_function(description="Round number to precision", capabilities=[])
    def round(self, value: float, precision: int = 0) -> float:
        """Round number to given precision.

        Args:
            value: Number to round
            precision: Number of decimal places (default 0)

        Returns:
            Rounded number

        Examples:
            round(3.14159) => 3.0
            round(3.14159, 2) => 3.14
        """
        return round(value, precision)

    @ml_function(description="Zip multiple arrays", capabilities=[])
    def zip(self, *arrays) -> list:
        """Zip multiple arrays into tuples.

        Args:
            *arrays: Arrays to zip together

        Returns:
            List of tuples

        Examples:
            zip([1,2,3], ['a','b','c']) => [(1,'a'), (2,'b'), (3,'c')]
        """
        return list(zip(*arrays))

    @ml_function(description="Get sorted copy of array", capabilities=[])
    def sorted(self, array: list, reverse: bool = False) -> list:
        """Return sorted copy of array.

        Args:
            array: Array to sort
            reverse: Sort in descending order (default false)

        Returns:
            New sorted array

        Examples:
            sorted([3, 1, 2]) => [1, 2, 3]
            sorted([3, 1, 2], true) => [3, 2, 1]
        """
        return sorted(array, reverse=reverse)

    @ml_function(description="Get object keys", capabilities=[])
    def keys(self, obj: dict) -> list:
        """Get all keys from object.

        Args:
            obj: Object to get keys from

        Returns:
            List of keys

        Examples:
            keys({a: 1, b: 2}) => ["a", "b"]
        """
        return list(obj.keys())

    @ml_function(description="Get object values", capabilities=[])
    def values(self, obj: dict) -> list:
        """Get all values from object.

        Args:
            obj: Object to get values from

        Returns:
            List of values

        Examples:
            values({a: 1, b: 2}) => [1, 2]
        """
        return list(obj.values())

    # =====================================================================
    # Safe Utility Functions
    # =====================================================================

    @ml_function(description="Check if object is callable", capabilities=[])
    def callable(self, obj: Any) -> bool:
        """Check if object is callable (function, method, etc.).

        Args:
            obj: Object to check

        Returns:
            True if callable, False otherwise

        Examples:
            callable(print) => true
            callable(42) => false
            callable(lambda x: x) => true
        """
        return callable(obj)

    @ml_function(description="Check if all elements are truthy", capabilities=[])
    def all(self, iterable: list) -> bool:
        """Return True if all elements are truthy.

        Args:
            iterable: List to check

        Returns:
            True if all elements truthy, False otherwise

        Examples:
            all([true, true, true]) => true
            all([true, false, true]) => false
            all([1, 2, 3]) => true
            all([1, 0, 3]) => false
        """
        return all(iterable)

    @ml_function(description="Check if any element is truthy", capabilities=[])
    def any(self, iterable: list) -> bool:
        """Return True if any element is truthy.

        Args:
            iterable: List to check

        Returns:
            True if any element truthy, False otherwise

        Examples:
            any([false, false, true]) => true
            any([false, false, false]) => false
            any([0, 0, 1]) => true
        """
        return any(iterable)

    @ml_function(description="Sum numeric values", capabilities=[])
    def sum(self, iterable: list, start: float = 0) -> float:
        """Sum numeric values with optional start value.

        Args:
            iterable: List of numbers to sum
            start: Starting value (default 0)

        Returns:
            Sum of all values

        Examples:
            sum([1, 2, 3]) => 6
            sum([1.5, 2.5, 3.0]) => 7.0
            sum([1, 2, 3], 10) => 16
        """
        return sum(iterable, start)

    @ml_function(description="Convert integer to character", capabilities=[])
    def chr(self, i: int) -> str:
        """Convert Unicode code point to character.

        Args:
            i: Unicode code point

        Returns:
            Character string

        Examples:
            chr(65) => "A"
            chr(97) => "a"
            chr(8364) => "€"
        """
        return chr(i)

    @ml_function(description="Convert character to integer", capabilities=[])
    def ord(self, c: str) -> int:
        """Convert character to Unicode code point.

        Args:
            c: Single character string

        Returns:
            Unicode code point

        Examples:
            ord("A") => 65
            ord("a") => 97
            ord("€") => 8364
        """
        return ord(c)

    @ml_function(description="Convert to hexadecimal", capabilities=[])
    def hex(self, n: int) -> str:
        """Convert integer to hexadecimal string.

        Args:
            n: Integer to convert

        Returns:
            Hexadecimal string with '0x' prefix

        Examples:
            hex(255) => "0xff"
            hex(16) => "0x10"
        """
        return hex(n)

    @ml_function(description="Convert to binary", capabilities=[])
    def bin(self, n: int) -> str:
        """Convert integer to binary string.

        Args:
            n: Integer to convert

        Returns:
            Binary string with '0b' prefix

        Examples:
            bin(10) => "0b1010"
            bin(255) => "0b11111111"
        """
        return bin(n)

    @ml_function(description="Convert to octal", capabilities=[])
    def oct(self, n: int) -> str:
        """Convert integer to octal string.

        Args:
            n: Integer to convert

        Returns:
            Octal string with '0o' prefix

        Examples:
            oct(8) => "0o10"
            oct(64) => "0o100"
        """
        return oct(n)

    @ml_function(description="Get string representation", capabilities=[])
    def repr(self, obj: Any) -> str:
        """Get string representation of object.

        Uses ML-compatible boolean formatting.

        Args:
            obj: Object to represent

        Returns:
            String representation

        Examples:
            repr(42) => "42"
            repr(true) => "true"
            repr("hello") => "'hello'"
        """
        # Use ML-compatible boolean formatting
        if isinstance(obj, bool):
            return "true" if obj else "false"
        return repr(obj)

    @ml_function(description="Format value with format specifier", capabilities=[])
    def format(self, value: Any, format_spec: str = "") -> str:
        """Format value with format specifier.

        Args:
            value: Value to format
            format_spec: Format specification string

        Returns:
            Formatted string

        Examples:
            format(3.14159, ".2f") => "3.14"
            format(42, "05d") => "00042"
            format(255, "x") => "ff"
        """
        return format(value, format_spec)

    @ml_function(description="Create reverse iterator", capabilities=[])
    def reversed(self, seq: list) -> list:
        """Return reversed sequence.

        Args:
            seq: Sequence to reverse

        Returns:
            Reversed list

        Examples:
            reversed([1, 2, 3]) => [3, 2, 1]
            reversed("hello") => ['o', 'l', 'l', 'e', 'h']
        """
        return list(reversed(seq))

    # =====================================================================
    # Iterator Functions
    # =====================================================================

    @ml_function(description="Create iterator from iterable", capabilities=[])
    def iter(self, iterable: Any) -> Any:
        """Create iterator from iterable.

        Args:
            iterable: Sequence to create iterator from (list, string, etc.)

        Returns:
            Iterator object

        Examples:
            it = iter([1, 2, 3])
            next(it) => 1
            next(it) => 2

        Note:
            In ML, iterators are typically consumed by converting to list
            or using next() to get individual elements.
        """
        return iter(iterable)

    @ml_function(description="Get next item from iterator", capabilities=[])
    def next(self, iterator: Any, *args) -> Any:
        """Get next item from iterator.

        Args:
            iterator: Iterator object (created with iter())
            *args: Optional default value to return if iterator is exhausted

        Returns:
            Next item from iterator, or default if exhausted (and default provided)

        Raises:
            StopIteration: If iterator exhausted and no default provided

        Examples:
            it = iter([1, 2, 3])
            next(it) => 1
            next(it) => 2
            next(it) => 3
            next(it, "done") => "done"  (exhausted)
            next(it, null) => null  (exhausted, explicit null default)

        Note:
            Use default parameter to avoid StopIteration errors.
            In ML, catch StopIteration by always providing a default value.
        """
        # Use Python's built-in next() with sentinel pattern
        # If args is empty, next() will raise StopIteration
        # If args has a value, next() will return that value when exhausted
        if len(args) == 0:
            # No default - let StopIteration propagate (will cause error in ML)
            # In ML, users should always use default to avoid errors
            try:
                return next(iterator)
            except StopIteration:
                # Convert to ML-friendly error message
                raise RuntimeError("Iterator exhausted - use default parameter to avoid error")
        else:
            # Has default - return it when exhausted
            return next(iterator, args[0])


# Global builtin instance for ML import
# This is auto-imported by the code generator
builtin = Builtin()


# Helper functions for direct use (maintains backward compatibility)
def typeof_helper(value: Any) -> str:
    """Helper function for typeof()."""
    return builtin.typeof(value)


def len_helper(collection: Any) -> int:
    """Helper function for len()."""
    return builtin.len(collection)


def print_helper(*values: Any) -> None:
    """Helper function for print()."""
    return builtin.print(*values)


# Export public API
__all__ = [
    "Builtin",
    "builtin",
    "typeof_helper",
    "len_helper",
    "print_helper",
]
