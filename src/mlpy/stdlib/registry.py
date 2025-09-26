"""ML Standard Library registry and module management."""

import importlib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mlpy.ml.grammar.ast_nodes import Program
from mlpy.ml.grammar.parser import parse_ml_code
from mlpy.ml.resolution.resolver import ModuleInfo
from mlpy.runtime.capabilities.manager import CapabilityManager, get_capability_manager


@dataclass
class StandardLibraryModule:
    """Information about a standard library module."""

    name: str
    module_path: str
    source_file: str
    capabilities_required: list[str]
    description: str
    version: str = "1.0.0"
    python_bridge_modules: list[str] = None

    def __post_init__(self):
        if self.python_bridge_modules is None:
            self.python_bridge_modules = []


@dataclass
class BridgeFunction:
    """Python function bridge configuration."""

    ml_name: str
    python_module: str
    python_function: str
    capabilities_required: list[str]
    parameter_types: list[str] = None
    return_type: str = None
    validation_function: Callable | None = None

    def __post_init__(self):
        if self.parameter_types is None:
            self.parameter_types = []


class StandardLibraryRegistry:
    """Registry for ML Standard Library modules."""

    def __init__(self, capability_manager: CapabilityManager = None):
        """Initialize standard library registry.

        Args:
            capability_manager: Capability manager for security validation
        """
        self.capability_manager = capability_manager or get_capability_manager()
        self.modules: dict[str, StandardLibraryModule] = {}
        self.bridge_functions: dict[str, list[BridgeFunction]] = {}
        self._stdlib_path = Path(__file__).parent

    def register_module(
        self,
        name: str,
        source_file: str,
        capabilities_required: list[str],
        description: str,
        version: str = "1.0.0",
        python_bridge_modules: list[str] = None,
    ) -> None:
        """Register a standard library module.

        Args:
            name: Module name (e.g., 'math', 'json')
            source_file: ML source file path
            capabilities_required: Required capabilities
            description: Module description
            version: Module version
            python_bridge_modules: Python modules needed for bridging
        """
        module = StandardLibraryModule(
            name=name,
            module_path=name,
            source_file=source_file,
            capabilities_required=capabilities_required,
            description=description,
            version=version,
            python_bridge_modules=python_bridge_modules or [],
        )

        self.modules[name] = module

    def register_bridge_function(
        self,
        module_name: str,
        ml_name: str,
        python_module: str,
        python_function: str,
        capabilities_required: list[str],
        parameter_types: list[str] = None,
        return_type: str = None,
        validation_function: Callable | None = None,
    ) -> None:
        """Register a Python bridge function.

        Args:
            module_name: ML module name
            ml_name: ML function name
            python_module: Python module name
            python_function: Python function name
            capabilities_required: Required capabilities
            parameter_types: Parameter type annotations
            return_type: Return type annotation
            validation_function: Optional validation function
        """
        if module_name not in self.bridge_functions:
            self.bridge_functions[module_name] = []

        bridge_func = BridgeFunction(
            ml_name=ml_name,
            python_module=python_module,
            python_function=python_function,
            capabilities_required=capabilities_required,
            parameter_types=parameter_types or [],
            return_type=return_type,
            validation_function=validation_function,
        )

        self.bridge_functions[module_name].append(bridge_func)

    def get_module(self, name: str) -> ModuleInfo | None:
        """Get module info for a standard library module.

        Args:
            name: Module name

        Returns:
            ModuleInfo if module exists, None otherwise
        """
        if name not in self.modules:
            return None

        module = self.modules[name]
        source_file_path = self._stdlib_path / module.source_file

        try:
            # Load and parse the ML source file
            with open(source_file_path, encoding="utf-8") as f:
                source_code = f.read()

            ast = parse_ml_code(source_code, str(source_file_path))

            return ModuleInfo(
                name=module.name,
                module_path=module.module_path,
                ast=ast,
                source_code=source_code,
                file_path=str(source_file_path),
                is_stdlib=True,
                is_python=False,
                dependencies=self._extract_dependencies(ast),
                capabilities_required=module.capabilities_required,
            )

        except OSError:
            # Module file doesn't exist or can't be read
            return None
        except Exception:
            # Parsing error
            return None

    def get_bridge_functions(self, module_name: str) -> list[BridgeFunction]:
        """Get Python bridge functions for a module.

        Args:
            module_name: Module name

        Returns:
            List of bridge functions
        """
        return self.bridge_functions.get(module_name, [])

    def validate_capabilities(self, module_name: str, required_capabilities: list[str]) -> bool:
        """Validate that required capabilities are available.

        Args:
            module_name: Module requesting capabilities
            required_capabilities: Capabilities needed

        Returns:
            True if all capabilities are available
        """
        # TODO: Integrate with capability manager
        # For now, assume all capabilities are available
        return True

    def call_bridge_function(self, module_name: str, function_name: str, args: list[Any]) -> Any:
        """Call a Python bridge function with capability validation.

        Args:
            module_name: Module name
            function_name: Function name
            args: Function arguments

        Returns:
            Function result

        Raises:
            ImportError: If function not found
            CapabilityError: If capabilities not available
            ValueError: If validation fails
        """
        bridge_functions = self.get_bridge_functions(module_name)
        bridge_func = None

        for func in bridge_functions:
            if func.ml_name == function_name:
                bridge_func = func
                break

        if not bridge_func:
            raise ImportError(
                f"Bridge function '{function_name}' not found in module '{module_name}'"
            )

        # Validate capabilities
        if not self.validate_capabilities(module_name, bridge_func.capabilities_required):
            raise ImportError(f"Required capabilities not available for function '{function_name}'")

        # Validate arguments if validation function provided
        if bridge_func.validation_function:
            try:
                bridge_func.validation_function(args)
            except Exception as e:
                raise ValueError(f"Argument validation failed for '{function_name}': {e}")

        # Import Python module and call function
        try:
            python_module = importlib.import_module(bridge_func.python_module)
            python_function = getattr(python_module, bridge_func.python_function)
            return python_function(*args)
        except ImportError as e:
            raise ImportError(f"Failed to import Python module '{bridge_func.python_module}': {e}")
        except AttributeError as e:
            raise ImportError(
                f"Function '{bridge_func.python_function}' not found in module '{bridge_func.python_module}': {e}"
            )
        except Exception as e:
            raise RuntimeError(f"Error calling bridge function '{function_name}': {e}")

    def list_modules(self) -> list[str]:
        """List all registered modules.

        Returns:
            List of module names
        """
        return list(self.modules.keys())

    def get_module_info(self, name: str) -> StandardLibraryModule | None:
        """Get detailed module information.

        Args:
            name: Module name

        Returns:
            StandardLibraryModule if exists, None otherwise
        """
        return self.modules.get(name)

    def _extract_dependencies(self, ast: Program) -> list[str]:
        """Extract import dependencies from AST."""
        dependencies = []

        for item in ast.items:
            if (
                hasattr(item, "target")
                and hasattr(item, "__class__")
                and "Import" in item.__class__.__name__
            ):
                dep_path = (
                    ".".join(item.target) if isinstance(item.target, list) else str(item.target)
                )
                dependencies.append(dep_path)

        return dependencies

    def auto_discover_modules(self) -> None:
        """Auto-discover and register ML standard library modules."""
        stdlib_dir = Path(__file__).parent

        # Look for .ml files in the stdlib directory
        for ml_file in stdlib_dir.glob("*.ml"):
            module_name = ml_file.stem

            # Skip if already registered
            if module_name in self.modules:
                continue

            try:
                # Try to parse the file to extract metadata
                with open(ml_file, encoding="utf-8") as f:
                    content = f.read()

                # Look for module metadata in comments
                capabilities = self._extract_capabilities_from_source(content)
                description = self._extract_description_from_source(content, module_name)

                self.register_module(
                    name=module_name,
                    source_file=ml_file.name,
                    capabilities_required=capabilities,
                    description=description,
                )

            except Exception:
                # Skip files that can't be parsed
                continue

    def _extract_capabilities_from_source(self, source_code: str) -> list[str]:
        """Extract capability requirements from source code comments."""
        capabilities = []

        for line in source_code.split("\n"):
            line = line.strip()
            if line.startswith("// @capability:"):
                cap = line[15:].strip()
                if cap:
                    capabilities.append(cap)
            elif line.startswith("// @requires:"):
                cap = line[13:].strip()
                if cap:
                    capabilities.append(cap)

        return capabilities

    def _extract_description_from_source(self, source_code: str, default_name: str) -> str:
        """Extract description from source code comments."""
        lines = source_code.split("\n")

        # Look for module docstring or description comment
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith("// @description:"):
                return line[16:].strip()
            elif line.startswith("/**") or line.startswith("/*"):
                # Multi-line comment - extract first line
                comment_lines = []
                for j in range(i, len(lines)):
                    comment_line = lines[j].strip()
                    if comment_line.endswith("*/"):
                        comment_lines.append(comment_line[:-2].strip())
                        break
                    elif comment_line.startswith("*"):
                        comment_lines.append(comment_line[1:].strip())
                    elif j == i:  # First line
                        comment_lines.append(comment_line[2:].strip())

                if comment_lines and comment_lines[0]:
                    return comment_lines[0]

        return f"ML {default_name.title()} Module"


# Global registry instance
_stdlib_registry: StandardLibraryRegistry | None = None


def get_stdlib_registry() -> StandardLibraryRegistry:
    """Get global standard library registry."""
    global _stdlib_registry
    if _stdlib_registry is None:
        _stdlib_registry = StandardLibraryRegistry()
        # Register core modules
        _register_core_modules(_stdlib_registry)
        # Auto-discover additional modules
        _stdlib_registry.auto_discover_modules()
    return _stdlib_registry


def _register_core_modules(registry: StandardLibraryRegistry) -> None:
    """Register core standard library modules."""

    # Math module
    registry.register_module(
        name="math",
        source_file="math.ml",
        capabilities_required=["read:math_constants", "execute:calculations"],
        description="Mathematical operations and constants",
        python_bridge_modules=["mlpy.stdlib.math"],
    )

    # Register math bridge functions
    math_functions = [
        ("sqrt", "mlpy.stdlib.math", "math.sqrt", ["execute:calculations"]),
        ("pow", "mlpy.stdlib.math", "math.pow", ["execute:calculations"]),
        ("sin", "mlpy.stdlib.math", "math.sin", ["execute:calculations"]),
        ("cos", "mlpy.stdlib.math", "math.cos", ["execute:calculations"]),
        ("tan", "mlpy.stdlib.math", "math.tan", ["execute:calculations"]),
        ("log", "mlpy.stdlib.math", "math.log", ["execute:calculations"]),
        ("ln", "mlpy.stdlib.math", "math.ln", ["execute:calculations"]),
        ("exp", "mlpy.stdlib.math", "math.exp", ["execute:calculations"]),
        ("floor", "mlpy.stdlib.math", "math.floor", ["execute:calculations"]),
        ("ceil", "mlpy.stdlib.math", "math.ceil", ["execute:calculations"]),
        ("round", "mlpy.stdlib.math", "math.round", ["execute:calculations"]),
        ("abs", "mlpy.stdlib.math", "math.abs", ["execute:calculations"]),
        ("min", "mlpy.stdlib.math", "math.min", ["execute:calculations"]),
        ("max", "mlpy.stdlib.math", "math.max", ["execute:calculations"]),
        ("random", "mlpy.stdlib.math", "math.random", ["execute:calculations", "read:system_entropy"]),
    ]

    for ml_name, py_module, py_func, caps in math_functions:
        registry.register_bridge_function(
            module_name="math",
            ml_name=ml_name,
            python_module=py_module,
            python_function=py_func,
            capabilities_required=caps,
        )

    # JSON module
    registry.register_module(
        name="json",
        source_file="json.ml",
        capabilities_required=["read:json_data", "write:json_data"],
        description="JSON encoding and decoding",
        python_bridge_modules=["json"],
    )

    # Register JSON bridge functions
    json_functions = [
        ("dumps", "json", "dumps", ["write:json_data"]),
        ("loads", "json", "loads", ["read:json_data"]),
    ]

    for ml_name, py_module, py_func, caps in json_functions:
        registry.register_bridge_function(
            module_name="json",
            ml_name=ml_name,
            python_module=py_module,
            python_function=py_func,
            capabilities_required=caps,
        )

    # String module
    registry.register_module(
        name="string",
        source_file="string.ml",
        capabilities_required=["execute:string_operations"],
        description="String manipulation utilities",
        python_bridge_modules=["builtins"],
    )

    # DateTime module
    registry.register_module(
        name="datetime",
        source_file="datetime.ml",
        capabilities_required=["read:system_time", "read:timezone_data"],
        description="Date and time operations",
        python_bridge_modules=["datetime"],
    )

    # Functional programming module
    registry.register_module(
        name="functional",
        source_file="functional.ml",
        capabilities_required=["execute:functional_operations", "read:function_data"],
        description="Comprehensive functional programming utilities",
        python_bridge_modules=["builtins", "functools", "itertools"],
    )

    # Register functional programming bridge functions
    functional_functions = [
        ("len", "builtins", "len", ["read:function_data"]),
        ("list_append", "builtins", "list_append_helper", ["execute:functional_operations"]),
        ("isinstance", "builtins", "isinstance", ["read:function_data"]),
        ("str", "builtins", "str", ["execute:functional_operations"]),
        ("reduce", "functools", "reduce", ["execute:functional_operations"]),
        ("partial", "functools", "partial", ["execute:functional_operations"]),
    ]

    for ml_name, py_module, py_func, caps in functional_functions:
        registry.register_bridge_function(
            module_name="functional",
            ml_name=ml_name,
            python_module=py_module,
            python_function=py_func,
            capabilities_required=caps,
        )

    # Collections module
    registry.register_module(
        name="collections",
        source_file="collections.ml",
        capabilities_required=["execute:collection_operations"],
        description="List and dictionary operations",
        python_bridge_modules=["mlpy.stdlib.collections"],
    )

    # Register collections bridge functions
    collections_functions = [
        ("length", "mlpy.stdlib.collections", "collections.length", ["execute:collection_operations"]),
        ("append", "mlpy.stdlib.collections", "collections.append", ["execute:collection_operations"]),
        ("prepend", "mlpy.stdlib.collections", "collections.prepend", ["execute:collection_operations"]),
        ("concat", "mlpy.stdlib.collections", "collections.concat", ["execute:collection_operations"]),
        ("get", "mlpy.stdlib.collections", "collections.get", ["execute:collection_operations"]),
        ("first", "mlpy.stdlib.collections", "collections.first", ["execute:collection_operations"]),
        ("last", "mlpy.stdlib.collections", "collections.last", ["execute:collection_operations"]),
        ("slice", "mlpy.stdlib.collections", "collections.slice", ["execute:collection_operations"]),
        ("reverse", "mlpy.stdlib.collections", "collections.reverse", ["execute:collection_operations"]),
        ("contains", "mlpy.stdlib.collections", "collections.contains", ["execute:collection_operations"]),
        ("indexOf", "mlpy.stdlib.collections", "collections.indexOf", ["execute:collection_operations"]),
        ("filter", "mlpy.stdlib.collections", "collections.filter", ["execute:collection_operations"]),
        ("map", "mlpy.stdlib.collections", "collections.map", ["execute:collection_operations"]),
        ("find", "mlpy.stdlib.collections", "collections.find", ["execute:collection_operations"]),
        ("reduce", "mlpy.stdlib.collections", "collections.reduce", ["execute:collection_operations"]),
        ("removeAt", "mlpy.stdlib.collections", "collections.removeAt", ["execute:collection_operations"]),
    ]

    for ml_name, py_module, py_func, caps in collections_functions:
        registry.register_bridge_function(
            module_name="collections",
            ml_name=ml_name,
            python_module=py_module,
            python_function=py_func,
            capabilities_required=caps,
        )

    # Random module
    registry.register_module(
        name="random",
        source_file="random.ml",
        capabilities_required=["execute:random_operations", "read:system_entropy"],
        description="Random number generation and utilities",
        python_bridge_modules=["mlpy.stdlib.random"],
    )

    # Register random bridge functions
    random_functions = [
        ("setSeed", "mlpy.stdlib.random", "random.setSeed", ["execute:random_operations"]),
        ("getSeed", "mlpy.stdlib.random", "random.getSeed", ["execute:random_operations"]),
        ("nextInt", "mlpy.stdlib.random", "random.nextInt", ["execute:random_operations", "read:system_entropy"]),
        ("random", "mlpy.stdlib.random", "random.random", ["execute:random_operations", "read:system_entropy"]),
        ("randomFloat", "mlpy.stdlib.random", "random.randomFloat", ["execute:random_operations", "read:system_entropy"]),
        ("randomInt", "mlpy.stdlib.random", "random.randomInt", ["execute:random_operations", "read:system_entropy"]),
        ("randomBool", "mlpy.stdlib.random", "random.randomBool", ["execute:random_operations", "read:system_entropy"]),
        ("randomBoolWeighted", "mlpy.stdlib.random", "random.randomBoolWeighted", ["execute:random_operations", "read:system_entropy"]),
        ("choice", "mlpy.stdlib.random", "random.choice", ["execute:random_operations", "read:system_entropy"]),
        ("shuffle", "mlpy.stdlib.random", "random.shuffle", ["execute:random_operations", "read:system_entropy"]),
        ("sample", "mlpy.stdlib.random", "random.sample", ["execute:random_operations", "read:system_entropy"]),
        ("randomNormal", "mlpy.stdlib.random", "random.randomNormal", ["execute:random_operations", "read:system_entropy"]),
        ("length", "mlpy.stdlib.random", "random.length", ["execute:random_operations"]),
        ("sqrt", "mlpy.stdlib.random", "random.sqrt", ["execute:random_operations"]),
        ("abs", "mlpy.stdlib.random", "random.abs", ["execute:random_operations"]),
        ("sin", "mlpy.stdlib.random", "random.sin", ["execute:random_operations"]),
        ("cos", "mlpy.stdlib.random", "random.cos", ["execute:random_operations"]),
        ("ln", "mlpy.stdlib.random", "random.ln", ["execute:random_operations"]),
    ]

    for ml_name, py_module, py_func, caps in random_functions:
        registry.register_bridge_function(
            module_name="random",
            ml_name=ml_name,
            python_module=py_module,
            python_function=py_func,
            capabilities_required=caps,
        )
