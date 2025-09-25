"""
ML Language Server Protocol Server Implementation
Main LSP server class that handles client communication and coordination.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

try:
    from pygls.server import LanguageServer
    from pygls.workspace import Workspace
    from lsprotocol.types import (
        TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_CHANGE, TEXT_DOCUMENT_DID_SAVE,
        TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_HOVER, TEXT_DOCUMENT_DEFINITION,
        TEXT_DOCUMENT_DIAGNOSTIC, WORKSPACE_DID_CHANGE_CONFIGURATION,
        CompletionItem, CompletionList, CompletionParams,
        Diagnostic, DiagnosticSeverity, DiagnosticTag,
        DidOpenTextDocumentParams, DidChangeTextDocumentParams, DidSaveTextDocumentParams,
        HoverParams, Hover, MarkupContent, MarkupKind,
        DefinitionParams, Location, Position, Range,
        PublishDiagnosticsParams, ConfigurationParams,
        ServerCapabilities, TextDocumentSyncMode,
        CompletionOptions, HoverOptions, DefinitionOptions
    )
    LSP_AVAILABLE = True
except ImportError:
    # Create mock classes if LSP dependencies aren't available
    class LanguageServer:
        def __init__(self, *args, **kwargs): pass

    LSP_AVAILABLE = False

from ..ml.parser import MLParser
from ..ml.analysis.parallel_analyzer import ParallelSecurityAnalyzer
from ..ml.grammar.ast_nodes import ASTNode
from ..ml.errors import MLError

logger = logging.getLogger(__name__)


@dataclass
class DocumentInfo:
    """Information about an open document."""
    uri: str
    content: str
    version: int
    ast: Optional[ASTNode] = None
    diagnostics: List[Any] = None


class MLLanguageServer:
    """
    ML Language Server Protocol implementation.
    Provides IDE integration with syntax highlighting, diagnostics, and IntelliSense.
    """

    def __init__(self):
        if not LSP_AVAILABLE:
            logger.warning("LSP dependencies not available. Server will run in limited mode.")
            self.server = None
            return

        self.server = LanguageServer('mlpy-lsp', 'v2.0.0')
        self.documents: Dict[str, DocumentInfo] = {}
        self.parser = MLParser()
        self.analyzer = ParallelSecurityAnalyzer()

        # Register handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register LSP event handlers."""
        if not self.server:
            return

        # Document lifecycle
        self.server.feature(TEXT_DOCUMENT_DID_OPEN)(self._did_open)
        self.server.feature(TEXT_DOCUMENT_DID_CHANGE)(self._did_change)
        self.server.feature(TEXT_DOCUMENT_DID_SAVE)(self._did_save)

        # Language features
        self.server.feature(TEXT_DOCUMENT_COMPLETION)(self._completion)
        self.server.feature(TEXT_DOCUMENT_HOVER)(self._hover)
        self.server.feature(TEXT_DOCUMENT_DEFINITION)(self._definition)

        # Configuration
        self.server.feature(WORKSPACE_DID_CHANGE_CONFIGURATION)(self._configuration_changed)

    def get_server_capabilities(self) -> Optional[Any]:
        """Get server capabilities for initialization."""
        if not LSP_AVAILABLE:
            return None

        return ServerCapabilities(
            text_document_sync=TextDocumentSyncMode.Full,
            completion_provider=CompletionOptions(
                trigger_characters=['.', ':', '(', '[', '{'],
                resolve_provider=True
            ),
            hover_provider=HoverOptions(),
            definition_provider=DefinitionOptions(),
            diagnostic_provider=True
        )

    async def _did_open(self, params: Any) -> None:
        """Handle document open event."""
        if not LSP_AVAILABLE:
            return

        uri = params.text_document.uri
        content = params.text_document.text
        version = params.text_document.version

        doc_info = DocumentInfo(
            uri=uri,
            content=content,
            version=version
        )

        self.documents[uri] = doc_info
        await self._analyze_document(doc_info)

    async def _did_change(self, params: Any) -> None:
        """Handle document change event."""
        if not LSP_AVAILABLE:
            return

        uri = params.text_document.uri
        version = params.text_document.version

        if uri in self.documents:
            doc_info = self.documents[uri]

            # Apply changes
            for change in params.content_changes:
                if hasattr(change, 'range') and change.range:
                    # Incremental change (not implemented for simplicity)
                    doc_info.content = change.text
                else:
                    # Full document change
                    doc_info.content = change.text

            doc_info.version = version
            await self._analyze_document(doc_info)

    async def _did_save(self, params: Any) -> None:
        """Handle document save event."""
        if not LSP_AVAILABLE:
            return

        uri = params.text_document.uri

        if uri in self.documents:
            doc_info = self.documents[uri]
            await self._analyze_document(doc_info, force=True)

    async def _analyze_document(self, doc_info: DocumentInfo, force: bool = False) -> None:
        """Analyze document for diagnostics."""
        if not self.server:
            return

        try:
            # Parse ML code
            ast = self.parser.parse_string(doc_info.content)
            doc_info.ast = ast

            # Run security analysis
            issues = self.analyzer.analyze_ast(ast)

            # Convert to LSP diagnostics
            diagnostics = []
            for issue in issues:
                severity = self._convert_severity(issue.severity)

                diagnostic = Diagnostic(
                    range=Range(
                        start=Position(line=max(0, issue.line_number - 1), character=issue.column or 0),
                        end=Position(line=max(0, issue.line_number - 1), character=(issue.column or 0) + 10)
                    ),
                    message=issue.message,
                    severity=severity,
                    code=issue.issue_type,
                    source="mlpy",
                    tags=[DiagnosticTag.Security] if issue.cwe_id else None
                )
                diagnostics.append(diagnostic)

            doc_info.diagnostics = diagnostics

            # Publish diagnostics
            await self.server.publish_diagnostics(
                PublishDiagnosticsParams(
                    uri=doc_info.uri,
                    diagnostics=diagnostics
                )
            )

        except Exception as e:
            logger.error(f"Error analyzing document {doc_info.uri}: {e}")

            # Send parsing error as diagnostic
            error_diagnostic = Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=10)
                ),
                message=f"Parse error: {str(e)}",
                severity=DiagnosticSeverity.Error,
                source="mlpy"
            )

            await self.server.publish_diagnostics(
                PublishDiagnosticsParams(
                    uri=doc_info.uri,
                    diagnostics=[error_diagnostic]
                )
            )

    def _convert_severity(self, severity) -> Any:
        """Convert ML severity to LSP severity."""
        if not LSP_AVAILABLE:
            return None

        severity_map = {
            'CRITICAL': DiagnosticSeverity.Error,
            'HIGH': DiagnosticSeverity.Error,
            'MEDIUM': DiagnosticSeverity.Warning,
            'LOW': DiagnosticSeverity.Information,
        }

        return severity_map.get(severity.name, DiagnosticSeverity.Warning)

    async def _completion(self, params: Any) -> Optional[Any]:
        """Handle completion request."""
        if not LSP_AVAILABLE:
            return None

        uri = params.text_document.uri
        position = params.position

        if uri not in self.documents:
            return CompletionList(is_incomplete=False, items=[])

        doc_info = self.documents[uri]

        # Get completion items based on context
        items = self._get_completion_items(doc_info, position)

        return CompletionList(
            is_incomplete=False,
            items=items
        )

    def _get_completion_items(self, doc_info: DocumentInfo, position: Any) -> List[Any]:
        """Get completion items for the current position."""
        if not LSP_AVAILABLE:
            return []

        items = []

        # ML Keywords
        keywords = [
            'function', 'if', 'else', 'while', 'for', 'return', 'break', 'continue',
            'match', 'when', 'async', 'await', 'capability', 'type', 'interface',
            'import', 'export', 'from', 'as', 'true', 'false', 'null'
        ]

        for keyword in keywords:
            items.append(CompletionItem(
                label=keyword,
                kind=14,  # CompletionItemKind.Keyword
                detail="ML keyword",
                insert_text=keyword
            ))

        # Built-in functions
        builtins = [
            ('print', 'print(message)'),
            ('console.log', 'console.log(message)'),
            ('typeof', 'typeof(value)'),
            ('parseInt', 'parseInt(string)'),
            ('parseFloat', 'parseFloat(string)')
        ]

        for name, snippet in builtins:
            items.append(CompletionItem(
                label=name,
                kind=3,  # CompletionItemKind.Function
                detail="Built-in function",
                insert_text=snippet
            ))

        # Types
        types = ['number', 'string', 'boolean', 'void', 'any', 'Array', 'Object', 'Promise']

        for type_name in types:
            items.append(CompletionItem(
                label=type_name,
                kind=25,  # CompletionItemKind.TypeParameter
                detail="ML type",
                insert_text=type_name
            ))

        return items

    async def _hover(self, params: Any) -> Optional[Any]:
        """Handle hover request."""
        if not LSP_AVAILABLE:
            return None

        uri = params.text_document.uri
        position = params.position

        if uri not in self.documents:
            return None

        doc_info = self.documents[uri]

        # Get hover information
        hover_info = self._get_hover_info(doc_info, position)

        if hover_info:
            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=hover_info
                )
            )

        return None

    def _get_hover_info(self, doc_info: DocumentInfo, position: Any) -> Optional[str]:
        """Get hover information for the current position."""
        # Simple implementation - could be enhanced with AST analysis
        lines = doc_info.content.split('\n')

        if position.line < len(lines):
            line = lines[position.line]

            # Basic keyword documentation
            if 'function' in line:
                return "**function** - Defines a reusable block of code"
            elif 'capability' in line:
                return "**capability** - Defines security capabilities required by a function"
            elif 'match' in line:
                return "**match** - Pattern matching expression for control flow"

        return None

    async def _definition(self, params: Any) -> Optional[Any]:
        """Handle go-to-definition request."""
        if not LSP_AVAILABLE:
            return None

        # This would require symbol table analysis
        # For now, return None (not implemented)
        return None

    async def _configuration_changed(self, params: Any) -> None:
        """Handle configuration change event."""
        if not LSP_AVAILABLE:
            return

        # Handle configuration changes
        logger.info("Configuration changed")

    def start_server(self, host: str = "127.0.0.1", port: int = 2087) -> None:
        """Start the language server."""
        if not self.server:
            logger.error("LSP server not available. Install 'pygls' and 'lsprotocol' packages.")
            return

        logger.info(f"Starting ML Language Server on {host}:{port}")

        try:
            self.server.start_tcp(host, port)
        except Exception as e:
            logger.error(f"Failed to start server: {e}")

    def start_stdio_server(self) -> None:
        """Start the language server with stdio communication."""
        if not self.server:
            logger.error("LSP server not available. Install 'pygls' and 'lsprotocol' packages.")
            return

        logger.info("Starting ML Language Server with stdio")

        try:
            self.server.start_io()
        except Exception as e:
            logger.error(f"Failed to start stdio server: {e}")


def main():
    """Main entry point for the language server."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="ML Language Server")
    parser.add_argument("--tcp", action="store_true", help="Use TCP instead of stdio")
    parser.add_argument("--host", default="127.0.0.1", help="TCP host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=2087, help="TCP port (default: 2087)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Check LSP availability
    if not LSP_AVAILABLE:
        logger.error("LSP dependencies not available. Install with: pip install pygls lsprotocol")
        sys.exit(1)

    # Create and start server
    server = MLLanguageServer()

    if args.tcp:
        server.start_server(args.host, args.port)
    else:
        server.start_stdio_server()


if __name__ == "__main__":
    main()