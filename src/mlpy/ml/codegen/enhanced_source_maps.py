"""
Enhanced source map generation for Sprint 7.
Provides detailed debugging information and IDE integration support.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mlpy.ml.grammar.ast_nodes import ASTNode


@dataclass
class SourceLocation:
    """Enhanced source location with full position information."""

    line: int
    column: int
    offset: int = 0
    length: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "line": self.line,
            "column": self.column,
            "offset": self.offset,
            "length": self.length,
        }


@dataclass
class SourceMapping:
    """Enhanced source mapping with detailed debugging info."""

    # Generated Python code location
    generated: SourceLocation

    # Original ML code location
    original: SourceLocation | None = None

    # Source file information
    source_file: str | None = None

    # Symbol name (variable, function, etc.)
    name: str | None = None

    # AST node type
    node_type: str | None = None

    # Additional metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {"generated": self.generated.to_dict()}

        if self.original:
            result["original"] = self.original.to_dict()

        if self.source_file:
            result["source_file"] = self.source_file

        if self.name:
            result["name"] = self.name

        if self.node_type:
            result["node_type"] = self.node_type

        if self.metadata:
            result["metadata"] = self.metadata

        return result


@dataclass
class EnhancedSourceMap:
    """Enhanced source map with full debugging capabilities."""

    version: int = 3
    sources: list[str] = field(default_factory=list)
    names: list[str] = field(default_factory=list)
    mappings: list[SourceMapping] = field(default_factory=list)
    source_content: dict[str, str] = field(default_factory=dict)

    # Enhanced debugging information
    symbol_table: dict[str, Any] = field(default_factory=dict)
    type_information: dict[str, str] = field(default_factory=dict)
    scope_information: list[dict[str, Any]] = field(default_factory=list)

    def add_source(self, file_path: str, content: str | None = None) -> int:
        """Add source file to the map."""
        if file_path not in self.sources:
            self.sources.append(file_path)

            if content:
                self.source_content[file_path] = content
            elif Path(file_path).exists():
                self.source_content[file_path] = Path(file_path).read_text(encoding="utf-8")

        return self.sources.index(file_path)

    def add_name(self, name: str) -> int:
        """Add symbol name to the map."""
        if name not in self.names:
            self.names.append(name)
        return self.names.index(name)

    def add_mapping(
        self,
        generated_line: int,
        generated_column: int,
        original_line: int | None = None,
        original_column: int | None = None,
        source_file: str | None = None,
        name: str | None = None,
        node_type: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        """Add a source mapping entry."""
        generated = SourceLocation(generated_line, generated_column)
        original = None

        if original_line is not None and original_column is not None:
            original = SourceLocation(original_line, original_column)

        mapping = SourceMapping(
            generated=generated,
            original=original,
            source_file=source_file,
            name=name,
            node_type=node_type,
            metadata=metadata or {},
        )

        self.mappings.append(mapping)

    def add_symbol(self, name: str, symbol_info: dict[str, Any]):
        """Add symbol information for debugging."""
        self.symbol_table[name] = symbol_info

    def add_type_info(self, expression: str, type_name: str):
        """Add type information for expressions."""
        self.type_information[expression] = type_name

    def add_scope(self, scope_info: dict[str, Any]):
        """Add scope information."""
        self.scope_information.append(scope_info)

    def to_json(self, indent: int | None = 2) -> str:
        """Convert to JSON source map format."""
        # Standard source map format
        standard_map = {
            "version": self.version,
            "sources": self.sources,
            "names": self.names,
            "sourcesContent": [self.source_content.get(src, "") for src in self.sources],
            "mappings": self._encode_mappings(),
        }

        # Enhanced debugging information
        enhanced_info = {
            "symbolTable": self.symbol_table,
            "typeInformation": self.type_information,
            "scopeInformation": self.scope_information,
            "detailedMappings": [mapping.to_dict() for mapping in self.mappings],
        }

        result = {"sourceMap": standard_map, "debugInfo": enhanced_info}

        return json.dumps(result, indent=indent)

    def _encode_mappings(self) -> str:
        """Encode mappings in VLQ format (simplified version)."""
        # For now, return a simple representation
        # In a full implementation, this would use Variable Length Quantity encoding
        encoded_segments = []

        for mapping in self.mappings:
            segment = f"{mapping.generated.column}"

            if mapping.original and mapping.source_file:
                source_idx = self.sources.index(mapping.source_file)
                segment += f",{source_idx},{mapping.original.line},{mapping.original.column}"

                if mapping.name and mapping.name in self.names:
                    name_idx = self.names.index(mapping.name)
                    segment += f",{name_idx}"

            encoded_segments.append(segment)

        return ";".join(encoded_segments)

    def save(self, output_path: str):
        """Save source map to file."""
        Path(output_path).write_text(self.to_json(), encoding="utf-8")


class EnhancedSourceMapGenerator:
    """Generator for enhanced source maps with debugging support."""

    def __init__(self, source_file: str | None = None):
        self.source_file = source_file
        self.source_map = EnhancedSourceMap()
        self.current_line = 1
        self.current_column = 0

        if source_file:
            self.source_map.add_source(source_file)

    def track_node(
        self,
        node: ASTNode,
        generated_line: int,
        generated_column: int,
        symbol_name: str | None = None,
    ):
        """Track an AST node in the source map."""
        if hasattr(node, "line") and hasattr(node, "column"):
            self.source_map.add_mapping(
                generated_line=generated_line,
                generated_column=generated_column,
                original_line=node.line,
                original_column=node.column,
                source_file=self.source_file,
                name=symbol_name,
                node_type=type(node).__name__,
                metadata={"ast_id": id(node), "source_span": getattr(node, "source_span", None)},
            )

    def track_symbol(self, name: str, node: ASTNode, symbol_type: str):
        """Track symbol definition or usage."""
        symbol_info = {
            "type": symbol_type,
            "defined_at": {
                "line": getattr(node, "line", None),
                "column": getattr(node, "column", None),
                "file": self.source_file,
            },
            "node_type": type(node).__name__,
            "scope_level": getattr(node, "scope_level", 0),
        }

        self.source_map.add_symbol(name, symbol_info)

    def track_scope(self, scope_type: str, start_node: ASTNode, end_node: ASTNode | None = None):
        """Track scope boundaries."""
        scope_info = {
            "type": scope_type,
            "start": {
                "line": getattr(start_node, "line", None),
                "column": getattr(start_node, "column", None),
            },
        }

        if end_node:
            scope_info["end"] = {
                "line": getattr(end_node, "line", None),
                "column": getattr(end_node, "column", None),
            }

        self.source_map.add_scope(scope_info)

    def finalize(self) -> EnhancedSourceMap:
        """Finalize and return the source map."""
        return self.source_map


def create_debug_source_map(
    ml_source: str, python_code: str, source_file: str | None = None
) -> EnhancedSourceMap:
    """Create a comprehensive debug source map."""
    generator = EnhancedSourceMapGenerator(source_file)

    # Add the source content
    if source_file:
        generator.source_map.source_content[source_file] = ml_source

    # For now, create a basic mapping
    # In a full implementation, this would be integrated with the AST visitor
    lines = python_code.split("\n")
    for i, line in enumerate(lines, 1):
        if line.strip() and not line.strip().startswith("#"):
            generator.source_map.add_mapping(
                generated_line=i,
                generated_column=0,
                original_line=1,  # Would be mapped from actual AST
                original_column=0,
                source_file=source_file,
            )

    return generator.finalize()


# Integration function for the existing transpiler
def generate_enhanced_source_map(
    ast: ASTNode, python_code: str, source_file: str | None = None, ml_source: str | None = None
) -> dict[str, Any]:
    """Generate enhanced source map for transpilation."""
    source_map = create_debug_source_map(ml_source or "", python_code, source_file)

    return json.loads(source_map.to_json())
