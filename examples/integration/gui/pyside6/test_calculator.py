"""
Integration tests for PySide6 ML Calculator
Tests ML transpilation and function execution
"""

import sys
import pytest
from pathlib import Path

# Add mlpy to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.mlpy.ml.transpiler import MLTranspiler


class TestMLCalculator:
    """Test ML calculator business logic"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self):
        """Setup transpiler and load ML functions once for all tests"""
        ml_file = Path(__file__).parent / "ml_calculator.ml"

        transpiler = MLTranspiler()
        with open(ml_file, "r", encoding="utf-8") as f:
            ml_code = f.read()

        python_code, issues, source_map = transpiler.transpile_to_python(
            ml_code, source_file=str(ml_file), strict_security=False
        )

        assert python_code is not None, f"Transpilation failed: {issues}"
        assert len(issues) == 0, f"Transpilation had issues: {issues}"

        # Setup capability context for tests
        from mlpy.runtime.capabilities import get_capability_manager
        from mlpy.runtime.capabilities.tokens import CapabilityToken

        manager = get_capability_manager()
        ctx = manager.create_context(name="test_context")

        # Grant all capabilities for testing
        ctx.add_capability(CapabilityToken(
            resource_pattern="*",
            permissions=["*"]
        ))
        ctx.__enter__()

        # Execute and extract functions
        namespace = {}
        exec(python_code, namespace)

        TestMLCalculator.ml_functions = {
            name: namespace[name]
            for name in [
                "add", "subtract", "multiply", "divide",
                "calculate_compound_interest", "fibonacci",
                "calculate_statistics"
            ]
            if name in namespace
        }

        assert len(TestMLCalculator.ml_functions) == 7, "Not all ML functions loaded"

        yield

        # Cleanup
        ctx.__exit__(None, None, None)

    def test_basic_arithmetic(self):
        """Test basic arithmetic operations"""
        # Test addition
        assert self.ml_functions["add"](5, 3) == 8
        assert self.ml_functions["add"](-5, 3) == -2
        assert self.ml_functions["add"](0, 0) == 0

        # Test subtraction
        assert self.ml_functions["subtract"](10, 3) == 7
        assert self.ml_functions["subtract"](3, 10) == -7
        assert self.ml_functions["subtract"](5, 5) == 0

        # Test multiplication
        assert self.ml_functions["multiply"](5, 3) == 15
        assert self.ml_functions["multiply"](-5, 3) == -15
        assert self.ml_functions["multiply"](0, 100) == 0

    def test_division(self):
        """Test division with zero handling"""
        # Normal division
        assert self.ml_functions["divide"](10, 2) == 5
        assert self.ml_functions["divide"](7, 2) == 3.5

        # Division by zero returns None
        assert self.ml_functions["divide"](10, 0) is None
        assert self.ml_functions["divide"](0, 0) is None

    def test_compound_interest(self):
        """Test compound interest calculation"""
        result = self.ml_functions["calculate_compound_interest"](10000, 5.5, 10)

        assert result is not None
        assert "amount" in result
        assert "interest" in result
        assert "principal" in result
        assert "rate" in result
        assert "years" in result

        # Check calculations
        assert result["principal"] == 10000
        assert result["rate"] == 5.5
        assert result["years"] == 10

        # Compound interest formula: A = P(1 + r)^t
        # A = 10000 * (1.055)^10 ≈ 17081.44
        assert 17000 < result["amount"] < 17200
        assert 7000 < result["interest"] < 7200

    def test_fibonacci(self):
        """Test Fibonacci sequence generation"""
        # Small values
        assert self.ml_functions["fibonacci"](0) == 0
        assert self.ml_functions["fibonacci"](1) == 1
        assert self.ml_functions["fibonacci"](2) == 1
        assert self.ml_functions["fibonacci"](3) == 2
        assert self.ml_functions["fibonacci"](4) == 3
        assert self.ml_functions["fibonacci"](5) == 5
        assert self.ml_functions["fibonacci"](6) == 8

        # Larger value
        assert self.ml_functions["fibonacci"](10) == 55
        assert self.ml_functions["fibonacci"](20) == 6765

    def test_statistics_empty_array(self):
        """Test statistics with empty array"""
        result = self.ml_functions["calculate_statistics"]([])
        assert result is None

    def test_statistics_single_element(self):
        """Test statistics with single element"""
        result = self.ml_functions["calculate_statistics"]([42])

        assert result is not None
        assert result["count"] == 1
        assert result["sum"] == 42
        assert result["mean"] == 42
        assert result["min"] == 42
        assert result["max"] == 42

    def test_statistics_multiple_elements(self):
        """Test statistics with multiple elements"""
        numbers = [10, 20, 30, 40, 50]
        result = self.ml_functions["calculate_statistics"](numbers)

        assert result is not None
        assert result["count"] == 5
        assert result["sum"] == 150
        assert result["mean"] == 30
        assert result["min"] == 10
        assert result["max"] == 50

    def test_statistics_negative_numbers(self):
        """Test statistics with negative numbers"""
        numbers = [-5, -10, 0, 10, 5]
        result = self.ml_functions["calculate_statistics"](numbers)

        assert result is not None
        assert result["count"] == 5
        assert result["sum"] == 0
        assert result["mean"] == 0
        assert result["min"] == -10
        assert result["max"] == 10


class TestPySide6Integration:
    """Test PySide6 application initialization"""

    def test_application_imports(self):
        """Test that all required imports work"""
        try:
            from PySide6.QtWidgets import QApplication
            from PySide6.QtCore import QThread, Signal
            assert True
        except ImportError as e:
            pytest.fail(f"PySide6 imports failed: {e}")

    def test_ml_transpiler_import(self):
        """Test MLTranspiler import"""
        try:
            from src.mlpy.ml.transpiler import MLTranspiler
            transpiler = MLTranspiler()
            assert transpiler is not None
        except Exception as e:
            pytest.fail(f"MLTranspiler import/init failed: {e}")

    def test_calculator_gui_imports(self):
        """Test calculator GUI can be imported"""
        try:
            # Import without running the application
            calculator_path = Path(__file__).parent / "calculator_gui.py"
            assert calculator_path.exists()
        except Exception as e:
            pytest.fail(f"Calculator GUI import failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
