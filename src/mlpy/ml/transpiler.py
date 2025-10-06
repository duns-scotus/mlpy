"""Main ML transpiler with integrated security analysis."""

from pathlib import Path

from mlpy.ml.analysis.security_analyzer import SecurityAnalyzer
from mlpy.ml.codegen.python_generator import generate_python_code
from mlpy.ml.errors.context import ErrorContext
from mlpy.ml.grammar.ast_nodes import Program
from mlpy.ml.grammar.parser import MLParser
from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.tokens import CapabilityToken
from mlpy.runtime.profiling.decorators import profile_parser, profile_security
from mlpy.runtime.sandbox import MLSandbox, SandboxConfig, SandboxResult


class MLTranspiler:
    """Main ML transpiler with integrated parsing and security analysis."""

    def __init__(self) -> None:
        """Initialize the transpiler."""
        self.parser = MLParser()
        self.sandbox_enabled = False
        self.default_sandbox_config = SandboxConfig()

    @profile_parser
    def parse_with_security_analysis(
        self, source_code: str, source_file: str | None = None
    ) -> tuple[Program | None, list[ErrorContext]]:
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
    def _analyze_security(self, ast: Program, source_file: str | None) -> list[ErrorContext]:
        """Run security analysis on parsed AST."""
        analyzer = SecurityAnalyzer(source_file)
        return analyzer.analyze(ast)

    def transpile_to_python(
        self,
        source_code: str,
        source_file: str | None = None,
        strict_security: bool = True,
        generate_source_maps: bool = False,
        import_paths: list[str] | None = None,
        allow_current_dir: bool = True,
        module_output_mode: str = 'separate',
    ) -> tuple[str | None, list[ErrorContext], dict | None]:
        """Transpile ML code to Python with security validation.

        Args:
            source_code: The ML source code to transpile
            source_file: Optional source file path for error reporting
            strict_security: If True, fail on any security issues
            generate_source_maps: If True, generate source map data
            import_paths: Paths to search for user modules
            allow_current_dir: Allow imports from current directory
            module_output_mode: 'separate' (create .py files) or 'inline' (embed in main file)

        Returns:
            Tuple of (Python code string, List of issues found, source map data)
            Python code will be None if transpilation fails.
        """
        # Parse and analyze
        ast, security_issues = self.parse_with_security_analysis(source_code, source_file)

        if ast is None:
            return None, [], None

        # Check for critical security issues
        critical_issues = [
            issue for issue in security_issues if issue.error.severity.value in ["critical", "high"]
        ]

        if strict_security and critical_issues:
            # Don't transpile if there are critical security issues
            return None, security_issues, None

        # Generate Python code
        try:
            python_code, source_map = generate_python_code(
                ast,
                source_file=source_file,
                generate_source_maps=generate_source_maps,
                import_paths=import_paths,
                allow_current_dir=allow_current_dir,
                module_output_mode=module_output_mode
            )
            return python_code, security_issues, source_map

        except Exception as e:
            from mlpy.ml.errors.context import create_error_context
            from mlpy.ml.errors.exceptions import MLError

            error = MLError(
                f"Code generation failed: {str(e)}",
                suggestions=[
                    "Check for unsupported ML language features",
                    "Verify that the AST was parsed correctly",
                    "Report this issue if it persists",
                ],
                context={"error_type": type(e).__name__, "source_file": source_file},
            )

            error_context = create_error_context(error)
            return None, security_issues + [error_context], None

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
        output_path: str | None = None,
        strict_security: bool = True,
        generate_source_maps: bool = False,
    ) -> tuple[str | None, list[ErrorContext], dict | None]:
        """Transpile ML file to Python.

        Args:
            file_path: Path to ML source file
            output_path: Optional output file path
            strict_security: If True, fail on any security issues
            generate_source_maps: If True, generate source map data

        Returns:
            Tuple of (Python code string, List of issues found, source map data)
        """
        try:
            path = Path(file_path)
            source_code = path.read_text(encoding="utf-8")

            python_code, issues, source_map = self.transpile_to_python(
                source_code,
                source_file=file_path,
                strict_security=strict_security,
                generate_source_maps=generate_source_maps,
            )

            # Write output file if specified and transpilation succeeded
            if output_path and python_code:
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(python_code, encoding="utf-8")

                # Write source map if generated
                if source_map and generate_source_maps:
                    source_map_path = output_file.with_suffix(".py.map")
                    import json

                    source_map_path.write_text(json.dumps(source_map, indent=2), encoding="utf-8")

            return python_code, issues, source_map

        except Exception as e:
            from mlpy.ml.errors.context import create_error_context
            from mlpy.ml.errors.exceptions import MLParseError

            error = MLParseError(
                f"Failed to transpile file: {str(e)}",
                suggestions=[
                    "Check that the input file exists and is readable",
                    "Verify file permissions and encoding",
                    "Ensure output directory is writable",
                ],
                context={
                    "file_path": file_path,
                    "output_path": output_path,
                    "error_type": type(e).__name__,
                },
                source_file=file_path,
            )

            error_context = create_error_context(error)
            return None, [error_context], None

    def execute_with_sandbox(
        self,
        source_code: str,
        source_file: str | None = None,
        capabilities: list[CapabilityToken] | None = None,
        context: CapabilityContext | None = None,
        sandbox_config: SandboxConfig | None = None,
        strict_security: bool = True,
    ) -> tuple[SandboxResult | None, list[ErrorContext]]:
        """Execute ML code in sandbox environment.

        Args:
            source_code: The ML source code to execute
            source_file: Optional source file path for error reporting
            capabilities: Capability tokens for sandbox execution
            context: Existing capability context to use
            sandbox_config: Sandbox configuration
            strict_security: If True, fail on any security issues

        Returns:
            Tuple of (SandboxResult, List of issues found)
            SandboxResult will be None if execution setup fails.
        """
        # Parse and analyze first
        ast, security_issues = self.parse_with_security_analysis(source_code, source_file)

        if ast is None:
            return None, security_issues

        # Check for critical security issues
        critical_issues = [
            issue for issue in security_issues if issue.error.severity.value in ["critical", "high"]
        ]

        if strict_security and critical_issues:
            return None, security_issues

        # Execute in sandbox
        try:
            config = sandbox_config or self.default_sandbox_config

            with MLSandbox(config) as sandbox:
                result = sandbox.execute(source_code, capabilities, context)

                return result, security_issues

        except Exception as e:
            from mlpy.ml.errors.context import create_error_context
            from mlpy.ml.errors.exceptions import MLError

            error = MLError(
                f"Sandbox execution failed: {str(e)}",
                suggestions=[
                    "Check sandbox configuration",
                    "Verify capability permissions",
                    "Ensure system resources are available",
                ],
                context={"error_type": type(e).__name__, "source_file": source_file},
            )

            error_context = create_error_context(error)
            return None, security_issues + [error_context]

    def set_sandbox_config(self, config: SandboxConfig) -> None:
        """Set default sandbox configuration."""
        self.default_sandbox_config = config

    def enable_sandbox(self, enabled: bool = True) -> None:
        """Enable/disable sandbox execution by default."""
        self.sandbox_enabled = enabled

    def validate_security_only(
        self, source_code: str, source_file: str | None = None
    ) -> list[ErrorContext]:
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
    source_file: str | None = None,
    strict_security: bool = True,
    generate_source_maps: bool = False,
) -> tuple[str | None, list[ErrorContext], dict | None]:
    """Transpile ML source code using the global transpiler.

    Args:
        source_code: The ML source code to transpile
        source_file: Optional source file path for error reporting
        strict_security: If True, fail on any security issues
        generate_source_maps: If True, generate source map data

    Returns:
        Tuple of (Python code string, List of issues found, source map data)
    """
    return ml_transpiler.transpile_to_python(
        source_code, source_file, strict_security, generate_source_maps
    )


def transpile_ml_file(
    file_path: str,
    output_path: str | None = None,
    strict_security: bool = True,
    generate_source_maps: bool = False,
) -> tuple[str | None, list[ErrorContext], dict | None]:
    """Transpile ML file using the global transpiler.

    Args:
        file_path: Path to ML source file
        output_path: Optional output file path
        strict_security: If True, fail on any security issues
        generate_source_maps: If True, generate source map data

    Returns:
        Tuple of (Python code string, List of issues found, source map data)
    """
    return ml_transpiler.transpile_file(
        file_path, output_path, strict_security, generate_source_maps
    )


def validate_ml_security(source_code: str, source_file: str | None = None) -> list[ErrorContext]:
    """Validate ML code security using the global transpiler.

    Args:
        source_code: The ML source code to validate
        source_file: Optional source file path for error reporting

    Returns:
        List of security issues found
    """
    return ml_transpiler.validate_security_only(source_code, source_file)


def execute_ml_code_sandbox(
    source_code: str,
    source_file: str | None = None,
    capabilities: list[CapabilityToken] | None = None,
    context: CapabilityContext | None = None,
    sandbox_config: SandboxConfig | None = None,
    strict_security: bool = True,
) -> tuple[SandboxResult | None, list[ErrorContext]]:
    """Execute ML code in sandbox using the global transpiler.

    Args:
        source_code: The ML source code to execute
        source_file: Optional source file path for error reporting
        capabilities: Capability tokens for sandbox execution
        context: Existing capability context to use
        sandbox_config: Sandbox configuration
        strict_security: If True, fail on any security issues

    Returns:
        Tuple of (SandboxResult, List of issues found)
    """
    return ml_transpiler.execute_with_sandbox(
        source_code, source_file, capabilities, context, sandbox_config, strict_security
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python transpiler.py <ml_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    output_path = file_path.replace(".ml", ".py")

    print(f"Transpiling {file_path} to {output_path}...")

    try:
        python_code, issues, source_map = transpile_ml_file(
            file_path, output_path, strict_security=False, generate_source_maps=False
        )

        if python_code:
            print(f"SUCCESS: Successfully transpiled to {output_path}")
            if issues:
                print(f"WARNING: Found {len(issues)} issues:")
                for issue in issues:
                    print(f"  - {issue.error.message}")
        else:
            print("ERROR: Transpilation failed")
            if issues:
                print("Issues found:")
                for issue in issues:
                    print(f"  - {issue.error.message}")
            else:
                print("No specific issues reported")
    except Exception as e:
        print(f"EXCEPTION: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
