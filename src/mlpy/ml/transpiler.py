"""Main ML transpiler with integrated security analysis."""

from typing import List, Optional, Tuple
from pathlib import Path

from mlpy.runtime.profiling.decorators import profile_parser, profile_security
from mlpy.ml.errors.context import ErrorContext
from mlpy.ml.grammar.parser import MLParser
from mlpy.ml.grammar.ast_nodes import Program
from mlpy.ml.analysis.security_analyzer import SecurityAnalyzer


class MLTranspiler:
    """Main ML transpiler with integrated parsing and security analysis."""

    def __init__(self) -> None:
        """Initialize the transpiler."""
        self.parser = MLParser()

    @profile_parser
    def parse_with_security_analysis(
        self,
        source_code: str,
        source_file: Optional[str] = None
    ) -> Tuple[Optional[Program], List[ErrorContext]]:
        """Parse ML code and run security analysis.

        Args:
            source_code: The ML source code to parse
            source_file: Optional source file path for error reporting

        Returns:
            Tuple of (AST Program node, List of security issues)
            AST will be None if parsing fails.
        """
        try:
            # Parse the source code
            ast = self.parser.parse(source_code, source_file)

            # Run security analysis
            security_issues = self._analyze_security(ast, source_file)

            return ast, security_issues

        except Exception:
            # If parsing fails, return None AST and empty security issues
            # The parser will have already created appropriate error contexts
            return None, []

    @profile_security
    def _analyze_security(
        self,
        ast: Program,
        source_file: Optional[str]
    ) -> List[ErrorContext]:
        """Run security analysis on parsed AST."""
        analyzer = SecurityAnalyzer(source_file)
        return analyzer.analyze(ast)

    def transpile_to_python(
        self,
        source_code: str,
        source_file: Optional[str] = None,
        strict_security: bool = True
    ) -> Tuple[Optional[str], List[ErrorContext]]:
        """Transpile ML code to Python with security validation.

        Args:
            source_code: The ML source code to transpile
            source_file: Optional source file path for error reporting
            strict_security: If True, fail on any security issues

        Returns:
            Tuple of (Python code string, List of issues found)
            Python code will be None if transpilation fails.
        """
        # Parse and analyze
        ast, security_issues = self.parse_with_security_analysis(source_code, source_file)

        if ast is None:
            return None, []

        # Check for critical security issues
        critical_issues = [
            issue for issue in security_issues
            if issue.error.severity.value in ["critical", "high"]
        ]

        if strict_security and critical_issues:
            # Don't transpile if there are critical security issues
            return None, security_issues

        # TODO: Implement actual Python code generation
        # For now, return a placeholder
        python_code = self._generate_python_placeholder(ast)

        return python_code, security_issues

    def _generate_python_placeholder(self, ast: Program) -> str:
        """Generate placeholder Python code.

        This is a temporary implementation until the full transpiler is built.
        """
        return f'''"""
Generated Python code from ML transpiler
AST contains {len(ast.items)} top-level items
TODO: Implement full transpilation in Sprint 3
"""

# Placeholder Python code
def main():
    print("ML code successfully parsed and analyzed")
    print("Security analysis completed")
    return True

if __name__ == "__main__":
    main()
'''

    def transpile_file(
        self,
        file_path: str,
        output_path: Optional[str] = None,
        strict_security: bool = True
    ) -> Tuple[Optional[str], List[ErrorContext]]:
        """Transpile ML file to Python.

        Args:
            file_path: Path to ML source file
            output_path: Optional output file path
            strict_security: If True, fail on any security issues

        Returns:
            Tuple of (Python code string, List of issues found)
        """
        try:
            path = Path(file_path)
            source_code = path.read_text(encoding='utf-8')

            python_code, issues = self.transpile_to_python(
                source_code,
                source_file=file_path,
                strict_security=strict_security
            )

            # Write output file if specified and transpilation succeeded
            if output_path and python_code:
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(python_code, encoding='utf-8')

            return python_code, issues

        except Exception as e:
            from mlpy.ml.errors.exceptions import MLParseError
            from mlpy.ml.errors.context import create_error_context

            error = MLParseError(
                f"Failed to transpile file: {str(e)}",
                suggestions=[
                    "Check that the input file exists and is readable",
                    "Verify file permissions and encoding",
                    "Ensure output directory is writable"
                ],
                context={
                    "file_path": file_path,
                    "output_path": output_path,
                    "error_type": type(e).__name__
                },
                source_file=file_path
            )

            error_context = create_error_context(error)
            return None, [error_context]

    def validate_security_only(
        self,
        source_code: str,
        source_file: Optional[str] = None
    ) -> List[ErrorContext]:
        """Run only security validation without full transpilation.

        Args:
            source_code: The ML source code to validate
            source_file: Optional source file path for error reporting

        Returns:
            List of security issues found
        """
        _, security_issues = self.parse_with_security_analysis(source_code, source_file)
        return security_issues


# Global transpiler instance
ml_transpiler = MLTranspiler()


def transpile_ml_code(
    source_code: str,
    source_file: Optional[str] = None,
    strict_security: bool = True
) -> Tuple[Optional[str], List[ErrorContext]]:
    """Transpile ML source code using the global transpiler.

    Args:
        source_code: The ML source code to transpile
        source_file: Optional source file path for error reporting
        strict_security: If True, fail on any security issues

    Returns:
        Tuple of (Python code string, List of issues found)
    """
    return ml_transpiler.transpile_to_python(source_code, source_file, strict_security)


def transpile_ml_file(
    file_path: str,
    output_path: Optional[str] = None,
    strict_security: bool = True
) -> Tuple[Optional[str], List[ErrorContext]]:
    """Transpile ML file using the global transpiler.

    Args:
        file_path: Path to ML source file
        output_path: Optional output file path
        strict_security: If True, fail on any security issues

    Returns:
        Tuple of (Python code string, List of issues found)
    """
    return ml_transpiler.transpile_file(file_path, output_path, strict_security)


def validate_ml_security(
    source_code: str,
    source_file: Optional[str] = None
) -> List[ErrorContext]:
    """Validate ML code security using the global transpiler.

    Args:
        source_code: The ML source code to validate
        source_file: Optional source file path for error reporting

    Returns:
        List of security issues found
    """
    return ml_transpiler.validate_security_only(source_code, source_file)