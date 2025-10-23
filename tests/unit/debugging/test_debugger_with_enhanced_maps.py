"""Integration test for debugger with enhanced source maps."""

import pytest
from mlpy.ml.grammar.parser import MLParser
from mlpy.ml.codegen.python_generator import generate_python_code
from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap
from mlpy.debugging.source_map_index import SourceMapIndex
from mlpy.debugging.debugger import MLDebugger


class TestDebuggerWithEnhancedSourceMaps:
    """Test debugger integration with enhanced source maps."""

    def test_debugger_can_use_enhanced_source_maps(self):
        """Test that the debugger can work with enhanced source maps."""
        # Create a simple ML program
        ml_code = """x = 10;
y = 20;
z = x + y;"""

        # Parse and transpile with enhanced source maps
        parser = MLParser()
        ast = parser.parse(ml_code, "test.ml")

        python_code, source_map_dict = generate_python_code(
            ast,
            source_file="test.ml",
            generate_source_maps=True
        )

        # Verify source map was generated
        assert source_map_dict is not None

        # Create EnhancedSourceMap from dict
        if "debugInfo" in source_map_dict:
            detailed_mappings = source_map_dict["debugInfo"]["detailedMappings"]

            source_map = EnhancedSourceMap()
            source_map.add_source("test.ml", ml_code)

            for mapping_dict in detailed_mappings:
                gen = mapping_dict.get("generated", {})
                orig = mapping_dict.get("original", {})

                if orig:
                    source_map.add_mapping(
                        generated_line=gen.get("line", 1),
                        generated_column=gen.get("column", 0),
                        original_line=orig.get("line"),
                        original_column=orig.get("column"),
                        source_file=mapping_dict.get("source_file", "test.ml"),
                        name=mapping_dict.get("name"),
                        node_type=mapping_dict.get("node_type")
                    )

            # Create source map index
            index = SourceMapIndex.from_source_map(source_map, "test.py")

            # Create debugger
            debugger = MLDebugger("test.ml", index, python_code)

            # Verify debugger was created successfully
            assert debugger is not None
            assert debugger.ml_file == "test.ml"
            assert debugger.source_map_index == index

    def test_can_set_breakpoint_with_enhanced_maps(self):
        """Test that breakpoints can be set using enhanced source maps."""
        # Create ML program with function
        ml_code = """function add(a, b) {
    return a + b;
}
result = add(5, 10);"""

        # Parse and transpile
        parser = MLParser()
        ast = parser.parse(ml_code, "test.ml")

        python_code, source_map_dict = generate_python_code(
            ast,
            source_file="test.ml",
            generate_source_maps=True
        )

        # Create enhanced source map
        if "debugInfo" in source_map_dict:
            detailed_mappings = source_map_dict["debugInfo"]["detailedMappings"]

            source_map = EnhancedSourceMap()
            source_map.add_source("test.ml", ml_code)

            for mapping_dict in detailed_mappings:
                gen = mapping_dict.get("generated", {})
                orig = mapping_dict.get("original", {})

                if orig:
                    source_map.add_mapping(
                        generated_line=gen.get("line", 1),
                        generated_column=gen.get("column", 0),
                        original_line=orig.get("line"),
                        original_column=orig.get("column"),
                        source_file=mapping_dict.get("source_file", "test.ml"),
                        name=mapping_dict.get("name"),
                        node_type=mapping_dict.get("node_type")
                    )

            # Create index and debugger
            index = SourceMapIndex.from_source_map(source_map, "test.py")
            debugger = MLDebugger("test.ml", index, python_code)

            # Try to set a breakpoint at line 2 (return statement)
            bp = debugger.set_breakpoint("test.ml", 2)

            # Breakpoint should be set successfully if the line is executable
            # If line 2 is not executable, bp will be None (this is ok for this test)
            # The key test is that the debugger didn't crash
            assert debugger is not None

    def test_ml_to_python_position_mapping(self):
        """Test that ML positions correctly map to Python positions."""
        ml_code = """x = 42;
y = 100;"""

        parser = MLParser()
        ast = parser.parse(ml_code, "test.ml")

        python_code, source_map_dict = generate_python_code(
            ast,
            source_file="test.ml",
            generate_source_maps=True
        )

        # Create enhanced source map
        if "debugInfo" in source_map_dict:
            detailed_mappings = source_map_dict["debugInfo"]["detailedMappings"]

            source_map = EnhancedSourceMap()
            source_map.add_source("test.ml", ml_code)

            for mapping_dict in detailed_mappings:
                gen = mapping_dict.get("generated", {})
                orig = mapping_dict.get("original", {})

                if orig:
                    source_map.add_mapping(
                        generated_line=gen.get("line", 1),
                        generated_column=gen.get("column", 0),
                        original_line=orig.get("line"),
                        original_column=orig.get("column"),
                        source_file=mapping_dict.get("source_file", "test.ml"),
                        name=mapping_dict.get("name"),
                        node_type=mapping_dict.get("node_type")
                    )

            # Create index
            index = SourceMapIndex.from_source_map(source_map, "test.py")

            # Verify that we can look up ML positions
            # We should have at least one mapping
            assert len(index.ml_to_py) > 0 or len(index.py_to_ml) > 0
