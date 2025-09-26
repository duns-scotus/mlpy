"""
ML Language Server Capabilities
Defines the capabilities and features supported by the ML LSP server.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class MLServerCapabilities:
    """ML Language Server capabilities configuration."""

    # Text Document Sync
    text_document_sync_full: bool = True
    text_document_sync_incremental: bool = False

    # Completion Support
    completion_enabled: bool = True
    completion_trigger_characters: list[str] = None
    completion_resolve_provider: bool = True

    # Hover Support
    hover_enabled: bool = True

    # Signature Help
    signature_help_enabled: bool = True
    signature_help_trigger_characters: list[str] = None

    # Definition Support
    definition_enabled: bool = True
    type_definition_enabled: bool = True
    implementation_enabled: bool = False

    # References
    references_enabled: bool = True

    # Document Highlights
    document_highlight_enabled: bool = True

    # Document Symbols
    document_symbol_enabled: bool = True
    workspace_symbol_enabled: bool = True

    # Code Actions
    code_action_enabled: bool = True
    code_action_kinds: list[str] = None

    # Code Lens
    code_lens_enabled: bool = True
    code_lens_resolve_provider: bool = True

    # Document Formatting
    document_formatting_enabled: bool = True
    document_range_formatting_enabled: bool = True
    document_on_type_formatting_enabled: bool = False

    # Rename
    rename_enabled: bool = True
    rename_prepare_provider: bool = True

    # Folding Range
    folding_range_enabled: bool = True

    # Selection Range
    selection_range_enabled: bool = True

    # Semantic Tokens
    semantic_tokens_enabled: bool = True

    # Diagnostics
    diagnostic_provider: bool = True
    diagnostic_inter_file_dependencies: bool = True
    diagnostic_workspace_diagnostics: bool = True

    def __post_init__(self):
        """Initialize default values."""
        if self.completion_trigger_characters is None:
            self.completion_trigger_characters = [".", ":", "(", "[", "{", " "]

        if self.signature_help_trigger_characters is None:
            self.signature_help_trigger_characters = ["(", ","]

        if self.code_action_kinds is None:
            self.code_action_kinds = [
                "quickfix",
                "refactor",
                "refactor.extract",
                "refactor.inline",
                "refactor.rewrite",
                "source",
                "source.organizeImports",
                "source.fixAll",
            ]

    def to_lsp_capabilities(self) -> dict[str, Any]:
        """Convert to LSP server capabilities format."""
        capabilities = {}

        # Text Document Sync
        if self.text_document_sync_full:
            capabilities["textDocumentSync"] = 1  # Full
        elif self.text_document_sync_incremental:
            capabilities["textDocumentSync"] = 2  # Incremental

        # Completion
        if self.completion_enabled:
            capabilities["completionProvider"] = {
                "triggerCharacters": self.completion_trigger_characters,
                "resolveProvider": self.completion_resolve_provider,
            }

        # Hover
        if self.hover_enabled:
            capabilities["hoverProvider"] = True

        # Signature Help
        if self.signature_help_enabled:
            capabilities["signatureHelpProvider"] = {
                "triggerCharacters": self.signature_help_trigger_characters
            }

        # Definition
        if self.definition_enabled:
            capabilities["definitionProvider"] = True

        if self.type_definition_enabled:
            capabilities["typeDefinitionProvider"] = True

        if self.implementation_enabled:
            capabilities["implementationProvider"] = True

        # References
        if self.references_enabled:
            capabilities["referencesProvider"] = True

        # Document Highlights
        if self.document_highlight_enabled:
            capabilities["documentHighlightProvider"] = True

        # Document Symbols
        if self.document_symbol_enabled:
            capabilities["documentSymbolProvider"] = True

        if self.workspace_symbol_enabled:
            capabilities["workspaceSymbolProvider"] = True

        # Code Actions
        if self.code_action_enabled:
            capabilities["codeActionProvider"] = {"codeActionKinds": self.code_action_kinds}

        # Code Lens
        if self.code_lens_enabled:
            capabilities["codeLensProvider"] = {"resolveProvider": self.code_lens_resolve_provider}

        # Document Formatting
        if self.document_formatting_enabled:
            capabilities["documentFormattingProvider"] = True

        if self.document_range_formatting_enabled:
            capabilities["documentRangeFormattingProvider"] = True

        if self.document_on_type_formatting_enabled:
            capabilities["documentOnTypeFormattingProvider"] = {
                "firstTriggerCharacter": ";",
                "moreTriggerCharacter": ["}", "\n"],
            }

        # Rename
        if self.rename_enabled:
            capabilities["renameProvider"] = {"prepareProvider": self.rename_prepare_provider}

        # Folding Range
        if self.folding_range_enabled:
            capabilities["foldingRangeProvider"] = True

        # Selection Range
        if self.selection_range_enabled:
            capabilities["selectionRangeProvider"] = True

        # Semantic Tokens
        if self.semantic_tokens_enabled:
            capabilities["semanticTokensProvider"] = {
                "legend": {
                    "tokenTypes": self._get_semantic_token_types(),
                    "tokenModifiers": self._get_semantic_token_modifiers(),
                },
                "range": True,
                "full": {"delta": True},
            }

        # Diagnostics
        if self.diagnostic_provider:
            capabilities["diagnosticProvider"] = {
                "interFileDependencies": self.diagnostic_inter_file_dependencies,
                "workspaceDiagnostics": self.diagnostic_workspace_diagnostics,
            }

        return capabilities

    def _get_semantic_token_types(self) -> list[str]:
        """Get semantic token types for ML language."""
        return [
            "namespace",
            "type",
            "class",
            "enum",
            "interface",
            "struct",
            "typeParameter",
            "parameter",
            "variable",
            "property",
            "enumMember",
            "event",
            "function",
            "method",
            "macro",
            "keyword",
            "modifier",
            "comment",
            "string",
            "number",
            "regexp",
            "operator",
            "decorator",
        ]

    def _get_semantic_token_modifiers(self) -> list[str]:
        """Get semantic token modifiers for ML language."""
        return [
            "declaration",
            "definition",
            "readonly",
            "static",
            "deprecated",
            "abstract",
            "async",
            "modification",
            "documentation",
            "defaultLibrary",
        ]


class MLFeatureFlags:
    """Feature flags for experimental or optional ML LSP features."""

    def __init__(self):
        # Security Analysis Features
        self.security_diagnostics: bool = True
        self.capability_validation: bool = True
        self.sandbox_analysis: bool = True

        # Advanced Language Features
        self.pattern_matching_support: bool = True
        self.async_await_support: bool = True
        self.generic_type_support: bool = True
        self.macro_expansion: bool = False  # Disabled for security

        # IDE Integration Features
        self.auto_import: bool = True
        self.smart_completion: bool = True
        self.refactoring_support: bool = True
        self.code_generation: bool = True

        # Performance Features
        self.incremental_parsing: bool = True
        self.parallel_analysis: bool = True
        self.background_compilation: bool = True
        self.caching_enabled: bool = True

        # Debugging Features
        self.source_map_support: bool = True
        self.breakpoint_support: bool = True
        self.variable_inspection: bool = True

        # Experimental Features
        self.ai_assisted_completion: bool = False
        self.automatic_error_fixes: bool = False
        self.performance_profiling: bool = False

    def to_dict(self) -> dict[str, bool]:
        """Convert feature flags to dictionary."""
        return {
            # Security Analysis
            "security_diagnostics": self.security_diagnostics,
            "capability_validation": self.capability_validation,
            "sandbox_analysis": self.sandbox_analysis,
            # Advanced Language Features
            "pattern_matching_support": self.pattern_matching_support,
            "async_await_support": self.async_await_support,
            "generic_type_support": self.generic_type_support,
            "macro_expansion": self.macro_expansion,
            # IDE Integration
            "auto_import": self.auto_import,
            "smart_completion": self.smart_completion,
            "refactoring_support": self.refactoring_support,
            "code_generation": self.code_generation,
            # Performance
            "incremental_parsing": self.incremental_parsing,
            "parallel_analysis": self.parallel_analysis,
            "background_compilation": self.background_compilation,
            "caching_enabled": self.caching_enabled,
            # Debugging
            "source_map_support": self.source_map_support,
            "breakpoint_support": self.breakpoint_support,
            "variable_inspection": self.variable_inspection,
            # Experimental
            "ai_assisted_completion": self.ai_assisted_completion,
            "automatic_error_fixes": self.automatic_error_fixes,
            "performance_profiling": self.performance_profiling,
        }

    @classmethod
    def from_dict(cls, data: dict[str, bool]) -> "MLFeatureFlags":
        """Create feature flags from dictionary."""
        flags = cls()

        for key, value in data.items():
            if hasattr(flags, key):
                setattr(flags, key, value)

        return flags


# Default configurations for different use cases
DEFAULT_DEVELOPMENT = MLServerCapabilities(
    # Enable all development features
    completion_enabled=True,
    hover_enabled=True,
    definition_enabled=True,
    references_enabled=True,
    document_symbol_enabled=True,
    code_action_enabled=True,
    document_formatting_enabled=True,
    rename_enabled=True,
    diagnostic_provider=True,
)

MINIMAL_CONFIG = MLServerCapabilities(
    # Minimal configuration for basic editing
    completion_enabled=True,
    hover_enabled=True,
    diagnostic_provider=True,
    # Disable advanced features
    signature_help_enabled=False,
    definition_enabled=False,
    references_enabled=False,
    code_action_enabled=False,
    code_lens_enabled=False,
    document_formatting_enabled=False,
    rename_enabled=False,
)

SECURITY_FOCUSED = MLServerCapabilities(
    # Focus on security analysis
    diagnostic_provider=True,
    diagnostic_inter_file_dependencies=True,
    diagnostic_workspace_diagnostics=True,
    # Basic editing features
    completion_enabled=True,
    hover_enabled=True,
    # Disable potentially risky features
    code_action_enabled=False,
    document_formatting_enabled=False,
    rename_enabled=False,
)
