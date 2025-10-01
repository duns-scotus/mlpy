"""
Unit tests for ML Language Server Protocol implementation.
Tests LSP server functionality, handlers, and capabilities.
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.mlpy.lsp.capabilities import MLServerCapabilities
from src.mlpy.lsp.handlers import MLRequestHandlers
from src.mlpy.lsp.server import DocumentInfo, MLLanguageServer

# Mock LSP dependencies if not available
LSP_AVAILABLE = True
try:
    from lsprotocol.types import (
        CompletionItem,
        CompletionList,
        Diagnostic,
        DiagnosticSeverity,
        Hover,
        MarkupContent,
        MarkupKind,
        Position,
        Range,
    )
except ImportError:
    LSP_AVAILABLE = False

    # Create mock classes
    class Position:
        def __init__(self, line=0, character=0):
            self.line = line
            self.character = character

    class Range:
        def __init__(self, start=None, end=None):
            self.start = start or Position()
            self.end = end or Position()

    class CompletionItem:
        def __init__(self, label="", **kwargs):
            self.label = label

    class CompletionList:
        def __init__(self, is_incomplete=False, items=None):
            self.is_incomplete = is_incomplete
            self.items = items or []

    class Hover:
        def __init__(self, contents=None):
            self.contents = contents

    class MarkupContent:
        def __init__(self, kind="", value=""):
            self.kind = kind
            self.value = value

    class Diagnostic:
        def __init__(self, range=None, message="", severity=None, **kwargs):
            self.range = range
            self.message = message
            self.severity = severity

    DiagnosticSeverity = Mock()
    MarkupKind = Mock()


class TestMLServerCapabilities:
    """Test ML server capabilities configuration."""

    def test_default_capabilities(self):
        """Test default capability settings."""
        caps = MLServerCapabilities()

        assert caps.completion_enabled is True
        assert caps.hover_enabled is True
        assert caps.diagnostic_provider is True
        assert caps.text_document_sync_full is True

    def test_capability_conversion_to_lsp(self):
        """Test conversion to LSP capabilities format."""
        caps = MLServerCapabilities()
        lsp_caps = caps.to_lsp_capabilities()

        assert "completionProvider" in lsp_caps
        assert "hoverProvider" in lsp_caps
        assert "diagnosticProvider" in lsp_caps
        assert lsp_caps["textDocumentSync"] == 1  # Full sync

    def test_custom_trigger_characters(self):
        """Test custom trigger characters configuration."""
        caps = MLServerCapabilities(completion_trigger_characters=[".", "::", "->"])

        lsp_caps = caps.to_lsp_capabilities()
        expected_chars = [".", "::", "->"]
        assert lsp_caps["completionProvider"]["triggerCharacters"] == expected_chars

    def test_disabled_features(self):
        """Test disabled feature configuration."""
        caps = MLServerCapabilities(
            completion_enabled=False, hover_enabled=False, diagnostic_provider=False
        )

        lsp_caps = caps.to_lsp_capabilities()
        assert "completionProvider" not in lsp_caps
        assert "hoverProvider" not in lsp_caps
        assert "diagnosticProvider" not in lsp_caps


class TestMLRequestHandlers:
    """Test ML LSP request handlers."""

    def setup_method(self):
        """Set up test fixtures."""
        self.handlers = MLRequestHandlers()

    def test_keyword_completions(self):
        """Test ML keyword completion generation."""
        items = self.handlers._get_keyword_completions()

        assert len(items) > 0

        # Check for specific keywords
        labels = [item.label for item in items]
        assert "function" in labels
        assert "if" in labels
        assert "match" in labels
        assert "capability" in labels

    def test_builtin_completions(self):
        """Test built-in function completions."""
        items = self.handlers._get_builtin_completions()

        assert len(items) > 0

        labels = [item.label for item in items]
        assert "print" in labels
        assert "console.log" in labels
        assert "typeof" in labels

    def test_type_completions(self):
        """Test type completion generation."""
        items = self.handlers._get_type_completions()

        assert len(items) > 0

        labels = [item.label for item in items]
        assert "number" in labels
        assert "string" in labels
        assert "Array<T>" in labels
        assert "Promise<T>" in labels

    def test_snippet_completions(self):
        """Test code snippet completions."""
        items = self.handlers._get_snippet_completions()

        assert len(items) > 0

        labels = [item.label for item in items]
        assert "if-else" in labels
        assert "function" in labels
        assert "match" in labels

    def test_completion_request(self):
        """Test completion request handling."""
        position = Position(line=5, character=10)

        result = self.handlers.handle_completion(document_uri="file:///test.ml", position=position)

        assert isinstance(result, CompletionList)
        assert len(result.items) > 0
        assert result.is_incomplete is False

    def test_hover_request_no_ast(self):
        """Test hover request without AST."""
        position = Position(line=2, character=5)

        result = self.handlers.handle_hover(
            document_uri="file:///test.ml", position=position, ast=None
        )

        # Should return None when no symbol found
        assert result is None

    def test_document_symbols_no_ast(self):
        """Test document symbols with no AST."""
        result = self.handlers.handle_document_symbols(document_uri="file:///test.ml", ast=None)

        assert result == []

    def test_code_actions_empty_context(self):
        """Test code actions with empty context."""
        mock_context = Mock()
        mock_context.diagnostics = []

        result = self.handlers.handle_code_actions(
            document_uri="file:///test.ml", range_param=Range(), context=mock_context
        )

        assert isinstance(result, list)
        # Should return empty list with no diagnostics
        assert len(result) == 0


class TestMLLanguageServer:
    """Test ML Language Server main class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.server = MLLanguageServer()

    def test_server_initialization(self):
        """Test language server initialization."""
        assert self.server.documents == {}
        assert self.server.parser is not None
        assert self.server.analyzer is not None

    def test_capabilities_generation(self):
        """Test server capabilities generation."""
        capabilities = self.server.get_server_capabilities()

        if LSP_AVAILABLE:
            assert capabilities is not None
        else:
            assert capabilities is None

    def test_severity_conversion(self):
        """Test security severity to LSP severity conversion."""
        if not LSP_AVAILABLE:
            pytest.skip("LSP not available")

        # Mock severity with name attribute
        mock_severity = Mock()
        mock_severity.name = "HIGH"

        lsp_severity = self.server._convert_severity(mock_severity)
        assert lsp_severity == DiagnosticSeverity.Error

        mock_severity.name = "MEDIUM"
        lsp_severity = self.server._convert_severity(mock_severity)
        assert lsp_severity == DiagnosticSeverity.Warning

    @pytest.mark.asyncio
    async def test_document_open(self):
        """Test document open handling."""
        if not self.server.server:
            pytest.skip("LSP server not available")

        # Mock parameters
        mock_params = Mock()
        mock_params.text_document.uri = "file:///test.ml"
        mock_params.text_document.text = "x = 42\nprint(x)"
        mock_params.text_document.version = 1

        # Mock server publish_diagnostics method
        self.server.server.publish_diagnostics = AsyncMock()

        await self.server._did_open(mock_params)

        # Check document was stored
        assert "file:///test.ml" in self.server.documents
        doc_info = self.server.documents["file:///test.ml"]
        assert doc_info.content == "x = 42\nprint(x)"
        assert doc_info.version == 1

    @pytest.mark.asyncio
    async def test_document_change(self):
        """Test document change handling."""
        if not self.server.server:
            pytest.skip("LSP server not available")

        # First open a document
        uri = "file:///test.ml"
        doc_info = DocumentInfo(uri=uri, content="x = 42", version=1)
        self.server.documents[uri] = doc_info

        # Mock change parameters
        mock_params = Mock()
        mock_params.text_document.uri = uri
        mock_params.text_document.version = 2
        mock_params.content_changes = [Mock()]
        mock_params.content_changes[0].text = "x = 100\nprint(x)"
        # Mock as full document change (no range)
        mock_params.content_changes[0].range = None

        # Mock server method
        self.server.server.publish_diagnostics = AsyncMock()

        await self.server._did_change(mock_params)

        # Check document was updated
        updated_doc = self.server.documents[uri]
        assert updated_doc.content == "x = 100\nprint(x)"
        assert updated_doc.version == 2

    @pytest.mark.asyncio
    async def test_document_analysis_error(self):
        """Test document analysis with parsing error."""
        if not self.server.server:
            pytest.skip("LSP server not available")

        # Create document with invalid syntax
        doc_info = DocumentInfo(uri="file:///test.ml", content="invalid syntax {{{", version=1)

        # Mock parser to raise exception
        with patch.object(self.server.parser, "parse_string", side_effect=Exception("Parse error")):
            self.server.server.publish_diagnostics = AsyncMock()

            await self.server._analyze_document(doc_info)

        # Should have called publish_diagnostics even with error
        self.server.server.publish_diagnostics.assert_called_once()

    def test_command_line_args_tcp(self):
        """Test TCP mode command line argument handling."""
        # This would normally test the main() function
        # For now, just test that the server can be configured for TCP
        assert hasattr(self.server, "start_server")

    def test_command_line_args_stdio(self):
        """Test stdio mode command line argument handling."""
        # Test that the server can be configured for stdio
        assert hasattr(self.server, "start_stdio_server")


class TestDocumentInfo:
    """Test DocumentInfo data class."""

    def test_document_info_creation(self):
        """Test DocumentInfo creation and attributes."""
        doc_info = DocumentInfo(uri="file:///test.ml", content="test content", version=1)

        assert doc_info.uri == "file:///test.ml"
        assert doc_info.content == "test content"
        assert doc_info.version == 1
        assert doc_info.ast is None
        assert doc_info.diagnostics is None

    def test_document_info_with_ast(self):
        """Test DocumentInfo with AST."""
        mock_ast = Mock()

        doc_info = DocumentInfo(
            uri="file:///test.ml", content="test content", version=1, ast=mock_ast
        )

        assert doc_info.ast is mock_ast


@pytest.mark.integration
class TestLSPIntegration:
    """Integration tests for LSP functionality."""

    def test_full_completion_workflow(self):
        """Test complete completion workflow."""
        server = MLLanguageServer()
        handlers = MLRequestHandlers()

        # Test completion request
        position = Position(line=0, character=5)
        result = handlers.handle_completion("file:///test.ml", position)

        assert isinstance(result, CompletionList)
        assert len(result.items) > 0

        # Verify we have different types of completions
        labels = [item.label for item in result.items]
        has_keywords = any(label in ["function", "if", "match"] for label in labels)
        has_builtins = any(label in ["print", "console.log"] for label in labels)
        has_types = any(label in ["number", "string"] for label in labels)

        assert has_keywords
        assert has_builtins
        assert has_types

    @pytest.mark.asyncio
    async def test_error_diagnostics_workflow(self):
        """Test error diagnostics workflow."""
        if not LSP_AVAILABLE:
            pytest.skip("LSP not available")

        server = MLLanguageServer()
        if not server.server:
            pytest.skip("LSP server not available")

        # Mock dangerous ML code
        dangerous_code = """
        // This should trigger security diagnostics
        eval("dangerous_code")
        exec("more_danger")
        """

        doc_info = DocumentInfo(uri="file:///dangerous.ml", content=dangerous_code, version=1)

        server.server.publish_diagnostics = AsyncMock()

        await server._analyze_document(doc_info)

        # Should have published diagnostics
        server.server.publish_diagnostics.assert_called_once()

    def test_capabilities_configuration(self):
        """Test capabilities can be configured correctly."""
        # Test minimal configuration
        caps = MLServerCapabilities(completion_enabled=False, hover_enabled=False)

        lsp_caps = caps.to_lsp_capabilities()
        assert "completionProvider" not in lsp_caps
        assert "hoverProvider" not in lsp_caps

        # Test full configuration
        caps = MLServerCapabilities(
            completion_enabled=True,
            hover_enabled=True,
            diagnostic_provider=True,
            code_action_enabled=True,
        )

        lsp_caps = caps.to_lsp_capabilities()
        assert "completionProvider" in lsp_caps
        assert "hoverProvider" in lsp_caps
        assert "diagnosticProvider" in lsp_caps
        assert "codeActionProvider" in lsp_caps


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
