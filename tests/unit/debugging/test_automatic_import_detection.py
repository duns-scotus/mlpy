"""Tests for automatic import detection and source map loading.

These tests verify that the import hook system automatically loads source
maps and activates pending breakpoints when modules are imported at runtime.
"""

import pytest
import tempfile
import shutil
import json
import sys
from pathlib import Path
from mlpy.ml.transpiler import MLTranspiler
from mlpy.debugging.debugger import MLDebugger
from mlpy.debugging.source_map_index import SourceMapIndex
from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap


@pytest.fixture
def runtime_import_project():
    """Create a project with modules that import each other at runtime."""
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir)

    # Create main.ml that imports utils dynamically
    main_ml = project_path / "main.ml"
    main_ml.write_text("""function main() {
    x = 10;
    y = 20;
    result = x + y;
    return result;
}

output = main();
""", encoding='utf-8')

    # Create utils.ml
    utils_ml = project_path / "utils.ml"
    utils_ml.write_text("""function helper(a, b) {
    return a * b;
}

function process(data) {
    return data + 100;
}
""", encoding='utf-8')

    # Create Python file that will import utils at runtime
    import_test_py = project_path / "import_test.py"
    import_test_py.write_text(f"""
# This Python file imports the transpiled utils module
import sys
sys.path.insert(0, r'{project_path}')

# Import the transpiled utils module
import utils

# Use the imported module
result = utils.helper(5, 3)
print(f"Result: {{result}}")
""", encoding='utf-8')

    # Transpile both ML files
    transpiler = MLTranspiler()

    for ml_file in [main_ml, utils_ml]:
        ml_source = ml_file.read_text(encoding='utf-8')

        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(ml_file),
            generate_source_maps=True,
            strict_security=False
        )

        if python_code and source_map_data:
            # Save .py file
            py_file = ml_file.with_suffix('.py')
            py_file.write_text(python_code, encoding='utf-8')

            # Save .ml.map file
            map_file = ml_file.with_suffix('.ml.map')
            map_file.write_text(json.dumps(source_map_data, indent=2), encoding='utf-8')

    yield project_path

    # Cleanup
    # Remove from sys.modules to avoid conflicts
    if 'utils' in sys.modules:
        del sys.modules['utils']
    if 'main' in sys.modules:
        del sys.modules['main']

    shutil.rmtree(temp_dir)


class TestAutomaticImportDetection:
    """Test automatic source map loading when modules are imported."""

    def test_import_hook_detects_module_load(self, runtime_import_project):
        """Test that import hook detects when a module is imported."""
        main_ml = runtime_import_project / "main.ml"
        utils_ml = runtime_import_project / "utils.ml"

        # Setup debugger with only main file
        ml_source = main_ml.read_text(encoding='utf-8')
        transpiler = MLTranspiler()
        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False
        )

        source_map = EnhancedSourceMap()
        if "debugInfo" in source_map_data and "detailedMappings" in source_map_data["debugInfo"]:
            for mapping_dict in source_map_data["debugInfo"]["detailedMappings"]:
                gen = mapping_dict.get("generated", {})
                orig = mapping_dict.get("original", {})
                if orig:
                    source_map.add_mapping(
                        generated_line=gen.get("line", 1),
                        generated_column=gen.get("column", 0),
                        original_line=orig.get("line"),
                        original_column=orig.get("column"),
                        source_file=mapping_dict.get("source_file", str(main_ml)),
                        name=mapping_dict.get("name"),
                        node_type=mapping_dict.get("node_type")
                    )

        py_file = main_ml.with_suffix('.py')
        source_index = SourceMapIndex.from_source_map(source_map, str(py_file))

        debugger = MLDebugger(str(main_ml), source_index, python_code)

        # Set pending breakpoint in utils.ml (not loaded yet)
        bp_id, is_pending = debugger.set_breakpoint(str(utils_ml), 1)
        assert is_pending, "Breakpoint should be pending initially"
        assert bp_id in debugger.pending_breakpoints

        # Start debugger (this installs import hook)
        debugger.start()

        try:
            # Add project path to sys.path for import
            sys.path.insert(0, str(runtime_import_project))

            # Import utils module - this should trigger the import hook
            import utils

            # Give hook time to process (it happens synchronously)
            # The hook should have:
            # 1. Detected the import
            # 2. Loaded utils.ml.map
            # 3. Activated the pending breakpoint

            # Verify breakpoint was activated
            assert bp_id not in debugger.pending_breakpoints, "Breakpoint should no longer be pending"
            assert bp_id in debugger.breakpoints, "Breakpoint should be active"

            # Verify source map was loaded
            assert str(utils_ml.resolve()) in debugger.loaded_source_maps

        finally:
            debugger.stop()
            # Clean up sys.path
            if str(runtime_import_project) in sys.path:
                sys.path.remove(str(runtime_import_project))

    def test_multiple_imports_activate_multiple_breakpoints(self, runtime_import_project):
        """Test that multiple module imports activate their respective breakpoints."""
        main_ml = runtime_import_project / "main.ml"
        utils_ml = runtime_import_project / "utils.ml"

        # Create an additional helper module
        helper_ml = runtime_import_project / "helper.ml"
        helper_ml.write_text("""function calculate(x) {
    return x * 2;
}
""", encoding='utf-8')

        # Transpile helper.ml
        transpiler = MLTranspiler()
        helper_source = helper_ml.read_text(encoding='utf-8')
        helper_code, helper_issues, helper_map_data = transpiler.transpile_to_python(
            helper_source,
            source_file=str(helper_ml),
            generate_source_maps=True,
            strict_security=False
        )

        if helper_code and helper_map_data:
            helper_py = helper_ml.with_suffix('.py')
            helper_py.write_text(helper_code, encoding='utf-8')
            helper_map = helper_ml.with_suffix('.ml.map')
            helper_map.write_text(json.dumps(helper_map_data, indent=2), encoding='utf-8')

        # Setup debugger
        ml_source = main_ml.read_text(encoding='utf-8')
        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False
        )

        source_map = EnhancedSourceMap()
        if "debugInfo" in source_map_data and "detailedMappings" in source_map_data["debugInfo"]:
            for mapping_dict in source_map_data["debugInfo"]["detailedMappings"]:
                gen = mapping_dict.get("generated", {})
                orig = mapping_dict.get("original", {})
                if orig:
                    source_map.add_mapping(
                        generated_line=gen.get("line", 1),
                        generated_column=gen.get("column", 0),
                        original_line=orig.get("line"),
                        original_column=orig.get("column"),
                        source_file=mapping_dict.get("source_file", str(main_ml)),
                        name=mapping_dict.get("name"),
                        node_type=mapping_dict.get("node_type")
                    )

        py_file = main_ml.with_suffix('.py')
        source_index = SourceMapIndex.from_source_map(source_map, str(py_file))

        debugger = MLDebugger(str(main_ml), source_index, python_code)

        # Set pending breakpoints in both modules
        bp_utils, is_pending_utils = debugger.set_breakpoint(str(utils_ml), 1)
        bp_helper, is_pending_helper = debugger.set_breakpoint(str(helper_ml), 1)

        assert is_pending_utils
        assert is_pending_helper

        # Start debugger
        debugger.start()

        try:
            sys.path.insert(0, str(runtime_import_project))

            # Import both modules
            import utils
            import helper

            # Both breakpoints should be activated
            assert bp_utils in debugger.breakpoints
            assert bp_helper in debugger.breakpoints
            assert bp_utils not in debugger.pending_breakpoints
            assert bp_helper not in debugger.pending_breakpoints

            # Both source maps should be loaded
            assert str(utils_ml.resolve()) in debugger.loaded_source_maps
            assert str(helper_ml.resolve()) in debugger.loaded_source_maps

        finally:
            debugger.stop()
            if str(runtime_import_project) in sys.path:
                sys.path.remove(str(runtime_import_project))
            # Clean up imports
            for mod in ['utils', 'helper']:
                if mod in sys.modules:
                    del sys.modules[mod]

    def test_import_hook_does_not_affect_non_ml_modules(self, runtime_import_project):
        """Test that import hook doesn't interfere with normal Python imports."""
        main_ml = runtime_import_project / "main.ml"

        # Setup debugger
        ml_source = main_ml.read_text(encoding='utf-8')
        transpiler = MLTranspiler()
        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False
        )

        source_map = EnhancedSourceMap()
        if "debugInfo" in source_map_data and "detailedMappings" in source_map_data["debugInfo"]:
            for mapping_dict in source_map_data["debugInfo"]["detailedMappings"]:
                gen = mapping_dict.get("generated", {})
                orig = mapping_dict.get("original", {})
                if orig:
                    source_map.add_mapping(
                        generated_line=gen.get("line", 1),
                        generated_column=gen.get("column", 0),
                        original_line=orig.get("line"),
                        original_column=orig.get("column"),
                        source_file=mapping_dict.get("source_file", str(main_ml)),
                        name=mapping_dict.get("name"),
                        node_type=mapping_dict.get("node_type")
                    )

        py_file = main_ml.with_suffix('.py')
        source_index = SourceMapIndex.from_source_map(source_map, str(py_file))

        debugger = MLDebugger(str(main_ml), source_index, python_code)

        # Start debugger
        debugger.start()

        try:
            # Import standard Python modules - should work normally
            import json
            import pathlib
            import collections

            # Should not affect debugger state
            assert len(debugger.loaded_source_maps) == 1  # Only main.ml

        finally:
            debugger.stop()

    def test_conditional_pending_breakpoint_activates_with_condition(self, runtime_import_project):
        """Test that conditional pending breakpoints preserve conditions when activated."""
        main_ml = runtime_import_project / "main.ml"
        utils_ml = runtime_import_project / "utils.ml"

        # Setup debugger
        ml_source = main_ml.read_text(encoding='utf-8')
        transpiler = MLTranspiler()
        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False
        )

        source_map = EnhancedSourceMap()
        if "debugInfo" in source_map_data and "detailedMappings" in source_map_data["debugInfo"]:
            for mapping_dict in source_map_data["debugInfo"]["detailedMappings"]:
                gen = mapping_dict.get("generated", {})
                orig = mapping_dict.get("original", {})
                if orig:
                    source_map.add_mapping(
                        generated_line=gen.get("line", 1),
                        generated_column=gen.get("column", 0),
                        original_line=orig.get("line"),
                        original_column=orig.get("column"),
                        source_file=mapping_dict.get("source_file", str(main_ml)),
                        name=mapping_dict.get("name"),
                        node_type=mapping_dict.get("node_type")
                    )

        py_file = main_ml.with_suffix('.py')
        source_index = SourceMapIndex.from_source_map(source_map, str(py_file))

        debugger = MLDebugger(str(main_ml), source_index, python_code)

        # Set conditional pending breakpoint
        condition = "a > 10"
        bp_id, is_pending = debugger.set_breakpoint(str(utils_ml), 1, condition=condition)
        assert is_pending

        # Start debugger
        debugger.start()

        try:
            sys.path.insert(0, str(runtime_import_project))

            # Import utils - should activate breakpoint
            import utils

            # Breakpoint should be active with condition preserved
            assert bp_id in debugger.breakpoints
            bp = debugger.breakpoints[bp_id]
            assert bp.condition == condition

        finally:
            debugger.stop()
            if str(runtime_import_project) in sys.path:
                sys.path.remove(str(runtime_import_project))
            if 'utils' in sys.modules:
                del sys.modules['utils']
