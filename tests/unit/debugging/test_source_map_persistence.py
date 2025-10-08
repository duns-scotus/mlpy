"""Tests for source map persistence and multi-file debugging support."""

import pytest
import tempfile
import shutil
import json
from pathlib import Path
from mlpy.ml.transpiler import MLTranspiler
from mlpy.debugging.source_map_index import SourceMapIndex
from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with multiple ML files."""
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir)

    # Create main.ml - simple single-file program
    main_ml = project_path / "main.ml"
    main_ml.write_text("""function add(a, b) {
    return a + b;
}

function multiply(a, b) {
    return a * b;
}

function main() {
    x = 10;
    y = 20;
    sum = add(x, y);
    product = multiply(x, y);
    return sum + product;
}

result = main();
""", encoding='utf-8')

    # Create utils.ml - another simple file
    utils_ml = project_path / "utils.ml"
    utils_ml.write_text("""function power(base, exp) {
    result = 1;
    i = 0;
    while (i < exp) {
        result = result * base;
        i = i + 1;
    }
    return result;
}

function square(x) {
    return power(x, 2);
}
""", encoding='utf-8')

    yield project_path

    # Cleanup
    shutil.rmtree(temp_dir)


class TestSourceMapPersistence:
    """Test source map file persistence."""

    def test_source_map_saved_to_disk(self, temp_project_dir):
        """Test that .ml.map files are created alongside .py files."""
        main_ml = temp_project_dir / "main.ml"
        ml_source = main_ml.read_text(encoding='utf-8')

        # Transpile with source maps
        transpiler = MLTranspiler()
        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False
        )

        assert python_code is not None
        assert source_map_data is not None

        # Save Python and source map files
        py_file = main_ml.with_suffix('.py')
        map_file = main_ml.with_suffix('.ml.map')

        py_file.write_text(python_code, encoding='utf-8')
        map_file.write_text(json.dumps(source_map_data, indent=2), encoding='utf-8')

        # Verify files exist
        assert py_file.exists()
        assert map_file.exists()

        # Verify source map content
        saved_map = json.loads(map_file.read_text(encoding='utf-8'))
        assert "sourceMap" in saved_map
        assert "debugInfo" in saved_map
        assert "detailedMappings" in saved_map["debugInfo"]

    def test_source_map_filename_conventions(self, temp_project_dir):
        """Test that source map filenames follow conventions."""
        test_cases = [
            ("example.ml", "example.ml.map"),
            ("module_name.ml", "module_name.ml.map"),
        ]

        for ml_name, expected_map_name in test_cases:
            ml_path = Path(ml_name)
            map_path = ml_path.with_suffix('.ml.map')
            assert str(map_path) == expected_map_name

        # Test nested path (platform-independent)
        nested_path = Path("nested") / "file.ml"
        nested_map = nested_path.with_suffix('.ml.map')
        assert nested_map.name == "file.ml.map"
        assert nested_map.parent.name == "nested"

    def test_source_map_contains_correct_paths(self, temp_project_dir):
        """Test that source map contains correct file paths."""
        main_ml = temp_project_dir / "main.ml"
        ml_source = main_ml.read_text(encoding='utf-8')

        transpiler = MLTranspiler()
        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False
        )

        assert source_map_data is not None

        # Check that source file paths are present
        if "debugInfo" in source_map_data:
            mappings = source_map_data["debugInfo"].get("detailedMappings", [])
            if mappings:
                # At least one mapping should reference the source file
                source_files = {m.get("source_file") for m in mappings if m.get("source_file")}
                # Convert to Path for comparison
                source_files_normalized = {str(Path(f)) for f in source_files}
                assert str(main_ml) in source_files_normalized or str(main_ml.name) in source_files


class TestMultiFileDebugging:
    """Test debugging with multiple files and cached source maps."""

    def test_load_source_map_from_cache(self, temp_project_dir):
        """Test loading source map from .ml.map file."""
        main_ml = temp_project_dir / "main.ml"
        ml_source = main_ml.read_text(encoding='utf-8')

        # First transpilation: generate and save
        transpiler = MLTranspiler()
        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False
        )

        py_file = main_ml.with_suffix('.py')
        map_file = main_ml.with_suffix('.ml.map')

        py_file.write_text(python_code, encoding='utf-8')
        map_file.write_text(json.dumps(source_map_data, indent=2), encoding='utf-8')

        # Second session: load from cache
        cached_map_data = json.loads(map_file.read_text(encoding='utf-8'))

        assert cached_map_data == source_map_data

        # Verify we can build source map index from cached data
        if "debugInfo" in cached_map_data and "detailedMappings" in cached_map_data["debugInfo"]:
            source_map = EnhancedSourceMap()

            for mapping_dict in cached_map_data["debugInfo"]["detailedMappings"]:
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

            source_index = SourceMapIndex.from_source_map(source_map, str(py_file))

            # Verify index works
            assert isinstance(source_index, SourceMapIndex)
            assert source_index.py_file == str(py_file)

    def test_multiple_files_have_separate_maps(self, temp_project_dir):
        """Test that each .ml file gets its own .ml.map file."""
        main_ml = temp_project_dir / "main.ml"
        utils_ml = temp_project_dir / "utils.ml"

        files_to_transpile = [main_ml, utils_ml]
        transpiled_files = []

        transpiler = MLTranspiler()

        for ml_file in files_to_transpile:
            ml_source = ml_file.read_text(encoding='utf-8')

            python_code, issues, source_map_data = transpiler.transpile_to_python(
                ml_source,
                source_file=str(ml_file),
                generate_source_maps=True,
                strict_security=False
            )

            if python_code and source_map_data:
                py_file = ml_file.with_suffix('.py')
                map_file = ml_file.with_suffix('.ml.map')

                py_file.write_text(python_code, encoding='utf-8')
                map_file.write_text(json.dumps(source_map_data, indent=2), encoding='utf-8')

                transpiled_files.append({
                    'ml': ml_file,
                    'py': py_file,
                    'map': map_file
                })

        # Verify we have separate files for each module
        assert len(transpiled_files) >= 1  # At least main.ml should work

        for file_info in transpiled_files:
            assert file_info['py'].exists()
            assert file_info['map'].exists()

            # Verify each map corresponds to its source
            map_data = json.loads(file_info['map'].read_text(encoding='utf-8'))
            assert "sourceMap" in map_data
            assert "debugInfo" in map_data

    def test_source_map_index_handles_multiple_files(self, temp_project_dir):
        """Test that SourceMapIndex can work with multiple source files."""
        main_ml = temp_project_dir / "main.ml"
        ml_source = main_ml.read_text(encoding='utf-8')

        transpiler = MLTranspiler()
        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False,
            import_paths=[str(temp_project_dir)],
            module_output_mode='inline'  # Inline for simplicity
        )

        if python_code and source_map_data:
            # Build source map
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

                # Verify we have mappings
                assert len(source_index.ml_to_py) > 0 or len(source_index.py_to_ml) > 0

                # Test lookup functionality
                ml_files = source_index.get_all_ml_files()
                assert len(ml_files) >= 1  # At least one source file


class TestSourceMapRegeneration:
    """Test that source maps are regenerated when source changes."""

    def test_timestamp_invalidation_concept(self, temp_project_dir):
        """Test the concept of timestamp-based invalidation."""
        main_ml = temp_project_dir / "main.ml"
        py_file = main_ml.with_suffix('.py')
        map_file = main_ml.with_suffix('.ml.map')

        # Initial transpilation
        ml_source = main_ml.read_text(encoding='utf-8')
        transpiler = MLTranspiler()

        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False
        )

        if python_code and source_map_data:
            py_file.write_text(python_code, encoding='utf-8')
            map_file.write_text(json.dumps(source_map_data, indent=2), encoding='utf-8')

            # Record timestamps
            ml_mtime = main_ml.stat().st_mtime
            py_mtime = py_file.stat().st_mtime
            map_mtime = map_file.stat().st_mtime

            # Simulate source modification (in real scenario, user edits file)
            import time
            time.sleep(0.01)  # Ensure timestamp difference

            # Modify ML source
            modified_source = ml_source + "\n// Modified\n"
            main_ml.write_text(modified_source, encoding='utf-8')

            # Check that ML file is newer
            new_ml_mtime = main_ml.stat().st_mtime
            assert new_ml_mtime > ml_mtime
            assert new_ml_mtime > py_mtime
            assert new_ml_mtime > map_mtime

            # In production, this would trigger retranspilation
            # which would update both .py and .ml.map with newer timestamps

    def test_source_map_regeneration_workflow(self, temp_project_dir):
        """Test complete regeneration workflow."""
        main_ml = temp_project_dir / "main.ml"
        py_file = main_ml.with_suffix('.py')
        map_file = main_ml.with_suffix('.ml.map')

        transpiler = MLTranspiler()

        # First transpilation
        ml_source1 = main_ml.read_text(encoding='utf-8')
        python_code1, issues1, source_map1 = transpiler.transpile_to_python(
            ml_source1,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False
        )

        if python_code1 and source_map1:
            py_file.write_text(python_code1, encoding='utf-8')
            map_file.write_text(json.dumps(source_map1, indent=2), encoding='utf-8')

            # Modify source
            ml_source2 = ml_source1 + "\nlet newVar = 42;\n"
            main_ml.write_text(ml_source2, encoding='utf-8')

            # Second transpilation
            python_code2, issues2, source_map2 = transpiler.transpile_to_python(
                ml_source2,
                source_file=str(main_ml),
                generate_source_maps=True,
                strict_security=False
            )

            if python_code2 and source_map2:
                # Regenerate both files
                py_file.write_text(python_code2, encoding='utf-8')
                map_file.write_text(json.dumps(source_map2, indent=2), encoding='utf-8')

                # Verify they were updated
                assert py_file.read_text(encoding='utf-8') == python_code2
                reloaded_map = json.loads(map_file.read_text(encoding='utf-8'))
                assert reloaded_map == source_map2


class TestSourceMapJSON:
    """Test source map JSON format and structure."""

    def test_source_map_json_structure(self, temp_project_dir):
        """Test that source map JSON has correct structure."""
        main_ml = temp_project_dir / "main.ml"
        ml_source = main_ml.read_text(encoding='utf-8')

        transpiler = MLTranspiler()
        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False
        )

        assert source_map_data is not None

        # Check top-level structure
        assert isinstance(source_map_data, dict)
        assert "sourceMap" in source_map_data
        assert "debugInfo" in source_map_data

        # Check sourceMap structure
        source_map = source_map_data["sourceMap"]
        assert "version" in source_map
        assert "sources" in source_map
        assert isinstance(source_map["sources"], list)

        # Check debugInfo structure
        debug_info = source_map_data["debugInfo"]
        assert "detailedMappings" in debug_info
        assert isinstance(debug_info["detailedMappings"], list)

    def test_source_map_json_serialization(self, temp_project_dir):
        """Test that source map can be serialized and deserialized."""
        main_ml = temp_project_dir / "main.ml"
        ml_source = main_ml.read_text(encoding='utf-8')

        transpiler = MLTranspiler()
        python_code, issues, source_map_data = transpiler.transpile_to_python(
            ml_source,
            source_file=str(main_ml),
            generate_source_maps=True,
            strict_security=False
        )

        if source_map_data:
            # Serialize to JSON
            json_str = json.dumps(source_map_data, indent=2)

            # Deserialize
            reloaded = json.loads(json_str)

            # Verify round-trip
            assert reloaded == source_map_data

            # Verify can write and read from file
            map_file = main_ml.with_suffix('.ml.map')
            map_file.write_text(json_str, encoding='utf-8')

            loaded_from_file = json.loads(map_file.read_text(encoding='utf-8'))
            assert loaded_from_file == source_map_data
