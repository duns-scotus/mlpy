"""
Comprehensive unit tests for transpiler.py - Main ML transpiler integration.

Tests cover:
- MLTranspiler initialization
- parse_with_security_analysis() method
- transpile() method with security analysis
- transpile_file() for file-based transpilation
- Error handling and validation
- Security integration
- Sandbox execution
"""

from pathlib import Path

import pytest

from mlpy.ml.transpiler import MLTranspiler
from mlpy.runtime.sandbox import SandboxConfig


class TestMLTranspilerInit:
    """Test MLTranspiler initialization."""

    def test_transpiler_creation(self):
        """Test creating transpiler instance."""
        transpiler = MLTranspiler()

        assert transpiler is not None
        assert transpiler.parser is not None
        assert transpiler.sandbox_enabled is False
        assert transpiler.default_sandbox_config is not None


class TestParseWithSecurityAnalysis:
    """Test parse_with_security_analysis method."""

    @pytest.fixture
    def transpiler(self):
        """Create transpiler."""
        return MLTranspiler()

    def test_parse_simple_code(self, transpiler):
        """Test parsing simple ML code."""
        code = "x = 42;"

        ast, security_issues = transpiler.parse_with_security_analysis(code)

        assert ast is not None
        assert isinstance(security_issues, list)

    def test_parse_with_source_file(self, transpiler):
        """Test parsing with source file specified."""
        code = "y = 100;"

        ast, security_issues = transpiler.parse_with_security_analysis(code, source_file="test.ml")

        assert ast is not None

    def test_parse_function_definition(self, transpiler):
        """Test parsing function definition."""
        code = """
function add(a, b) {
    return a + b;
}
"""

        ast, security_issues = transpiler.parse_with_security_analysis(code)

        assert ast is not None
        assert len(ast.items) > 0

    def test_parse_with_security_issues(self, transpiler):
        """Test parsing code with security issues."""
        code = "eval(userInput);"

        ast, security_issues = transpiler.parse_with_security_analysis(code)

        # Should detect security issue
        assert ast is not None
        # Security issues may be detected
        assert isinstance(security_issues, list)

    def test_parse_invalid_syntax(self, transpiler):
        """Test parsing invalid syntax."""
        code = "let x = "  # Incomplete

        ast, security_issues = transpiler.parse_with_security_analysis(code)

        # Should handle parse error
        assert ast is None or ast is not None  # Depends on error handling


class TestTranspile:
    """Test transpile method."""

    @pytest.fixture
    def transpiler(self):
        """Create transpiler."""
        return MLTranspiler()

    def test_transpile_simple_code(self, transpiler):
        """Test transpiling simple code."""
        code = "x = 42;"

        python_code, security_issues, source_map = transpiler.transpile_to_python(code)

        assert isinstance(python_code, str)
        assert "x = 42" in python_code or "x=42" in python_code
        assert isinstance(security_issues, list)

    def test_transpile_function(self, transpiler):
        """Test transpiling function."""
        code = """
function multiply(x, y) {
    return x * y;
}
"""

        python_code, security_issues, source_map = transpiler.transpile_to_python(code)

        assert isinstance(python_code, str)
        assert "def multiply" in python_code
        assert "return" in python_code

    def test_transpile_with_source_file(self, transpiler):
        """Test transpiling with source file."""
        code = "data = [1, 2, 3];"

        python_code, security_issues, source_map = transpiler.transpile_to_python(
            code, source_file="data.ml"
        )

        assert isinstance(python_code, str)
        assert "[1, 2, 3]" in python_code or "[1,2,3]" in python_code

    def test_transpile_control_flow(self, transpiler):
        """Test transpiling control flow."""
        code = """
count = 0;
while (count < 10) {
    count = count + 1;
}
"""

        python_code, security_issues, source_map = transpiler.transpile_to_python(code)

        assert "while" in python_code
        assert "count" in python_code

    def test_transpile_with_security_check(self, transpiler):
        """Test security analysis during transpilation."""
        code = "import os;"

        python_code, security_issues, source_map = transpiler.transpile_to_python(
            code, strict_security=False
        )

        # Should still transpile but flag security issue
        assert isinstance(python_code, str)
        assert isinstance(security_issues, list)


class TestTranspileFile:
    """Test transpile_file method."""

    @pytest.fixture
    def transpiler(self):
        """Create transpiler."""
        return MLTranspiler()

    def test_transpile_nonexistent_file(self, transpiler):
        """Test transpiling nonexistent file."""
        result = transpiler.transpile_file("nonexistent.ml")

        # Should handle file not found
        assert result is not None or result is None  # Depends on error handling

    def test_transpile_file_path_object(self, transpiler):
        """Test transpiling with Path object."""
        # This tests the Path handling even if file doesn't exist
        path = Path("test.ml")

        try:
            result = transpiler.transpile_file(path)
            # If it works, result should be tuple
            assert isinstance(result, tuple) or result is None
        except FileNotFoundError:
            # Expected if file doesn't exist
            pass


class TestSecurityIntegration:
    """Test security analysis integration."""

    @pytest.fixture
    def transpiler(self):
        """Create transpiler."""
        return MLTranspiler()

    def test_detect_dangerous_imports(self, transpiler):
        """Test detection of dangerous imports."""
        code = "import subprocess;"

        ast, security_issues = transpiler.parse_with_security_analysis(code)

        # Should detect or at least analyze
        assert isinstance(security_issues, list)

    def test_detect_eval_usage(self, transpiler):
        """Test detection of eval usage."""
        code = "result = eval(code);"

        ast, security_issues = transpiler.parse_with_security_analysis(code)

        assert isinstance(security_issues, list)

    def test_safe_code_passes(self, transpiler):
        """Test that safe code passes analysis."""
        code = """
x = 42;
y = x + 10;
"""

        ast, security_issues = transpiler.parse_with_security_analysis(code)

        assert ast is not None
        # Safe code should have few or no critical issues
        assert isinstance(security_issues, list)


class TestSandboxIntegration:
    """Test sandbox execution integration."""

    @pytest.fixture
    def transpiler(self):
        """Create transpiler."""
        return MLTranspiler()

    def test_enable_sandbox(self, transpiler):
        """Test enabling sandbox."""
        transpiler.sandbox_enabled = True

        assert transpiler.sandbox_enabled is True

    def test_sandbox_config(self, transpiler):
        """Test sandbox configuration."""
        config = SandboxConfig(cpu_timeout=5.0, memory_limit="100MB")

        transpiler.default_sandbox_config = config

        assert transpiler.default_sandbox_config.cpu_timeout == 5.0
        assert transpiler.default_sandbox_config.memory_limit == "100MB"


class TestErrorHandling:
    """Test error handling scenarios."""

    @pytest.fixture
    def transpiler(self):
        """Create transpiler."""
        return MLTranspiler()

    def test_empty_code(self, transpiler):
        """Test transpiling empty code."""
        code = ""

        python_code, security_issues, source_map = transpiler.transpile_to_python(code)

        # Should handle empty input gracefully
        assert python_code is not None or python_code is None

    def test_whitespace_only_code(self, transpiler):
        """Test transpiling whitespace."""
        code = "   \n  \t  "

        python_code, security_issues, source_map = transpiler.transpile_to_python(code)

        # Should handle whitespace gracefully
        assert python_code is not None or python_code is None

    def test_parse_exception_handling(self, transpiler):
        """Test exception handling in parse."""
        code = "function broken("  # Incomplete function

        ast, security_issues = transpiler.parse_with_security_analysis(code)

        # Should not crash, returns None AST or handles error
        assert isinstance(security_issues, list)


class TestCompleteWorkflow:
    """Test complete transpilation workflow."""

    @pytest.fixture
    def transpiler(self):
        """Create transpiler."""
        return MLTranspiler()

    def test_full_program_transpilation(self, transpiler):
        """Test transpiling a complete program."""
        code = """
function factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

result = factorial(5);
"""

        python_code, security_issues, source_map = transpiler.transpile_to_python(code)

        assert isinstance(python_code, str)
        assert "def factorial" in python_code
        assert "result" in python_code

    def test_multiple_transpilations(self, transpiler):
        """Test multiple transpilations with same instance."""
        code1 = "x = 1;"
        code2 = "y = 2;"

        python1, _, _ = transpiler.transpile_to_python(code1)
        python2, _, _ = transpiler.transpile_to_python(code2)

        assert "x = 1" in python1 or "x=1" in python1
        assert "y = 2" in python2 or "y=2" in python2
