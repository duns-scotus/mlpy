"""Integration tests for ML capability system integration.

These tests validate that capability declarations in ML code are correctly
transpiled to Python code with proper capability infrastructure.
"""

import tempfile

import pytest

from mlpy.ml.transpiler import MLTranspiler
from mlpy.runtime.capabilities import get_capability_manager


class TestCapabilityMLIntegration:
    """Test integration between ML language and capability system."""

    def setup_method(self):
        """Set up test fixtures."""
        self.transpiler = MLTranspiler()
        self.manager = get_capability_manager()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

    def test_capability_declaration_compilation(self):
        """Test that capability declarations compile to Python correctly."""
        ml_code = """capability FileAccess { resource "*.txt"; allow read; allow write; } function main() { return "Hello World"; }"""

        # Transpile ML code to Python
        python_code, security_issues, source_map = self.transpiler.transpile_to_python(
            ml_code, strict_security=False, generate_source_maps=True
        )

        # Verify transpilation succeeded
        assert python_code is not None, "Transpilation failed"
        assert len(python_code) > 0, "Generated Python code is empty"

        # Verify generated Python contains capability system imports and functions
        assert (
            "create_capability_token" in python_code
        ), "Missing capability token import"
        assert (
            "def _create_FileAccess_capability():" in python_code
        ), "Missing capability creation function"
        assert (
            "def FileAccess_context():" in python_code
        ), "Missing capability context manager"
        assert (
            "@contextlib.contextmanager" in python_code
        ), "Missing context manager decorator"

        # Verify resource patterns and permissions are correctly generated
        assert "*.txt" in python_code, "Resource pattern not in generated code"
        assert "read" in python_code and "write" in python_code, "Permissions missing"

    def test_multiple_capability_declarations(self):
        """Test multiple capability declarations in one program."""
        ml_code = """capability FileAccess { resource "*.txt"; allow read; } capability NetworkAccess { resource "api.example.com"; allow network; } function main() { return "Multi-capability demo"; }"""

        python_code, security_issues, source_map = self.transpiler.transpile_to_python(
            ml_code, strict_security=False
        )

        assert python_code is not None, "Transpilation failed"

        # Verify both capabilities are generated
        assert (
            "_create_FileAccess_capability" in python_code
        ), "FileAccess capability missing"
        assert (
            "_create_NetworkAccess_capability" in python_code
        ), "NetworkAccess capability missing"
        assert "FileAccess_context" in python_code, "FileAccess context missing"
        assert (
            "NetworkAccess_context" in python_code
        ), "NetworkAccess context missing"

    def test_capability_with_complex_resources(self):
        """Test capability with multiple resource patterns."""
        ml_code = """capability DataAccess { resource "data/*.json"; resource "config/*.yaml"; resource "logs/*.log"; allow read; allow write; allow execute; }"""

        python_code, security_issues, source_map = self.transpiler.transpile_to_python(
            ml_code, strict_security=False
        )

        assert python_code is not None, "Transpilation failed"

        # Verify all resource patterns are included
        assert "data/*.json" in python_code, "JSON pattern missing"
        assert "config/*.yaml" in python_code, "YAML pattern missing"
        assert "logs/*.log" in python_code, "LOG pattern missing"

        # Verify all permissions are included
        assert "read" in python_code, "Read permission missing"
        assert "write" in python_code, "Write permission missing"
        assert "execute" in python_code, "Execute permission missing"

    def test_generated_capability_execution(self):
        """Test that generated capability code actually works."""
        ml_code = """capability TestCapability { resource "test*.txt"; allow read; }"""

        python_code, security_issues, source_map = self.transpiler.transpile_to_python(
            ml_code, strict_security=False
        )

        assert python_code is not None, "Transpilation failed"

        # Execute the generated Python code
        exec_globals = {}
        exec(python_code, exec_globals)

        # Test that capability functions exist and work
        assert (
            "_create_TestCapability_capability" in exec_globals
        ), "Capability creation function not in globals"
        assert (
            "TestCapability_context" in exec_globals
        ), "Capability context manager not in globals"

        # Create capability token
        token = exec_globals["_create_TestCapability_capability"]()
        assert token.capability_type == "TestCapability", "Wrong capability type"
        assert (
            "test*.txt" in token.constraints.resource_patterns
        ), "Resource pattern not in token"
        assert (
            "read" in token.constraints.allowed_operations
        ), "Read operation not in token"

        # Test context manager
        from mlpy.runtime.capabilities.context import get_current_context

        with exec_globals["TestCapability_context"]():
            # Verify we're in a capability context
            context = get_current_context()
            assert context is not None, "No current context"
            assert context.has_capability(
                "TestCapability"
            ), "Context doesn't have TestCapability"

    def test_integration_with_function_calls(self):
        """Test capability integration with function calls."""
        ml_code = """capability FileOps { resource "*.txt"; allow read; allow write; } function readFile(filename) { return "Contents of " + filename; } function main() { return readFile("test.txt"); }"""

        python_code, security_issues, source_map = self.transpiler.transpile_to_python(
            ml_code, strict_security=False
        )

        assert python_code is not None, "Transpilation failed"

        # The generated code should include capability infrastructure
        assert "FileOps_context" in python_code, "FileOps context missing"

        # Execute and test
        exec_globals = {}
        exec(python_code, exec_globals)

        # Functions should be callable
        assert "main" in exec_globals, "main function not in globals"
        result = exec_globals["main"]()
        assert "Contents of test.txt" in result, "Function execution failed"

    def test_capability_security_metadata(self):
        """Test that capability metadata is correctly preserved."""
        ml_code = """capability SecurityTest { resource "/secure/*.data"; allow read; }"""

        python_code, security_issues, source_map = self.transpiler.transpile_to_python(
            ml_code, strict_security=False
        )

        assert python_code is not None, "Transpilation failed"

        # Execute and test metadata
        exec_globals = {}
        exec(python_code, exec_globals)

        token = exec_globals["_create_SecurityTest_capability"]()

        # Verify security constraints
        assert not token.can_access_resource(
            "/etc/passwd", "read"
        ), "Should not access /etc/passwd"
        assert not token.can_access_resource(
            "secure/file.data", "write"
        ), "Should not have write access"
        assert token.can_access_resource(
            "/secure/test.data", "read"
        ), "Should access /secure/test.data"

    def test_empty_capability_declaration(self):
        """Test capability declaration with no items."""
        ml_code = """capability EmptyCapability { } function test() { return "empty"; }"""

        python_code, security_issues, source_map = self.transpiler.transpile_to_python(
            ml_code, strict_security=False
        )

        assert python_code is not None, "Transpilation failed"

        # Should still generate basic capability structure
        assert (
            "_create_EmptyCapability_capability" in python_code
        ), "Empty capability creation function missing"
        assert (
            "EmptyCapability_context" in python_code
        ), "Empty capability context missing"

        # Execute and verify
        exec_globals = {}
        exec(python_code, exec_globals)

        token = exec_globals["_create_EmptyCapability_capability"]()
        assert token.capability_type == "EmptyCapability", "Wrong capability type"
        assert (
            len(token.constraints.resource_patterns) == 0
        ), "Should have no resource patterns"
        assert (
            len(token.constraints.allowed_operations) == 0
        ), "Should have no operations"

    def test_capability_name_with_underscores_and_numbers(self):
        """Test that capability names with underscores and numbers work correctly."""
        # Note: ML grammar only allows [a-zA-Z_][a-zA-Z0-9_]* for identifiers
        # Hyphens are not valid in ML identifiers
        ml_code = """capability File_Access_2024 { resource "*.txt"; allow read; }"""

        python_code, security_issues, source_map = self.transpiler.transpile_to_python(
            ml_code, strict_security=False
        )

        assert python_code is not None, "Transpilation failed"

        # Python identifiers should preserve underscores and numbers
        assert "File_Access_2024" in python_code, "Capability name not in code"

        # Functions should work with the name
        exec_globals = {}
        exec(python_code, exec_globals)

        assert (
            "_create_File_Access_2024_capability" in exec_globals
        ), "Creation function not in globals"
        assert (
            "File_Access_2024_context" in exec_globals
        ), "Context not in globals"

    def test_source_map_generation_with_capabilities(self):
        """Test that source maps work correctly with capability declarations."""
        ml_code = """capability Test { resource "*.txt"; } function main() { return "test"; }"""

        python_code, security_issues, source_map = self.transpiler.transpile_to_python(
            ml_code, strict_security=False, generate_source_maps=True
        )

        assert python_code is not None, "Transpilation failed"

        # Verify code contains both capability and function
        assert "Test_context" in python_code, "Test context missing"
        assert "def main():" in python_code, "main function missing"

        # Verify source map was generated
        assert source_map is not None, "Source map not generated"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
