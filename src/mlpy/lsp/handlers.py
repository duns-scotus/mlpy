"""
ML Language Server Request Handlers
Implements specific LSP request handlers for ML language features.
"""

import logging
from dataclasses import dataclass
from typing import Any

try:
    from lsprotocol.types import (
        CodeAction,
        CodeActionKind,
        CompletionItem,
        CompletionItemKind,
        CompletionList,
        Definition,
        Diagnostic,
        DiagnosticSeverity,
        DiagnosticTag,
        DocumentSymbol,
        Hover,
        Location,
        MarkupContent,
        MarkupKind,
        ParameterInformation,
        Position,
        Range,
        SignatureHelp,
        SignatureInformation,
        SymbolInformation,
        SymbolKind,
        TextEdit,
        WorkspaceEdit,
    )

    LSP_AVAILABLE = True
except ImportError:
    LSP_AVAILABLE = False

from ..ml.analysis.parallel_analyzer import ParallelSecurityAnalyzer
from ..ml.grammar.ast_nodes import ASTNode, FunctionDefinition

logger = logging.getLogger(__name__)


@dataclass
class Symbol:
    """Symbol information for ML code."""

    name: str
    kind: str
    location: tuple[int, int]  # (line, column)
    definition_range: tuple[int, int, int, int] | None = (
        None  # (start_line, start_col, end_line, end_col)
    )
    type_info: str | None = None
    documentation: str | None = None


class MLRequestHandlers:
    """Handles specific LSP requests for ML language features."""

    def __init__(self):
        self.analyzer = ParallelSecurityAnalyzer()
        self.symbols_cache: dict[str, list[Symbol]] = {}

    # Completion Handlers
    def handle_completion(
        self, document_uri: str, position: Any, context: Any | None = None
    ) -> Any:
        """Handle text completion request."""
        if not LSP_AVAILABLE:
            return None

        items = []

        # Get context-aware completions
        items.extend(self._get_keyword_completions())
        items.extend(self._get_builtin_completions())
        items.extend(self._get_type_completions())
        items.extend(self._get_snippet_completions())

        # Add contextual completions based on cursor position
        if context:
            items.extend(self._get_contextual_completions(document_uri, position, context))

        return CompletionList(is_incomplete=False, items=items)

    def _get_keyword_completions(self) -> list[Any]:
        """Get ML keyword completions."""
        if not LSP_AVAILABLE:
            return []

        keywords = [
            # Control flow
            ("if", "if (condition) { }", "Conditional statement"),
            ("else", "else { }", "Alternative branch"),
            ("while", "while (condition) { }", "While loop"),
            ("for", "for (init; condition; increment) { }", "For loop"),
            ("break", "break", "Break out of loop"),
            ("continue", "continue", "Continue to next iteration"),
            ("return", "return value", "Return from function"),
            # Functions
            ("function", "function name() { }", "Function definition"),
            ("async", "async function name() { }", "Async function"),
            ("await", "await expression", "Await async result"),
            # Pattern matching
            ("match", "match value { }", "Pattern matching"),
            ("when", "when condition", "Pattern guard"),
            # Types and interfaces
            ("type", "type Name = { }", "Type definition"),
            ("interface", "interface Name { }", "Interface definition"),
            # Module system
            ("import", 'import { } from "module"', "Import statement"),
            ("export", "export item", "Export statement"),
            # Security
            ("capability", "capability (cap1, cap2) function", "Capability requirement"),
            ("secure", "secure import", "Secure import"),
            ("sandbox", "sandbox { }", "Sandboxed execution"),
            # Literals
            ("true", "true", "Boolean true"),
            ("false", "false", "Boolean false"),
            ("null", "null", "Null value"),
        ]

        items = []
        for label, insert_text, detail in keywords:
            items.append(
                CompletionItem(
                    label=label,
                    kind=CompletionItemKind.Keyword,
                    detail=detail,
                    insert_text=insert_text,
                    documentation=MarkupContent(
                        kind=MarkupKind.Markdown, value=f"**{label}** - {detail}"
                    ),
                )
            )

        return items

    def _get_builtin_completions(self) -> list[Any]:
        """Get built-in function completions."""
        if not LSP_AVAILABLE:
            return []

        builtins = [
            # I/O functions
            ("print", "print(message)", "Print message to console"),
            ("console.log", "console.log(message)", "Log message to console"),
            ("console.error", "console.error(message)", "Log error to console"),
            ("console.warn", "console.warn(message)", "Log warning to console"),
            # Type checking
            ("typeof", "typeof(value)", "Get type of value"),
            ("instanceof", "value instanceof Type", "Check instance type"),
            # String functions
            ("parseInt", "parseInt(string)", "Parse integer from string"),
            ("parseFloat", "parseFloat(string)", "Parse float from string"),
            ("isNaN", "isNaN(value)", "Check if value is NaN"),
            ("isFinite", "isFinite(value)", "Check if value is finite"),
            # Array functions
            ("Array.from", "Array.from(arrayLike)", "Create array from array-like"),
            ("Array.isArray", "Array.isArray(value)", "Check if value is array"),
            # Object functions
            ("Object.keys", "Object.keys(object)", "Get object keys"),
            ("Object.values", "Object.values(object)", "Get object values"),
            ("Object.entries", "Object.entries(object)", "Get object entries"),
            # Math functions
            ("Math.abs", "Math.abs(number)", "Absolute value"),
            ("Math.max", "Math.max(...numbers)", "Maximum value"),
            ("Math.min", "Math.min(...numbers)", "Minimum value"),
            ("Math.random", "Math.random()", "Random number 0-1"),
            # JSON functions
            ("JSON.parse", "JSON.parse(string)", "Parse JSON string"),
            ("JSON.stringify", "JSON.stringify(value)", "Convert to JSON string"),
        ]

        items = []
        for label, insert_text, detail in builtins:
            items.append(
                CompletionItem(
                    label=label,
                    kind=CompletionItemKind.Function,
                    detail=detail,
                    insert_text=insert_text,
                    documentation=MarkupContent(
                        kind=MarkupKind.Markdown, value=f"**{label}** - {detail}"
                    ),
                )
            )

        return items

    def _get_type_completions(self) -> list[Any]:
        """Get type completions."""
        if not LSP_AVAILABLE:
            return []

        types = [
            # Primitive types
            ("number", "number", "Numeric type"),
            ("string", "string", "String type"),
            ("boolean", "boolean", "Boolean type"),
            ("void", "void", "Void type"),
            ("any", "any", "Any type"),
            # Collection types
            ("Array<T>", "Array<${1:T}>", "Array type"),
            ("Object", "Object", "Object type"),
            # Advanced types
            ("Promise<T>", "Promise<${1:T}>", "Promise type"),
            ("Result<T, E>", "Result<${1:T}, ${2:E}>", "Result type"),
            ("Option<T>", "Option<${1:T}>", "Option type"),
            # Function types
            ("() => T", "(${1:}) => ${2:T}", "Function type"),
        ]

        items = []
        for label, insert_text, detail in types:
            items.append(
                CompletionItem(
                    label=label,
                    kind=CompletionItemKind.TypeParameter,
                    detail=detail,
                    insert_text=insert_text,
                    insert_text_format=2,  # Snippet
                    documentation=MarkupContent(
                        kind=MarkupKind.Markdown, value=f"**{label}** - {detail}"
                    ),
                )
            )

        return items

    def _get_snippet_completions(self) -> list[Any]:
        """Get code snippet completions."""
        if not LSP_AVAILABLE:
            return []

        snippets = [
            (
                "if-else",
                "if (${1:condition}) {\n    ${2}\n} else {\n    ${3}\n}",
                "If-else statement",
            ),
            ("function", "function ${1:name}(${2:params}) {\n    ${3}\n}", "Function definition"),
            (
                "for-loop",
                "for (${1:i} = 0; ${1:i} < ${2:length}; ${1:i}++) {\n    ${3}\n}",
                "For loop",
            ),
            ("while-loop", "while (${1:condition}) {\n    ${2}\n}", "While loop"),
            (
                "try-catch",
                "try {\n    ${1}\n} catch (${2:error}) {\n    ${3}\n}",
                "Try-catch block",
            ),
            (
                "match",
                "match ${1:value} {\n    ${2:pattern} => ${3:result};\n    _ => ${4:default};\n}",
                "Match expression",
            ),
            (
                "capability-function",
                "capability (${1:caps}) function ${2:name}(${3:params}) {\n    ${4}\n}",
                "Capability function",
            ),
            (
                "type-definition",
                "type ${1:Name} = {\n    ${2:field}: ${3:type};\n}",
                "Type definition",
            ),
            (
                "interface",
                "interface ${1:Name} {\n    ${2:method}(): ${3:type};\n}",
                "Interface definition",
            ),
        ]

        items = []
        for label, insert_text, detail in snippets:
            items.append(
                CompletionItem(
                    label=label,
                    kind=CompletionItemKind.Snippet,
                    detail=detail,
                    insert_text=insert_text,
                    insert_text_format=2,  # Snippet
                    documentation=MarkupContent(
                        kind=MarkupKind.Markdown, value=f"```ml\n{insert_text}\n```\n\n{detail}"
                    ),
                )
            )

        return items

    def _get_contextual_completions(
        self, document_uri: str, position: Any, context: Any
    ) -> list[Any]:
        """Get contextual completions based on cursor position."""
        # This would analyze the AST to provide context-aware suggestions
        # For now, return empty list
        return []

    # Hover Handlers
    def handle_hover(
        self, document_uri: str, position: Any, ast: ASTNode | None = None
    ) -> Any | None:
        """Handle hover request."""
        if not LSP_AVAILABLE:
            return None

        # Find symbol at position
        symbol_info = self._find_symbol_at_position(document_uri, position, ast)

        if symbol_info:
            content = self._create_hover_content(symbol_info)
            return Hover(contents=content)

        return None

    def _find_symbol_at_position(
        self, document_uri: str, position: Any, ast: ASTNode | None
    ) -> dict[str, Any] | None:
        """Find symbol information at the given position."""
        # Return None if no AST is available
        if ast is None:
            return None

        # This would traverse the AST to find the symbol at the position
        # For now, return basic information
        return {
            "type": "unknown",
            "name": "symbol",
            "documentation": "Symbol information not available",
        }

    def _create_hover_content(self, symbol_info: dict[str, Any]) -> Any:
        """Create hover content for symbol information."""
        if not LSP_AVAILABLE:
            return None

        content_parts = []

        # Symbol signature
        if "signature" in symbol_info:
            content_parts.append(f"```ml\n{symbol_info['signature']}\n```")

        # Type information
        if "type" in symbol_info:
            content_parts.append(f"**Type:** `{symbol_info['type']}`")

        # Documentation
        if "documentation" in symbol_info:
            content_parts.append(symbol_info["documentation"])

        # Security information
        if "security_info" in symbol_info:
            content_parts.append(f"🔒 **Security:** {symbol_info['security_info']}")

        content = "\n\n".join(content_parts)

        return MarkupContent(kind=MarkupKind.Markdown, value=content)

    # Definition Handlers
    def handle_definition(
        self, document_uri: str, position: Any, ast: ASTNode | None = None
    ) -> Any | None:
        """Handle go-to-definition request."""
        if not LSP_AVAILABLE:
            return None

        # Find definition location
        definition_location = self._find_definition_location(document_uri, position, ast)

        if definition_location:
            return Location(
                uri=definition_location["uri"],
                range=Range(
                    start=Position(
                        line=definition_location["line"], character=definition_location["character"]
                    ),
                    end=Position(
                        line=definition_location["end_line"],
                        character=definition_location["end_character"],
                    ),
                ),
            )

        return None

    def _find_definition_location(
        self, document_uri: str, position: Any, ast: ASTNode | None
    ) -> dict[str, Any] | None:
        """Find the definition location for a symbol."""
        # This would analyze the AST to find symbol definitions
        # For now, return None
        return None

    # Document Symbol Handlers
    def handle_document_symbols(self, document_uri: str, ast: ASTNode | None = None) -> list[Any]:
        """Handle document symbols request."""
        if not LSP_AVAILABLE or not ast:
            return []

        symbols = []
        self._collect_symbols(ast, symbols)
        return symbols

    def _collect_symbols(self, node: ASTNode, symbols: list[Any]) -> None:
        """Collect symbols from AST node."""
        if not LSP_AVAILABLE:
            return

        # Function definitions
        if isinstance(node, FunctionDefinition):
            symbols.append(
                DocumentSymbol(
                    name=node.name,
                    kind=SymbolKind.Function,
                    range=self._node_to_range(node),
                    selection_range=self._node_to_range(node),
                    detail=f"function {node.name}",
                    children=[],
                )
            )

        # Recursively collect from children
        for child in node.get_children():
            self._collect_symbols(child, symbols)

    def _node_to_range(self, node: ASTNode) -> Any:
        """Convert AST node to LSP range."""
        if not LSP_AVAILABLE:
            return None

        return Range(
            start=Position(line=getattr(node, "line_number", 0) - 1, character=0),
            end=Position(line=getattr(node, "line_number", 0) - 1, character=100),
        )

    # Code Action Handlers
    def handle_code_actions(self, document_uri: str, range_param: Any, context: Any) -> list[Any]:
        """Handle code actions request."""
        if not LSP_AVAILABLE:
            return []

        actions = []

        # Security fix actions
        actions.extend(self._get_security_fix_actions(document_uri, range_param, context))

        # Refactoring actions
        actions.extend(self._get_refactoring_actions(document_uri, range_param, context))

        # Quick fix actions
        actions.extend(self._get_quick_fix_actions(document_uri, range_param, context))

        return actions

    def _get_security_fix_actions(
        self, document_uri: str, range_param: Any, context: Any
    ) -> list[Any]:
        """Get security-related code actions."""
        if not LSP_AVAILABLE:
            return []

        actions = []

        # Check for security diagnostics in the range
        for diagnostic in context.diagnostics:
            if "SECURITY" in diagnostic.code or "INJECTION" in diagnostic.code:
                action = CodeAction(
                    title="Apply security fix",
                    kind=CodeActionKind.QuickFix,
                    diagnostics=[diagnostic],
                    edit=self._create_security_fix_edit(document_uri, diagnostic),
                )
                actions.append(action)

        return actions

    def _create_security_fix_edit(self, document_uri: str, diagnostic: Any) -> Any:
        """Create edit for security fix."""
        if not LSP_AVAILABLE:
            return None

        # This would create specific edits based on the security issue
        return WorkspaceEdit(changes={})

    def _get_refactoring_actions(
        self, document_uri: str, range_param: Any, context: Any
    ) -> list[Any]:
        """Get refactoring actions."""
        # Implementation would provide refactoring suggestions
        return []

    def _get_quick_fix_actions(
        self, document_uri: str, range_param: Any, context: Any
    ) -> list[Any]:
        """Get quick fix actions."""
        # Implementation would provide quick fixes for common issues
        return []

    # Signature Help Handlers
    def handle_signature_help(self, document_uri: str, position: Any) -> Any | None:
        """Handle signature help request."""
        if not LSP_AVAILABLE:
            return None

        # Find function call at position
        function_info = self._find_function_call_at_position(document_uri, position)

        if function_info:
            signatures = []
            for signature_info in function_info["signatures"]:
                parameters = []
                for param in signature_info["parameters"]:
                    parameters.append(
                        ParameterInformation(
                            label=param["name"], documentation=param.get("documentation")
                        )
                    )

                signatures.append(
                    SignatureInformation(
                        label=signature_info["label"],
                        documentation=signature_info.get("documentation"),
                        parameters=parameters,
                    )
                )

            return SignatureHelp(
                signatures=signatures,
                active_signature=0,
                active_parameter=function_info.get("active_parameter", 0),
            )

        return None

    def _find_function_call_at_position(
        self, document_uri: str, position: Any
    ) -> dict[str, Any] | None:
        """Find function call information at position."""
        # This would analyze the code to find function calls and parameter positions
        return None


# Utility functions for LSP handlers
def get_default_ml_handlers() -> MLRequestHandlers:
    """Get default ML request handlers instance."""
    return MLRequestHandlers()


def create_diagnostic_from_security_issue(issue: Any) -> Any | None:
    """Create LSP diagnostic from security issue."""
    if not LSP_AVAILABLE:
        return None

    severity_map = {
        "CRITICAL": DiagnosticSeverity.Error,
        "HIGH": DiagnosticSeverity.Error,
        "MEDIUM": DiagnosticSeverity.Warning,
        "LOW": DiagnosticSeverity.Information,
    }

    return Diagnostic(
        range=Range(
            start=Position(line=max(0, issue.line_number - 1), character=issue.column or 0),
            end=Position(line=max(0, issue.line_number - 1), character=(issue.column or 0) + 10),
        ),
        message=issue.message,
        severity=severity_map.get(issue.severity.name, DiagnosticSeverity.Warning),
        code=issue.issue_type,
        source="mlpy-security",
        tags=[DiagnosticTag.Security] if hasattr(issue, "cwe_id") and issue.cwe_id else None,
    )
