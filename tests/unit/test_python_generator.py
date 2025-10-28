"""Tests for Python code generation from ML AST."""

import pytest

from src.mlpy.ml.codegen.python_generator import PythonCodeGenerator
from src.mlpy.ml.grammar.ast_nodes import *


class TestPythonCodeGenerator:
    """Test suite for Python code generation."""

    def setup_method(self):
        """Set up test fixtures."""
        from src.mlpy.ml.transpiler import MLTranspiler

        self.transpiler = MLTranspiler()

    def _parse_and_generate(self, ml_code: str) -> str:
        """Helper to parse ML code and generate Python."""
        python_code, issues, _ = self.transpiler.transpile_to_python(ml_code)
        return python_code

    def test_simple_function(self):
        """Test simple function generation."""
        ml_code = """
        function add(a, b) {
            return a + b;
        }
        """
        python_code = self._parse_and_generate(ml_code)

        assert "def add(a, b):" in python_code
        assert "return (a + b)" in python_code

    def test_all_binary_operators(self):
        """Test all binary operators."""
        ml_code = """
        function test_ops(a, b) {
            sum = a + b;
            diff = a - b;
            prod = a * b;
            quot = a / b;
            mod = a % b;
            eq = a == b;
            neq = a != b;
            lt = a < b;
            gt = a > b;
            le = a <= b;
            ge = a >= b;
            and_op = a && b;
            or_op = a || b;
            return sum;
        }
        """
        python_code = self._parse_and_generate(ml_code)

        # Check that all operators are correctly translated
        assert "sum = (a + b)" in python_code
        assert "diff = (a - b)" in python_code
        assert "prod = (a * b)" in python_code
        assert "quot = (a / b)" in python_code
        assert "mod = (a % b)" in python_code
        assert "eq = (a == b)" in python_code
        assert "neq = (a != b)" in python_code
        assert "lt = (a < b)" in python_code
        assert "gt = (a > b)" in python_code
        assert "le = (a <= b)" in python_code
        assert "ge = (a >= b)" in python_code
        assert "and_op = (a and b)" in python_code
        assert "or_op = (a or b)" in python_code

    def test_control_flow(self):
        """Test if-else, while, and for statements."""
        ml_code = """
        function control_test(n, arr) {
            if (n > 0) {
                return n;
            } else {
                return 0;
            }
        }
        """
        python_code = self._parse_and_generate(ml_code)

        assert "if (n > 0):" in python_code
        assert "return n" in python_code
        assert "else:" in python_code
        assert "return 0" in python_code

    def test_object_literals_and_member_access(self):
        """Test object literal creation and member access."""
        ml_code = """
        function obj_test() {
            obj = {"name": "test", "value": 42};
            return obj.name;
        }
        """
        python_code = self._parse_and_generate(ml_code)

        assert "obj = {'name': 'test', 'value': 42}" in python_code
        # System now uses safe attribute access wrapper
        assert (
            "return obj['name']" in python_code or "_safe_attr_access(obj, 'name')" in python_code
        )

    def test_array_literals_and_access(self):
        """Test array literal creation and access."""
        ml_code = """
        function array_test() {
            arr = [1, 2, 3];
            return arr[0];
        }
        """
        python_code = self._parse_and_generate(ml_code)

        assert "arr = [1, 2, 3]" in python_code
        assert "return arr[0]" in python_code

    def test_function_calls(self):
        """Test function call generation."""
        ml_code = """
        function caller() {
            result = add(1, 2);
            return result;
        }
        """
        python_code = self._parse_and_generate(ml_code)

        # Function calls now use _safe_call wrapper for security
        assert "_safe_call(add, 1, 2)" in python_code or "result = add(1, 2)" in python_code

    def test_recursive_function(self):
        """Test recursive function generation."""
        ml_code = """
        function fibonacci(n) {
            if (n <= 1) {
                return n;
            } else {
                return fibonacci(n - 1) + fibonacci(n - 2);
            }
        }
        """
        python_code = self._parse_and_generate(ml_code)

        assert "def fibonacci(n):" in python_code
        assert "if (n <= 1):" in python_code
        assert "return n" in python_code
        assert "else:" in python_code
        assert "return (fibonacci((n - 1)) + fibonacci((n - 2)))" in python_code

    def test_capability_generation(self):
        """Test capability declaration generation."""
        ml_code = """
        capability FileAccess {
            resource "*.txt";
            allow read;
        }
        """
        python_code = self._parse_and_generate(ml_code)

        assert "@contextlib.contextmanager" in python_code
        assert "def _create_FileAccess_capability():" in python_code
        assert "def FileAccess_context():" in python_code
        assert "yield" in python_code

    def test_import_statements(self):
        """Test import statement generation."""
        ml_code = """
        import math;
        import json as JSON;
        """
        python_code = self._parse_and_generate(ml_code)

        assert "import math" in python_code
        assert "import json as JSON" in python_code

    def test_type_annotations(self):
        """Test function parameters with type annotations."""
        ml_code = """
        function typed_func(x: int, y: string) {
            return x;
        }
        """
        python_code = self._parse_and_generate(ml_code)

        assert "def typed_func(x: int, y: string):" in python_code

    def test_safe_identifier_conversion(self):
        """Test that Python keywords are safely converted."""
        ml_code = """
        function test() {
            class = "my_class";
            return class;
        }
        """
        python_code = self._parse_and_generate(ml_code)

        # Should convert Python keyword 'class' to safe identifier
        assert "ml_class = 'my_class'" in python_code
        assert "return ml_class" in python_code

    def test_source_map_generation(self):
        """Test source map generation."""
        ml_code = """
        function simple() {
            return 42;
        }
        """
        python_code, issues, source_map = self.transpiler.transpile_to_python(
            ml_code, source_file="test.ml", generate_source_maps=True
        )

        assert source_map is not None
        assert source_map["sourceMap"]["version"] == 3
        assert "test.ml" in source_map["sourceMap"]["sources"]

    def test_complex_expressions(self):
        """Test complex nested expressions."""
        ml_code = """
        function complex_expr(a, b, c) {
            return (a + b) * c - 5 / 2 && a > b || c <= 10;
        }
        """
        python_code = self._parse_and_generate(ml_code)

        # Should generate properly parenthesized Python expression
        assert "return (((((a + b) * c) - (5 / 2)) and (a > b)) or (c <= 10))" in python_code

    def test_generate_python_code_function(self):
        """Test the module-level generate_python_code function."""
        ml_code = """
        function test() {
            return "hello";
        }
        """
        python_code = self._parse_and_generate(ml_code)

        assert "def test():" in python_code
        assert "return 'hello'" in python_code


class TestCodeGenerationEdgeCases:
    """Test edge cases and error conditions."""

    def setup_method(self):
        """Set up test fixtures."""
        from src.mlpy.ml.transpiler import MLTranspiler

        self.transpiler = MLTranspiler()

    def test_empty_program(self):
        """Test generation for empty program."""

        generator = PythonCodeGenerator()
        ast = Program(items=[])
        python_code, _ = generator.generate(ast)

        # Should still generate header and footer
        assert '"""Generated Python code from mlpy ML transpiler."""' in python_code
        assert "# End of generated code" in python_code

    def test_empty_function(self):
        """Test generation for function with no body."""
        ml_code = """
        function empty() {
        }
        """
        python_code, issues, _ = self.transpiler.transpile_to_python(ml_code)

        assert "def empty():" in python_code
        assert "pass" in python_code

    def test_function_with_no_parameters(self):
        """Test function with no parameters."""
        ml_code = """
        function no_params() {
            return 42;
        }
        """
        python_code, issues, _ = self.transpiler.transpile_to_python(ml_code)

        assert "def no_params():" in python_code

    def test_nested_object_access(self):
        """Test nested object member access."""
        ml_code = """
        function nested_access() {
            obj = {"inner": {"value": 10}};
            return obj.inner.value;
        }
        """
        python_code, issues, _ = self.transpiler.transpile_to_python(ml_code)

        # System now uses safe attribute access wrapper
        assert (
            "return obj['inner']['value']" in python_code
            or "_safe_attr_access(_safe_attr_access(obj, 'inner'), 'value')" in python_code
        )


if __name__ == "__main__":
    pytest.main([__file__])
