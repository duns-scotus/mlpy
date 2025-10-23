"""Code generation context and source mapping classes.

This module contains dataclasses that track state during code generation.
"""

from dataclasses import dataclass, field


@dataclass
class SourceMapping:
    """Source map entry linking generated Python to original ML."""

    generated_line: int
    generated_column: int
    original_line: int | None = None
    original_column: int | None = None
    original_file: str | None = None
    name: str | None = None


@dataclass
class CodeGenerationContext:
    """Context for code generation with tracking."""

    indentation_level: int = 0
    current_line: int = 1
    current_column: int = 0
    source_mappings: list[SourceMapping] = field(default_factory=list)
    variable_mappings: dict[str, str] = field(default_factory=dict)
    function_mappings: dict[str, str] = field(default_factory=dict)
    imports_needed: set = field(default_factory=set)
    imported_modules: set[str] = field(default_factory=set)
    runtime_helpers_imported: bool = False
    builtin_functions_used: set[str] = field(default_factory=set)  # Track which builtins are called
    enhanced_source_map_generator: 'EnhancedSourceMapGenerator | None' = None  # Enhanced source map tracking


__all__ = ['SourceMapping', 'CodeGenerationContext']
