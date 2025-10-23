"""Main ML language parser using Lark with security-first design."""

import time
from pathlib import Path

from lark import Lark, LarkError
from lark.exceptions import UnexpectedInput, UnexpectedToken

from mlpy.ml.errors.exceptions import MLParseError, MLSyntaxError
from mlpy.runtime.profiling.decorators import profile_parser

from .ast_nodes import Program
from .transformer import MLTransformer


class MLParser:
    """Security-first ML language parser."""

    def __init__(self) -> None:
        """Initialize the parser with grammar and transformer."""
        self._parser: Lark | None = None
        self._transformer = MLTransformer()
        self._grammar_path = Path(__file__).parent / "ml.lark"

    @property
    def parser(self) -> Lark:
        """Lazy-loaded Lark parser instance.

        Uses pre-compiled grammar if available for 60-80% faster cold-start.
        Falls back to compiling from .lark file if compiled version not found.
        """
        if self._parser is None:
            compiled_path = self._grammar_path.with_name('ml_parser.compiled')

            try:
                # Try loading pre-compiled grammar (60-80% faster)
                if compiled_path.exists():
                    try:
                        with compiled_path.open('rb') as f:
                            self._parser = Lark.load(f)
                        return self._parser
                    except Exception:
                        # Compiled grammar failed, fall through to .lark compilation
                        pass

                # Fall back to compiling from .lark file
                self._parser = Lark.open(
                    self._grammar_path,
                    parser="lalr",  # Fast LALR(1) parser
                    propagate_positions=True,  # For error reporting and source maps
                    maybe_placeholders=False,  # Strict parsing
                    debug=False,  # Production mode
                )
            except Exception as e:
                raise MLParseError(
                    f"Failed to initialize parser: {str(e)}",
                    suggestions=[
                        "Check that ml.lark grammar file exists and is valid",
                        "Verify Lark installation: pip install lark-parser",
                        "Review grammar syntax for any errors",
                        "Try running: python -m scripts.compile_grammar",
                    ],
                    context={
                        "grammar_file": str(self._grammar_path),
                        "compiled_file": str(compiled_path),
                        "error_type": type(e).__name__,
                    },
                )
        return self._parser

    @profile_parser
    def parse(self, source_code: str, source_file: str | None = None) -> Program:
        """Parse ML source code into an AST.

        Args:
            source_code: The ML source code to parse
            source_file: Optional source file path for error reporting

        Returns:
            Program AST node representing the parsed code

        Raises:
            MLSyntaxError: For syntax errors in the source code
            MLParseError: For parser internal errors
        """
        if not source_code.strip():
            return Program(items=[])

        try:
            start_time = time.perf_counter()
            tree = self.parser.parse(source_code)

            # Apply transformer manually to get AST with line/column info
            ast = self._transformer.transform(tree)
            parse_time = time.perf_counter() - start_time

            # Verify we got a Program node
            if not isinstance(ast, Program):
                raise MLParseError(
                    "Parser produced invalid AST root node",
                    suggestions=[
                        "Check grammar transformer configuration",
                        "Verify that program rule returns Program node",
                    ],
                    context={"actual_type": type(ast).__name__, "expected_type": "Program"},
                )

            # Add performance context
            if hasattr(ast, "parse_time"):
                ast.parse_time = parse_time

            return ast

        except UnexpectedToken as e:
            # Convert Lark syntax errors to MLSyntaxError
            raise self._create_syntax_error(e, source_code, source_file)

        except UnexpectedInput as e:
            # Convert Lark parse errors to MLSyntaxError
            raise self._create_syntax_error(e, source_code, source_file)

        except LarkError as e:
            # Generic Lark errors
            raise MLParseError(
                f"Parse error: {str(e)}",
                suggestions=[
                    "Check source code syntax against ML language specification",
                    "Verify that all brackets and parentheses are properly closed",
                    "Ensure proper statement termination with semicolons",
                ],
                context={"error_type": type(e).__name__, "source_file": source_file or "unknown"},
                source_file=source_file,
            )

        except Exception as e:
            # Unexpected errors
            raise MLParseError(
                f"Unexpected parser error: {str(e)}",
                suggestions=[
                    "This appears to be an internal parser error",
                    "Please report this issue with the source code that caused it",
                    "Try simplifying the source code to isolate the problem",
                ],
                context={"error_type": type(e).__name__, "source_file": source_file or "unknown"},
                source_file=source_file,
            )

    def _create_syntax_error(
        self, lark_error: Exception, source_code: str, source_file: str | None
    ) -> MLSyntaxError:
        """Create MLSyntaxError from Lark parsing error."""
        # Extract error details from Lark exception
        line_number = None
        column = None
        error_message = str(lark_error)

        if hasattr(lark_error, "line"):
            line_number = lark_error.line

        if hasattr(lark_error, "column"):
            column = lark_error.column

        # Generate helpful suggestions based on error type
        suggestions = self._generate_syntax_suggestions(lark_error, source_code)

        # Extract problematic token if available
        problematic_token = None
        if hasattr(lark_error, "token") and lark_error.token:
            problematic_token = str(lark_error.token)

        return MLSyntaxError(
            message=error_message,
            suggestions=suggestions,
            context={
                "error_type": type(lark_error).__name__,
                "token": problematic_token,
                "source_file": source_file or "unknown",
            },
            source_file=source_file,
            line_number=line_number,
            column=column,
        )

    def _generate_syntax_suggestions(self, error: Exception, source_code: str) -> list[str]:
        """Generate helpful suggestions based on syntax error."""
        suggestions = []

        error_str = str(error).lower()

        # Common syntax error patterns
        if "unexpected token" in error_str:
            suggestions.extend(
                [
                    "Check for missing semicolons at the end of statements",
                    "Verify that brackets and parentheses are properly matched",
                    "Ensure proper spacing around operators",
                ]
            )

        if "expected" in error_str and "got" in error_str:
            suggestions.extend(
                [
                    "Check the syntax around the error location",
                    "Verify that keywords are spelled correctly",
                    "Ensure proper statement structure",
                ]
            )

        if "unexpected end of input" in error_str:
            suggestions.extend(
                [
                    "Check for unclosed brackets, parentheses, or braces",
                    "Verify that all statements are properly terminated",
                    "Ensure the last statement has a semicolon if required",
                ]
            )

        # Add generic suggestions if none specific
        if not suggestions:
            suggestions.extend(
                [
                    "Review ML language syntax documentation",
                    "Check for typos in keywords and identifiers",
                    "Verify proper statement and expression structure",
                ]
            )

        return suggestions

    def parse_file(self, file_path: str) -> Program:
        """Parse ML source file.

        Args:
            file_path: Path to the ML source file

        Returns:
            Program AST node representing the parsed file

        Raises:
            MLParseError: If file cannot be read or parsed
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise MLParseError(
                    f"Source file not found: {file_path}",
                    suggestions=[
                        "Check that the file path is correct",
                        "Verify that the file exists and is readable",
                        "Use absolute path if relative path is not working",
                    ],
                    context={"file_path": file_path},
                )

            source_code = path.read_text(encoding="utf-8")
            return self.parse(source_code, source_file=file_path)

        except UnicodeDecodeError as e:
            raise MLParseError(
                f"Cannot read source file: {str(e)}",
                suggestions=[
                    "Ensure the file is saved with UTF-8 encoding",
                    "Check that the file is a valid text file",
                    "Try converting the file encoding to UTF-8",
                ],
                context={"file_path": file_path, "encoding_error": str(e)},
            )

        except Exception as e:
            raise MLParseError(
                f"Failed to read source file: {str(e)}",
                suggestions=[
                    "Check file permissions",
                    "Verify that the file is not locked by another process",
                    "Ensure sufficient system resources are available",
                ],
                context={"file_path": file_path, "error_type": type(e).__name__},
            )


# Global parser instance for convenience
ml_parser = MLParser()


def parse_ml_code(source_code: str, source_file: str | None = None) -> Program:
    """Parse ML source code using the global parser.

    Args:
        source_code: The ML source code to parse
        source_file: Optional source file path for error reporting

    Returns:
        Program AST node representing the parsed code
    """
    return ml_parser.parse(source_code, source_file)


def parse_ml_file(file_path: str) -> Program:
    """Parse ML source file using the global parser.

    Args:
        file_path: Path to the ML source file

    Returns:
        Program AST node representing the parsed file
    """
    return ml_parser.parse_file(file_path)
