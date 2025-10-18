"""
Smoke tests for integration examples
Verifies that all examples can be loaded and initialized
"""

import sys
import pytest
from pathlib import Path

# Add mlpy to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.mlpy.ml.transpiler import MLTranspiler


class TestPySide6Example:
    """Test PySide6 calculator example"""

    def test_ml_file_transpiles(self):
        """Test that ML calculator file transpiles successfully"""
        ml_file = Path(__file__).parent / "gui/pyside6/ml_calculator.ml"

        transpiler = MLTranspiler()
        with open(ml_file, encoding='utf-8') as f:
            ml_code = f.read()

        python_code, issues, source_map = transpiler.transpile_to_python(
            ml_code, source_file=str(ml_file), strict_security=False
        )

        assert python_code is not None, f"Transpilation failed with issues: {issues}"
        assert len(python_code) > 0
        print(f"✓ PySide6 ML file transpiled: {len(python_code)} bytes")

    def test_gui_module_can_import(self):
        """Test that GUI calculator module exists"""
        gui_file = Path(__file__).parent / "gui/pyside6/calculator_gui.py"
        assert gui_file.exists()


class TestFlaskExample:
    """Test Flask API example"""

    def test_ml_file_transpiles(self):
        """Test that ML API file transpiles successfully"""
        ml_file = Path(__file__).parent / "web/flask/ml_api.ml"

        transpiler = MLTranspiler()
        with open(ml_file, encoding='utf-8') as f:
            ml_code = f.read()

        python_code, issues, source_map = transpiler.transpile_to_python(
            ml_code, source_file=str(ml_file), strict_security=False
        )

        assert python_code is not None, f"Transpilation failed with issues: {issues}"
        assert len(python_code) > 0
        print(f"✓ Flask ML file transpiled: {len(python_code)} bytes")

    def test_api_module_can_import(self):
        """Test that Flask API can be imported"""
        try:
            from examples.integration.web.flask.app import MLFlaskAPI
            assert MLFlaskAPI is not None
            print("✓ Flask MLFlaskAPI class imported successfully")
        except ImportError as e:
            pytest.fail(f"Failed to import Flask API: {e}")


class TestFastAPIExample:
    """Test FastAPI analytics example"""

    def test_ml_file_transpiles(self):
        """Test that ML analytics file transpiles successfully"""
        ml_file = Path(__file__).parent / "web/fastapi/ml_analytics.ml"

        transpiler = MLTranspiler()
        with open(ml_file, encoding='utf-8') as f:
            ml_code = f.read()

        python_code, issues, source_map = transpiler.transpile_to_python(
            ml_code, source_file=str(ml_file), strict_security=False
        )

        assert python_code is not None, f"Transpilation failed with issues: {issues}"
        assert len(python_code) > 0
        print(f"✓ FastAPI ML file transpiled: {len(python_code)} bytes")

    def test_api_module_can_import(self):
        """Test that FastAPI app can be created"""
        try:
            from examples.integration.web.fastapi.app import create_app
            app = create_app()
            assert app is not None
            print("✓ FastAPI app created successfully")
        except Exception as e:
            pytest.fail(f"Failed to create FastAPI app: {e}")


class TestIntegrationExamplesDocumentation:
    """Test that documentation exists"""

    def test_readme_exists(self):
        """Test that README.md exists"""
        readme = Path(__file__).parent / "README.md"
        assert readme.exists()
        content = readme.read_text()
        assert len(content) > 1000
        print(f"✓ README.md exists: {len(content)} characters")

    def test_all_ml_files_exist(self):
        """Test that all ML source files exist"""
        ml_files = [
            "gui/pyside6/ml_calculator.ml",
            "web/flask/ml_api.ml",
            "web/fastapi/ml_analytics.ml",
        ]

        for ml_file in ml_files:
            path = Path(__file__).parent / ml_file
            assert path.exists(), f"ML file not found: {ml_file}"
            print(f"✓ {ml_file} exists")

    def test_all_python_apps_exist(self):
        """Test that all Python applications exist"""
        app_files = [
            "gui/pyside6/calculator_gui.py",
            "web/flask/app.py",
            "web/fastapi/app.py",
        ]

        for app_file in app_files:
            path = Path(__file__).parent / app_file
            assert path.exists(), f"App file not found: {app_file}"
            print(f"✓ {app_file} exists")

    def test_test_clients_exist(self):
        """Test that test clients exist for web APIs"""
        test_clients = [
            "web/flask/test_client.py",
            "web/fastapi/test_client.py",
        ]

        for client_file in test_clients:
            path = Path(__file__).parent / client_file
            assert path.exists(), f"Test client not found: {client_file}"
            print(f"✓ {client_file} exists")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
