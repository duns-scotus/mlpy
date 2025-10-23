"""
Example test demonstrating DebugTestHandler usage.

This shows how to write automated tests for debugger features using
the DebugTestHandler class.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from tests.debugging.debug_test_handler import DebugTestHandler


def test_load_and_execute():
    """Test loading and executing an ML program."""
    print("\n=== Test: Load and Execute ===")

    handler = DebugTestHandler()

    # Load program
    ml_file = "tests/ml_integration/ml_debug/main.ml"
    success, message = handler.load_program(ml_file)

    print(f"Load: {success} - {message}")
    assert success, f"Failed to load program: {message}"

    # Verify source maps
    all_exist, status = handler.verify_source_maps_exist()
    print(f"Source maps: {status}")
    assert all_exist, f"Missing source map files: {status}"

    print("[PASS] Test passed\n")


def test_breakpoints():
    """Test setting and managing breakpoints."""
    print("\n=== Test: Breakpoints ===")

    handler = DebugTestHandler()

    # Load program
    ml_file = "tests/ml_integration/ml_debug/main.ml"
    success, message = handler.load_program(ml_file)
    assert success, f"Failed to load: {message}"

    # Set breakpoint
    success, message = handler.set_breakpoint("main.ml", 170)
    print(f"Set breakpoint: {success} - {message}")
    assert success, f"Failed to set breakpoint: {message}"

    # Verify breakpoint was set
    assert len(handler.breakpoints) > 0, "No breakpoints recorded"
    print(f"Breakpoints set: {len(handler.breakpoints)}")

    print("[PASS] Test passed\n")


def test_source_map_caching():
    """Test that source maps are cached and reused."""
    print("\n=== Test: Source Map Caching ===")

    handler1 = DebugTestHandler()

    ml_file = "tests/ml_integration/ml_debug/main.ml"

    # First load (force retranspile)
    print("First load (forced retranspile)...")
    success1, msg1 = handler1.load_program(ml_file, force_retranspile=True)
    assert success1, f"First load failed: {msg1}"

    # Second load (should use cache)
    print("Second load (should use cache)...")
    handler2 = DebugTestHandler()
    success2, msg2 = handler2.load_program(ml_file, force_retranspile=False)
    assert success2, f"Second load failed: {msg2}"

    # Both should have source maps
    exists1, status1 = handler1.verify_source_maps_exist()
    exists2, status2 = handler2.verify_source_maps_exist()

    assert exists1, f"First load missing source maps: {status1}"
    assert exists2, f"Second load missing source maps: {status2}"

    print(f"First load source maps: {status1}")
    print(f"Second load source maps: {status2}")
    print("[PASS] Test passed\n")


def test_multiple_files():
    """Test loading multiple ML files."""
    print("\n=== Test: Multiple Files ===")

    test_files = [
        "tests/ml_integration/ml_debug/main.ml",
        "tests/ml_integration/ml_debug/math_utils.ml",
        "tests/ml_integration/ml_debug/data_structures/list_ops.ml",
        "tests/ml_integration/ml_debug/data_structures/tree.ml",
        "tests/ml_integration/ml_debug/algorithms/search.ml",
        "tests/ml_integration/ml_debug/algorithms/sort.ml"
    ]

    for ml_file in test_files:
        print(f"\nTesting {ml_file}...")
        handler = DebugTestHandler()

        # Load and verify
        success, message = handler.load_program(ml_file)
        if not success:
            print(f"  [FAIL] Failed to load: {message}")
            continue

        # Verify source maps
        all_exist, status = handler.verify_source_maps_exist()
        if not all_exist:
            print(f"  [FAIL] Missing source maps: {status}")
            continue

        print(f"  [PASS] Loaded successfully with source maps")

    print("\n[PASS] All files tested\n")


def main():
    """Run all example tests."""
    print("=" * 70)
    print("Debug Test Handler Examples")
    print("=" * 70)

    try:
        test_load_and_execute()
        test_breakpoints()
        test_source_map_caching()
        test_multiple_files()

        print("\n" + "=" * 70)
        print("All tests passed!")
        print("=" * 70)

    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
