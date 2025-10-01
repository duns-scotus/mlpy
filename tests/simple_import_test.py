#!/usr/bin/env python3
"""Simple test script for ML import system functionality."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_module_resolution():
    """Test basic module resolution functionality."""
    print("=== Testing ML Module Resolution System ===\n")

    try:
        from mlpy.cli.import_config import ImportConfiguration, apply_import_config
        from mlpy.ml.resolution.resolver import ModuleResolver
        from mlpy.stdlib.registry import get_stdlib_registry

        print("[OK] All imports successful")

        # Test 1: Initialize stdlib registry
        print("\n--- Test 1: Standard Library Registry ---")
        registry = get_stdlib_registry()
        modules = registry.list_modules()
        print(f"[OK] Registered modules: {modules}")

        for module_name in modules:
            module_info = registry.get_module_info(module_name)
            if module_info:
                print(f"  - {module_name}: {module_info.description}")

        # Test 2: Module resolver with stdlib
        print("\n--- Test 2: Module Resolver ---")
        resolver = ModuleResolver()

        # Test math module resolution
        try:
            math_module = resolver.resolve_import(["math"])
            print(
                f"[OK] Math module resolved: {math_module.name} (stdlib: {math_module.is_stdlib})"
            )
        except Exception as e:
            print(f"[FAIL] Math module resolution failed: {e}")

        # Test json module resolution
        try:
            json_module = resolver.resolve_import(["json"])
            print(
                f"[OK] JSON module resolved: {json_module.name} (stdlib: {json_module.is_stdlib})"
            )
        except Exception as e:
            print(f"[FAIL] JSON module resolution failed: {e}")

        # Test unknown module (should fail)
        try:
            unknown_module = resolver.resolve_import(["unknown_module"])
            print(f"[FAIL] Unknown module should have failed but got: {unknown_module.name}")
        except Exception as e:
            print(f"[OK] Unknown module correctly failed: {type(e).__name__}")

        # Test 3: Import configuration
        print("\n--- Test 3: Import Configuration ---")
        config = ImportConfiguration(
            import_paths=[],
            allow_current_dir=False,
            stdlib_mode="native",
            python_whitelist=["urllib"],
        )

        summary = config.get_config_summary()
        print(f"[OK] Config created: {summary['stdlib_mode']} mode")
        print(f"  - Import paths: {summary['import_paths_count']}")
        print(f"  - Python whitelist: {summary['python_whitelist_count']}")

        # Test 4: Bridge functions (if available)
        print("\n--- Test 4: Bridge Functions ---")
        math_bridges = registry.get_bridge_functions("math")
        print(f"[OK] Math bridge functions: {len(math_bridges)}")

        if math_bridges:
            for bridge in math_bridges[:3]:  # Show first 3
                print(f"  - {bridge.ml_name} -> {bridge.python_module}.{bridge.python_function}")

        print("\n=== All Tests Completed Successfully ===")
        return True

    except ImportError as e:
        print(f"[FAIL] Import failed: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_cli_integration():
    """Test CLI integration functionality."""
    print("\n=== Testing CLI Integration ===\n")

    try:
        from mlpy.cli.import_config import (
            create_import_config_from_cli,
            parse_import_paths,
        )

        # Test path parsing
        print("--- Test: Path Parsing ---")
        paths1 = parse_import_paths("./modules:./lib:/usr/local/ml")
        print(f"[OK] Parsed colon-separated paths: {paths1}")

        paths2 = parse_import_paths("./modules;./lib;C:\\ml")
        print(f"[OK] Parsed semicolon-separated paths: {paths2}")

        # Test config creation
        print("\n--- Test: Config Creation ---")
        config = create_import_config_from_cli(
            import_paths="./test-modules:./lib",
            allow_current_dir=True,
            stdlib_mode="native",
            allow_python_modules="urllib,hashlib",
        )

        summary = config.get_config_summary()
        print("[OK] CLI config created successfully")
        print(f"  - Mode: {summary['stdlib_mode']}")
        print(f"  - Current dir: {summary['allow_current_dir']}")
        print(f"  - Python modules: {summary['python_whitelist']}")

        return True

    except Exception as e:
        print(f"[FAIL] CLI integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("ML Import System Test Suite")
    print("=" * 50)

    success = True

    # Run tests
    success &= test_module_resolution()
    success &= test_cli_integration()

    print("\n" + "=" * 50)
    if success:
        print("SUCCESS: ALL TESTS PASSED!")
        return 0
    else:
        print("FAILURE: SOME TESTS FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
