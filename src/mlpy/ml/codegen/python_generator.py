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
from .helpers.module_handlers import ModuleHandlersMixin
from .helpers.source_map_helpers import SourceMapHelpersMixin
from .helpers.utility_helpers import UtilityHelpersMixin
from .visitors.statement_visitors import StatementVisitorsMixin
from .visitors.expression_visitors import ExpressionVisitorsMixin
from .visitors.literal_visitors import LiteralVisitorsMixin


class PythonCodeGenerator(
    LiteralVisitorsMixin,
    ExpressionVisitorsMixin,
    StatementVisitorsMixin,
    FunctionCallHelpersMixin,
    ModuleHandlersMixin,
    SourceMapHelpersMixin,
    UtilityHelpersMixin,
    ExpressionHelpersMixin,
    GeneratorBase
):
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
        repl_mode: bool = False,
        known_imports: list[str] | None = None
    ):
        """Initialize Python code generator.

        Args:
            source_file: Source ML file path for source maps
            generate_source_maps: Whether to generate source map data
            import_paths: Paths to search for user modules
            allow_current_dir: Allow imports from current directory
            module_output_mode: 'separate' (create .py files) or 'inline' (embed in main file)
            repl_mode: Enable REPL mode (skip undefined variable validation)
            known_imports: List of module names already imported (for REPL mode)
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
        self.known_imports = known_imports or []  # Pre-imported modules (REPL)

        # Symbol table for compile-time identifier validation
        # In REPL mode, pre-populate with known imports from previous lines
        initial_imports = {'builtin'}
        if known_imports:
            initial_imports.update(known_imports)

        self.symbol_table = {
            'variables': set(),      # User-defined variables
            'functions': set(),      # User-defined functions
            'parameters': [],        # Function parameters (stack for nested scopes)
            'imports': initial_imports,  # Imported module names (builtin always available)
            'ml_builtins': self._discover_ml_builtins()  # ML stdlib builtins
        }

    # NOTE: _discover_ml_builtins() moved to UtilityHelpersMixin

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

        # Reset symbol table (preserve ml_builtins and known_imports from initialization)
        ml_builtins = self.symbol_table['ml_builtins']

        # In REPL mode, preserve known imports from previous executions
        initial_imports = {'builtin'}
        if self.known_imports:
            initial_imports.update(self.known_imports)

        self.symbol_table = {
            'variables': set(),
            'functions': set(),
            'parameters': [],  # Stack for nested function scopes
            'imports': initial_imports,  # builtin + known imports (REPL)
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

    # NOTE: _extract_symbol_name() moved to SourceMapHelpersMixin

    # NOTE: _safe_identifier() moved to UtilityHelpersMixin

    # NOTE: _generate_source_map() moved to SourceMapHelpersMixin

    # NOTE: _encode_mappings() moved to SourceMapHelpersMixin

    # NOTE: _get_source_content() moved to SourceMapHelpersMixin

    # AST Visitor Methods

    # NOTE: visit_program() moved to StatementVisitorsMixin

    # NOTE: visit_capability_declaration() moved to StatementVisitorsMixin

    # NOTE: visit_resource_pattern() moved to StatementVisitorsMixin

    # NOTE: visit_permission_grant() moved to StatementVisitorsMixin

    # NOTE: visit_import_statement() moved to StatementVisitorsMixin

    # NOTE: _find_similar_names() moved to ModuleHandlersMixin

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
    # User Module Resolution (Phase 4)
    # ============================================================================
    # Module handling methods extracted to helpers/module_handlers.py (ModuleHandlersMixin)
    #
    # Extracted methods:
    # - _get_ml_module_info() - Convert registry metadata to module info dict
    # - _resolve_user_module() - Resolve module using import paths
    # - _generate_user_module_import() - Generate import code for user module
    # - _compile_module_to_file() - Compile module to .py file with caching
    # - _ensure_package_structure() - Create __init__.py files for packages
    # - _transpile_user_module() - Transpile user module to Python code

    # NOTE: _generate_assignment_target() moved to ExpressionHelpersMixin

def generate_python_code(
    ast: Program,
    source_file: str | None = None,
    generate_source_maps: bool = True,
    import_paths: list[str] | None = None,
    allow_current_dir: bool = True,
    module_output_mode: str = 'separate',
    repl_mode: bool = False,
    known_imports: list[str] | None = None
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
        known_imports: List of module names already imported (for REPL mode)

    Returns:
        Tuple of (Python code string, source map data)
    """
    generator = PythonCodeGenerator(
        source_file,
        generate_source_maps,
        import_paths,
        allow_current_dir,
        module_output_mode,
        repl_mode,  # Pass REPL mode to generator
        known_imports  # Pass known imports for REPL
    )
    python_code, source_map = generator.generate(ast)

    # The generator.generate() method creates the enhanced source map with
    # proper line tracking from EnhancedSourceMapGenerator.track_node()
    # which uses actual AST node line/column info (now extracted from Lark metadata)
    return python_code, source_map
