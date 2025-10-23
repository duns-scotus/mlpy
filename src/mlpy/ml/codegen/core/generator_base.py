"""Base code generator class with core infrastructure.

This module provides the foundational GeneratorBase class that handles
initialization, code generation orchestration, and code emission.
"""

import json
from pathlib import Path
from typing import Any

from mlpy.ml.grammar.ast_nodes import ASTNode, ASTVisitor, Program, FunctionDefinition, AssignmentStatement, Identifier, Parameter
from mlpy.runtime.profiling.decorators import profile_parser

from ..allowed_functions_registry import AllowedFunctionsRegistry
from ..enhanced_source_maps import EnhancedSourceMapGenerator, EnhancedSourceMap
from .context import SourceMapping, CodeGenerationContext


class GeneratorBase(ASTVisitor):
    """Base generator class providing core code generation infrastructure.

    This class handles:
    - Initialization and configuration
    - Code generation orchestration (generate method)
    - Code emission (_emit_* methods)
    - Indentation management
    - Source map generation
    - Symbol table management

    Subclasses should add visitor methods for specific AST node types.
    """

    def __init__(
        self,
        source_file: str | None = None,
        generate_source_maps: bool = True,
        import_paths: list[str] | None = None,
        allow_current_dir: bool = False,
        module_output_mode: str = 'separate',
        repl_mode: bool = False
    ):
        """Initialize the code generator.

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
        self.function_registry = AllowedFunctionsRegistry()
        self.import_paths = import_paths or []
        self.allow_current_dir = allow_current_dir
        self.module_output_mode = module_output_mode
        self.compiled_modules: dict[str, str] = {}
        self.module_py_files: dict[str, str] = {}
        self.repl_mode = repl_mode

        # Symbol table for compile-time identifier validation
        self.symbol_table = {
            'variables': set(),
            'functions': set(),
            'parameters': [],
            'imports': {'builtin'},
            'ml_builtins': self._discover_ml_builtins()
        }

    def _discover_ml_builtins(self) -> set[str]:
        """Discover all ML builtin functions by inspecting @ml_function decorators.

        Returns:
            Set of ML builtin function names
        """
        try:
            from mlpy.stdlib.builtin import builtin

            ml_builtins = set()
            for attr_name in dir(builtin):
                if attr_name.startswith('_'):
                    continue

                try:
                    attr = getattr(builtin, attr_name)
                    if callable(attr) and hasattr(attr, '_ml_function_metadata'):
                        ml_builtins.add(attr_name)
                except AttributeError:
                    continue

            return ml_builtins
        except ImportError:
            return set()

    @profile_parser
    def generate(self, ast: Program) -> tuple[str, dict[str, Any] | None]:
        """Generate Python code from ML AST.

        This is the main entry point that orchestrates the entire code generation process.

        Args:
            ast: Root Program AST node

        Returns:
            Tuple of (Python code string, source map data)
        """
        self.context = CodeGenerationContext()
        self.output_lines = []
        self.function_registry = AllowedFunctionsRegistry()

        # Initialize enhanced source map generator if enabled
        if self.generate_source_maps:
            self.context.enhanced_source_map_generator = EnhancedSourceMapGenerator(self.source_file)

        # Reset symbol table (preserve ml_builtins)
        ml_builtins = self.symbol_table['ml_builtins']
        self.symbol_table = {
            'variables': set(),
            'functions': set(),
            'parameters': [],
            'imports': {'builtin'},
            'ml_builtins': ml_builtins
        }

        # First pass: analyze AST to discover imports, variables, functions
        temp_context = self.context
        temp_registry = self.function_registry

        ast.accept(self)

        # Save state from first pass
        imports_from_first_pass = self.symbol_table['imports'].copy()
        variables_from_first_pass = self.symbol_table['variables'].copy()
        functions_from_first_pass = self.symbol_table['functions'].copy()

        # Reset for actual generation
        self.context = temp_context
        self.function_registry = temp_registry
        self.output_lines = []

        # Create fresh symbol table with first pass data
        ml_builtins = self.symbol_table['ml_builtins']
        self.symbol_table = {
            'variables': variables_from_first_pass,
            'functions': functions_from_first_pass,
            'parameters': [],
            'imports': imports_from_first_pass,
            'ml_builtins': ml_builtins
        }

        # Generate header
        self._emit_header()

        # Generate runtime imports
        self._generate_runtime_imports()

        # Auto-import builtin module if needed
        if self.context.builtin_functions_used:
            self._emit_line("from mlpy.stdlib.builtin import builtin")
            self._emit_line("")

        # Generate imports
        remaining_imports = self.context.imports_needed - {"contextlib"}
        if remaining_imports:
            for import_name in sorted(remaining_imports):
                if import_name.startswith("from ") or import_name.startswith("import "):
                    self._emit_line(import_name)
                elif import_name == "mlpy.stdlib.runtime_helpers":
                    self._emit_line(
                        "from mlpy.stdlib.runtime_helpers import safe_attr_access as _safe_attr_access, safe_method_call as _safe_method_call, get_safe_length"
                    )
                else:
                    self._emit_line(f"import {import_name}")
            self._emit_line("")

        # Add sys.path setup for user modules
        if self.module_output_mode == 'separate' and self.module_py_files:
            self._emit_line("import sys")
            self._emit_line("from pathlib import Path")
            self._emit_line("")
            self._emit_line("# ============================================================================")
            self._emit_line("# User Module Path Setup")
            self._emit_line("# ============================================================================")

            added_paths = set()
            for import_path in self.import_paths:
                if import_path not in added_paths:
                    self._emit_line(f"if str(Path({repr(import_path)}).resolve()) not in sys.path:")
                    self._indent()
                    self._emit_line(f"sys.path.insert(0, str(Path({repr(import_path)}).resolve()))")
                    self._dedent()
                    added_paths.add(import_path)

            if self.allow_current_dir and self.source_file and not self.repl_mode:
                self._emit_line("# Add source file directory to path")
                self._emit_line("_source_dir = Path(__file__).parent")
                self._emit_line("if str(_source_dir) not in sys.path:")
                self._indent()
                self._emit_line("sys.path.insert(0, str(_source_dir))")
                self._dedent()

            self._emit_line("")

        # Emit inline user modules
        if self.module_output_mode == 'inline' and self.compiled_modules:
            self._emit_line("# ============================================================================")
            self._emit_line("# User Module Definitions (Inline)")
            self._emit_line("# ============================================================================")
            self._emit_line("")
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

        # Generate source map
        source_map = self._generate_source_map() if self.generate_source_maps else None

        return python_code, source_map

    # ========================================================================
    # Code Emission Methods
    # ========================================================================

    def _emit_header(self):
        """Emit Python file header."""
        self._emit_line('"""Generated Python code from mlpy ML transpiler."""')
        self._emit_line("")
        self._emit_line("# This code was automatically generated from ML source")
        self._emit_line("# Modifications to this file may be lost on regeneration")
        self._emit_line("")

        if "contextlib" in self.context.imports_needed:
            self._emit_line("import contextlib")
            self._emit_line("")

    def _generate_runtime_imports(self):
        """Generate runtime validator import."""
        self._emit_line("# ============================================================================")
        self._emit_line("# Runtime Whitelist Enforcement")
        self._emit_line("# ============================================================================")
        self._emit_line("from mlpy.runtime.whitelist_validator import safe_call as _safe_call")
        self._emit_line("")

    def _emit_imports(self):
        """Emit necessary Python imports."""
        for import_name in sorted(self.context.imports_needed):
            if import_name.startswith("from ") or import_name.startswith("import "):
                self._emit_line(import_name)
            elif import_name == "mlpy.stdlib.runtime_helpers":
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

        # Track source mapping
        if self.generate_source_maps and original_node and self.context.enhanced_source_map_generator:
            generated_line = len(self.output_lines)
            generated_column = self.context.indentation_level * 4

            self.context.enhanced_source_map_generator.track_node(
                node=original_node,
                generated_line=generated_line,
                generated_column=generated_column,
                symbol_name=self._extract_symbol_name(original_node)
            )
        elif self.generate_source_maps and original_node:
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

    # ========================================================================
    # Indentation Management
    # ========================================================================

    def _get_indentation(self) -> str:
        """Get current indentation string."""
        return "    " * self.context.indentation_level

    def _indent(self):
        """Increase indentation level."""
        self.context.indentation_level += 1

    def _dedent(self):
        """Decrease indentation level."""
        self.context.indentation_level = max(0, self.context.indentation_level - 1)

    # ========================================================================
    # Helper Methods
    # ========================================================================

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
        if not isinstance(name, str):
            return f"ml_unknown_identifier_{id(name)}"

        if name == "null":
            return "None"

        python_keywords = {
            "and", "as", "assert", "break", "class", "continue", "def", "del",
            "elif", "else", "except", "finally", "for", "from", "global", "if",
            "import", "in", "is", "lambda", "not", "or", "pass", "raise",
            "return", "try", "while", "with", "yield", "True", "False", "None"
        }

        if name in python_keywords:
            return f"ml_{name}"

        return name

    def _generate_source_map(self) -> dict[str, Any]:
        """Generate source map data."""
        if self.context.enhanced_source_map_generator:
            enhanced_map = self.context.enhanced_source_map_generator.generate_enhanced_source_map()
            return {
                'version': 3,
                'file': self.source_file or 'generated.py',
                'sourceRoot': '',
                'sources': [self.source_file] if self.source_file else [],
                'names': enhanced_map.names,
                'mappings': self._encode_mappings(),
                'sourcesContent': [self._get_source_content()] if self.source_file else [],
                'enhanced': enhanced_map.to_dict()
            }

        return {
            'version': 3,
            'file': self.source_file or 'generated.py',
            'sourceRoot': '',
            'sources': [self.source_file] if self.source_file else [],
            'names': [],
            'mappings': self._encode_mappings(),
            'sourcesContent': [self._get_source_content()] if self.source_file else []
        }

    def _encode_mappings(self) -> str:
        """Encode source mappings in VLQ format."""
        # Simplified encoding - real implementation would use VLQ
        return ""

    def _get_source_content(self) -> str | None:
        """Get source file content."""
        if not self.source_file:
            return None
        try:
            return Path(self.source_file).read_text()
        except Exception:
            return None


__all__ = ['GeneratorBase']
