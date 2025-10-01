"""
Unit tests for enhanced_source_maps.py - Advanced source map generation.

Tests cover:
- SourceLocation dataclass and serialization
- SourceMapping dataclass with enhanced debugging info
- EnhancedSourceMap structure and JSON generation
- generate_enhanced_source_map() function
- AST node mapping
- Debug information generation
"""

import json

from mlpy.ml.codegen.enhanced_source_maps import (
    EnhancedSourceMap,
    SourceLocation,
    SourceMapping,
    generate_enhanced_source_map,
)
from mlpy.ml.grammar.ast_nodes import (
    AssignmentStatement,
    BinaryExpression,
    FunctionDefinition,
    Identifier,
    NumberLiteral,
    Parameter,
    Program,
    ReturnStatement,
    StringLiteral,
)


class TestSourceLocation:
    """Test SourceLocation dataclass."""

    def test_source_location_creation(self):
        """Test creating source location."""
        loc = SourceLocation(line=5, column=10, offset=100, length=20)

        assert loc.line == 5
        assert loc.column == 10
        assert loc.offset == 100
        assert loc.length == 20

    def test_source_location_minimal(self):
        """Test source location with minimal fields."""
        loc = SourceLocation(line=1, column=0)

        assert loc.line == 1
        assert loc.column == 0
        assert loc.offset == 0  # Default
        assert loc.length == 0  # Default

    def test_to_dict_conversion(self):
        """Test conversion to dictionary."""
        loc = SourceLocation(line=3, column=5, offset=50, length=15)
        result = loc.to_dict()

        assert isinstance(result, dict)
        assert result["line"] == 3
        assert result["column"] == 5
        assert result["offset"] == 50
        assert result["length"] == 15


class TestSourceMapping:
    """Test SourceMapping dataclass."""

    def test_source_mapping_creation(self):
        """Test creating source mapping."""
        generated = SourceLocation(line=10, column=0, offset=200, length=5)
        original = SourceLocation(line=1, column=0, offset=0, length=5)

        mapping = SourceMapping(
            generated=generated,
            original=original,
            source_file="test.ml",
            name="myVar",
            node_type="AssignmentStatement",
        )

        assert mapping.generated == generated
        assert mapping.original == original
        assert mapping.source_file == "test.ml"
        assert mapping.name == "myVar"
        assert mapping.node_type == "AssignmentStatement"

    def test_source_mapping_minimal(self):
        """Test source mapping with minimal fields."""
        generated = SourceLocation(line=1, column=0)

        mapping = SourceMapping(generated=generated)

        assert mapping.generated == generated
        assert mapping.original is None
        assert mapping.source_file is None
        assert mapping.name is None
        assert mapping.node_type is None

    def test_to_dict_conversion(self):
        """Test mapping to dictionary conversion."""
        generated = SourceLocation(line=5, column=4)
        original = SourceLocation(line=2, column=8)

        mapping = SourceMapping(
            generated=generated, original=original, source_file="app.ml", name="count"
        )

        result = mapping.to_dict()

        assert isinstance(result, dict)
        assert "generated" in result
        assert "original" in result
        assert result["source_file"] == "app.ml"
        assert result["name"] == "count"


class TestEnhancedSourceMap:
    """Test EnhancedSourceMap structure."""

    def test_enhanced_source_map_creation(self):
        """Test creating enhanced source map."""
        source_map = EnhancedSourceMap(
            version=3,
            sources=["test.ml"],
            names=["x", "y"],
        )

        assert source_map.version == 3
        assert "test.ml" in source_map.sources
        assert "x" in source_map.names

    def test_default_values(self):
        """Test enhanced source map with defaults."""
        source_map = EnhancedSourceMap()

        assert source_map.version == 3
        assert source_map.sources == []
        assert source_map.names == []
        assert source_map.mappings == []  # List of SourceMapping objects
        assert source_map.source_content == {}
        assert source_map.symbol_table == {}
        assert source_map.type_information == {}
        assert source_map.scope_information == []

    def test_add_source_method(self):
        """Test adding source files."""
        source_map = EnhancedSourceMap()

        idx = source_map.add_source("test.ml", "let x = 42")

        assert idx == 0
        assert "test.ml" in source_map.sources
        assert source_map.source_content["test.ml"] == "let x = 42"

    def test_add_name_method(self):
        """Test adding symbol names."""
        source_map = EnhancedSourceMap()

        idx1 = source_map.add_name("myVar")
        idx2 = source_map.add_name("myFunc")

        assert idx1 == 0
        assert idx2 == 1
        assert "myVar" in source_map.names
        assert "myFunc" in source_map.names

    def test_add_mapping_method(self):
        """Test adding source mappings."""
        source_map = EnhancedSourceMap()

        source_map.add_mapping(
            generated_line=10,
            generated_column=4,
            original_line=1,
            original_column=0,
            source_file="test.ml",
            name="x",
        )

        assert len(source_map.mappings) == 1
        assert source_map.mappings[0].generated.line == 10
        assert source_map.mappings[0].source_file == "test.ml"

    def test_to_json_conversion(self):
        """Test JSON serialization."""
        source_map = EnhancedSourceMap(
            version=3,
            sources=["test.ml"],
        )

        # Add a proper mapping
        source_map.add_mapping(
            generated_line=1,
            generated_column=0,
            original_line=1,
            original_column=0,
            source_file="test.ml",
        )

        json_str = source_map.to_json()

        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert "sourceMap" in parsed
        assert parsed["sourceMap"]["version"] == 3
        assert parsed["sourceMap"]["sources"] == ["test.ml"]


class TestGenerateEnhancedSourceMap:
    """Test generate_enhanced_source_map function."""

    def test_simple_program_mapping(self):
        """Test generating source map for simple program."""
        ast = Program([AssignmentStatement(target=Identifier("x"), value=NumberLiteral(42))])

        python_code = "x = 42"

        source_map = generate_enhanced_source_map(ast, python_code, "test.ml", "let x = 42")

        assert isinstance(source_map, dict)
        assert "sourceMap" in source_map
        assert source_map["sourceMap"]["version"] == 3

    def test_with_source_file(self):
        """Test source map with source file."""
        ast = Program([AssignmentStatement(target=Identifier("y"), value=StringLiteral("hello"))])

        python_code = 'y = "hello"'

        source_map = generate_enhanced_source_map(ast, python_code, "app.ml", 'let y = "hello"')

        assert source_map["sourceMap"]["sources"] == ["app.ml"]

    def test_without_ml_source(self):
        """Test source map generation without ML source."""
        ast = Program([AssignmentStatement(target=Identifier("z"), value=NumberLiteral(100))])

        python_code = "z = 100"

        source_map = generate_enhanced_source_map(ast, python_code, "test.ml", None)

        assert isinstance(source_map, dict)
        # Should still generate map even without ML source
        assert "sourceMap" in source_map

    def test_function_definition_mapping(self):
        """Test mapping for function definition."""
        ast = Program(
            [
                FunctionDefinition(
                    name="add",
                    parameters=[Parameter("a"), Parameter("b")],
                    body=[ReturnStatement(BinaryExpression(Identifier("a"), "+", Identifier("b")))],
                )
            ]
        )

        python_code = """def add(a, b):
    return a + b"""

        source_map = generate_enhanced_source_map(
            ast, python_code, "funcs.ml", "fn add(a, b) { return a + b; }"
        )

        assert "debugInfo" in source_map
        assert "detailedMappings" in source_map["debugInfo"]

    def test_json_serialization(self):
        """Test that generated map can be JSON serialized."""
        ast = Program([AssignmentStatement(target=Identifier("data"), value=StringLiteral("test"))])

        python_code = 'data = "test"'

        source_map = generate_enhanced_source_map(ast, python_code, "test.ml", 'let data = "test"')

        # Should be JSON serializable
        json_str = json.dumps(source_map)
        assert isinstance(json_str, str)

        # Should be deserializable
        parsed = json.loads(json_str)
        assert parsed["sourceMap"]["version"] == 3
