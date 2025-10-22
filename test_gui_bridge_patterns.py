"""Test case to verify GUI bridge integration patterns.

This test verifies the three key technical questions:
1. Module import dependencies work for deployment
2. Object attribute/method access with @ml_class decoration
3. Constant export patterns (class attributes vs methods)

Uses the module registry auto-discovery system:
- gui_bridge.py placed in test_extensions/ directory
- Registry configured to scan test_extensions/ via add_extension_paths()
- Module automatically discovered and loaded on import
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mlpy.ml.transpiler import MLTranspiler
from mlpy.stdlib.module_registry import get_registry


# =============================================================================
# Run Test
# =============================================================================

def test_gui_bridge_patterns():
    """Test all three integration patterns using module registry."""
    print("=" * 80)
    print("GUI BRIDGE INTEGRATION PATTERNS TEST")
    print("=" * 80)
    print()

    print("Testing:")
    print("1. Module imports (nested dependencies)")
    print("2. Object attribute/method access with @ml_class")
    print("3. Constant export (both class attributes and methods)")
    print()

    # Get module registry and add extension path
    registry = get_registry()
    test_extensions_path = os.path.join(os.path.dirname(__file__), 'test_extensions')

    print(f"Adding extension path: {test_extensions_path}")
    registry.add_extension_paths([test_extensions_path])

    # Verify gui module is available
    if not registry.is_available('gui'):
        print("[FAIL] GUI module not found in registry!")
        print(f"Available modules: {registry.get_all_module_names()}")
        return False

    print("[OK] GUI module discovered by registry")
    print()

    # Read ML test code
    ml_file = Path(__file__).parent / 'test_gui_integration.ml'
    if not ml_file.exists():
        print(f"[FAIL] ML test file not found: {ml_file}")
        return False

    ml_code = ml_file.read_text(encoding='utf-8')

    # Create transpiler
    transpiler = MLTranspiler()

    print("-" * 80)
    print("TRANSPILING ML CODE:")
    print("-" * 80)
    print(ml_code)
    print()

    # Transpile ML code
    python_code, issues, source_map = transpiler.transpile_to_python(
        ml_code,
        strict_security=False
    )

    if not python_code:
        print("[FAIL] TRANSPILATION FAILED!")
        for issue in issues:
            print(f"  - {issue}")
        return False

    print("-" * 80)
    print("GENERATED PYTHON CODE:")
    print("-" * 80)
    print(python_code)
    print()

    print("-" * 80)
    print("EXECUTING TRANSPILED CODE:")
    print("-" * 80)

    # Load gui module from registry
    gui_module = registry.get_module('gui')
    if not gui_module:
        print("[FAIL] Failed to load GUI module from registry!")
        return False

    # Create capability context for execution
    from mlpy.runtime.capabilities import CapabilityContext, CapabilityToken
    from mlpy.runtime.whitelist_validator import set_capability_context

    # Create execution environment with gui module from registry
    exec_globals = {
        'gui': gui_module,
        '__name__': '__main__',
    }

    try:
        # Execute with capability context (grant all gui.* capabilities)
        with CapabilityContext() as ctx:
            # Create capability tokens for GUI operations
            ctx.add_capability(CapabilityToken(capability_type='gui.create'))
            ctx.add_capability(CapabilityToken(capability_type='gui.window'))
            ctx.add_capability(CapabilityToken(capability_type='gui.event_loop'))

            # Set active context for capability checking
            set_capability_context(ctx)

            exec(python_code, exec_globals)

            # Clear active context
            set_capability_context(None)
        print()
        print("=" * 80)
        print("[SUCCESS] ALL TESTS PASSED!")
        print("=" * 80)
        print()
        print("Verified:")
        print("  [OK] Module auto-discovery works (registry found gui_bridge.py)")
        print("  [OK] Module imports work (gui_bridge could import Python modules)")
        print("  [OK] Object method calls work (window.setTitle(), button.click())")
        print("  [OK] Returned objects support method chaining")
        print("  [OK] Constants as attributes work (gui.VERSION, gui.MAX_WIDTH)")
        print("  [OK] Constants as methods work (gui.DEFAULT_WIDTH())")
        print("  [OK] ML callbacks work directly (no wrapper needed!)")
        print("  [OK] Object passing works (window.addWidget(button))")
        print()
        print("CONCLUSION:")
        print("  All three integration patterns are confirmed working!")
        print("  Ready to implement full tkinter bridge following these patterns.")
        print()
        return True

    except Exception as e:
        print()
        print("=" * 80)
        print("[FAIL] EXECUTION FAILED!")
        print("=" * 80)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_gui_bridge_patterns()
    sys.exit(0 if success else 1)
