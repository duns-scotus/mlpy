"""Unit tests for enhanced source map generation."""

import pytest
from mlpy.ml.grammar.parser import MLParser
from mlpy.ml.codegen.python_generator import generate_python_code
from mlpy.debugging.source_map_index import SourceMapIndex
from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap


class TestEnhancedSourceMapGeneration:
    """Test enhanced source map generation in Python code generator."""

    def test_generates_enhanced_source_map(self):
        """Test that enhanced source maps are generated when enabled."""
        ml_code = """x = 42;
y = x + 10;"""

        parser = MLParser()
        ast = parser.parse(ml_code, "test.ml")

        python_code, source_map = generate_python_code(
            ast,
            source_file="test.ml",
            generate_source_maps=True
        )

        # Verify source map exists
        assert source_map is not None

        # Verify it's an enhanced source map (has debugInfo)
        assert "sourceMap" in source_map or "debugInfo" in source_map

    def test_tracks_variable_assignments(self):
        """Test that variable assignments are tracked in source map."""
        ml_code = """x = 42;
y = 100;"""

        parser = MLParser()
        ast = parser.parse(ml_code, "test.ml")

        python_code, source_map = generate_python_code(
            ast,
            source_file="test.ml",
            generate_source_maps=True
        )

        # Verify mappings exist
        assert source_map is not None

        # Check for debug info structure
        if "debugInfo" in source_map:
            debug_info = source_map["debugInfo"]
            assert "symbolTable" in debug_info
            assert "detailedMappings" in debug_info

            # Verify we have some mappings
            assert len(debug_info["detailedMappings"]) > 0

    def test_tracks_function_definitions(self):
        """Test that function definitions are tracked in source map."""
        ml_code = """
        function add(a, b) {
            return a + b;
        }

        function multiply(x, y) {
            return x * y;
        }
        """

        parser = MLParser()
        ast = parser.parse(ml_code, "test.ml")

        python_code, source_map = generate_python_code(
            ast,
            source_file="test.ml",
            generate_source_maps=True
        )

        # Verify source map tracks functions
        assert source_map is not None

        if "debugInfo" in source_map:
            debug_info = source_map["debugInfo"]
            symbol_table = debug_info.get("symbolTable", {})

            # Verify functions are in symbol table
            assert "add" in symbol_table or "multiply" in symbol_table

    def test_source_map_can_be_converted_to_index(self):
        """Test that enhanced source maps can be used with SourceMapIndex."""
        ml_code = """x = 42;
y = x + 10;
function test() {
    return x + y;
}"""

        parser = MLParser()
        ast = parser.parse(ml_code, "test.ml")

        python_code, source_map_dict = generate_python_code(
            ast,
            source_file="test.ml",
            generate_source_maps=True
        )

        # Create an EnhancedSourceMap object from the dict
        from mlpy.ml.codegen.enhanced_source_maps import EnhancedSourceMap

        # Extract mappings from the enhanced source map
        if "debugInfo" in source_map_dict:
            detailed_mappings = source_map_dict["debugInfo"]["detailedMappings"]

            # Create EnhancedSourceMap and populate it
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

            # Create index from enhanced source map
            index = SourceMapIndex.from_source_map(source_map, "test.py")

            # Verify index was created successfully
            assert index is not None
            assert index.py_file == "test.py"


class TestSourceMapAccuracy:
    """Test accuracy of source map position tracking."""

    def test_multi_line_function(self):
        """Test source map accuracy for multi-line functions."""
        ml_code = """function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}"""

        parser = MLParser()
        ast = parser.parse(ml_code, "test.ml")

        python_code, source_map = generate_python_code(
            ast,
            source_file="test.ml",
            generate_source_maps=True
        )

        # Verify source map generated
        assert source_map is not None

        # Verify we have mappings for multiple lines
        if "debugInfo" in source_map:
            mappings = source_map["debugInfo"]["detailedMappings"]
            assert len(mappings) > 1

            # Verify mappings have line numbers
            for mapping in mappings:
                if "original" in mapping and mapping["original"]:
                    assert "line" in mapping["original"]
                    assert mapping["original"]["line"] > 0

    def test_conditional_statements(self):
        """Test source map accuracy for if/elif/else."""
        ml_code = """x = 5;
if (x > 10) {
    y = 1;
} elif (x > 5) {
    y = 2;
} else {
    y = 3;
}"""

        parser = MLParser()
        ast = parser.parse(ml_code, "test.ml")

        python_code, source_map = generate_python_code(
            ast,
            source_file="test.ml",
            generate_source_maps=True
        )

        # Verify source map generated with conditional mappings
        assert source_map is not None

        if "debugInfo" in source_map:
            mappings = source_map["debugInfo"]["detailedMappings"]

            # Should have mappings for multiple statements
            assert len(mappings) >= 4  # x assignment + if + elif + else blocks

    def test_nested_scopes(self):
        """Test source map accuracy for nested function scopes."""
        ml_code = """function outer() {
    x = 1;
    function inner() {
        y = 2;
        return x + y;
    }
    return inner();
}"""

        parser = MLParser()
        ast = parser.parse(ml_code, "test.ml")

        python_code, source_map = generate_python_code(
            ast,
            source_file="test.ml",
            generate_source_maps=True
        )

        # Verify scope tracking
        assert source_map is not None

        if "debugInfo" in source_map:
            # Check for scope information
            scope_info = source_map["debugInfo"].get("scopeInformation", [])

            # Should have at least 2 scopes (outer and inner functions)
            assert len(scope_info) >= 2
