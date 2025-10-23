"""Module resolution and user module handling for code generation.

This module provides mixin functionality for resolving, discovering, and transpiling
user-defined ML modules during code generation. It handles:

1. **User Module Discovery** - Resolving module paths to actual .ml files
2. **Module Compilation** - Transpiling ML modules to Python code
3. **Import Generation** - Creating appropriate Python import statements
4. **Package Structure** - Ensuring proper __init__.py files for Python packages

Security Considerations:
- Module resolution respects configured import paths and security boundaries
- File system operations are sandboxed to allowed directories
- Cross-module dependencies are properly tracked and validated
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mlpy.ml.grammar.ast_nodes import ASTNode


class ModuleHandlersMixin:
    """Mixin providing user module resolution and compilation functionality.

    This mixin handles all aspects of working with user-defined ML modules:
    - Discovering and resolving module files from import statements
    - Transpiling ML modules to Python code (inline or separate files)
    - Managing module dependencies and import chains
    - Creating proper Python package structures

    The mixin supports two output modes:
    - 'inline': Embed module code directly in the main output file
    - 'separate': Compile modules to separate .py files and use normal Python imports

    Thread Safety:
    - Module resolution and compilation operations are not thread-safe
    - Each code generator instance maintains its own module cache
    """

    def _find_similar_names(self, target: str, available: set) -> list[str]:
        """Find similar module names using Levenshtein distance.

        Used for generating helpful error messages when a module import fails.
        Suggests alternative module names that are close to the attempted import.

        Args:
            target: The module name that was not found
            available: Set of available module names to search

        Returns:
            List of up to 3 similar module names, sorted by similarity

        Example:
            >>> self._find_similar_names('matt', {'math', 'matrix', 'test'})
            ['math', 'matrix']
        """
        import difflib
        return difflib.get_close_matches(target, available, n=3, cutoff=0.6)

    def _get_ml_module_info(self, module_path: str, metadata) -> dict:
        """Convert UnifiedModuleMetadata to module info dict for transpilation.

        This method bridges between the module registry system and the code generator.
        It takes module metadata from the registry and converts it into a format
        suitable for the _generate_user_module_import() method.

        Args:
            module_path: Module path (e.g., "math_utils")
            metadata: Registry metadata for the ML module

        Returns:
            Module info dict with keys:
            - 'name': Module name (last component)
            - 'module_path': Full dotted path
            - 'ast': Parsed AST of the module
            - 'source_code': Original ML source code
            - 'file_path': Absolute path to the .ml file

        Note:
            This method parses the ML source file on demand. For large modules,
            consider caching the parsed AST.
        """
        from mlpy.ml.grammar.parser import MLParser

        ml_file = Path(metadata.file_path)

        # Parse the ML source
        parser = MLParser()
        source_code = ml_file.read_text(encoding='utf-8')
        ast = parser.parse(source_code, str(ml_file))

        return {
            'name': metadata.name.split('.')[-1],  # Last component
            'module_path': module_path,
            'ast': ast,
            'source_code': source_code,
            'file_path': str(ml_file)
        }

    def _resolve_user_module(self, import_target: list[str]) -> Any:
        """Resolve user module using import paths.

        Searches for a user-defined ML module file by checking:
        1. All configured import paths
        2. Source file directory (if allow_current_dir is True)

        Args:
            import_target: Module path components (e.g., ['user_modules', 'sorting'])

        Returns:
            Module info dict if module found, None otherwise

        Module Info Dict Structure:
            {
                'name': 'sorting',
                'module_path': 'user_modules.sorting',
                'ast': <parsed AST>,
                'source_code': <ML source>,
                'file_path': '/path/to/user_modules/sorting.ml'
            }

        Search Strategy:
            For import_target=['user_modules', 'sorting']:
            1. Tries: <import_path>/user_modules/sorting.ml
            2. If allow_current_dir: <source_dir>/user_modules/sorting.ml

        Example:
            >>> module = self._resolve_user_module(['utils', 'math'])
            >>> module['name']
            'math'
            >>> module['module_path']
            'utils.math'
        """
        module_path = ".".join(import_target)
        file_parts = import_target[:]

        # Try to find the module file in import paths
        for base_path in self.import_paths:
            # Try as direct file: user_modules/sorting.ml
            module_file = Path(base_path) / "/".join(file_parts[:-1]) / f"{file_parts[-1]}.ml"

            if module_file.exists():
                # Read and parse the module
                from mlpy.ml.grammar.parser import MLParser

                parser = MLParser()
                source_code = module_file.read_text(encoding='utf-8')
                ast = parser.parse(source_code, str(module_file))

                # Create a simple ModuleInfo-like dict
                return {
                    'name': file_parts[-1],
                    'module_path': module_path,
                    'ast': ast,
                    'source_code': source_code,
                    'file_path': str(module_file)
                }

        # Try from source file directory if available
        if self.source_file and self.allow_current_dir:
            source_dir = Path(self.source_file).parent
            module_file = source_dir / "/".join(file_parts[:-1]) / f"{file_parts[-1]}.ml"

            if module_file.exists():
                from mlpy.ml.grammar.parser import MLParser

                parser = MLParser()
                source_code = module_file.read_text(encoding='utf-8')
                ast = parser.parse(source_code, str(module_file))

                return {
                    'name': file_parts[-1],
                    'module_path': module_path,
                    'ast': ast,
                    'source_code': source_code,
                    'file_path': str(module_file)
                }

        return None

    def _generate_user_module_import(self, module_info: dict, alias: str | None, node: "ASTNode") -> None:
        """Generate import code for user-defined module.

        Generates appropriate Python import statements based on the module output mode:
        - 'separate': Generates normal Python import (module compiled to .py file)
        - 'inline': Embeds module code and creates alias assignment

        Args:
            module_info: Module information dict from _resolve_user_module()
            alias: Optional import alias (e.g., 'import foo as bar')
            node: AST node for source mapping

        Side Effects:
            - Updates self.symbol_table['imports'] with imported module names
            - In 'separate' mode: Calls _compile_module_to_file()
            - In 'inline' mode: Calls _transpile_user_module() if not cached
            - Emits import statement or alias assignment to output

        Examples:
            Separate mode: `import user_modules.sorting`
            Separate mode with alias: `import user_modules.sorting as sort`
            Inline mode: `sort = user_modules_sorting` (after embedding module code)
        """
        module_path = module_info['module_path']

        if self.module_output_mode == 'separate':
            # Separate file mode: compile to .py file and use normal Python import
            py_file = self._compile_module_to_file(module_info)

            # Generate Python import statement
            # Convert module path to Python module name (e.g., user_modules.sorting)
            if alias:
                self._emit_line(f"import {module_path} as {alias}", node)
                self.symbol_table['imports'].add(alias)
            else:
                # For nested imports, we need to import the full path
                parts = module_path.split('.')
                for i in range(len(parts)):
                    partial_path = '.'.join(parts[:i+1])
                    self.symbol_table['imports'].add(partial_path)

                self._emit_line(f"import {module_path}", node)
        else:
            # Inline mode: embed module code in output file
            if module_path not in self.compiled_modules:
                self._transpile_user_module(module_info)

            # Track all parts of the module path in imports
            parts = module_path.split('.')
            for i in range(len(parts)):
                partial_path = '.'.join(parts[:i+1])
                self.symbol_table['imports'].add(partial_path)
                python_name = partial_path.replace('.', '_')
                self.symbol_table['imports'].add(python_name)

            if alias:
                alias_name = self._safe_identifier(alias)
                python_module_name = module_path.replace('.', '_')
                self._emit_line(f"{alias_name} = {python_module_name}", node)
                self.symbol_table['imports'].add(alias_name)

    def _compile_module_to_file(self, module_info: dict) -> str:
        """Compile user module to .py file (with caching).

        Transpiles an ML module to a Python .py file in the same directory as the
        source .ml file. Uses file modification times to avoid unnecessary recompilation.

        Args:
            module_info: Module information dict

        Returns:
            Path to the generated .py file

        Caching Strategy:
            Only recompiles if:
            - .py file doesn't exist
            - .ml file is newer than .py file

        Side Effects:
            - Writes .py file to disk (same directory as .ml file)
            - Calls _ensure_package_structure() to create __init__.py files
            - Updates self.module_py_files cache

        Raises:
            Exception: If unable to write .py file (suggests using inline mode)

        Note:
            Recursive compilation uses the same module_output_mode, so nested
            imports will follow the same separate file pattern.
        """
        module_path = module_info['module_path']
        ml_file = Path(module_info['file_path'])

        # Determine output .py file path (same directory as .ml file)
        py_file = ml_file.with_suffix('.py')

        # Check if we need to recompile
        needs_compile = True
        if py_file.exists():
            ml_mtime = ml_file.stat().st_mtime
            py_mtime = py_file.stat().st_mtime
            if py_mtime >= ml_mtime:
                # .py file is up-to-date
                needs_compile = False

        if needs_compile:
            # Import here to avoid circular dependency at module level
            from mlpy.ml.codegen.python_generator import PythonCodeGenerator

            # Transpile the module
            module_generator = PythonCodeGenerator(
                source_file=str(ml_file),
                generate_source_maps=False,
                import_paths=self.import_paths,
                allow_current_dir=self.allow_current_dir,
                module_output_mode='separate'  # Recursive compilation uses same mode
            )

            python_code, _ = module_generator.generate(module_info['ast'])

            # Write to .py file
            try:
                py_file.write_text(python_code, encoding='utf-8')
            except (IOError, PermissionError) as e:
                # If we can't write the file, fall back to inline mode
                raise Exception(f"Cannot write module file {py_file}: {e}. Consider using inline mode.")

        # Create __init__.py files for package structure
        self._ensure_package_structure(ml_file.parent, module_path)

        # Track the compiled module
        self.module_py_files[module_path] = str(py_file)

        return str(py_file)

    def _ensure_package_structure(self, base_dir: Path, module_path: str) -> None:
        """Create __init__.py files for package directories.

        Ensures that all intermediate directories have __init__.py files so that
        Python recognizes them as packages. This is required for nested module imports.

        Args:
            base_dir: Base directory containing the module (where the .ml file's parent dir is)
            module_path: Dotted module path (e.g., 'user_modules.sorting')

        Example Structure:
            For module_path='user_modules.algorithms.quicksort':
            Creates:
            - user_modules/__init__.py
            - user_modules/algorithms/__init__.py

        Note:
            The deepest level (quicksort.py) doesn't need __init__.py as it's a module file.
        """
        parts = module_path.split('.')

        # Create __init__.py in the directory containing the module
        init_file = base_dir / '__init__.py'
        if not init_file.exists():
            init_file.write_text('# Auto-generated package file\n', encoding='utf-8')

        # For nested packages (e.g., user_modules.algorithms.quicksort),
        # create __init__.py for intermediate levels
        for i in range(1, len(parts) - 1):
            # For user_modules.algorithms.quicksort, create user_modules/algorithms/__init__.py
            package_path = base_dir / Path(*parts[1:i+1])
            init_file = package_path / '__init__.py'
            if not init_file.exists():
                package_path.mkdir(parents=True, exist_ok=True)
                init_file.write_text('# Auto-generated package file\n', encoding='utf-8')

    def _transpile_user_module(self, module_info: dict) -> None:
        """Transpile user module to Python code.

        Transpiles a user-defined ML module to Python code for inline embedding.
        This method creates a namespace class that holds all module functions,
        allowing them to be called as module.function_name().

        Args:
            module_info: Module information dict

        Side Effects:
            - Stores compiled module code in self.compiled_modules[module_path]
            - Functions are rewritten with prefixes to avoid name collisions
            - Creates namespace class for module isolation

        Code Generation Strategy:
            1. Extract function definitions from transpiled code
            2. Rewrite function names with unique prefix (_umod_module_path_funcname)
            3. Rewrite internal function calls to use prefixed names
            4. Create namespace class to hold module functions
            5. Attach rewritten functions to namespace instance

        Example Output (inline mode):
            ```python
            # Top-level function definitions (can call each other)
            def _umod_math_utils_add(a, b):
                return a + b

            def _umod_math_utils_multiply(a, b):
                result = _umod_math_utils_add(a, b)  # Internal call rewritten
                return result * 2

            # Namespace class
            class _ModuleNamespace:
                _ml_user_module = True
                pass

            # Module instance with attached functions
            math_utils = _ModuleNamespace()
            math_utils.add = _umod_math_utils_add
            math_utils.multiply = _umod_math_utils_multiply
            ```

        Note:
            This approach allows module functions to call each other naturally
            (same scope level) while preventing collisions with main program code.
        """
        module_path = module_info['module_path']
        parts = module_path.split('.')

        # Import here to avoid circular dependency at module level
        from mlpy.ml.codegen.python_generator import PythonCodeGenerator

        # Create a new generator for the module
        module_generator = PythonCodeGenerator(
            source_file=module_info['file_path'],
            generate_source_maps=False,  # Don't generate source maps for modules
            import_paths=self.import_paths,
            allow_current_dir=self.allow_current_dir
        )

        # Generate Python code from module AST
        python_code, _ = module_generator.generate(module_info['ast'])

        # Extract just the function definitions from the generated code
        # (skip header, imports, footer)
        lines = python_code.split('\n')
        code_lines = []
        in_code_section = False

        for line in lines:
            # Skip header and import sections
            if line.startswith('"""') or line.startswith('#') or line.startswith('from ') or line.startswith('import '):
                continue
            # Skip empty lines at the start
            if not line.strip() and not in_code_section:
                continue
            # Start collecting code
            in_code_section = True
            code_lines.append(line)

        module_code_body = '\n'.join(code_lines).strip()

        # Build the module definition code
        # NEW APPROACH: Define functions at top level with prefix, then attach to namespace
        # This allows functions to call each other normally (same scope level)

        module_class_name = module_path.replace('.', '_')
        function_prefix = f"_umod_{module_path.replace('.', '_')}_"
        module_definition = []

        module_definition.append(f"# --- Begin User Module: {module_path} ---")

        # Parse the module body to extract function names and rewrite calls
        import re
        lines = module_code_body.split('\n')

        # First pass: collect function names
        function_names = []
        for line in lines:
            if line.strip().startswith('def '):
                match = re.match(r'\s*def\s+(\w+)\s*\(', line)
                if match:
                    function_names.append(match.group(1))

        # Second pass: rewrite function definitions and calls
        rewritten_lines = []
        for line in lines:
            if not line.strip():
                continue

            # Rewrite function definitions to use prefix
            if line.strip().startswith('def '):
                match = re.match(r'(\s*)def\s+(\w+)(\s*\(.*)', line)
                if match:
                    indent, func_name, rest = match.groups()
                    rewritten_lines.append(f"{indent}def {function_prefix}{func_name}{rest}")
                    continue

            # Rewrite function calls to use prefix (only for functions defined in this module)
            modified_line = line
            for func_name in function_names:
                # Match function calls: func_name(args) but not def func_name(
                # Be careful not to match substrings
                pattern = r'\b' + re.escape(func_name) + r'\s*\('
                replacement = f'{function_prefix}{func_name}('
                modified_line = re.sub(pattern, replacement, modified_line)

            rewritten_lines.append(modified_line)

        # Emit rewritten function definitions at top level
        for line in rewritten_lines:
            module_definition.append(line)

        module_definition.append('')

        # Create namespace class
        module_definition.append(f"class _ModuleNamespace:")
        module_definition.append(f"    _ml_user_module = True")
        module_definition.append(f"    pass")
        module_definition.append('')

        # Create instance and attach functions
        module_definition.append(f"{module_class_name} = _ModuleNamespace()")
        for func_name in function_names:
            module_definition.append(f"{module_class_name}.{func_name} = {function_prefix}{func_name}")

        module_definition.append(f"# --- End User Module: {module_path} ---")
        module_definition.append('')

        # For nested modules, create the nested structure
        if len(parts) > 1:
            # Create parent namespace classes with module as attribute
            # We'll create a proper class hierarchy instead of using setattr
            parent_class_code = []
            for i in range(len(parts) - 1):
                parent_name = parts[i]
                parent_class_code.append(f"class {parent_name}:")
                # Add marker so runtime_helpers recognizes this as a user module namespace
                parent_class_code.append(f"    _ml_user_module = True")
                parent_class_code.append(f"    {parts[i+1]} = None")

            module_definition.insert(0, '\n'.join(parent_class_code))

            # Create instances and assign the module
            module_name = parts[-1]
            parent_instance_code = f"{parts[0]} = {parts[0]}()\n{parts[0]}.{parts[1]} = {module_class_name}"
            module_definition.append(parent_instance_code)

        # Store the complete module definition to be emitted later
        self.compiled_modules[module_path] = '\n'.join(module_definition)
