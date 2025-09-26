"""Unit tests for the ML transpiler."""

import pytest
from pathlib import Path
from mlpy.ml.transpiler import MLTranspiler, transpile_ml_code, validate_ml_security
from mlpy.ml.grammar.ast_nodes import Program
from mlpy.ml.errors.exceptions import MLSecurityError


class TestMLTranspiler:
    """Test the ML transpiler."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = MLTranspiler()

    def test_safe_code_transpilation(self):
        """Test transpiling safe code."""
        code = '''
        function add(a, b) {
            return a + b;
        }

        result = add(10, 20);
        '''

        python_code, issues, source_map = self.transpiler.transpile_to_python(code)

        # Should succeed with no critical issues
        assert python_code is not None
        assert len(issues) == 0
        assert "Generated Python code" in python_code

    def test_dangerous_code_strict_mode(self):
        """Test that dangerous code fails in strict security mode."""
        code = '''
        user_result = eval(user_input);
        '''

        python_code, issues, source_map = self.transpiler.transpile_to_python(
            code,
            strict_security=True
        )

        # Should fail in strict mode
        assert python_code is None
        assert len(issues) >= 1
        assert any(isinstance(issue.error, MLSecurityError) for issue in issues)

    def test_dangerous_code_permissive_mode(self):
        """Test that dangerous code succeeds in permissive mode."""
        code = '''
        user_result = eval(user_input);
        '''

        python_code, issues, source_map = self.transpiler.transpile_to_python(
            code,
            strict_security=False
        )

        # Should succeed but report issues
        assert python_code is not None
        assert len(issues) >= 1
        assert any(isinstance(issue.error, MLSecurityError) for issue in issues)

    def test_parse_with_security_analysis(self):
        """Test integrated parsing and security analysis."""
        code = '''
        import os;
        result = eval("test");
        '''

        ast, issues = self.transpiler.parse_with_security_analysis(code)

        # Should parse successfully
        assert isinstance(ast, Program)
        assert len(ast.items) == 2

        # Should detect security issues
        assert len(issues) >= 2
        assert all(isinstance(issue.error, MLSecurityError) for issue in issues)

    def test_parse_error_handling(self):
        """Test handling of parse errors."""
        code = "function incomplete("

        ast, issues = self.transpiler.parse_with_security_analysis(code)

        # Should fail parsing
        assert ast is None
        # Security analysis can't run if parsing fails
        assert len(issues) == 0

    def test_validate_security_only(self):
        """Test security-only validation."""
        code = '''
        import subprocess;
        data = eval(user_code);
        '''

        issues = self.transpiler.validate_security_only(code)

        # Should detect security issues
        assert len(issues) >= 2
        assert all(isinstance(issue.error, MLSecurityError) for issue in issues)

    def test_transpile_file_success(self):
        """Test transpiling from file."""
        # Create a temporary test file
        test_file = Path("test_ml_file.ml")
        test_content = '''
        function greet(name) {
            return "Hello, " + name;
        }
        '''

        try:
            test_file.write_text(test_content, encoding='utf-8')

            python_code, issues, source_map = self.transpiler.transpile_file(str(test_file))

            assert python_code is not None
            assert len(issues) == 0
            assert "Generated Python code" in python_code

        finally:
            # Clean up
            if test_file.exists():
                test_file.unlink()

    def test_transpile_file_not_found(self):
        """Test error handling for non-existent file."""
        python_code, issues, source_map = self.transpiler.transpile_file("non_existent.ml")

        assert python_code is None
        assert len(issues) >= 1

    def test_transpile_file_with_output(self):
        """Test transpiling file with output path."""
        # Create temporary test files
        input_file = Path("test_input.ml")
        output_file = Path("test_output.py")

        test_content = '''
        x = 42;
        '''

        try:
            input_file.write_text(test_content, encoding='utf-8')

            python_code, issues, source_map = self.transpiler.transpile_file(
                str(input_file),
                str(output_file)
            )

            assert python_code is not None
            assert len(issues) == 0
            assert output_file.exists()

            # Check output file content
            output_content = output_file.read_text(encoding='utf-8')
            assert "Generated Python code" in output_content

        finally:
            # Clean up
            for file in [input_file, output_file]:
                if file.exists():
                    file.unlink()

    def test_global_transpile_functions(self):
        """Test global convenience functions."""
        code = "x = 42;"

        # Test transpile_ml_code
        python_code, issues, source_map = transpile_ml_code(code)
        assert python_code is not None
        assert len(issues) == 0

        # Test validate_ml_security
        safe_issues = validate_ml_security(code)
        assert len(safe_issues) == 0

        # Test with dangerous code
        dangerous_code = 'result = eval("test");'
        dangerous_issues = validate_ml_security(dangerous_code)
        assert len(dangerous_issues) >= 1

    def test_comprehensive_security_analysis(self):
        """Test comprehensive security analysis on complex code."""
        code = '''
        import os;
        import sys;

        capability FileAccess {
            resource "*";
            allow system;
        }

        function process_user_data(input) {
            // Multiple security issues
            config = __import__("config");
            result = eval(input.code);
            globals_access = input.__globals__;

            return result;
        }
        '''

        ast, issues = self.transpiler.parse_with_security_analysis(code)

        # Should parse successfully
        assert isinstance(ast, Program)

        # Should detect multiple security issues
        assert len(issues) >= 5

        # Check for different types of issues
        issue_categories = set()
        for issue in issues:
            category = issue.error.context.get("category", "")
            issue_categories.add(category)

        expected_categories = {
            "unsafe_import", "code_injection", "reflection_abuse",
            "overly_broad_capability", "dangerous_permission"
        }

        # Should detect most security issue types
        assert len(issue_categories.intersection(expected_categories)) >= 3

    def test_error_reporting_with_source_file(self):
        """Test that error reporting includes source file information."""
        code = 'result = eval("dangerous");'
        source_file = "test_security.ml"

        issues = self.transpiler.validate_security_only(code, source_file)

        assert len(issues) >= 1
        for issue in issues:
            assert issue.error.source_file == source_file

    def test_capability_security_analysis(self):
        """Test security analysis of capability declarations."""
        code = '''
        capability SafeAccess {
            resource "/tmp/myapp/*";
            allow read "/etc/config";
        }

        capability DangerousAccess {
            resource "*";
            allow system;
            allow execute "*";
        }
        '''

        issues = self.transpiler.validate_security_only(code)

        # Should detect dangerous capability patterns
        dangerous_issues = [
            issue for issue in issues
            if issue.error.context.get("category") in [
                "overly_broad_capability", "dangerous_permission"
            ]
        ]

        assert len(dangerous_issues) >= 2

    def test_performance_context(self):
        """Test that performance profiling is integrated."""
        code = '''
        function calculate(n) {
            result = 0;
            for (i in range(n)) {
                result = result + i;
            }
            return result;
        }
        '''

        # Run multiple times to generate profiling data
        for _ in range(3):
            python_code, issues, source_map = self.transpiler.transpile_to_python(code)
            assert python_code is not None

        # Profiling should be working (tested in profiling tests)
        # This mainly tests integration

    def test_mixed_safe_and_dangerous_code(self):
        """Test analysis of code with both safe and dangerous parts."""
        code = '''
        // Safe operations
        function safe_math(a, b) {
            return a + b * 2;
        }

        result = safe_math(10, 5);

        // Dangerous operations
        import os;
        dangerous = eval(user_input);
        '''

        python_code, issues, source_map = self.transpiler.transpile_to_python(
            code,
            strict_security=True
        )

        # Should fail due to dangerous parts
        assert python_code is None
        assert len(issues) >= 2

        # But in permissive mode should succeed
        python_code_permissive, issues_permissive, source_map_permissive = self.transpiler.transpile_to_python(
            code,
            strict_security=False
        )

        assert python_code_permissive is not None
        assert len(issues_permissive) >= 2

    def test_empty_code_handling(self):
        """Test handling of empty or whitespace-only code."""
        empty_cases = ["", "   ", "\n\n", "// Just comments\n// More comments"]

        for empty_code in empty_cases:
            python_code, issues, source_map = self.transpiler.transpile_to_python(empty_code)

            assert python_code is not None  # Should generate placeholder
            assert len(issues) == 0  # No security issues in empty code