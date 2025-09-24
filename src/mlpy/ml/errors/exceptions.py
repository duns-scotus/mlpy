"""MLError hierarchy with CWE mapping for security-focused error reporting."""

from enum import Enum
from typing import Any


class CWECategory(Enum):
    """Common Weakness Enumeration categories for security mapping."""

    CODE_INJECTION = 95  # CWE-95: Improper Neutralization of Directives
    RESOURCE_INJECTION = 99  # CWE-99: Improper Control of Resource Identifiers
    COMMAND_INJECTION = 78  # CWE-78: OS Command Injection
    PATH_TRAVERSAL = 22  # CWE-22: Path Traversal
    MISSING_AUTHORIZATION = 862  # CWE-862: Missing Authorization
    UNSAFE_REFLECTION = 470  # CWE-470: Use of Externally-Controlled Input
    IMPROPER_INPUT_VALIDATION = 20  # CWE-20: Improper Input Validation
    BUFFER_OVERFLOW = 119  # CWE-119: Buffer Overflow
    INFORMATION_EXPOSURE = 200  # CWE-200: Information Exposure
    DENIAL_OF_SERVICE = 400  # CWE-400: Uncontrolled Resource Consumption


class ErrorSeverity(Enum):
    """Error severity levels for prioritization."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class MLError(Exception):
    """Base class for all mlpy errors with security context."""

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        cwe: CWECategory | None = None,
        suggestions: list[str] | None = None,
        context: dict[str, Any] | None = None,
        source_file: str | None = None,
        line_number: int | None = None,
        column: int | None = None,
    ) -> None:
        """Initialize MLError with comprehensive context.

        Args:
            message: Human-readable error message
            code: Unique error code for programmatic handling
            severity: Error severity level
            cwe: Common Weakness Enumeration category
            suggestions: List of actionable suggestions for fixing the error
            context: Additional context information
            source_file: Source file where error occurred
            line_number: Line number in source file
            column: Column number in source file
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.severity = severity
        self.cwe = cwe
        self.suggestions = suggestions or []
        self.context = context or {}
        self.source_file = source_file
        self.line_number = line_number
        self.column = column

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary for serialization."""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "severity": self.severity.value,
            "cwe": self.cwe.value if self.cwe else None,
            "suggestions": self.suggestions,
            "context": self.context,
            "source_file": self.source_file,
            "line_number": self.line_number,
            "column": self.column,
        }


class MLSyntaxError(MLError):
    """Syntax errors in ML source code."""

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message, code="ML_SYNTAX_ERROR", severity=ErrorSeverity.HIGH, **kwargs)


class MLParseError(MLError):
    """Parse errors in ML source code."""

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message, code="ML_PARSE_ERROR", severity=ErrorSeverity.HIGH, **kwargs)


class MLSecurityError(MLError):
    """Security-related errors with mandatory CWE mapping."""

    def __init__(self, message: str, cwe: CWECategory, **kwargs) -> None:
        super().__init__(
            message, code="ML_SECURITY_ERROR", severity=ErrorSeverity.CRITICAL, cwe=cwe, **kwargs
        )


class MLCapabilityError(MLError):
    """Capability system violations."""

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(
            message,
            code="ML_CAPABILITY_ERROR",
            severity=ErrorSeverity.CRITICAL,
            cwe=CWECategory.MISSING_AUTHORIZATION,
            **kwargs,
        )


class MLParserError(MLError):
    """Parser-specific errors."""

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message, code="ML_PARSER_ERROR", severity=ErrorSeverity.HIGH, **kwargs)


class MLTypeError(MLError):
    """Type-related errors."""

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message, code="ML_TYPE_ERROR", severity=ErrorSeverity.MEDIUM, **kwargs)


class MLRuntimeError(MLError):
    """Runtime execution errors."""

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message, code="ML_RUNTIME_ERROR", severity=ErrorSeverity.HIGH, **kwargs)


class MLSandboxError(MLError):
    """Sandbox execution violations."""

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(
            message,
            code="ML_SANDBOX_ERROR",
            severity=ErrorSeverity.CRITICAL,
            cwe=CWECategory.DENIAL_OF_SERVICE,
            **kwargs,
        )


class MLTranspilationError(MLError):
    """Transpilation process errors."""

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(
            message, code="ML_TRANSPILATION_ERROR", severity=ErrorSeverity.HIGH, **kwargs
        )


class MLConfigurationError(MLError):
    """Configuration and setup errors."""

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(
            message, code="ML_CONFIGURATION_ERROR", severity=ErrorSeverity.MEDIUM, **kwargs
        )


# Security-specific error creators for common vulnerabilities
def create_code_injection_error(
    operation: str,
    source_file: str | None = None,
    line_number: int | None = None,
    column: int | None = None,
) -> MLSecurityError:
    """Create error for code injection attempts."""
    return MLSecurityError(
        f"Dangerous code injection operation '{operation}' is not allowed",
        cwe=CWECategory.CODE_INJECTION,
        suggestions=[
            "Use safe alternatives provided by the mlpy runtime",
            "Consider using template strings for dynamic content",
            "Review the capability system documentation for secure patterns",
        ],
        context={"operation": operation, "category": "code_injection"},
        source_file=source_file,
        line_number=line_number,
        column=column,
    )


def create_unsafe_import_error(
    module_name: str,
    source_file: str | None = None,
    line_number: int | None = None,
    column: int | None = None,
) -> MLSecurityError:
    """Create error for unsafe module imports."""
    return MLSecurityError(
        f"Import of potentially dangerous module '{module_name}' requires explicit capability",
        cwe=CWECategory.MISSING_AUTHORIZATION,
        suggestions=[
            f'Use \'with capability("import_safe", modules=["{module_name}"]):\' to explicitly allow this import',
            "Review the list of safe built-in modules",
            "Consider using mlpy's safe module alternatives",
        ],
        context={"module": module_name, "category": "unsafe_import"},
        source_file=source_file,
        line_number=line_number,
        column=column,
    )


def create_reflection_abuse_error(
    attribute: str,
    source_file: str | None = None,
    line_number: int | None = None,
    column: int | None = None,
) -> MLSecurityError:
    """Create error for reflection abuse attempts."""
    return MLSecurityError(
        f"Access to reflection attribute '{attribute}' is prohibited for security",
        cwe=CWECategory.UNSAFE_REFLECTION,
        suggestions=[
            "Use standard object methods instead of reflection",
            "Consider restructuring code to avoid reflection patterns",
            "Review mlpy's safe object interaction patterns",
        ],
        context={"attribute": attribute, "category": "reflection_abuse"},
        source_file=source_file,
        line_number=line_number,
        column=column,
    )
