"""Integration tests for ML capability system integration."""

import pytest
import tempfile
import os
from pathlib import Path
from src.mlpy.ml.transpiler import MLTranspiler
from src.mlpy.runtime.capabilities import get_capability_manager


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
        ml_code = '''
capability FileAccess {
    resource "*.txt";
    allow read;
    allow write;
}

function main() {
    return "Hello World";
}
'''

        # Transpile ML code
        python_code, source_map = self.transpiler.transpile(ml_code)

        # Verify generated Python contains capability system imports and functions
        assert "from mlpy.runtime.capabilities import create_capability_token" in python_code
        assert "from mlpy.runtime.capabilities import get_capability_manager" in python_code
        assert "def _create_FileAccess_capability():" in python_code
        assert "def FileAccess_context():" in python_code
        assert '@contextlib.contextmanager' in python_code

        # Verify resource patterns and permissions are correctly generated
        assert 'resource_patterns=["*.txt"]' in python_code
        assert 'allowed_operations={"read", "write"}' in python_code or 'allowed_operations={"write", "read"}' in python_code

    def test_multiple_capability_declarations(self):
        """Test multiple capability declarations in one program."""
        ml_code = '''
capability FileAccess {
    resource "*.txt";
    allow read;
}

capability NetworkAccess {
    resource "api.example.com";
    allow network;
}

function main() {
    return "Multi-capability demo";
}
'''

        python_code, _ = self.transpiler.transpile(ml_code)

        # Verify both capabilities are generated
        assert "_create_FileAccess_capability" in python_code
        assert "_create_NetworkAccess_capability" in python_code
        assert "FileAccess_context" in python_code
        assert "NetworkAccess_context" in python_code

    def test_capability_with_complex_resources(self):
        """Test capability with multiple resource patterns."""
        ml_code = '''
capability DataAccess {
    resource "data/*.json";
    resource "config/*.yaml";
    resource "logs/*.log";
    allow read;
    allow write;
    allow execute;
}
'''

        python_code, _ = self.transpiler.transpile(ml_code)

        # Verify all resource patterns are included
        assert 'data/*.json' in python_code
        assert 'config/*.yaml' in python_code
        assert 'logs/*.log' in python_code

        # Verify all permissions are included
        permissions_in_code = python_code[python_code.find('allowed_operations='):python_code.find('description=')]
        assert 'read' in permissions_in_code
        assert 'write' in permissions_in_code
        assert 'execute' in permissions_in_code

    def test_generated_capability_execution(self):
        """Test that generated capability code actually works."""
        ml_code = '''
capability TestCapability {
    resource "test*.txt";
    allow read;
}
'''

        python_code, _ = self.transpiler.transpile(ml_code)

        # Execute the generated Python code
        exec_globals = {}
        exec(python_code, exec_globals)

        # Test that capability functions exist and work
        assert '_create_TestCapability_capability' in exec_globals
        assert 'TestCapability_context' in exec_globals

        # Create capability token
        token = exec_globals['_create_TestCapability_capability']()
        assert token.capability_type == "TestCapability"
        assert "test*.txt" in token.constraints.resource_patterns
        assert "read" in token.constraints.allowed_operations

        # Test context manager
        with exec_globals['TestCapability_context']():
            # Verify we're in a capability context
            context = self.manager.get_current_context()
            assert context is not None
            assert context.has_capability("TestCapability")

    def test_integration_with_function_calls(self):
        """Test capability integration with function calls."""
        ml_code = '''
capability FileOps {
    resource "*.txt";
    allow read;
    allow write;
}

function readFile(filename) {
    return "Contents of " + filename;
}

function main() {
    return readFile("test.txt");
}
'''

        python_code, _ = self.transpiler.transpile(ml_code)

        # The generated code should include capability infrastructure
        assert "FileOps_context" in python_code

        # Execute and test
        exec_globals = {}
        exec(python_code, exec_globals)

        # Functions should be callable
        assert 'main' in exec_globals
        result = exec_globals['main']()
        assert "Contents of test.txt" in result

    def test_capability_security_metadata(self):
        """Test that capability metadata is correctly preserved."""
        ml_code = '''
capability SecurityTest {
    resource "/secure/*.data";
    allow read;
}
'''

        python_code, _ = self.transpiler.transpile(ml_code)

        # Execute and test metadata
        exec_globals = {}
        exec(python_code, exec_globals)

        token = exec_globals['_create_SecurityTest_capability']()

        # Verify security constraints
        assert not token.can_access_resource("/etc/passwd", "read")
        assert not token.can_access_resource("secure/file.data", "write")
        assert token.can_access_resource("/secure/test.data", "read")

    def test_empty_capability_declaration(self):
        """Test capability declaration with no items."""
        ml_code = '''
capability EmptyCapability {
}

function test() {
    return "empty";
}
'''

        python_code, _ = self.transpiler.transpile(ml_code)

        # Should still generate basic capability structure
        assert "_create_EmptyCapability_capability" in python_code
        assert "EmptyCapability_context" in python_code

        # Execute and verify
        exec_globals = {}
        exec(python_code, exec_globals)

        token = exec_globals['_create_EmptyCapability_capability']()
        assert token.capability_type == "EmptyCapability"
        assert len(token.constraints.resource_patterns) == 0
        assert len(token.constraints.allowed_operations) == 0

    def test_capability_name_sanitization(self):
        """Test that capability names are properly sanitized for Python."""
        ml_code = '''
capability File-Access_2024 {
    resource "*.txt";
    allow read;
}
'''

        python_code, _ = self.transpiler.transpile(ml_code)

        # Python identifiers should be sanitized
        assert "File_Access_2024" in python_code
        assert "File-Access_2024" not in python_code

        # Functions should work with sanitized names
        exec_globals = {}
        exec(python_code, exec_globals)

        assert '_create_File_Access_2024_capability' in exec_globals
        assert 'File_Access_2024_context' in exec_globals

    def test_source_map_generation_with_capabilities(self):
        """Test that source maps work correctly with capability declarations."""
        ml_code = '''capability Test {
    resource "*.txt";
}

function main() {
    return "test";
}'''

        python_code, source_map = self.transpiler.transpile(ml_code, generate_source_maps=True)

        # Source map should exist
        assert source_map is not None
        assert 'version' in source_map
        assert 'mappings' in source_map

        # Should have mappings for both capability and function
        mappings = source_map.get('mappings', '')
        assert len(mappings) > 0  # Should have some mappings


if __name__ == "__main__":
    pytest.main([__file__, "-v"])