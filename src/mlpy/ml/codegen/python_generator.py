"""Python code generator from ML AST with source map support."""

import json
from pathlib import Path
from typing import Any

from mlpy.ml.grammar.ast_nodes import *
from mlpy.runtime.profiling.decorators import profile_parser

from .safe_attribute_registry import get_safe_registry
from .allowed_functions_registry import AllowedFunctionsRegistry
from .enhanced_source_maps import EnhancedSourceMapGenerator, EnhancedSourceMap
from .core.context import SourceMapping, CodeGenerationContext
from .core.generator_base import GeneratorBase
from .helpers.expression_helpers import ExpressionHelpersMixin
from .helpers.function_call_helpers import FunctionCallHelpersMixin
from .visitors.statement_visitors import StatementVisitorsMixin
from .visitors.expression_visitors import ExpressionVisitorsMixin
from .visitors.literal_visitors import LiteralVisitorsMixin


class PythonCodeGenerator(LiteralVisitorsMixin, ExpressionVisitorsMixin, StatementVisitorsMixin, FunctionCallHelpersMixin, ExpressionHelpersMixin, GeneratorBase):
    """Generates Python code from ML AST with security and source map support.

    Supports REPL mode for incremental compilation without full symbol validation.
    """

    def __init__(
        self,
        source_file: str | None = None,
        generate_source_maps: bool = True,
        import_paths: list[str] | None = None,
        allow_current_dir: bool = False,
        module_output_mode: str = 'separate',  # 'separate' or 'inline'
        repl_mode: bool = False
    ):
        """Initialize Python code generator.

        Args:
            source_file: Source ML file path for source maps
            generate_source_maps: Whether to generate source map data
            import_paths: Paths to search for user modules
            allow_current_dir: Allow imports from current directory
            module_output_mode: 'separate' (create .py files) or 'inline' (embed in main file)
            repl_mode: Enable REPL mode (skip undefined variable validation)
        """
        self.source_file = source_file
        self.generate_source_maps = generate_source_maps
        self.context = CodeGenerationContext()
        self.output_lines: list[str] = []
        self.function_registry = AllowedFunctionsRegistry()  # Whitelist enforcement
        self.import_paths = import_paths or []
        self.allow_current_dir = allow_current_dir
        self.module_output_mode = module_output_mode
        self.compiled_modules: dict[str, str] = {}  # Cache of transpiled user modules (for inline mode)
        self.module_py_files: dict[str, str] = {}  # Map of module_path -> .py file path (for separate mode)
        self.repl_mode = repl_mode  # REPL mode flag

        # Symbol table for compile-time identifier validation
        self.symbol_table = {
            'variables': set(),      # User-defined variables
            'functions': set(),      # User-defined functions
            'parameters': [],        # Function parameters (stack for nested scopes)
            'imports': {'builtin'},  # Imported module names (builtin always available)
            'ml_builtins': self._discover_ml_builtins()  # ML stdlib builtins
        }

    def _discover_ml_builtins(self) -> set[str]:
        """Discover all ML builtin functions by inspecting @ml_function decorators.

        This dynamically inspects the builtin module to find all functions
        decorated with @ml_function, rather than using a hardcoded list.

        Returns:
            Set of ML builtin function names
        """
        try:
            from mlpy.stdlib.builtin import builtin

            ml_builtins = set()
            for attr_name in dir(builtin):
                # Skip private/dunder attributes
                if attr_name.startswith('_'):
                    continue

                try:
                    attr = getattr(builtin, attr_name)
                    # Check if it's callable and has ML function metadata
                    if callable(attr) and hasattr(attr, '_ml_function_metadata'):
                        ml_builtins.add(attr_name)
                except AttributeError:
                    # Skip attributes that can't be accessed
                    continue

            return ml_builtins
        except ImportError:
            # If builtin module not available, return empty set
            # This allows code generator to work even without stdlib
            return set()

    @profile_parser
    def generate(self, ast: Program) -> tuple[str, dict[str, Any] | None]:
        """Generate Python code from ML AST.

        Args:
            ast: Root Program AST node

        Returns:
            Tuple of (Python code string, source map data)
        """
        self.context = CodeGenerationContext()
        self.output_lines = []
        self.function_registry = AllowedFunctionsRegistry()  # Fresh registry for each compilation

        # Initialize enhanced source map generator if source maps are enabled
        if self.generate_source_maps:
            self.context.enhanced_source_map_generator = EnhancedSourceMapGenerator(self.source_file)

        # Reset symbol table (preserve ml_builtins from initialization)
        ml_builtins = self.symbol_table['ml_builtins']
        self.symbol_table = {
            'variables': set(),
            'functions': set(),
            'parameters': [],  # Stack for nested function scopes
            'imports': {'builtin'},  # builtin module always available
            'ml_builtins': ml_builtins
        }

        # First pass: analyze AST to determine what imports are needed
        temp_context = self.context
        temp_registry = self.function_registry

        ast.accept(self)

        # Save state after first pass (includes discovered imports, variables, functions)
        imports_from_first_pass = self.symbol_table['imports'].copy()
        variables_from_first_pass = self.symbol_table['variables'].copy()
        functions_from_first_pass = self.symbol_table['functions'].copy()

        # Reset context for actual generation
        self.context = temp_context
        self.function_registry = temp_registry
        self.output_lines = []

        # Create fresh symbol table with data from first pass
        ml_builtins = self.symbol_table['ml_builtins']
        self.symbol_table = {
            'variables': variables_from_first_pass,
            'functions': functions_from_first_pass,
            'parameters': [],  # Fresh parameter stack
            'imports': imports_from_first_pass,
            'ml_builtins': ml_builtins
        }

        # Generate header
        self._emit_header()

        # Generate runtime validator import
        self._generate_runtime_imports()

        # Auto-import builtin module if any builtin functions were used
        if self.context.builtin_functions_used:
            self._emit_line("from mlpy.stdlib.builtin import builtin")
            self._emit_line("")

        # Generate imports if needed (but exclude contextlib as it's in header)
        remaining_imports = self.context.imports_needed - {"contextlib"}
        if remaining_imports:
            for import_name in sorted(remaining_imports):
                # Handle both "import xyz" and "from xyz import abc" statements
                if import_name.startswith("from ") or import_name.startswith("import "):
                    self._emit_line(import_name)
                elif import_name == "mlpy.stdlib.runtime_helpers":
                    # Special handling for runtime helpers to import specific functions
                    self._emit_line(
                        "from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length"
                    )
                else:
                    self._emit_line(f"import {import_name}")
            self._emit_line("")

        # Add sys.path setup for user modules in separate file mode
        if self.module_output_mode == 'separate' and self.module_py_files:
            # Import sys and Path for module path setup
            self._emit_line("import sys")
            self._emit_line("from pathlib import Path")
            self._emit_line("")
            self._emit_line("# ============================================================================")
            self._emit_line("# User Module Path Setup")
            self._emit_line("# ============================================================================")

            # Add import paths to sys.path
            added_paths = set()
            for import_path in self.import_paths:
                if import_path not in added_paths:
                    # Use repr() to properly escape Windows paths
                    self._emit_line(f"if str(Path({repr(import_path)}).resolve()) not in sys.path:")
                    self._indent()
                    self._emit_line(f"sys.path.insert(0, str(Path({repr(import_path)}).resolve()))")
                    self._dedent()
                    added_paths.add(import_path)

            # Add source file directory if allow_current_dir
            # Skip in REPL mode since __file__ is not available
            if self.allow_current_dir and self.source_file and not self.repl_mode:
                self._emit_line("# Add source file directory to path")
                self._emit_line("_source_dir = Path(__file__).parent")
                self._emit_line("if str(_source_dir) not in sys.path:")
                self._indent()
                self._emit_line("sys.path.insert(0, str(_source_dir))")
                self._dedent()

            self._emit_line("")

        # Emit user modules that were collected during first pass (inline mode only)
        if self.module_output_mode == 'inline' and self.compiled_modules:
            self._emit_line("# ============================================================================")
            self._emit_line("# User Module Definitions (Inline)")
            self._emit_line("# ============================================================================")
            self._emit_line("")
            # Emit the stored module code
            for module_path, module_code in self.compiled_modules.items():
                self._emit_line(f"# Module: {module_path}")
                self._emit_line(module_code.strip())
                self._emit_line("")
            self._emit_line("# ============================================================================")
            self._emit_line("# Main Program Code")
            self._emit_line("# ============================================================================")
            self._emit_line("")

        # Generate main code
        ast.accept(self)

        # Generate footer
        self._emit_footer()

        # Combine output
        python_code = "\n".join(self.output_lines)

        # Generate source map - use enhanced source map if available
        source_map = None
        if self.generate_source_maps and self.context.enhanced_source_map_generator:
            # Finalize enhanced source map and convert to dict format
            enhanced_map = self.context.enhanced_source_map_generator.finalize()
            source_map = json.loads(enhanced_map.to_json())
        elif self.generate_source_maps:
            # Fallback to basic source map
            source_map = self._generate_source_map()

        return python_code, source_map

    def _emit_header(self):
        """Emit Python file header."""
        self._emit_line('"""Generated Python code from mlpy ML transpiler."""')
        self._emit_line("")
        self._emit_line("# This code was automatically generated from ML source")
        self._emit_line("# Modifications to this file may be lost on regeneration")
        self._emit_line("")

        # Add contextlib import if capabilities are present
        if "contextlib" in self.context.imports_needed:
            self._emit_line("import contextlib")
            self._emit_line("")

    def _generate_runtime_imports(self):
        """Generate runtime validator import at top of file.

        Adds the safe_call import that will be used to wrap function calls.
        This is the foundation of runtime whitelist enforcement.
        """
        self._emit_line("# ============================================================================")
        self._emit_line("# Runtime Whitelist Enforcement")
        self._emit_line("# ============================================================================")
        self._emit_line("from mlpy.runtime.whitelist_validator import safe_call as _safe_call")
        self._emit_line("")

    def _emit_imports(self):
        """Emit necessary Python imports."""
        for import_name in sorted(self.context.imports_needed):
            # Handle both "import xyz" and "from xyz import abc" statements
            if import_name.startswith("from ") or import_name.startswith("import "):
                self._emit_line(import_name)
            elif import_name == "mlpy.stdlib.runtime_helpers":
                # Special handling for runtime helpers to import specific functions
                self._emit_line(
                    "from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length"
                )
            else:
                self._emit_line(f"import {import_name}")

    def _emit_footer(self):
        """Emit Python file footer."""
        self._emit_line("")
        self._emit_line("# End of generated code")

    def _emit_line(self, line: str, original_node: ASTNode | None = None):
        """Emit a line of Python code with source mapping."""
        self.output_lines.append(self._get_indentation() + line)

        # Track source mapping with enhanced source map generator
        if self.generate_source_maps and original_node and self.context.enhanced_source_map_generator:
            generated_line = len(self.output_lines)
            generated_column = self.context.indentation_level * 4

            # Use the enhanced source map generator to track this node
            self.context.enhanced_source_map_generator.track_node(
                node=original_node,
                generated_line=generated_line,
                generated_column=generated_column,
                symbol_name=self._extract_symbol_name(original_node)
            )
        elif self.generate_source_maps and original_node:
            # Fallback to basic source mapping
            mapping = SourceMapping(
                generated_line=len(self.output_lines),
                generated_column=self.context.indentation_level * 4,
                original_line=original_node.line,
                original_column=original_node.column,
                original_file=self.source_file,
            )
            self.context.source_mappings.append(mapping)

    def _emit_raw_line(self, line: str):
        """Emit a raw line without indentation."""
        self.output_lines.append(line)

    def _get_indentation(self) -> str:
        """Get current indentation string."""
        return "    " * self.context.indentation_level

    def _indent(self):
        """Increase indentation level."""
        self.context.indentation_level += 1

    def _dedent(self):
        """Decrease indentation level."""
        self.context.indentation_level = max(0, self.context.indentation_level - 1)

    def _extract_symbol_name(self, node: ASTNode) -> str | None:
        """Extract symbol name from an AST node for source map tracking."""
        if isinstance(node, FunctionDefinition):
            return node.name.name if hasattr(node.name, "name") else str(node.name)
        elif isinstance(node, AssignmentStatement):
            if isinstance(node.target, str):
                return node.target
            elif hasattr(node.target, "name"):
                return node.target.name
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, Parameter):
            return node.name if hasattr(node, "name") else None
        return None

    def _safe_identifier(self, name: str) -> str:
        """Convert ML identifier to safe Python identifier."""
        # Handle non-string inputs defensively
        if not isinstance(name, str):
            return f"ml_unknown_identifier_{id(name)}"

        # Handle ML-specific literals that need conversion to Python equivalents
        if name == "null":
            return "None"

        # Handle Python keywords and reserved names
        python_keywords = {
            "and",
            "as",
            "assert",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "not",
            "or",
            "pass",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield",
            "None",
            "True",
            "False",
        }

        if name in python_keywords:
            return f"ml_{name}"

        # Ensure valid Python identifier
        if not name.isidentifier():
            # Replace invalid characters with underscores
            safe_name = "".join(c if c.isalnum() or c == "_" else "_" for c in name)
            if safe_name[0].isdigit():
                safe_name = f"ml_{safe_name}"
            return safe_name

        return name

    def _generate_source_map(self) -> dict[str, Any]:
        """Generate source map data."""
        return {
            "version": 3,
            "file": f"{Path(self.source_file).stem}.py" if self.source_file else "generated.py",
            "sourceRoot": "",
            "sources": [self.source_file] if self.source_file else ["unknown.ml"],
            "names": [],
            "mappings": self._encode_mappings(),
            "sourcesContent": [self._get_source_content()] if self.source_file else [None],
        }

    def _encode_mappings(self) -> str:
        """Encode source mappings to VLQ format (simplified)."""
        # For now, return a simplified mapping representation
        # In a full implementation, this would use VLQ base64 encoding
        return json.dumps(
            [
                {
                    "generated": {"line": m.generated_line, "column": m.generated_column},
                    "original": {"line": m.original_line, "column": m.original_column},
                    "source": m.original_file,
                    "name": m.name,
                }
                for m in self.context.source_mappings
                if m.original_line is not None
            ]
        )

    def _get_source_content(self) -> str | None:
        """Get original source content for source map."""
        if not self.source_file:
            return None

        try:
            return Path(self.source_file).read_text(encoding="utf-8")
        except Exception:
            return None

    # AST Visitor Methods

    # NOTE: visit_program() moved to StatementVisitorsMixin

    # NOTE: visit_capability_declaration() moved to StatementVisitorsMixin

    # NOTE: visit_resource_pattern() moved to StatementVisitorsMixin

    # NOTE: visit_permission_grant() moved to StatementVisitorsMixin

    # NOTE: visit_import_statement() moved to StatementVisitorsMixin

    def _find_similar_names(self, target: str, available: set) -> list[str]:
        """Find similar module names using Levenshtein distance."""
        import difflib
        return difflib.get_close_matches(target, available, n=3, cutoff=0.6)

    # NOTE: visit_function_definition() moved to StatementVisitorsMixin

    # NOTE: visit_parameter() moved to StatementVisitorsMixin

    # NOTE: visit_expression_statement() moved to StatementVisitorsMixin

    # NOTE: visit_assignment_statement() moved to StatementVisitorsMixin

    # NOTE: visit_return_statement() moved to StatementVisitorsMixin

    # NOTE: visit_block_statement() moved to StatementVisitorsMixin

    # NOTE: visit_if_statement() moved to StatementVisitorsMixin

    # NOTE: visit_elif_clause() moved to StatementVisitorsMixin

    # NOTE: visit_while_statement() moved to StatementVisitorsMixin

    # NOTE: visit_for_statement() moved to StatementVisitorsMixin

    # NOTE: visit_try_statement() moved to StatementVisitorsMixin

    # NOTE: visit_except_clause() moved to StatementVisitorsMixin

    # NOTE: visit_break_statement() moved to StatementVisitorsMixin

    # NOTE: visit_continue_statement() moved to StatementVisitorsMixin

    # NOTE: visit_nonlocal_statement() moved to StatementVisitorsMixin

    # NOTE: visit_throw_statement() moved to StatementVisitorsMixin

    # Lambda generation methods extracted to helpers/function_call_helpers.py (Phase 3e)

    # ============================================================================
    # Runtime Whitelist Enforcement - Function Call Wrapping (Phase 3e)
    # ============================================================================
    # Function call wrapping and generation methods extracted to
    # helpers/function_call_helpers.py (FunctionCallHelpersMixin)
    #
    # Extracted methods:
    # - _should_wrap_call() - Wrapping decision logic
    # - _generate_function_call_wrapped() - Main entry point
    # - _generate_direct_call() - Direct unwrapped calls
    # - _generate_wrapped_call() - Wrapped secure calls
    # - _generate_simple_function_call() - Simple function calls (legacy)
    # - _generate_member_function_call() - Member calls (legacy)
    # - _raise_unknown_function_error() - Error handling
    # - _raise_unknown_module_function_error() - Module error handling

    #  ============================================================================
    # User Module Resolution
    # ============================================================================
    def _get_ml_module_info(self, module_path: str, metadata) -> dict:
        """Convert UnifiedModuleMetadata to module info dict for transpilation.

        Args:
            module_path: Module path (e.g., "math_utils")
            metadata: Registry metadata for the ML module

        Returns:
            Module info dict compatible with _generate_user_module_import()
        """
        from pathlib import Path
        from mlpy.ml.grammar.parser import MLParser

        ml_file = Path(metadata.file_path)

        # Parse the ML source
        parser = MLParser()
        source_code = ml_file.read_text(encoding='utf-8')
        ast = parser.parse(source_code, str(ml_file))

        return {
            'name': metadata.name.split('.')[-1],  # Last component
            'module_path': module_path,
            'ast': ast,
            'source_code': source_code,
            'file_path': str(ml_file)
        }

    def _resolve_user_module(self, import_target: list[str]) -> Any:
        """Resolve user module using import paths.

        Args:
            import_target: Module path components (e.g., ['user_modules', 'sorting'])

        Returns:
            ModuleInfo if module found, None otherwise
        """
        from pathlib import Path

        module_path = ".".join(import_target)
        file_parts = import_target[:]

        # Try to find the module file in import paths
        for base_path in self.import_paths:
            # Try as direct file: user_modules/sorting.ml
            module_file = Path(base_path) / "/".join(file_parts[:-1]) / f"{file_parts[-1]}.ml"

            if module_file.exists():
                # Read and parse the module
                from mlpy.ml.grammar.parser import MLParser

                parser = MLParser()
                source_code = module_file.read_text(encoding='utf-8')
                ast = parser.parse(source_code, str(module_file))

                # Create a simple ModuleInfo-like dict
                return {
                    'name': file_parts[-1],
                    'module_path': module_path,
                    'ast': ast,
                    'source_code': source_code,
                    'file_path': str(module_file)
                }

        # Try from source file directory if available
        if self.source_file and self.allow_current_dir:
            source_dir = Path(self.source_file).parent
            module_file = source_dir / "/".join(file_parts[:-1]) / f"{file_parts[-1]}.ml"

            if module_file.exists():
                from mlpy.ml.grammar.parser import MLParser

                parser = MLParser()
                source_code = module_file.read_text(encoding='utf-8')
                ast = parser.parse(source_code, str(module_file))

                return {
                    'name': file_parts[-1],
                    'module_path': module_path,
                    'ast': ast,
                    'source_code': source_code,
                    'file_path': str(module_file)
                }

        return None

    def _generate_user_module_import(self, module_info: dict, alias: str | None, node: Any) -> None:
        """Generate import code for user-defined module.

        Args:
            module_info: Module information dict
            alias: Optional import alias
            node: AST node for source mapping
        """
        module_path = module_info['module_path']

        if self.module_output_mode == 'separate':
            # Separate file mode: compile to .py file and use normal Python import
            py_file = self._compile_module_to_file(module_info)

            # Generate Python import statement
            # Convert module path to Python module name (e.g., user_modules.sorting)
            if alias:
                self._emit_line(f"import {module_path} as {alias}", node)
                self.symbol_table['imports'].add(alias)
            else:
                # For nested imports, we need to import the full path
                parts = module_path.split('.')
                for i in range(len(parts)):
                    partial_path = '.'.join(parts[:i+1])
                    self.symbol_table['imports'].add(partial_path)

                self._emit_line(f"import {module_path}", node)
        else:
            # Inline mode: embed module code in output file
            if module_path not in self.compiled_modules:
                self._transpile_user_module(module_info)

            # Track all parts of the module path in imports
            parts = module_path.split('.')
            for i in range(len(parts)):
                partial_path = '.'.join(parts[:i+1])
                self.symbol_table['imports'].add(partial_path)
                python_name = partial_path.replace('.', '_')
                self.symbol_table['imports'].add(python_name)

            if alias:
                alias_name = self._safe_identifier(alias)
                python_module_name = module_path.replace('.', '_')
                self._emit_line(f"{alias_name} = {python_module_name}", node)
                self.symbol_table['imports'].add(alias_name)

    def _compile_module_to_file(self, module_info: dict) -> str:
        """Compile user module to .py file (with caching).

        Args:
            module_info: Module information dict

        Returns:
            Path to the generated .py file
        """
        from pathlib import Path
        import os

        module_path = module_info['module_path']
        ml_file = Path(module_info['file_path'])

        # Determine output .py file path (same directory as .ml file)
        py_file = ml_file.with_suffix('.py')

        # Check if we need to recompile
        needs_compile = True
        if py_file.exists():
            ml_mtime = ml_file.stat().st_mtime
            py_mtime = py_file.stat().st_mtime
            if py_mtime >= ml_mtime:
                # .py file is up-to-date
                needs_compile = False

        if needs_compile:
            # Transpile the module
            module_generator = PythonCodeGenerator(
                source_file=str(ml_file),
                generate_source_maps=False,
                import_paths=self.import_paths,
                allow_current_dir=self.allow_current_dir,
                module_output_mode='separate'  # Recursive compilation uses same mode
            )

            python_code, _ = module_generator.generate(module_info['ast'])

            # Write to .py file
            try:
                py_file.write_text(python_code, encoding='utf-8')
            except (IOError, PermissionError) as e:
                # If we can't write the file, fall back to inline mode
                raise Exception(f"Cannot write module file {py_file}: {e}. Consider using inline mode.")

        # Create __init__.py files for package structure
        self._ensure_package_structure(ml_file.parent, module_path)

        # Track the compiled module
        self.module_py_files[module_path] = str(py_file)

        return str(py_file)

    def _ensure_package_structure(self, base_dir: Path, module_path: str) -> None:
        """Create __init__.py files for package directories.

        Args:
            base_dir: Base directory containing the module (where the .ml file's parent dir is)
            module_path: Dotted module path (e.g., 'user_modules.sorting')
        """
        from pathlib import Path

        parts = module_path.split('.')

        # For user_modules.sorting with sorting.ml in user_modules/ directory:
        # We need to create user_modules/__init__.py
        # base_dir is the parent of user_modules (e.g., tests/ml_integration/ml_module)

        # We look for the first part as a directory from base_dir
        # For 'user_modules.sorting', the sorting.ml is in 'user_modules/' so base_dir == user_modules
        # In this case we create user_modules/__init__.py

        # Actually, base_dir is ml_file.parent which is the directory containing the .ml file
        # For user_modules/sorting.ml, base_dir = user_modules/
        # So for user_modules.sorting, we need to go up one level and create user_modules/__init__.py

        # The .ml file structure is: tests/ml_integration/ml_module/user_modules/sorting.ml
        # base_dir = user_modules/
        # For a module path like 'user_modules.sorting', parts[0] = 'user_modules'
        # We need __init__.py at base_dir level (user_modules/__init__.py)

        # Create __init__.py in the directory containing the module
        init_file = base_dir / '__init__.py'
        if not init_file.exists():
            init_file.write_text('# Auto-generated package file\n', encoding='utf-8')

        # For nested packages (e.g., user_modules.algorithms.quicksort),
        # create __init__.py for intermediate levels
        for i in range(1, len(parts) - 1):
            # For user_modules.algorithms.quicksort, create user_modules/algorithms/__init__.py
            package_path = base_dir / Path(*parts[1:i+1])
            init_file = package_path / '__init__.py'
            if not init_file.exists():
                package_path.mkdir(parents=True, exist_ok=True)
                init_file.write_text('# Auto-generated package file\n', encoding='utf-8')

    def _transpile_user_module(self, module_info: dict) -> None:
        """Transpile user module to Python code.

        Args:
            module_info: Module information dict
        """
        module_path = module_info['module_path']
        parts = module_path.split('.')

        # Create a new generator for the module
        module_generator = PythonCodeGenerator(
            source_file=module_info['file_path'],
            generate_source_maps=False,  # Don't generate source maps for modules
            import_paths=self.import_paths,
            allow_current_dir=self.allow_current_dir
        )

        # Generate Python code from module AST
        python_code, _ = module_generator.generate(module_info['ast'])

        # Extract just the function definitions from the generated code
        # (skip header, imports, footer)
        lines = python_code.split('\n')
        code_lines = []
        in_code_section = False

        for line in lines:
            # Skip header and import sections
            if line.startswith('"""') or line.startswith('#') or line.startswith('from ') or line.startswith('import '):
                continue
            # Skip empty lines at the start
            if not line.strip() and not in_code_section:
                continue
            # Start collecting code
            in_code_section = True
            code_lines.append(line)

        module_code_body = '\n'.join(code_lines).strip()

        # Build the module definition code
        # NEW APPROACH: Define functions at top level with prefix, then attach to namespace
        # This allows functions to call each other normally (same scope level)

        module_class_name = module_path.replace('.', '_')
        function_prefix = f"_umod_{module_path.replace('.', '_')}_"
        module_definition = []

        module_definition.append(f"# --- Begin User Module: {module_path} ---")

        # Parse the module body to extract function names and rewrite calls
        import re
        lines = module_code_body.split('\n')

        # First pass: collect function names
        function_names = []
        for line in lines:
            if line.strip().startswith('def '):
                match = re.match(r'\s*def\s+(\w+)\s*\(', line)
                if match:
                    function_names.append(match.group(1))

        # Second pass: rewrite function definitions and calls
        rewritten_lines = []
        for line in lines:
            if not line.strip():
                continue

            # Rewrite function definitions to use prefix
            if line.strip().startswith('def '):
                match = re.match(r'(\s*)def\s+(\w+)(\s*\(.*)', line)
                if match:
                    indent, func_name, rest = match.groups()
                    rewritten_lines.append(f"{indent}def {function_prefix}{func_name}{rest}")
                    continue

            # Rewrite function calls to use prefix (only for functions defined in this module)
            modified_line = line
            for func_name in function_names:
                # Match function calls: func_name(args) but not def func_name(
                # Be careful not to match substrings
                pattern = r'\b' + re.escape(func_name) + r'\s*\('
                replacement = f'{function_prefix}{func_name}('
                modified_line = re.sub(pattern, replacement, modified_line)

            rewritten_lines.append(modified_line)

        # Emit rewritten function definitions at top level
        for line in rewritten_lines:
            module_definition.append(line)

        module_definition.append('')

        # Create namespace class
        module_definition.append(f"class _ModuleNamespace:")
        module_definition.append(f"    _ml_user_module = True")
        module_definition.append(f"    pass")
        module_definition.append('')

        # Create instance and attach functions
        module_definition.append(f"{module_class_name} = _ModuleNamespace()")
        for func_name in function_names:
            module_definition.append(f"{module_class_name}.{func_name} = {function_prefix}{func_name}")

        module_definition.append(f"# --- End User Module: {module_path} ---")
        module_definition.append('')

        # For nested modules, create the nested structure
        if len(parts) > 1:
            # Create parent namespace classes with module as attribute
            # We'll create a proper class hierarchy instead of using setattr
            parent_class_code = []
            for i in range(len(parts) - 1):
                parent_name = parts[i]
                parent_class_code.append(f"class {parent_name}:")
                # Add marker so runtime_helpers recognizes this as a user module namespace
                parent_class_code.append(f"    _ml_user_module = True")
                parent_class_code.append(f"    {parts[i+1]} = None")

            module_definition.insert(0, '\n'.join(parent_class_code))

            # Create instances and assign the module
            module_name = parts[-1]
            parent_instance_code = f"{parts[0]} = {parts[0]}()\n{parts[0]}.{parts[1]} = {module_class_name}"
            module_definition.append(parent_instance_code)

        # Store the complete module definition to be emitted later
        self.compiled_modules[module_path] = '\n'.join(module_definition)

    # NOTE: _generate_assignment_target() moved to ExpressionHelpersMixin

def generate_python_code(
    ast: Program,
    source_file: str | None = None,
    generate_source_maps: bool = True,
    import_paths: list[str] | None = None,
    allow_current_dir: bool = True,
    module_output_mode: str = 'separate',
    repl_mode: bool = False
) -> tuple[str, dict[str, Any] | None]:
    """Generate Python code from ML AST.

    Args:
        ast: Root Program AST node
        source_file: Source ML file path for source maps
        generate_source_maps: Whether to generate source map data
        import_paths: Paths to search for user modules
        allow_current_dir: Allow imports from current directory
        module_output_mode: 'separate' (create .py files) or 'inline' (embed in main file)
        repl_mode: Enable REPL mode (skip undefined variable validation)

    Returns:
        Tuple of (Python code string, source map data)
    """
    generator = PythonCodeGenerator(
        source_file,
        generate_source_maps,
        import_paths,
        allow_current_dir,
        module_output_mode,
        repl_mode  # Pass REPL mode to generator
    )
    python_code, source_map = generator.generate(ast)

    # The generator.generate() method creates the enhanced source map with
    # proper line tracking from EnhancedSourceMapGenerator.track_node()
    # which uses actual AST node line/column info (now extracted from Lark metadata)
    return python_code, source_map
