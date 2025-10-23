"""Source map generation and encoding helpers for code generation.

This module provides mixin functionality for generating source maps that link
generated Python code back to original ML source code. Source maps enable:

1. **Debugging Support** - Map runtime errors back to ML source lines
2. **IDE Integration** - Enable breakpoints and navigation in ML source
3. **Stack Trace Translation** - Convert Python stack traces to ML context
4. **Symbol Tracking** - Track variable and function name mappings

The source map format follows the Source Map v3 specification with
simplified VLQ encoding for efficient storage.
"""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mlpy.ml.grammar.ast_nodes import (
        ASTNode, FunctionDefinition, AssignmentStatement,
        Identifier, Parameter
    )


class SourceMapHelpersMixin:
    """Mixin providing source map generation and encoding functionality.

    This mixin handles all aspects of source map generation:
    - Extracting symbol names from AST nodes
    - Generating Source Map v3 compatible data structures
    - Encoding source mappings in simplified VLQ format
    - Loading original source content for debugging

    Source maps track the relationship between generated Python code and
    original ML source code, enabling proper debugging and error reporting.

    Thread Safety:
    - Source map generation operations are not thread-safe
    - Each code generator instance maintains its own source map state
    """

    def _extract_symbol_name(self, node: "ASTNode") -> str | None:
        """Extract symbol name from an AST node for source map tracking.

        Extracts meaningful symbol names from different AST node types to
        enable symbol-level source map tracking. This is used for:
        - Function definition names
        - Variable assignment targets
        - Identifier references
        - Function parameters

        Args:
            node: AST node to extract symbol name from

        Returns:
            Symbol name string if extractable, None otherwise

        Symbol Extraction Rules:
            - FunctionDefinition: Returns function name
            - AssignmentStatement: Returns assignment target name
            - Identifier: Returns identifier name
            - Parameter: Returns parameter name
            - Other nodes: Returns None

        Examples:
            >>> # For FunctionDefinition with name="calculate"
            >>> self._extract_symbol_name(func_def_node)
            'calculate'

            >>> # For AssignmentStatement with target="count"
            >>> self._extract_symbol_name(assignment_node)
            'count'

            >>> # For Identifier with name="x"
            >>> self._extract_symbol_name(identifier_node)
            'x'

        Note:
            Symbol names are used in source maps for enhanced debugging.
            IDEs can use these to provide better hover information and navigation.
        """
        # Import here to avoid circular dependency
        from mlpy.ml.grammar.ast_nodes import (
            FunctionDefinition, AssignmentStatement, Identifier, Parameter
        )

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

    def _generate_source_map(self) -> dict[str, Any]:
        """Generate source map data in Source Map v3 format.

        Creates a source map following the Source Map v3 specification:
        https://sourcemaps.info/spec.html

        The source map enables debuggers and IDEs to map generated Python code
        back to the original ML source code.

        Returns:
            Source map dict with keys:
            - version: Source map version (always 3)
            - file: Generated Python file name
            - sourceRoot: Root path for source files (empty string)
            - sources: List of source file paths
            - names: List of symbol names (currently empty)
            - mappings: Encoded source mappings (simplified VLQ format)
            - sourcesContent: Original ML source code (for inline debugging)

        Example Output:
            ```python
            {
                'version': 3,
                'file': 'program.py',
                'sourceRoot': '',
                'sources': ['program.ml'],
                'names': [],
                'mappings': '[{"generated": {"line": 10, "column": 4}, ...}]',
                'sourcesContent': ['let x = 42\nprint(x)']
            }
            ```

        Note:
            This uses a simplified mapping format instead of full VLQ encoding.
            For production use, consider implementing full VLQ base64 encoding.
        """
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
        """Encode source mappings to VLQ format (simplified).

        Converts source mapping data to a JSON string representation.
        In a full implementation, this would use VLQ base64 encoding as specified
        in the Source Map v3 specification.

        The simplified format stores each mapping as a JSON object with:
        - generated: Line and column in generated Python code
        - original: Line and column in original ML source
        - source: Source file path
        - name: Symbol name (if available)

        Returns:
            JSON string of mapping data

        Mapping Format:
            ```json
            [
                {
                    "generated": {"line": 15, "column": 4},
                    "original": {"line": 3, "column": 0},
                    "source": "program.ml",
                    "name": "calculate"
                },
                ...
            ]
            ```

        Performance Considerations:
            - Simplified format is larger than VLQ encoding (~3-5x size)
            - For production, implement full VLQ base64 encoding
            - Current format prioritizes readability and debugging

        Note:
            Only mappings with valid original line numbers are included.
            This filters out generated helper code and boilerplate.
        """
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
        """Get original source content for source map.

        Reads the original ML source file content to include in the source map.
        This enables "inline" debugging where the debugger can show the original
        source without needing access to the source file.

        Returns:
            ML source code as string, or None if unavailable

        Error Handling:
            Returns None on any file read error (missing file, encoding issues, etc.)

        Example:
            >>> self._get_source_content()
            'let x = 42\\nlet y = x * 2\\nprint(y)'

        Note:
            Including source content increases source map size but enables
            better debugging when original source files are not available.
        """
        if not self.source_file:
            return None

        try:
            return Path(self.source_file).read_text(encoding="utf-8")
        except Exception:
            return None
