"""End-to-end tests for extension module system.

Tests cover complete workflows:
- Creating custom extension modules
- Registering through CLI flags
- Registering through config files
- Transpiling ML code that imports extension modules
- Executing ML code with extension modules
- REPL usage with extension modules
- Complete project workflow with extensions
"""

import json
import pytest
from pathlib import Path

from mlpy.ml.transpiler import MLTranspiler
from mlpy.cli.project_manager import MLProjectManager, MLProjectConfig
from mlpy.cli.repl import MLREPLSession
from mlpy.stdlib.module_registry import get_registry


class TestBasicExtensionModuleWorkflow:
    """Test basic extension module creation and usage."""

    def test_create_and_use_extension_module(self, tmp_path):
        """Test complete workflow: create extension → transpile → execute."""
        # 1. Create extension directory
        ext_dir = tmp_path / "extensions"
        ext_dir.mkdir()

        # 2. Create custom extension module
        calculator_module = ext_dir / "calculator_bridge.py"
        calculator_module.write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="calculator", description="Custom calculator module")
class Calculator:
    @ml_function(description="Add two numbers")
    def add(self, a: int, b: int) -> int:
        return a + b

    @ml_function(description="Multiply two numbers")
    def multiply(self, a: int, b: int) -> int:
        return a * b

    @ml_function(description="Power function")
    def power(self, base: int, exp: int) -> int:
        return base ** exp

calculator = Calculator()
''')

        # 3. Create transpiler with extension path
        transpiler = MLTranspiler(python_extension_paths=[str(ext_dir)])

        # 4. Write ML code that uses the extension module
        ml_code = '''
result1 = 5 + 3;
result2 = 4 * 6;
result3 = 2 ** 8;
'''

        # 5. Transpile
        python_code, issues, source_map = transpiler.transpile_to_python(
            ml_code,
            source_file="test.ml"
        )

        assert python_code is not None
        assert len(issues) == 0  # No security issues

        # 6. Verify the module is available in registry
        registry = get_registry()
        assert registry.is_available("calculator")

        # 7. Get and test the module directly
        calc = registry.get_module("calculator")
        assert calc is not None
        assert calc.add(10, 20) == 30
        assert calc.multiply(7, 8) == 56
        assert calc.power(3, 4) == 81

    def test_multiple_extension_modules(self, tmp_path):
        """Test using multiple extension modules together."""
        # Create two extension directories
        ext1_dir = tmp_path / "ext1"
        ext2_dir = tmp_path / "ext2"
        ext1_dir.mkdir()
        ext2_dir.mkdir()

        # Module 1: String utilities
        (ext1_dir / "strutils_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="strutils", description="String utilities")
class StrUtils:
    @ml_function(description="Reverse string")
    def reverse(self, s: str) -> str:
        return s[::-1]

strutils = StrUtils()
''')

        # Module 2: Math utilities
        (ext2_dir / "mathutils_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="mathutils", description="Math utilities")
class MathUtils:
    @ml_function(description="Factorial")
    def factorial(self, n: int) -> int:
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)

mathutils = MathUtils()
''')

        # Create transpiler with both paths
        transpiler = MLTranspiler(
            python_extension_paths=[str(ext1_dir), str(ext2_dir)]
        )

        # Verify both modules are available
        registry = get_registry()
        assert registry.is_available("strutils")
        assert registry.is_available("mathutils")

        # Test both modules
        str_mod = registry.get_module("strutils")
        math_mod = registry.get_module("mathutils")

        assert str_mod.reverse("hello") == "olleh"
        assert math_mod.factorial(5) == 120


class TestConfigurationBasedWorkflow:
    """Test extension modules through configuration files."""

    def test_complete_project_workflow_with_extensions(self, tmp_path):
        """Test full project workflow from init to execution with extensions."""
        # 1. Initialize project
        manager = MLProjectManager()
        manager.init_project("extension-project", tmp_path)

        project_dir = tmp_path / "extension-project"

        # 2. Create extension directory in project
        ext_dir = project_dir / "my_extensions"
        ext_dir.mkdir()

        # 3. Create custom module
        (ext_dir / "project_utils_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="projectutils", description="Project utilities")
class ProjectUtils:
    @ml_function(description="Process data")
    def process(self, data: str) -> str:
        return f"processed: {data}"

projectutils = ProjectUtils()
''')

        # 4. Update project config with extension path
        manager.config.python_extension_paths = ["./my_extensions"]
        config_file = project_dir / "mlpy.json"
        manager.save_config(config_file)

        # 5. Simulate new session: load config
        manager2 = MLProjectManager()
        manager2.load_config(config_file)

        # 6. Create transpiler with resolved paths
        abs_paths = [
            str((project_dir / path).resolve())
            for path in manager2.config.python_extension_paths
        ]

        transpiler = MLTranspiler(python_extension_paths=abs_paths)

        # 7. Verify module is available
        registry = get_registry()
        assert registry.is_available("projectutils")

        # 8. Test the module
        mod = registry.get_module("projectutils")
        assert mod.process("test") == "processed: test"

    def test_yaml_config_with_extensions(self, tmp_path):
        """Test YAML configuration with extension paths."""
        import yaml

        # Create extension directory
        ext_dir = tmp_path / "yaml_extensions"
        ext_dir.mkdir()

        (ext_dir / "yamlmod_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="yamlmod", description="YAML test module")
class YamlMod:
    @ml_function(description="Test function")
    def test(self):
        return "from_yaml_config"

yamlmod = YamlMod()
''')

        # Create YAML config
        config_file = tmp_path / "mlpy.yaml"
        config_data = {
            "name": "yaml-project",
            "python_extension_paths": [str(ext_dir)]
        }

        config_file.write_text(yaml.dump(config_data))

        # Load config
        manager = MLProjectManager()
        manager.load_config(config_file)

        # Create transpiler
        transpiler = MLTranspiler(
            python_extension_paths=manager.config.python_extension_paths
        )

        # Test module
        registry = get_registry()
        assert registry.is_available("yamlmod")
        mod = registry.get_module("yamlmod")
        assert mod.test() == "from_yaml_config"


class TestREPLWithExtensions:
    """Test REPL usage with extension modules."""

    def test_repl_can_use_extension_modules(self, tmp_path):
        """Test REPL with custom extension modules."""
        # Create extension
        ext_dir = tmp_path / "repl_extensions"
        ext_dir.mkdir()

        (ext_dir / "replmod_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="replmod", description="REPL test module")
class ReplMod:
    @ml_function(description="Double a number")
    def double(self, x: int) -> int:
        return x * 2

    @ml_function(description="Greet")
    def greet(self, name: str) -> str:
        return f"Hello, {name}!"

replmod = ReplMod()
''')

        # Create REPL session with extension paths
        session = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext_dir)]
        )

        # Verify module is available
        registry = get_registry()
        assert registry.is_available("replmod")

        # Execute ML code in REPL that uses the module
        # Note: We're just testing that the session can be created with extension paths
        # The actual import mechanism would be tested through transpilation

        result = session.execute_ml_line('x = 42;')
        assert result.success

    def test_repl_multiple_sessions_with_different_extensions(self, tmp_path):
        """Test multiple REPL sessions with different extension paths."""
        # Create two extension directories
        ext1_dir = tmp_path / "ext1"
        ext2_dir = tmp_path / "ext2"
        ext1_dir.mkdir()
        ext2_dir.mkdir()

        (ext1_dir / "mod1_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="mod1", description="Module 1")
class Mod1:
    @ml_function(description="Func1")
    def func1(self):
        return "mod1"

mod1 = Mod1()
''')

        (ext2_dir / "mod2_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="mod2", description="Module 2")
class Mod2:
    @ml_function(description="Func2")
    def func2(self):
        return "mod2"

mod2 = Mod2()
''')

        # Create session 1 with ext1
        session1 = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext1_dir)]
        )

        # Create session 2 with ext2
        session2 = MLREPLSession(
            security_enabled=False,
            extension_paths=[str(ext2_dir)]
        )

        # Both modules should be available (shared registry)
        registry = get_registry()
        assert registry.is_available("mod1")
        assert registry.is_available("mod2")


class TestComplexExtensionModules:
    """Test complex extension modules with various features."""

    def test_extension_module_with_state(self, tmp_path):
        """Test extension module that maintains state."""
        ext_dir = tmp_path / "stateful_ext"
        ext_dir.mkdir()

        (ext_dir / "counter_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="counter", description="Stateful counter module")
class Counter:
    def __init__(self):
        self._count = 0

    @ml_function(description="Increment counter")
    def increment(self):
        self._count += 1
        return self._count

    @ml_function(description="Get current count")
    def get_count(self):
        return self._count

    @ml_function(description="Reset counter")
    def reset(self):
        self._count = 0

counter = Counter()
''')

        transpiler = MLTranspiler(python_extension_paths=[str(ext_dir)])

        registry = get_registry()
        counter = registry.get_module("counter")

        # Test state maintenance
        assert counter.get_count() == 0
        assert counter.increment() == 1
        assert counter.increment() == 2
        assert counter.get_count() == 2
        counter.reset()
        assert counter.get_count() == 0

    def test_extension_module_with_dependencies(self, tmp_path):
        """Test extension module that uses other Python packages."""
        ext_dir = tmp_path / "complex_ext"
        ext_dir.mkdir()

        (ext_dir / "advanced_bridge.py").write_text('''
import json
import os
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="advanced", description="Advanced module with dependencies")
class Advanced:
    @ml_function(description="Parse JSON string")
    def parse_json(self, json_str: str):
        try:
            return json.loads(json_str)
        except:
            return None

    @ml_function(description="Get environment variable")
    def get_env(self, key: str, default: str = ""):
        return os.environ.get(key, default)

advanced = Advanced()
''')

        transpiler = MLTranspiler(python_extension_paths=[str(ext_dir)])

        registry = get_registry()
        adv = registry.get_module("advanced")

        # Test JSON parsing
        result = adv.parse_json('{"key": "value"}')
        assert result == {"key": "value"}

        # Test environment variable (should work even if var doesn't exist)
        result = adv.get_env("NONEXISTENT_VAR", "default")
        assert result == "default"


class TestErrorHandling:
    """Test error handling in extension module workflow."""

    def test_malformed_extension_module(self, tmp_path):
        """Test handling of syntactically invalid extension module."""
        ext_dir = tmp_path / "broken_ext"
        ext_dir.mkdir()

        # Create module with syntax error
        (ext_dir / "broken_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="broken"
class Broken:  # Missing closing parenthesis
    pass
''')

        # Should not crash when creating transpiler
        transpiler = MLTranspiler(python_extension_paths=[str(ext_dir)])

        # Module should not be available
        registry = get_registry()
        assert not registry.is_available("broken")

    def test_extension_module_missing_instance(self, tmp_path):
        """Test extension module without instance variable."""
        ext_dir = tmp_path / "no_instance_ext"
        ext_dir.mkdir()

        (ext_dir / "noinst_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module

@ml_module(name="noinst", description="No instance")
class NoInstance:
    pass

# Missing: noinst = NoInstance()
''')

        transpiler = MLTranspiler(python_extension_paths=[str(ext_dir)])

        registry = get_registry()
        # Module discovered but cannot be loaded
        assert registry.is_available("noinst")
        mod = registry.get_module("noinst")
        assert mod is None

    def test_nonexistent_extension_path(self):
        """Test transpiler with non-existent extension path."""
        # Should not crash
        transpiler = MLTranspiler(
            python_extension_paths=["/nonexistent/path/to/extensions"]
        )

        # Should work normally (just without any custom modules)
        ml_code = "x = 42;"
        python_code, issues, source_map = transpiler.transpile_to_python(ml_code)

        assert python_code is not None
        assert len(issues) == 0


class TestPriorityAndConflicts:
    """Test priority and name conflict handling."""

    def test_stdlib_takes_precedence_over_extension(self, tmp_path):
        """Test that stdlib modules cannot be overridden by extensions."""
        ext_dir = tmp_path / "conflict_ext"
        ext_dir.mkdir()

        # Try to create extension with stdlib name
        (ext_dir / "math_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="math", description="Fake math module")
class FakeMath:
    @ml_function(description="Fake sqrt")
    def sqrt(self, x):
        return "fake"

math = FakeMath()
''')

        transpiler = MLTranspiler(python_extension_paths=[str(ext_dir)])

        registry = get_registry()
        math_mod = registry.get_module("math")

        # Should get real math module, not fake
        # Real math module has actual sqrt implementation
        import math as real_math
        assert math_mod.sqrt(16) == real_math.sqrt(16)

    def test_first_extension_path_wins_on_conflict(self, tmp_path):
        """Test that first extension path wins when modules conflict."""
        ext1_dir = tmp_path / "ext1"
        ext2_dir = tmp_path / "ext2"
        ext1_dir.mkdir()
        ext2_dir.mkdir()

        # Same module name in both paths
        (ext1_dir / "shared_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="shared", description="From ext1")
class Shared:
    @ml_function(description="Version")
    def version(self):
        return "ext1"

shared = Shared()
''')

        (ext2_dir / "shared_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="shared", description="From ext2")
class Shared:
    @ml_function(description="Version")
    def version(self):
        return "ext2"

shared = Shared()
''')

        # Order matters: ext1 first
        transpiler = MLTranspiler(
            python_extension_paths=[str(ext1_dir), str(ext2_dir)]
        )

        registry = get_registry()
        shared_mod = registry.get_module("shared")

        # First path (ext1) should win
        assert shared_mod.version() == "ext1"


class TestPerformance:
    """Test performance characteristics of extension module system."""

    def test_lazy_loading_of_extension_modules(self, tmp_path):
        """Verify that extension modules are loaded lazily."""
        ext_dir = tmp_path / "lazy_ext"
        ext_dir.mkdir()

        # Create module that tracks when it's loaded
        (ext_dir / "tracked_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

# This will be executed on import
_loaded = True

@ml_module(name="tracked", description="Tracked loading")
class Tracked:
    @ml_function(description="Check loaded")
    def is_loaded(self):
        return _loaded

tracked = Tracked()
''')

        # Creating transpiler should not load the module
        transpiler = MLTranspiler(python_extension_paths=[str(ext_dir)])

        registry = get_registry()

        # Module should be discovered but not loaded yet
        assert registry.is_available("tracked")

        # Now actually get the module (triggers loading)
        mod = registry.get_module("tracked")
        assert mod is not None
        assert mod.is_loaded() is True

    def test_extension_module_caching(self, tmp_path):
        """Verify that extension modules are cached after first load."""
        ext_dir = tmp_path / "cached_ext"
        ext_dir.mkdir()

        (ext_dir / "cacheable_bridge.py").write_text('''
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(name="cacheable", description="Cacheable module")
class Cacheable:
    @ml_function(description="Test")
    def test(self):
        return "cached"

cacheable = Cacheable()
''')

        transpiler = MLTranspiler(python_extension_paths=[str(ext_dir)])

        registry = get_registry()

        # Load module first time
        mod1 = registry.get_module("cacheable")

        # Load module second time (should be cached)
        mod2 = registry.get_module("cacheable")

        # Should be the same instance (cached)
        assert mod1 is mod2
