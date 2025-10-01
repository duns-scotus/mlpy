"""Pytest configuration for mlpy tests."""

import sys
from pathlib import Path

import pytest

# Add src directory to Python path for testing
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def project_root_path():
    """Provide path to project root directory."""
    return project_root


@pytest.fixture(scope="session")
def test_data_path():
    """Provide path to test data directory."""
    return project_root / "tests" / "fixtures"


@pytest.fixture
def temp_ml_file(tmp_path):
    """Create a temporary ML file for testing."""

    def _create_file(content: str, filename: str = "test.ml") -> Path:
        file_path = tmp_path / filename
        file_path.write_text(content)
        return file_path

    return _create_file


@pytest.fixture
def sample_ml_code():
    """Provide sample ML code for testing."""
    return """
function greet(name) {
    return `Hello, ${name}!`
}

with capability("console_write") {
    message = greet("World")
    print(message)
}
"""


@pytest.fixture
def malicious_ml_code():
    """Provide malicious ML code for security testing."""
    return """
// This should be blocked by security analysis
eval("import os; os.system('rm -rf /')")
__import__("subprocess").run(["malicious", "command"])
open("/etc/passwd", "r").read()
"""
