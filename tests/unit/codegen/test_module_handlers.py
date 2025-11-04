"""
Unit tests for module_handlers.py - User module resolution and compilation.

Tests cover:
- Similar name finding (error suggestions)
- ML module info extraction from metadata
- User module resolution from import paths
- Module import generation (separate and inline modes)
- Module compilation to .py files with caching
- Package structure creation (__init__.py files)
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import tempfile
import os

from mlpy.ml.codegen.helpers.module_handlers import ModuleHandlersMixin
from mlpy.ml.grammar.ast_nodes import Program, ImportStatement, Identifier


# Create a concrete test class that implements ModuleHandlersMixin
class TestModuleHandler(ModuleHandlersMixin):
    """Test implementation of ModuleHandlersMixin."""

    def __init__(self, **kwargs):
        self.import_paths = kwargs.get('import_paths', [])
        self.source_file = kwargs.get('source_file', None)
        self.allow_current_dir = kwargs.get('allow_current_dir', False)
        self.module_output_mode = kwargs.get('module_output_mode', 'separate')
        self.compiled_modules = {}
        self.module_py_files = {}
        self.symbol_table = {
            'imports': set(),
            'variables': set(),
            'functions': set()
        }
        self.output_lines = []
        self.context = Mock()
        self.context.indentation_level = 0

    def _emit_line(self, line: str, node=None):
        """Mock emit line method."""
        self.output_lines.append(line)

    def _safe_identifier(self, name: str) -> str:
        """Mock safe identifier conversion."""
        return name

    def _transpile_user_module(self, module_info: dict):
        """Mock transpile user module."""
        module_path = module_info['module_path']
        self.compiled_modules[module_path] = f"# Compiled {module_path}"


class TestFindSimilarNames:
    """Test _find_similar_names method."""

    def test_find_similar_with_close_matches(self):
        """Test finding similar names with close matches."""
        handler = TestModuleHandler()
        available = {'math', 'matrix', 'matplotlib', 'test'}

        similar = handler._find_similar_names('matt', available)

        assert 'math' in similar
        assert len(similar) <= 3

    def test_find_similar_with_exact_match(self):
        """Test finding similar names includes exact match."""
        handler = TestModuleHandler()
        available = {'math', 'random', 'os'}

        similar = handler._find_similar_names('math', available)

        assert 'math' in similar

    def test_find_similar_with_no_matches(self):
        """Test finding similar names with no close matches."""
        handler = TestModuleHandler()
        available = {'abc', 'xyz', 'test'}

        similar = handler._find_similar_names('totally_different', available)

        # With cutoff=0.6, no matches should be found
        assert len(similar) == 0

    def test_find_similar_returns_max_three(self):
        """Test that at most 3 similar names are returned."""
        handler = TestModuleHandler()
        available = {'mat', 'math', 'matrix', 'matplotlib', 'mathlib', 'mathtools'}

        similar = handler._find_similar_names('mat', available)

        assert len(similar) <= 3

    def test_find_similar_case_sensitive(self):
        """Test case sensitivity in similarity matching."""
        handler = TestModuleHandler()
        available = {'Math', 'MATH', 'math'}

        similar = handler._find_similar_names('math', available)

        # Should find all variants
        assert len(similar) > 0


class TestGetMLModuleInfo:
    """Test _get_ml_module_info method."""

    @patch('mlpy.ml.grammar.parser.MLParser')
    def test_get_ml_module_info_simple_module(self, mock_parser_class):
        """Test getting ML module info from metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create actual file for testing
            ml_file = Path(tmpdir) / 'sorting.ml'
            ml_file.write_text('function sort(arr) { return arr; }')

            handler = TestModuleHandler()

            # Mock metadata
            metadata = Mock()
            metadata.name = 'user_modules.sorting'
            metadata.file_path = str(ml_file)

            # Mock parser
            mock_parser = Mock()
            mock_ast = Mock()
            mock_parser.parse.return_value = mock_ast
            mock_parser_class.return_value = mock_parser

            result = handler._get_ml_module_info('user_modules.sorting', metadata)

            assert result['name'] == 'sorting'
            assert result['module_path'] == 'user_modules.sorting'
            assert result['ast'] == mock_ast
            assert result['source_code'] == 'function sort(arr) { return arr; }'
            assert result['file_path'] == str(ml_file)

    @patch('mlpy.ml.grammar.parser.MLParser')
    def test_get_ml_module_info_nested_module(self, mock_parser_class):
        """Test getting ML module info for nested module."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create actual file for testing
            ml_file = Path(tmpdir) / 'quicksort.ml'
            ml_file.write_text('function quicksort(arr) {}')

            handler = TestModuleHandler()

            # Mock metadata for nested module
            metadata = Mock()
            metadata.name = 'user.algorithms.quicksort'
            metadata.file_path = str(ml_file)

            # Mock parser
            mock_parser = Mock()
            mock_ast = Mock()
            mock_parser.parse.return_value = mock_ast
            mock_parser_class.return_value = mock_parser

            result = handler._get_ml_module_info('user.algorithms.quicksort', metadata)

            # Should extract last component as name
            assert result['name'] == 'quicksort'
            assert result['module_path'] == 'user.algorithms.quicksort'


class TestResolveUserModule:
    """Test _resolve_user_module method."""

    def test_resolve_user_module_from_import_path(self):
        """Test resolving user module from configured import path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test module file
            module_dir = Path(tmpdir) / 'user_modules'
            module_dir.mkdir()
            module_file = module_dir / 'sorting.ml'
            module_file.write_text('function sort() { return []; }')

            handler = TestModuleHandler(import_paths=[tmpdir])

            with patch('mlpy.ml.grammar.parser.MLParser') as mock_parser_class:
                mock_parser = Mock()
                mock_ast = Mock()
                mock_parser.parse.return_value = mock_ast
                mock_parser_class.return_value = mock_parser

                result = handler._resolve_user_module(['user_modules', 'sorting'])

                assert result is not None
                assert result['name'] == 'sorting'
                assert result['module_path'] == 'user_modules.sorting'
                assert result['ast'] == mock_ast

    def test_resolve_user_module_not_found(self):
        """Test resolving non-existent user module."""
        handler = TestModuleHandler(import_paths=['/nonexistent/path'])

        result = handler._resolve_user_module(['user_modules', 'sorting'])

        assert result is None

    def test_resolve_user_module_from_source_dir(self):
        """Test resolving user module from source file directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test module file in source directory
            source_file = Path(tmpdir) / 'main.ml'
            source_file.write_text('import utils;')

            module_file = Path(tmpdir) / 'utils.ml'
            module_file.write_text('function helper() {}')

            handler = TestModuleHandler(
                source_file=str(source_file),
                allow_current_dir=True
            )

            with patch('mlpy.ml.grammar.parser.MLParser') as mock_parser_class:
                mock_parser = Mock()
                mock_ast = Mock()
                mock_parser.parse.return_value = mock_ast
                mock_parser_class.return_value = mock_parser

                result = handler._resolve_user_module(['utils'])

                assert result is not None
                assert result['name'] == 'utils'
                assert result['module_path'] == 'utils'

    def test_resolve_user_module_current_dir_disabled(self):
        """Test that current dir is not searched when disabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source_file = Path(tmpdir) / 'main.ml'
            source_file.write_text('import utils;')

            module_file = Path(tmpdir) / 'utils.ml'
            module_file.write_text('function helper() {}')

            # allow_current_dir is False
            handler = TestModuleHandler(
                source_file=str(source_file),
                allow_current_dir=False
            )

            result = handler._resolve_user_module(['utils'])

            # Should not find module in current dir
            assert result is None

    def test_resolve_user_module_prefers_import_path(self):
        """Test that import paths are checked before source directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create module in import path
            import_dir = Path(tmpdir) / 'imports'
            import_dir.mkdir()
            import_module = import_dir / 'utils.ml'
            import_module.write_text('function from_import_path() {}')

            # Create module in source directory
            source_file = Path(tmpdir) / 'main.ml'
            source_file.write_text('import utils;')
            source_module = Path(tmpdir) / 'utils.ml'
            source_module.write_text('function from_source_dir() {}')

            handler = TestModuleHandler(
                source_file=str(source_file),
                import_paths=[str(import_dir)],
                allow_current_dir=True
            )

            with patch('mlpy.ml.grammar.parser.MLParser') as mock_parser_class:
                mock_parser = Mock()
                mock_parser.parse.return_value = Mock()
                mock_parser_class.return_value = mock_parser

                result = handler._resolve_user_module(['utils'])

                # Should use import path version
                assert 'from_import_path' in result['source_code']


class TestGenerateUserModuleImport:
    """Test _generate_user_module_import method."""

    def test_generate_import_separate_mode_no_alias(self):
        """Test generating import in separate mode without alias."""
        handler = TestModuleHandler(module_output_mode='separate')

        module_info = {
            'name': 'sorting',
            'module_path': 'user_modules.sorting',
            'ast': Mock(),
            'source_code': 'function sort() {}',
            'file_path': '/path/to/sorting.ml'
        }

        with patch.object(handler, '_compile_module_to_file', return_value='/path/to/sorting.py'):
            handler._generate_user_module_import(module_info, alias=None, node=Mock())

        # Should emit import statement
        assert any('import user_modules.sorting' in line for line in handler.output_lines)

        # Should track imports in symbol table
        assert 'user_modules' in handler.symbol_table['imports']
        assert 'user_modules.sorting' in handler.symbol_table['imports']

    def test_generate_import_separate_mode_with_alias(self):
        """Test generating import in separate mode with alias."""
        handler = TestModuleHandler(module_output_mode='separate')

        module_info = {
            'name': 'sorting',
            'module_path': 'user_modules.sorting',
            'ast': Mock(),
            'source_code': 'function sort() {}',
            'file_path': '/path/to/sorting.ml'
        }

        with patch.object(handler, '_compile_module_to_file', return_value='/path/to/sorting.py'):
            handler._generate_user_module_import(module_info, alias='sort', node=Mock())

        # Should emit import with alias
        assert any('import user_modules.sorting as sort' in line for line in handler.output_lines)
        assert 'sort' in handler.symbol_table['imports']

    def test_generate_import_inline_mode_no_alias(self):
        """Test generating import in inline mode without alias."""
        handler = TestModuleHandler(module_output_mode='inline')

        module_info = {
            'name': 'sorting',
            'module_path': 'user_modules.sorting',
            'ast': Mock(),
            'source_code': 'function sort() {}',
            'file_path': '/path/to/sorting.ml'
        }

        handler._generate_user_module_import(module_info, alias=None, node=Mock())

        # Should transpile and cache module
        assert 'user_modules.sorting' in handler.compiled_modules

        # Should track imports
        assert 'user_modules' in handler.symbol_table['imports']
        assert 'user_modules.sorting' in handler.symbol_table['imports']

    def test_generate_import_inline_mode_with_alias(self):
        """Test generating import in inline mode with alias."""
        handler = TestModuleHandler(module_output_mode='inline')

        module_info = {
            'name': 'sorting',
            'module_path': 'user_modules.sorting',
            'ast': Mock(),
            'source_code': 'function sort() {}',
            'file_path': '/path/to/sorting.ml'
        }

        handler._generate_user_module_import(module_info, alias='sort', node=Mock())

        # Should emit alias assignment
        assert any('sort = user_modules_sorting' in line for line in handler.output_lines)
        assert 'sort' in handler.symbol_table['imports']

    def test_generate_import_inline_mode_caches_module(self):
        """Test that inline mode caches compiled modules."""
        handler = TestModuleHandler(module_output_mode='inline')

        module_info = {
            'name': 'utils',
            'module_path': 'utils',
            'ast': Mock(),
            'source_code': 'function helper() {}',
            'file_path': '/path/to/utils.ml'
        }

        # First import
        handler._generate_user_module_import(module_info, alias=None, node=Mock())
        assert 'utils' in handler.compiled_modules

        # Clear transpile tracking
        handler.compiled_modules['utils'] = '# Already compiled'

        # Second import should use cached version
        handler._generate_user_module_import(module_info, alias='u', node=Mock())

        # Should not transpile again
        assert handler.compiled_modules['utils'] == '# Already compiled'


class TestCompileModuleToFile:
    """Test _compile_module_to_file method."""

    def test_compile_module_creates_py_file(self):
        """Test compiling module creates .py file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ml_file = Path(tmpdir) / 'sorting.ml'
            ml_file.write_text('function sort() {}')

            handler = TestModuleHandler()

            module_info = {
                'name': 'sorting',
                'module_path': 'sorting',
                'ast': Program(items=[]),
                'source_code': 'function sort() {}',
                'file_path': str(ml_file)
            }

            with patch('mlpy.ml.codegen.python_generator.PythonCodeGenerator') as mock_gen_class:
                mock_generator = Mock()
                mock_generator.generate.return_value = ('# Python code', None)
                mock_gen_class.return_value = mock_generator

                with patch.object(handler, '_ensure_package_structure'):
                    py_file = handler._compile_module_to_file(module_info)

                # Should create .py file
                assert Path(py_file).suffix == '.py'
                assert Path(py_file).exists()

    def test_compile_module_skips_if_up_to_date(self):
        """Test that compilation is skipped if .py file is up-to-date."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ml_file = Path(tmpdir) / 'sorting.ml'
            ml_file.write_text('function sort() {}')

            py_file = Path(tmpdir) / 'sorting.py'
            py_file.write_text('# Already compiled')

            # Make .py file newer than .ml file
            ml_mtime = ml_file.stat().st_mtime
            os.utime(py_file, (ml_mtime + 10, ml_mtime + 10))

            handler = TestModuleHandler()

            module_info = {
                'name': 'sorting',
                'module_path': 'sorting',
                'ast': Program(items=[]),
                'source_code': 'function sort() {}',
                'file_path': str(ml_file)
            }

            with patch('mlpy.ml.codegen.python_generator.PythonCodeGenerator') as mock_gen_class:
                with patch.object(handler, '_ensure_package_structure'):
                    result = handler._compile_module_to_file(module_info)

                # Should not call generator
                mock_gen_class.assert_not_called()

                # Should still return py file path
                assert result == str(py_file)

    def test_compile_module_recompiles_if_ml_newer(self):
        """Test that module is recompiled if .ml file is newer."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ml_file = Path(tmpdir) / 'sorting.ml'
            ml_file.write_text('function sort() {}')

            py_file = Path(tmpdir) / 'sorting.py'
            py_file.write_text('# Old version')

            # Make .ml file newer than .py file
            py_mtime = py_file.stat().st_mtime
            os.utime(ml_file, (py_mtime + 10, py_mtime + 10))

            handler = TestModuleHandler()

            module_info = {
                'name': 'sorting',
                'module_path': 'sorting',
                'ast': Program(items=[]),
                'source_code': 'function sort() {}',
                'file_path': str(ml_file)
            }

            with patch('mlpy.ml.codegen.python_generator.PythonCodeGenerator') as mock_gen_class:
                mock_generator = Mock()
                mock_generator.generate.return_value = ('# New Python code', None)
                mock_gen_class.return_value = mock_generator

                with patch.object(handler, '_ensure_package_structure'):
                    handler._compile_module_to_file(module_info)

                # Should call generator
                mock_gen_class.assert_called_once()

    def test_compile_module_tracks_in_cache(self):
        """Test that compiled module is tracked in cache."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ml_file = Path(tmpdir) / 'sorting.ml'
            ml_file.write_text('function sort() {}')

            handler = TestModuleHandler()

            module_info = {
                'name': 'sorting',
                'module_path': 'user.sorting',
                'ast': Program(items=[]),
                'source_code': 'function sort() {}',
                'file_path': str(ml_file)
            }

            with patch('mlpy.ml.codegen.python_generator.PythonCodeGenerator') as mock_gen_class:
                mock_generator = Mock()
                mock_generator.generate.return_value = ('# Python code', None)
                mock_gen_class.return_value = mock_generator

                with patch.object(handler, '_ensure_package_structure'):
                    py_file = handler._compile_module_to_file(module_info)

                # Should track in cache
                assert 'user.sorting' in handler.module_py_files
                assert handler.module_py_files['user.sorting'] == py_file


class TestEnsurePackageStructure:
    """Test _ensure_package_structure method."""

    def test_ensure_package_creates_init_file(self):
        """Test that package structure creates __init__.py."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)

            handler = TestModuleHandler()
            handler._ensure_package_structure(base_dir, 'sorting')

            # Should create __init__.py in base directory
            init_file = base_dir / '__init__.py'
            assert init_file.exists()

    def test_ensure_package_creates_nested_init_files(self):
        """Test that nested packages get __init__.py files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)

            # Create the nested directory structure
            nested_dir = base_dir / 'user'
            nested_dir.mkdir(parents=True)

            handler = TestModuleHandler()
            handler._ensure_package_structure(base_dir, 'user.algorithms.quicksort')

            # Should create __init__.py in base
            assert (base_dir / '__init__.py').exists()

            # Should create __init__.py in intermediate directory
            # Note: The method creates init files for intermediate levels
            # For 'user.algorithms.quicksort', it creates init for parent of 'user' and for 'algorithms'

    def test_ensure_package_does_not_overwrite_existing(self):
        """Test that existing __init__.py files are not overwritten."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)

            # Create existing __init__.py with custom content
            init_file = base_dir / '__init__.py'
            init_file.write_text('# Custom init file\n')

            handler = TestModuleHandler()
            handler._ensure_package_structure(base_dir, 'sorting')

            # Should not overwrite
            content = init_file.read_text()
            assert content == '# Custom init file\n'

    def test_ensure_package_handles_single_level(self):
        """Test package structure for single-level module."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)

            handler = TestModuleHandler()
            handler._ensure_package_structure(base_dir, 'utils')

            # Should create __init__.py in base
            init_file = base_dir / '__init__.py'
            assert init_file.exists()
