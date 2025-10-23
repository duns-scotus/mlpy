"""Tests for multi-file debugging with deferred breakpoint resolution."""

import pytest
import tempfile
import shutil
import json
from pathlib import Path
from mlpy.ml.transpiler import MLTranspiler
from mlpy.debugging.debugger import MLDebugger, PendingBreakpoint, Breakpoint
from mlpy.debugging.source_map_index import SourceMapIndex
from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap


@pytest.fixture
def multi_file_project():
    """Create a temporary multi-file ML project with transpiled files and source maps."""
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir)

    # Create main.ml
    main_ml = project_path / "main.ml"
    main_ml.write_text("""function main() {
    x = 10;
    y = 20;
    result = add(x, y);
    return result;
}

function add(a, b) {
    return a + b;
}

output = main();
""", encoding='utf-8')

    # Create utils.ml
    utils_ml = project_path / "utils.ml"
    utils_ml.write_text("""function multiply(a, b) {
    result = 1;
    i = 0;
    while (i < b) {
        result = result + a;
        i = i + 1;
    }
    return result;
}

function power(base, exp) {
    result = 1;
    i = 0;
    while (i < exp) {
        result = multiply(result, base);
        i = i + 1;
    }
    return result;
}
""", encoding='utf-8')

    # Transpile both files and save source maps
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
    shutil.rmtree(temp_dir)


class TestPendingBreakpoints:
    """Test pending breakpoint creation and resolution."""

    def test_pending_breakpoint_creation(self, multi_file_project):
        """Test that breakpoints are pending when file not loaded."""
        main_ml = multi_file_project / "main.ml"
        utils_ml = multi_file_project / "utils.ml"

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

        # Set breakpoint in main.ml - should be active (line 1 is function definition)
        bp_main = debugger.set_breakpoint(str(main_ml), 1)
        assert isinstance(bp_main, Breakpoint), "Breakpoint in loaded file should be active"
        assert bp_main.id in debugger.breakpoints
        assert bp_main.id not in debugger.pending_breakpoints

        # Set breakpoint in utils.ml (not loaded) - should be pending
        bp_utils = debugger.set_breakpoint(str(utils_ml), 1)
        assert isinstance(bp_utils, PendingBreakpoint), "Breakpoint in unloaded file should be pending"
        assert bp_utils.id in debugger.pending_breakpoints
        assert bp_utils.id not in debugger.breakpoints

    def test_pending_breakpoint_activation(self, multi_file_project):
        """Test that pending breakpoints activate when source map loads."""
        main_ml = multi_file_project / "main.ml"
        utils_ml = multi_file_project / "utils.ml"

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

        # Set pending breakpoint in utils.ml
        bp = debugger.set_breakpoint(str(utils_ml), 1)
        assert isinstance(bp, PendingBreakpoint)
        bp_id = bp.id
        assert bp_id in debugger.pending_breakpoints

        # Load source map for utils.ml
        success = debugger.load_source_map_for_file(str(utils_ml))
        assert success, "Source map should load successfully"

        # Breakpoint should now be activated
        assert bp_id not in debugger.pending_breakpoints, "Breakpoint should no longer be pending"
        assert bp_id in debugger.breakpoints, "Breakpoint should be active"

        # Verify breakpoint has correct properties
        bp_active = debugger.breakpoints[bp_id]
        assert bp_active.ml_file == str(utils_ml.resolve())
        assert bp_active.ml_line == 1
        assert len(bp_active.py_lines) > 0

    def test_conditional_pending_breakpoint(self, multi_file_project):
        """Test that conditions are preserved when pending breakpoints activate."""
        main_ml = multi_file_project / "main.ml"
        utils_ml = multi_file_project / "utils.ml"

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
        condition = "i > 5"
        bp = debugger.set_breakpoint(str(utils_ml), 1, condition=condition)
        assert isinstance(bp, PendingBreakpoint)
        bp_id = bp.id

        # Verify pending breakpoint has condition
        pending_bp = debugger.pending_breakpoints[bp_id]
        assert pending_bp.condition == condition

        # Load source map
        debugger.load_source_map_for_file(str(utils_ml))

        # Verify activated breakpoint preserved condition
        assert bp_id in debugger.breakpoints
        bp_active = debugger.breakpoints[bp_id]
        assert bp_active.condition == condition

    def test_delete_pending_breakpoint(self, multi_file_project):
        """Test deleting pending breakpoints."""
        main_ml = multi_file_project / "main.ml"
        utils_ml = multi_file_project / "utils.ml"

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

        # Set pending breakpoint
        bp = debugger.set_breakpoint(str(utils_ml), 1)
        assert isinstance(bp, PendingBreakpoint)
        bp_id = bp.id
        assert bp_id in debugger.pending_breakpoints

        # Delete pending breakpoint
        success = debugger.delete_breakpoint(bp_id)
        assert success
        assert bp_id not in debugger.pending_breakpoints
        assert bp_id not in debugger.breakpoints

    def test_get_all_breakpoints(self, multi_file_project):
        """Test that get_all_breakpoints returns both active and pending breakpoints."""
        main_ml = multi_file_project / "main.ml"
        utils_ml = multi_file_project / "utils.ml"

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

        # Set active breakpoint in main.ml
        bp_active = debugger.set_breakpoint(str(main_ml), 1)
        assert isinstance(bp_active, Breakpoint)
        bp_id_active = bp_active.id

        # Set pending breakpoint in utils.ml
        bp_pending = debugger.set_breakpoint(str(utils_ml), 1)
        assert isinstance(bp_pending, PendingBreakpoint)
        bp_id_pending = bp_pending.id

        # Get all breakpoints
        all_breakpoints = debugger.get_all_breakpoints()

        assert len(all_breakpoints) == 2
        assert bp_id_active in all_breakpoints
        assert bp_id_pending in all_breakpoints

        # Check statuses
        ml_file_active, ml_line_active, status_active, condition_active, enabled_active = all_breakpoints[bp_id_active]
        assert status_active == "active"

        ml_file_pending, ml_line_pending, status_pending, condition_pending, enabled_pending = all_breakpoints[bp_id_pending]
        assert status_pending == "pending"


class TestMultiFileSourceMapLoading:
    """Test on-demand source map loading from .ml.map files."""

    def test_load_source_map_from_disk(self, multi_file_project):
        """Test loading source map from .ml.map file."""
        main_ml = multi_file_project / "main.ml"
        utils_ml = multi_file_project / "utils.ml"

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

        # Initially, utils.ml should not be loaded
        assert str(utils_ml.resolve()) not in debugger.loaded_source_maps

        # Load source map for utils.ml
        success = debugger.load_source_map_for_file(str(utils_ml))
        assert success

        # Now utils.ml should be loaded
        assert str(utils_ml.resolve()) in debugger.loaded_source_maps

        # Verify we can set active breakpoints in utils.ml
        bp = debugger.set_breakpoint(str(utils_ml), 1)
        assert isinstance(bp, Breakpoint)  # Should be active now
        assert bp.id in debugger.breakpoints

    def test_load_nonexistent_source_map(self, multi_file_project):
        """Test that loading nonexistent source map returns False."""
        main_ml = multi_file_project / "main.ml"

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

        # Try to load nonexistent file
        fake_file = multi_file_project / "nonexistent.ml"
        success = debugger.load_source_map_for_file(str(fake_file))
        assert not success
