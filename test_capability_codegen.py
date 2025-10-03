#!/usr/bin/env python3
"""Quick test to verify capability code generation."""

from mlpy.ml.transpiler import MLTranspiler


def test_capability_codegen():
    """Test that MLTranspiler generates correct capability code."""

    transpiler = MLTranspiler()

    ml_code = '''capability FileAccess {
    resource "*.txt";
    allow read;
    allow write;
}

function main() {
    return "Hello World";
}'''

    python_code, issues, source_map = transpiler.transpile_to_python(
        ml_code,
        strict_security=False
    )

    # Verify transpilation succeeded
    assert python_code is not None, "Transpilation should succeed"
    assert len(issues) == 0, f"Should have no issues, got {len(issues)}"

    # Verify capability infrastructure
    assert "from mlpy.runtime.capabilities import create_capability_token" in python_code
    assert "from mlpy.runtime.capabilities import get_capability_manager" in python_code
    assert "def _create_FileAccess_capability():" in python_code
    assert "def FileAccess_context():" in python_code
    assert "@contextlib.contextmanager" in python_code

    # Verify resource patterns and permissions
    assert '"*.txt"' in python_code
    assert '"read"' in python_code or "'read'" in python_code
    assert '"write"' in python_code or "'write'" in python_code

    # Verify function was generated
    assert "def main():" in python_code
    assert "return 'Hello World'" in python_code

    print("SUCCESS: All assertions passed!")
    print()
    print("Generated Python code:")
    print("=" * 70)
    print(python_code)
    print("=" * 70)

    # Test execution
    print()
    print("Testing execution of generated code...")
    exec_globals = {}
    exec(python_code, exec_globals)

    assert "_create_FileAccess_capability" in exec_globals
    assert "FileAccess_context" in exec_globals
    assert "main" in exec_globals

    # Test capability token
    token = exec_globals["_create_FileAccess_capability"]()
    assert token.capability_type == "FileAccess"
    assert "*.txt" in token.constraints.resource_patterns
    assert "read" in token.constraints.allowed_operations
    assert "write" in token.constraints.allowed_operations

    # Test main function
    result = exec_globals["main"]()
    assert result == "Hello World"

    print("SUCCESS: Execution test passed!")
    print(f"  - Capability token created: {token.capability_type}")
    print(f"  - Resource patterns: {token.constraints.resource_patterns}")
    print(f"  - Allowed operations: {token.constraints.allowed_operations}")
    print(f"  - main() returned: {result}")


if __name__ == "__main__":
    test_capability_codegen()
