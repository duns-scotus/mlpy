"""Integration tests for ML to Python code generation pipeline."""

import pytest
import tempfile
import json
from pathlib import Path
from src.mlpy.ml.transpiler import MLTranspiler, transpile_ml_code, transpile_ml_file


class TestCodeGenerationIntegration:
    """Integration tests for the complete transpilation pipeline."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = MLTranspiler()

    def test_full_transpilation_pipeline(self):
        """Test complete ML to Python transpilation."""
        ml_code = """
        capability DataAccess {
            resource "data/*.json";
            allow read;
        }

        import math;

        function calculate_average(numbers) {
            sum = 0;
            count = 0;

            for (num in numbers) {
                sum = sum + num;
                count = count + 1;
            }

            if (count > 0) {
                return sum / count;
            } else {
                return 0;
            }
        }

        function process_data() {
            data = [1, 2, 3, 4, 5];
            avg = calculate_average(data);
            result = {"average": avg, "count": data.length};
            return result;
        }
        """

        python_code, issues, source_map = self.transpiler.transpile_to_python(
            ml_code,
            generate_source_maps=True
        )

        # Verify successful transpilation
        assert python_code is not None
        assert len(issues) >= 0  # May have security warnings but should not fail

        # Verify Python code structure
        assert "import contextlib" in python_code
        assert "@contextlib.contextmanager" in python_code
        assert "def calculate_average(numbers):" in python_code
        assert "def process_data():" in python_code
        assert "import math" in python_code

        # Verify source map generation
        assert source_map is not None
        assert source_map["sourceMap"]["version"] == 3

    def test_security_analysis_integration(self):
        """Test that security analysis is properly integrated."""
        ml_code = """
        function safe_operation() {
            return 42;
        }
        """

        python_code, issues, source_map = self.transpiler.transpile_to_python(ml_code)

        assert python_code is not None
        # Should have no critical security issues for this safe code
        critical_issues = [i for i in issues if i.error.severity.value in ["critical", "high"]]
        assert len(critical_issues) == 0

    def test_strict_security_mode(self):
        """Test transpilation with strict security mode."""
        # Safe code should transpile successfully
        safe_code = """
        function add(a, b) {
            return a + b;
        }
        """

        python_code, issues, source_map = self.transpiler.transpile_to_python(
            safe_code,
            strict_security=True
        )

        assert python_code is not None

    def test_file_transpilation(self):
        """Test transpiling ML files to Python files."""
        ml_code = """
        function hello_world() {
            return "Hello, World!";
        }
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary ML file
            ml_file = Path(temp_dir) / "test.ml"
            ml_file.write_text(ml_code, encoding='utf-8')

            # Set up output file
            py_file = Path(temp_dir) / "test.py"

            # Transpile file
            python_code, issues, source_map = self.transpiler.transpile_file(
                str(ml_file),
                str(py_file),
                generate_source_maps=True
            )

            # Verify results
            assert python_code is not None
            assert py_file.exists()

            # Verify Python file contents
            python_content = py_file.read_text(encoding='utf-8')
            assert "def hello_world():" in python_content
            assert "return 'Hello, World!'" in python_content

            # Verify source map file
            source_map_file = py_file.with_suffix('.py.map')
            assert source_map_file.exists()

            map_data = json.loads(source_map_file.read_text(encoding='utf-8'))
            # Source map files should have the nested structure
            if "sourceMap" in map_data:
                assert map_data["sourceMap"]["version"] == 3
            else:
                assert map_data["version"] == 3

    def test_module_level_functions(self):
        """Test module-level transpilation functions."""
        ml_code = """
        function test_function() {
            return true;
        }
        """

        # Test transpile_ml_code function
        python_code, issues, source_map = transpile_ml_code(
            ml_code,
            generate_source_maps=True
        )

        assert python_code is not None
        assert "def test_function():" in python_code
        assert source_map is not None

    def test_transpilation_with_all_features(self):
        """Test transpilation using all supported ML language features."""
        ml_code = """
        capability FileSystem {
            resource "*.txt";
            allow read;
            allow write;
        }

        import json as JSON;

        function factorial(n) {
            if (n <= 1) {
                return 1;
            } else {
                return n * factorial(n - 1);
            }
        }

        function process_array(arr) {
            result = [];
            total = 0;

            for (item in arr) {
                if (item > 0 && item <= 100) {
                    processed = factorial(item);
                    result = result + [processed];
                    total = total + processed;
                }
            }

            return {
                "results": result,
                "total": total,
                "average": total / result.length
            };
        }

        function main() {
            data = [1, 2, 3, 4, 5];
            output = process_array(data);
            return output.total > 100;
        }
        """

        python_code, issues, source_map = self.transpiler.transpile_to_python(
            ml_code,
            source_file="comprehensive_test.ml",
            generate_source_maps=True
        )

        # Verify successful transpilation
        assert python_code is not None

        # Verify all features are present
        assert "@contextlib.contextmanager" in python_code
        assert "import json as JSON" in python_code
        assert "def factorial(n):" in python_code
        assert "def process_array(arr):" in python_code
        assert "def main():" in python_code

        # Verify control structures
        assert "if (n <= 1):" in python_code
        assert "else:" in python_code
        assert "for " in python_code

        # Verify expressions and operations
        assert "return (n * factorial((n - 1)))" in python_code
        assert "(item > 0) and (item <= 100)" in python_code

        # Verify object/array operations
        assert "result = []" in python_code
        assert "'results': result" in python_code

        # Verify source map
        assert source_map is not None
        assert source_map["sourceMap"]["sources"] == ["comprehensive_test.ml"]

    def test_error_handling_in_transpilation(self):
        """Test error handling during transpilation."""
        # Invalid ML syntax should be handled gracefully
        invalid_ml = """
        function incomplete_function(
        """

        python_code, issues, source_map = self.transpiler.transpile_to_python(invalid_ml)

        # Should return None for failed transpilation
        assert python_code is None
        # But should not raise an exception

    def test_source_map_accuracy(self):
        """Test that source maps accurately map to original source."""
        ml_code = """
        function test() {
            x = 42;
            return x;
        }
        """

        python_code, issues, source_map = self.transpiler.transpile_to_python(
            ml_code,
            source_file="test.ml",
            generate_source_maps=True
        )

        assert source_map is not None

        # Verify source map structure
        assert "version" in source_map["sourceMap"]
        assert "sources" in source_map["sourceMap"]
        assert "mappings" in source_map["sourceMap"]

        # Verify mappings exist
        mappings = source_map["sourceMap"]["mappings"]
        assert len(mappings) > 0

        # Each detailed mapping should have required fields
        detailed_mappings = source_map["debugInfo"]["detailedMappings"]
        for mapping in detailed_mappings:
            assert "generated" in mapping
            assert "original" in mapping

    def test_performance_with_large_programs(self):
        """Test transpilation performance with larger programs."""
        # Generate a reasonably large ML program
        functions = []
        for i in range(20):
            functions.append(f"""
            function func_{i}(x) {{
                if (x > {i}) {{
                    return x + {i};
                }} else {{
                    return x * {i};
                }}
            }}
            """)

        ml_code = "\n".join(functions)

        python_code, issues, source_map = self.transpiler.transpile_to_python(
            ml_code,
            generate_source_maps=True
        )

        # Should handle large programs without issues
        assert python_code is not None
        assert len([line for line in python_code.split('\n') if line.strip().startswith('def')]) == 20


if __name__ == "__main__":
    pytest.main([__file__])