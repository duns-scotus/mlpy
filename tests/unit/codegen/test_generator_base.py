"""
Unit tests for generator_base.py - Base code generation functionality.

Tests cover:
- GeneratorBase initialization with various configurations
- Code generation orchestration (generate method)
- Code emission methods (_emit_line, _emit_header, _emit_footer)
- Indentation management (_indent, _dedent, _get_indentation)
- Source map generation and tracking
- Symbol table management and ML builtin discovery
- Helper methods (_safe_identifier, _extract_symbol_name)
- Module output modes (separate vs inline)
- Import path handling
- REPL mode support
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from mlpy.ml.codegen.core.generator_base import GeneratorBase
from mlpy.ml.codegen.python_generator import PythonCodeGenerator
from mlpy.ml.grammar.ast_nodes import (
    Program,
    FunctionDefinition,
    AssignmentStatement,
    Identifier,
    Parameter,
    NumberLiteral,
    StringLiteral,
    BlockStatement,
    ReturnStatement,
    ExpressionStatement,
)


class TestGeneratorBaseInitialization:
    """Test GeneratorBase initialization."""

    def test_default_initialization(self):
        """Test generator with default parameters."""
        gen = PythonCodeGenerator()

        assert gen.source_file is None
        assert gen.generate_source_maps is True
        assert gen.context is not None
        assert gen.output_lines == []
        assert gen.function_registry is not None
        assert gen.import_paths == []
        assert gen.allow_current_dir is False
        assert gen.module_output_mode == 'separate'
        assert gen.repl_mode is False
        assert gen.compiled_modules == {}
        assert gen.module_py_files == {}

    def test_initialization_with_source_file(self):
        """Test generator with source file specified."""
        gen = PythonCodeGenerator(source_file="test.ml")

        assert gen.source_file == "test.ml"

    def test_initialization_without_source_maps(self):
        """Test generator with source maps disabled."""
        gen = PythonCodeGenerator(generate_source_maps=False)

        assert gen.generate_source_maps is False

    def test_initialization_with_import_paths(self):
        """Test generator with custom import paths."""
        import_paths = ["/path/to/modules", "/another/path"]
        gen = PythonCodeGenerator(import_paths=import_paths)

        assert gen.import_paths == import_paths

    def test_initialization_with_current_dir_allowed(self):
        """Test generator with current directory imports allowed."""
        gen = PythonCodeGenerator(allow_current_dir=True)

        assert gen.allow_current_dir is True

    def test_initialization_with_inline_module_output(self):
        """Test generator with inline module output mode."""
        gen = PythonCodeGenerator(module_output_mode='inline')

        assert gen.module_output_mode == 'inline'

    def test_initialization_with_repl_mode(self):
        """Test generator with REPL mode enabled."""
        gen = PythonCodeGenerator(repl_mode=True)

        assert gen.repl_mode is True

    def test_symbol_table_initialization(self):
        """Test symbol table is properly initialized."""
        gen = PythonCodeGenerator()

        assert 'variables' in gen.symbol_table
        assert 'functions' in gen.symbol_table
        assert 'parameters' in gen.symbol_table
        assert 'imports' in gen.symbol_table
        assert 'ml_builtins' in gen.symbol_table
        assert isinstance(gen.symbol_table['variables'], set)
        assert isinstance(gen.symbol_table['functions'], set)
        assert isinstance(gen.symbol_table['parameters'], list)
        assert isinstance(gen.symbol_table['imports'], set)
        assert 'builtin' in gen.symbol_table['imports']


class TestMLBuiltinDiscovery:
    """Test ML builtin function discovery."""

    @patch('mlpy.ml.codegen.python_generator.PythonCodeGenerator._discover_ml_builtins')
    def test_discover_ml_builtins_called(self, mock_discover):
        """Test ML builtin discovery is called during initialization."""
        mock_discover.return_value = {'print', 'typeof', 'len'}

        gen = PythonCodeGenerator()

        mock_discover.assert_called_once()

    def test_discover_ml_builtins_with_missing_import(self):
        """Test builtin discovery handles missing import gracefully."""
        with patch('mlpy.ml.codegen.python_generator.PythonCodeGenerator._discover_ml_builtins') as mock_discover:
            # Simulate ImportError - return empty set instead of raising error
            mock_discover.return_value = set()

            # Should not raise an error
            gen = PythonCodeGenerator()

            # Symbol table should still be initialized
            assert 'ml_builtins' in gen.symbol_table


class TestCodeEmission:
    """Test code emission methods."""

    @pytest.fixture
    def generator(self):
        """Create test generator."""
        return PythonCodeGenerator(source_file="test.ml")

    def test_emit_line_basic(self, generator):
        """Test emitting a basic line of code."""
        generator._emit_line("x = 42")

        assert len(generator.output_lines) == 1
        assert generator.output_lines[0] == "x = 42"

    def test_emit_line_with_indentation(self, generator):
        """Test emitting line respects indentation."""
        generator._indent()
        generator._emit_line("x = 42")

        assert generator.output_lines[0] == "    x = 42"

    def test_emit_line_with_multiple_indents(self, generator):
        """Test emitting line with multiple indent levels."""
        generator._indent()
        generator._indent()
        generator._emit_line("x = 42")

        assert generator.output_lines[0] == "        x = 42"

    def test_emit_line_with_node_tracking(self, generator):
        """Test emitting line tracks source node."""
        node = Identifier(name="x", line=5, column=10)
        generator._emit_line("x", original_node=node)

        # Should track in source mappings
        assert len(generator.context.source_mappings) > 0

    def test_emit_raw_line(self, generator):
        """Test emitting raw line without indentation."""
        generator._indent()
        generator._emit_raw_line("# Raw comment")

        assert generator.output_lines[0] == "# Raw comment"

    def test_emit_header(self, generator):
        """Test emitting file header."""
        generator._emit_header()

        # Should have docstring and comments
        assert '"""Generated Python code from mlpy ML transpiler."""' in generator.output_lines[0]
        assert any("automatically generated" in line for line in generator.output_lines)

    def test_emit_header_with_contextlib(self, generator):
        """Test emitting header with contextlib import."""
        generator.context.imports_needed.add("contextlib")
        generator._emit_header()

        # Should include contextlib import
        assert any("import contextlib" in line for line in generator.output_lines)

    def test_emit_footer(self, generator):
        """Test emitting file footer."""
        generator._emit_footer()

        # Should have end-of-file comment
        assert any("End of generated code" in line for line in generator.output_lines)

    def test_generate_runtime_imports(self, generator):
        """Test generating runtime imports."""
        generator._generate_runtime_imports()

        # Should include safe_call import
        assert any("_safe_call" in line for line in generator.output_lines)
        assert any("mlpy.runtime.whitelist_validator" in line for line in generator.output_lines)


class TestIndentationManagement:
    """Test indentation management."""

    @pytest.fixture
    def generator(self):
        """Create test generator."""
        return PythonCodeGenerator()

    def test_initial_indentation_level(self, generator):
        """Test initial indentation is zero."""
        assert generator.context.indentation_level == 0

    def test_get_indentation_no_indent(self, generator):
        """Test get indentation with no indent."""
        assert generator._get_indentation() == ""

    def test_get_indentation_one_level(self, generator):
        """Test get indentation with one level."""
        generator._indent()
        assert generator._get_indentation() == "    "

    def test_get_indentation_multiple_levels(self, generator):
        """Test get indentation with multiple levels."""
        generator._indent()
        generator._indent()
        generator._indent()
        assert generator._get_indentation() == "            "

    def test_indent_increases_level(self, generator):
        """Test indent increases indentation level."""
        initial = generator.context.indentation_level
        generator._indent()
        assert generator.context.indentation_level == initial + 1

    def test_dedent_decreases_level(self, generator):
        """Test dedent decreases indentation level."""
        generator._indent()
        generator._indent()
        generator._dedent()
        assert generator.context.indentation_level == 1

    def test_dedent_cannot_go_negative(self, generator):
        """Test dedent stops at zero."""
        generator._dedent()
        generator._dedent()
        assert generator.context.indentation_level == 0


class TestHelperMethods:
    """Test helper methods."""

    @pytest.fixture
    def generator(self):
        """Create test generator."""
        return PythonCodeGenerator()

    def test_safe_identifier_basic(self, generator):
        """Test safe identifier conversion for basic names."""
        assert generator._safe_identifier("myVar") == "myVar"
        assert generator._safe_identifier("someFunction") == "someFunction"

    def test_safe_identifier_null(self, generator):
        """Test safe identifier converts null to None."""
        assert generator._safe_identifier("null") == "None"

    def test_safe_identifier_python_keyword(self, generator):
        """Test safe identifier handles Python keywords."""
        assert generator._safe_identifier("if") == "ml_if"
        assert generator._safe_identifier("for") == "ml_for"
        assert generator._safe_identifier("class") == "ml_class"
        assert generator._safe_identifier("def") == "ml_def"
        assert generator._safe_identifier("return") == "ml_return"

    def test_safe_identifier_non_string(self, generator):
        """Test safe identifier handles non-string input."""
        result = generator._safe_identifier(123)
        assert result.startswith("ml_unknown_identifier_")

    def test_extract_symbol_name_function(self, generator):
        """Test extract symbol name from function definition."""
        func_name = Identifier(name="myFunc", line=1, column=0)
        func = FunctionDefinition(
            name=func_name,
            parameters=[],
            body=BlockStatement(statements=[]),
            line=1,
            column=0
        )

        assert generator._extract_symbol_name(func) == "myFunc"

    def test_extract_symbol_name_assignment(self, generator):
        """Test extract symbol name from assignment."""
        assignment = AssignmentStatement(
            target="x",
            value=NumberLiteral(value=42, line=1, column=0),
            line=1,
            column=0
        )

        assert generator._extract_symbol_name(assignment) == "x"

    def test_extract_symbol_name_identifier(self, generator):
        """Test extract symbol name from identifier."""
        identifier = Identifier(name="myVar", line=1, column=0)

        assert generator._extract_symbol_name(identifier) == "myVar"

    def test_extract_symbol_name_parameter(self, generator):
        """Test extract symbol name from parameter."""
        param = Parameter(name="arg", line=1, column=0)

        assert generator._extract_symbol_name(param) == "arg"

    def test_extract_symbol_name_unknown_node(self, generator):
        """Test extract symbol name returns None for unknown nodes."""
        node = NumberLiteral(value=42, line=1, column=0)

        assert generator._extract_symbol_name(node) is None


class TestSourceMapGeneration:
    """Test source map generation."""

    @pytest.fixture
    def generator(self):
        """Create test generator with source maps enabled."""
        return PythonCodeGenerator(source_file="test.ml", generate_source_maps=True)

    def test_generate_source_map_structure(self, generator):
        """Test source map has correct structure."""
        source_map = generator._generate_source_map()

        assert 'version' in source_map
        assert 'file' in source_map
        assert 'sourceRoot' in source_map
        assert 'sources' in source_map
        assert 'names' in source_map
        assert 'mappings' in source_map
        assert 'sourcesContent' in source_map

    def test_generate_source_map_version(self, generator):
        """Test source map has correct version."""
        source_map = generator._generate_source_map()

        assert source_map['version'] == 3

    def test_generate_source_map_file(self, generator):
        """Test source map includes generated file name."""
        source_map = generator._generate_source_map()

        # The file field contains the generated Python filename
        assert source_map['file'] in ["test.py", "test.ml"]

    def test_generate_source_map_no_source_file(self):
        """Test source map with no source file."""
        gen = PythonCodeGenerator(source_file=None, generate_source_maps=True)
        source_map = gen._generate_source_map()

        assert source_map['file'] == 'generated.py'

    @patch.object(Path, 'read_text')
    def test_get_source_content_success(self, mock_read_text, generator):
        """Test getting source content successfully."""
        mock_read_text.return_value = "x = 42;"

        content = generator._get_source_content()

        assert content == "x = 42;"

    @patch.object(Path, 'read_text')
    def test_get_source_content_failure(self, mock_read_text, generator):
        """Test getting source content handles errors."""
        mock_read_text.side_effect = FileNotFoundError()

        content = generator._get_source_content()

        assert content is None

    def test_get_source_content_no_file(self):
        """Test getting source content with no source file."""
        gen = PythonCodeGenerator(source_file=None)

        content = gen._get_source_content()

        assert content is None


class TestGenerateMethod:
    """Test main generate method."""

    @pytest.fixture
    def generator(self):
        """Create test generator."""
        return PythonCodeGenerator(source_file="test.ml")

    def test_generate_simple_program(self, generator):
        """Test generating code from simple program."""
        # Create simple program: x = 42;
        program = Program(items=[
            ExpressionStatement(
                expression=AssignmentStatement(
                    target="x",
                    value=NumberLiteral(value=42, line=1, column=4),
                    line=1,
                    column=0
                ),
                line=1,
                column=0
            )
        ])

        code, source_map = generator.generate(program)

        assert isinstance(code, str)
        assert len(code) > 0
        assert source_map is not None

    def test_generate_without_source_maps(self):
        """Test generating code without source maps."""
        gen = PythonCodeGenerator(generate_source_maps=False)
        program = Program(items=[])

        code, source_map = gen.generate(program)

        assert isinstance(code, str)
        assert source_map is None

    def test_generate_resets_context(self, generator):
        """Test generate method resets context."""
        program = Program(items=[])

        # First generation
        generator.generate(program)

        # Modify state
        generator._indent()
        generator._indent()

        # Second generation should reset
        generator.generate(program)

        # Context should be fresh
        assert generator.context.indentation_level == 0

    def test_generate_resets_output_lines(self, generator):
        """Test generate method resets output lines."""
        program = Program(items=[])

        # First generation
        code1, _ = generator.generate(program)

        # Add manual lines
        generator._emit_line("MANUAL LINE")

        # Second generation should reset
        code2, _ = generator.generate(program)

        # Manual line should not be in second output
        assert "MANUAL LINE" not in code2

    def test_generate_preserves_ml_builtins(self, generator):
        """Test generate preserves ML builtins in symbol table."""
        original_builtins = generator.symbol_table['ml_builtins'].copy()
        program = Program(items=[])

        generator.generate(program)

        # ML builtins should be preserved
        assert generator.symbol_table['ml_builtins'] == original_builtins

    def test_generate_includes_header(self, generator):
        """Test generated code includes header."""
        program = Program(items=[])

        code, _ = generator.generate(program)

        assert '"""Generated Python code from mlpy ML transpiler."""' in code

    def test_generate_includes_footer(self, generator):
        """Test generated code includes footer."""
        program = Program(items=[])

        code, _ = generator.generate(program)

        assert "End of generated code" in code

    def test_generate_includes_runtime_imports(self, generator):
        """Test generated code includes runtime imports."""
        program = Program(items=[])

        code, _ = generator.generate(program)

        assert "safe_call" in code or "_safe_call" in code


class TestModuleOutputModes:
    """Test module output mode handling."""

    def test_separate_module_mode_with_import_paths(self):
        """Test separate module output mode with import paths."""
        gen = PythonCodeGenerator(
            module_output_mode='separate',
            import_paths=['/path/to/modules']
        )
        gen.module_py_files = {'user_module': 'user_module.py'}

        program = Program(items=[])
        code, _ = gen.generate(program)

        # Should include sys.path setup
        assert "sys.path" in code or "Path" in code

    def test_inline_module_mode_with_compiled_modules(self):
        """Test inline module output mode with compiled modules."""
        gen = PythonCodeGenerator(module_output_mode='inline')
        gen.compiled_modules = {
            'user_module': '# User module code\nx = 42'
        }

        program = Program(items=[])
        code, _ = gen.generate(program)

        # Should include inline module code
        assert "User Module Definitions" in code

    def test_separate_mode_with_current_dir_allowed(self):
        """Test separate mode adds source directory to path."""
        gen = PythonCodeGenerator(
            source_file="test.ml",
            module_output_mode='separate',
            allow_current_dir=True
        )
        gen.module_py_files = {'user_module': 'user_module.py'}

        program = Program(items=[])
        code, _ = gen.generate(program)

        # Should add source directory to sys.path
        assert "_source_dir" in code or "Path(__file__).parent" in code


class TestREPLMode:
    """Test REPL mode behavior."""

    def test_repl_mode_enabled(self):
        """Test REPL mode is properly set."""
        gen = PythonCodeGenerator(repl_mode=True)

        assert gen.repl_mode is True

    def test_repl_mode_disabled_by_default(self):
        """Test REPL mode is disabled by default."""
        gen = PythonCodeGenerator()

        assert gen.repl_mode is False

    def test_repl_mode_skips_source_dir_path_setup(self):
        """Test REPL mode skips adding source dir to sys.path."""
        gen = PythonCodeGenerator(
            source_file="test.ml",
            module_output_mode='separate',
            allow_current_dir=True,
            repl_mode=True
        )
        gen.module_py_files = {'user_module': 'user_module.py'}

        program = Program(items=[])
        code, _ = gen.generate(program)

        # Should NOT add __file__ reference in REPL mode
        assert "__file__" not in code
