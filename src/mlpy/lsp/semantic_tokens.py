"""
ML Language Server Semantic Tokens Implementation
Provides semantic highlighting support for ML language through LSP.
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional, Tuple, Dict, Any
from ..ml.grammar.ast_nodes import *


class SemanticTokenType(IntEnum):
    """Semantic token types for ML language (indices into token types array)."""
    NAMESPACE = 0
    TYPE = 1
    CLASS = 2
    ENUM = 3
    INTERFACE = 4
    STRUCT = 5
    TYPE_PARAMETER = 6
    PARAMETER = 7
    VARIABLE = 8
    PROPERTY = 9
    ENUM_MEMBER = 10
    EVENT = 11
    FUNCTION = 12
    METHOD = 13
    MACRO = 14
    KEYWORD = 15
    MODIFIER = 16
    COMMENT = 17
    STRING = 18
    NUMBER = 19
    REGEXP = 20
    OPERATOR = 21
    DECORATOR = 22


class SemanticTokenModifier(IntEnum):
    """Semantic token modifiers for ML language (bit flags)."""
    DECLARATION = 1 << 0
    DEFINITION = 1 << 1
    READONLY = 1 << 2
    STATIC = 1 << 3
    DEPRECATED = 1 << 4
    ABSTRACT = 1 << 5
    ASYNC = 1 << 6
    MODIFICATION = 1 << 7
    DOCUMENTATION = 1 << 8
    DEFAULT_LIBRARY = 1 << 9


@dataclass
class SemanticToken:
    """Represents a single semantic token with position and type information."""
    line: int
    column: int
    length: int
    token_type: SemanticTokenType
    token_modifiers: int = 0


class MLSemanticTokenMapper:
    """Maps ML AST nodes to semantic tokens."""

    def __init__(self):
        """Initialize the token mapper."""
        self.tokens: List[SemanticToken] = []
        self.ml_keywords = {
            # Control flow
            'if', 'else', 'elif', 'while', 'for', 'break', 'continue', 'return',
            # Functions
            'function', 'async', 'await', 'curry',
            # Variables
            'let', 'const', 'var',
            # Types and interfaces
            'type', 'interface', 'extends', 'implements',
            # Pattern matching
            'match', 'when',
            # Module system
            'import', 'export', 'from', 'as',
            # Capability system
            'capability', 'secure', 'sandbox',
            # Memory annotations
            'borrow', 'mut',
            # Error handling
            'try', 'catch', 'except', 'throw', 'finally'
        }

        self.ml_operators = {
            '+', '-', '*', '/', '%', '**',
            '=', '+=', '-=', '*=', '/=', '%=',
            '==', '!=', '<', '>', '<=', '>=', '===', '!==',
            '&&', '||', '!',
            '&', '|', '^', '~', '<<', '>>',
            '|>', '?', '..', '=>', '?.', '??'
        }

    def map_ast_to_tokens(self, ast: ASTNode, source_text: str) -> List[SemanticToken]:
        """Convert an ML AST to semantic tokens."""
        self.tokens = []
        self.source_lines = source_text.split('\n')
        self.source_text = source_text

        # First pass: keyword and literal detection from source text
        self._extract_keywords_and_literals()

        # Second pass: AST-based semantic analysis
        self._visit_node(ast)

        return sorted(self.tokens, key=lambda t: (t.line, t.column))

    def _extract_keywords_and_literals(self) -> None:
        """Extract keywords, strings, and numbers from source text."""
        import re

        for line_idx, line in enumerate(self.source_lines):
            # Find keywords
            for keyword in self.ml_keywords:
                # Use word boundaries to match whole words only
                pattern = r'\b' + re.escape(keyword) + r'\b'
                for match in re.finditer(pattern, line):
                    self._add_token_at_position(
                        line_idx, match.start(),
                        len(keyword),
                        SemanticTokenType.KEYWORD
                    )

            # Find string literals
            string_pattern = r'"([^"\\]|\\.)*"'
            for match in re.finditer(string_pattern, line):
                self._add_token_at_position(
                    line_idx, match.start(),
                    len(match.group()),
                    SemanticTokenType.STRING
                )

            # Find number literals
            number_pattern = r'\b\d+(\.\d+)?\b'
            for match in re.finditer(number_pattern, line):
                self._add_token_at_position(
                    line_idx, match.start(),
                    len(match.group()),
                    SemanticTokenType.NUMBER
                )

    def _visit_node(self, node: ASTNode) -> None:
        """Visit an AST node and extract semantic tokens."""
        if node is None:
            return

        # Map specific node types to semantic tokens
        if isinstance(node, FunctionDefinition):
            self._visit_function_definition(node)
        elif isinstance(node, ImportStatement):
            self._visit_import_statement(node)
        elif isinstance(node, CapabilityDeclaration):
            self._visit_capability_declaration(node)
        elif isinstance(node, Identifier):
            self._visit_identifier(node)
        elif isinstance(node, FunctionCall):
            self._visit_function_call(node)
        elif isinstance(node, NumberLiteral):
            self._visit_number_literal(node)
        elif isinstance(node, StringLiteral):
            self._visit_string_literal(node)
        elif isinstance(node, BooleanLiteral):
            self._visit_boolean_literal(node)
        elif isinstance(node, BinaryExpression):
            self._visit_binary_expression(node)
        elif isinstance(node, UnaryExpression):
            self._visit_unary_expression(node)
        elif isinstance(node, IfStatement):
            self._visit_if_statement(node)
        elif isinstance(node, WhileStatement):
            self._visit_while_statement(node)
        elif isinstance(node, ForStatement):
            self._visit_for_statement(node)
        elif isinstance(node, TryStatement):
            self._visit_try_statement(node)
        elif isinstance(node, AssignmentStatement):
            self._visit_assignment_statement(node)
        elif isinstance(node, ReturnStatement):
            self._visit_return_statement(node)
        elif isinstance(node, MemberAccess):
            self._visit_member_access(node)
        elif isinstance(node, ArrayAccess):
            self._visit_array_access(node)
        elif isinstance(node, Parameter):
            self._visit_parameter(node)

        # Recursively visit child nodes
        self._visit_children(node)

    def _visit_children(self, node: ASTNode) -> None:
        """Visit all child nodes of an AST node."""
        if hasattr(node, 'items') and isinstance(node.items, list):
            for item in node.items:
                self._visit_node(item)

        if hasattr(node, 'body') and isinstance(node.body, list):
            for stmt in node.body:
                self._visit_node(stmt)
        elif hasattr(node, 'body'):
            self._visit_node(node.body)

        if hasattr(node, 'condition'):
            self._visit_node(node.condition)

        if hasattr(node, 'left'):
            self._visit_node(node.left)
        if hasattr(node, 'right'):
            self._visit_node(node.right)

        if hasattr(node, 'expression'):
            self._visit_node(node.expression)

        if hasattr(node, 'arguments') and isinstance(node.arguments, list):
            for arg in node.arguments:
                self._visit_node(arg)

        if hasattr(node, 'parameters') and isinstance(node.parameters, list):
            for param in node.parameters:
                self._visit_node(param)

    def _visit_function_definition(self, node: FunctionDefinition) -> None:
        """Visit a function definition and create semantic tokens."""
        if node.name and hasattr(node.name, 'name'):
            # node.name is an Identifier object, we need node.name.name for the string
            self._add_token_at_position(
                node.name.line, node.name.column,
                len(node.name.name),
                SemanticTokenType.FUNCTION,
                SemanticTokenModifier.DEFINITION
            )

    def _visit_import_statement(self, node: ImportStatement) -> None:
        """Visit an import statement."""
        # Import keywords are handled by keyword detection
        # Module name will be handled by identifier visitor
        pass

    def _visit_capability_declaration(self, node: CapabilityDeclaration) -> None:
        """Visit a capability declaration."""
        if node.name:
            self._add_token_at_position(
                node.line, node.column,
                len(node.name),
                SemanticTokenType.DECORATOR,
                SemanticTokenModifier.DEFINITION
            )

    def _visit_identifier(self, node: Identifier) -> None:
        """Visit an identifier and determine its semantic type."""
        if not node.name:
            return

        # Check if it's a keyword first
        if node.name in self.ml_keywords:
            self._add_token_at_position(
                node.line, node.column,
                len(node.name),
                SemanticTokenType.KEYWORD
            )
        else:
            # Default to variable for now - context analysis could improve this
            self._add_token_at_position(
                node.line, node.column,
                len(node.name),
                SemanticTokenType.VARIABLE
            )

    def _visit_function_call(self, node: FunctionCall) -> None:
        """Visit a function call."""
        if isinstance(node.function, Identifier):
            self._add_token_at_position(
                node.function.line, node.function.column,
                len(node.function.name),
                SemanticTokenType.FUNCTION
            )

    def _visit_number_literal(self, node: NumberLiteral) -> None:
        """Visit a number literal."""
        if node.line is not None and node.column is not None:
            value_str = str(node.value)
            self._add_token_at_position(
                node.line, node.column,
                len(value_str),
                SemanticTokenType.NUMBER
            )

    def _visit_string_literal(self, node: StringLiteral) -> None:
        """Visit a string literal."""
        if node.line is not None and node.column is not None:
            # Include quotes in length
            value_str = f'"{node.value}"'
            self._add_token_at_position(
                node.line, node.column,
                len(value_str),
                SemanticTokenType.STRING
            )

    def _visit_boolean_literal(self, node: BooleanLiteral) -> None:
        """Visit a boolean literal."""
        if node.line is not None and node.column is not None:
            value_str = 'true' if node.value else 'false'
            self._add_token_at_position(
                node.line, node.column,
                len(value_str),
                SemanticTokenType.KEYWORD
            )

    def _visit_binary_expression(self, node: BinaryExpression) -> None:
        """Visit a binary expression and highlight operator."""
        if hasattr(node, 'operator') and node.operator in self.ml_operators:
            # We'd need operator position from the parser - for now skip
            pass

    def _visit_unary_expression(self, node: UnaryExpression) -> None:
        """Visit a unary expression and highlight operator."""
        if hasattr(node, 'operator') and node.operator in self.ml_operators:
            # We'd need operator position from the parser - for now skip
            pass

    def _visit_if_statement(self, node: IfStatement) -> None:
        """Visit an if statement."""
        # Keywords are handled by keyword detection in source text
        pass

    def _visit_while_statement(self, node: WhileStatement) -> None:
        """Visit a while statement."""
        # Keywords are handled by keyword detection in source text
        pass

    def _visit_for_statement(self, node: ForStatement) -> None:
        """Visit a for statement."""
        # Keywords are handled by keyword detection in source text
        pass

    def _visit_try_statement(self, node: TryStatement) -> None:
        """Visit a try statement."""
        # Keywords are handled by keyword detection in source text
        pass

    def _visit_assignment_statement(self, node: AssignmentStatement) -> None:
        """Visit an assignment statement."""
        if hasattr(node, 'target') and isinstance(node.target, Identifier):
            self._add_token_at_position(
                node.target.line, node.target.column,
                len(node.target.name),
                SemanticTokenType.VARIABLE,
                SemanticTokenModifier.DEFINITION
            )

    def _visit_return_statement(self, node: ReturnStatement) -> None:
        """Visit a return statement."""
        # Return keyword is handled by keyword detection
        pass

    def _visit_member_access(self, node: MemberAccess) -> None:
        """Visit a member access expression."""
        if hasattr(node, 'property') and isinstance(node.property, str):
            # Property access - we'd need position info for the property
            pass

    def _visit_array_access(self, node: ArrayAccess) -> None:
        """Visit an array access expression."""
        # The array and index expressions are handled recursively
        pass

    def _visit_parameter(self, node: Parameter) -> None:
        """Visit a function parameter."""
        if node.name:
            self._add_token_at_position(
                node.line, node.column,
                len(node.name),
                SemanticTokenType.PARAMETER,
                SemanticTokenModifier.DEFINITION
            )

    def _add_token_at_position(self, line: int, column: int, length: int,
                             token_type: SemanticTokenType,
                             modifiers: int = 0) -> None:
        """Add a semantic token at the specified position."""
        if line is not None and column is not None:
            token = SemanticToken(
                line=line,
                column=column,
                length=length,
                token_type=token_type,
                token_modifiers=modifiers
            )
            self.tokens.append(token)

    def _add_token_if_position_available(self, text: str, token_type: SemanticTokenType) -> None:
        """Add a token if we can determine its position from context."""
        # This is a fallback for when we don't have explicit position info
        # For now, we'll skip these tokens
        pass


class SemanticTokensEncoder:
    """Encodes semantic tokens in LSP format."""

    @staticmethod
    def encode_tokens(tokens: List[SemanticToken]) -> List[int]:
        """Encode semantic tokens in LSP delta format."""
        if not tokens:
            return []

        encoded = []
        prev_line = 0
        prev_column = 0

        for token in tokens:
            # Calculate deltas
            delta_line = token.line - prev_line
            delta_column = token.column - prev_column if delta_line == 0 else token.column

            # Add token data: [deltaLine, deltaColumn, length, tokenType, tokenModifiers]
            encoded.extend([
                delta_line,
                delta_column,
                token.length,
                int(token.token_type),
                token.token_modifiers
            ])

            # Update previous position
            prev_line = token.line
            prev_column = token.column

        return encoded

    @staticmethod
    def get_token_types() -> List[str]:
        """Get the list of token type names for LSP."""
        return [
            "namespace", "type", "class", "enum", "interface", "struct",
            "typeParameter", "parameter", "variable", "property", "enumMember",
            "event", "function", "method", "macro", "keyword", "modifier",
            "comment", "string", "number", "regexp", "operator", "decorator"
        ]

    @staticmethod
    def get_token_modifiers() -> List[str]:
        """Get the list of token modifier names for LSP."""
        return [
            "declaration", "definition", "readonly", "static", "deprecated",
            "abstract", "async", "modification", "documentation", "defaultLibrary"
        ]