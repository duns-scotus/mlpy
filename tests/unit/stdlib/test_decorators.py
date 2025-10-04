"""Unit tests for ML stdlib decorator system."""

import pytest
from mlpy.stdlib.decorators import (
    ml_module,
    ml_function,
    ml_class,
    ModuleMetadata,
    FunctionMetadata,
    ClassMetadata,
    get_module_metadata,
    get_all_modules,
    _MODULE_REGISTRY,
)


class TestMLFunctionDecorator:
    """Test @ml_function decorator."""

    def test_function_decorator_adds_metadata(self):
        """Test that @ml_function adds metadata to function."""

        @ml_function(description="Test function", capabilities=["test.read"])
        def test_func(x: int) -> int:
            return x * 2

        assert hasattr(test_func, "_ml_function_metadata")
        metadata = test_func._ml_function_metadata
        assert isinstance(metadata, FunctionMetadata)
        assert metadata.name == "test_func"
        assert metadata.description == "Test function"
        assert metadata.capabilities == ["test.read"]

    def test_function_decorator_preserves_behavior(self):
        """Test that decorated function still works."""

        @ml_function(description="Multiply by 2")
        def double(x: int) -> int:
            return x * 2

        assert double(5) == 10
        assert double(0) == 0
        assert double(-3) == -6

    def test_function_decorator_with_params_metadata(self):
        """Test @ml_function with parameter metadata."""

        @ml_function(
            description="Add two numbers",
            params=[
                {"name": "a", "type": "int", "description": "First number"},
                {"name": "b", "type": "int", "description": "Second number"},
            ],
            returns="int",
        )
        def add(a: int, b: int) -> int:
            return a + b

        metadata = add._ml_function_metadata
        assert len(metadata.params) == 2
        assert metadata.params[0]["name"] == "a"
        assert metadata.params[1]["name"] == "b"
        assert metadata.returns == "int"

    def test_function_decorator_without_capabilities(self):
        """Test @ml_function without capabilities (defaults to empty list)."""

        @ml_function(description="Simple function")
        def simple():
            return "hello"

        metadata = simple._ml_function_metadata
        assert metadata.capabilities == []


class TestMLClassDecorator:
    """Test @ml_class decorator."""

    def test_class_decorator_adds_metadata(self):
        """Test that @ml_class adds metadata to class."""

        @ml_class(description="Test class", capabilities=["test.read"])
        class TestClass:
            def method(self):
                return "test"

        assert hasattr(TestClass, "_ml_class_metadata")
        metadata = TestClass._ml_class_metadata
        assert isinstance(metadata, ClassMetadata)
        assert metadata.name == "TestClass"
        assert metadata.description == "Test class"
        assert metadata.capabilities == ["test.read"]

    def test_class_decorator_preserves_behavior(self):
        """Test that decorated class still works."""

        @ml_class(description="Counter class")
        class Counter:
            def __init__(self):
                self.count = 0

            def increment(self):
                self.count += 1
                return self.count

        counter = Counter()
        assert counter.increment() == 1
        assert counter.increment() == 2

    def test_class_decorator_scans_methods(self):
        """Test that @ml_class scans for decorated methods."""

        @ml_class(description="Math operations")
        class MathOps:
            @ml_function(description="Add numbers")
            def add(self, a, b):
                return a + b

            @ml_function(description="Multiply numbers")
            def multiply(self, a, b):
                return a * b

        metadata = MathOps._ml_class_metadata
        assert "add" in metadata.methods
        assert "multiply" in metadata.methods
        assert metadata.methods["add"].description == "Add numbers"


class TestMLModuleDecorator:
    """Test @ml_module decorator."""

    def test_module_decorator_adds_metadata(self):
        """Test that @ml_module adds metadata to class."""

        @ml_module(
            name="testmod",
            description="Test module",
            capabilities=["test.read", "test.write"],
            version="1.0.0",
        )
        class TestModule:
            pass

        assert hasattr(TestModule, "_ml_module_metadata")
        assert hasattr(TestModule, "_ml_module_name")
        metadata = TestModule._ml_module_metadata
        assert isinstance(metadata, ModuleMetadata)
        assert metadata.name == "testmod"
        assert metadata.description == "Test module"
        assert metadata.capabilities == ["test.read", "test.write"]
        assert metadata.version == "1.0.0"

    def test_module_decorator_registers_module(self):
        """Test that @ml_module registers module in global registry."""
        # Clear registry first
        _MODULE_REGISTRY.clear()

        @ml_module(name="registered_mod", description="Registered module")
        class RegisteredModule:
            pass

        assert "registered_mod" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["registered_mod"] == RegisteredModule

    def test_module_decorator_scans_functions(self):
        """Test that @ml_module scans for decorated functions."""

        @ml_module(name="funcmod", description="Module with functions")
        class FunctionModule:
            @ml_function(description="Function one")
            def func_one(self):
                return 1

            @ml_function(description="Function two")
            def func_two(self):
                return 2

            def private_method(self):
                return "private"

        metadata = FunctionModule._ml_module_metadata
        assert "func_one" in metadata.functions
        assert "func_two" in metadata.functions
        assert "private_method" not in metadata.functions  # Not decorated
        assert metadata.functions["func_one"].description == "Function one"

    def test_module_decorator_scans_classes(self):
        """Test that @ml_module scans for decorated classes."""

        @ml_module(name="classmod", description="Module with classes")
        class ClassModule:
            @ml_class(description="Pattern class")
            class Pattern:
                def test(self):
                    return True

            @ml_class(description="Match class")
            class Match:
                def group(self):
                    return "match"

        metadata = ClassModule._ml_module_metadata
        assert "Pattern" in metadata.classes
        assert "Match" in metadata.classes
        assert metadata.classes["Pattern"].description == "Pattern class"

    def test_module_decorator_mixed_functions_and_classes(self):
        """Test module with both functions and classes."""

        @ml_module(name="mixedmod", description="Mixed module")
        class MixedModule:
            @ml_function(description="Top-level function")
            def top_func(self):
                return "top"

            @ml_class(description="Inner class")
            class InnerClass:
                def method(self):
                    return "inner"

        metadata = MixedModule._ml_module_metadata
        assert "top_func" in metadata.functions
        assert "InnerClass" in metadata.classes


class TestModuleMetadata:
    """Test ModuleMetadata class."""

    def test_metadata_to_dict(self):
        """Test ModuleMetadata.to_dict() conversion."""
        metadata = ModuleMetadata(
            name="testmod",
            description="Test module",
            capabilities=["test.read"],
            version="2.0.0",
        )

        # Add function metadata
        func_meta = FunctionMetadata(
            name="test_func",
            description="Test function",
            capabilities=["test.read"],
            params=[{"name": "x", "type": "int"}],
            returns="int",
        )
        metadata.functions["test_func"] = func_meta

        # Add class metadata
        class_meta = ClassMetadata(
            name="TestClass", description="Test class", capabilities=["test.write"]
        )
        metadata.classes["TestClass"] = class_meta

        result = metadata.to_dict()
        assert result["name"] == "testmod"
        assert result["description"] == "Test module"
        assert result["capabilities"] == ["test.read"]
        assert result["version"] == "2.0.0"
        assert "test_func" in result["functions"]
        assert result["functions"]["test_func"]["description"] == "Test function"
        assert "TestClass" in result["classes"]


class TestGlobalRegistry:
    """Test global module registry functions."""

    def test_get_module_metadata(self):
        """Test get_module_metadata() function."""
        _MODULE_REGISTRY.clear()

        @ml_module(name="getmod", description="Gettable module")
        class GettableModule:
            pass

        metadata = get_module_metadata("getmod")
        assert metadata is not None
        assert metadata.name == "getmod"
        assert metadata.description == "Gettable module"

    def test_get_module_metadata_not_found(self):
        """Test get_module_metadata() returns None for unknown module."""
        _MODULE_REGISTRY.clear()

        metadata = get_module_metadata("nonexistent")
        assert metadata is None

    def test_get_all_modules(self):
        """Test get_all_modules() function."""
        _MODULE_REGISTRY.clear()

        @ml_module(name="mod1", description="Module 1")
        class Module1:
            pass

        @ml_module(name="mod2", description="Module 2")
        class Module2:
            pass

        all_modules = get_all_modules()
        assert "mod1" in all_modules
        assert "mod2" in all_modules
        assert all_modules["mod1"]["name"] == "mod1"
        assert all_modules["mod2"]["name"] == "mod2"


class TestIntegrationScenario:
    """Integration tests for complete decorator usage."""

    def test_complete_string_module_example(self):
        """Test complete example similar to real stdlib module."""
        _MODULE_REGISTRY.clear()

        @ml_module(
            name="string",
            description="String manipulation functions",
            capabilities=["string.read"],
            version="1.0.0",
        )
        class StringModule:
            @ml_function(
                description="Convert string to uppercase",
                params=[{"name": "s", "type": "str", "description": "Input string"}],
                returns="str",
            )
            def upper(self, s: str) -> str:
                return s.upper()

            @ml_function(
                description="Convert string to lowercase",
                params=[{"name": "s", "type": "str", "description": "Input string"}],
                returns="str",
            )
            def lower(self, s: str) -> str:
                return s.lower()

        # Test module is registered
        assert "string" in _MODULE_REGISTRY

        # Test metadata is correct
        metadata = get_module_metadata("string")
        assert metadata.name == "string"
        assert len(metadata.functions) == 2
        assert "upper" in metadata.functions
        assert "lower" in metadata.functions

        # Test functions still work
        instance = StringModule()
        assert instance.upper("hello") == "HELLO"
        assert instance.lower("WORLD") == "world"

        # Test introspection
        all_mods = get_all_modules()
        assert "string" in all_mods
        string_info = all_mods["string"]
        assert string_info["description"] == "String manipulation functions"
        assert "upper" in string_info["functions"]

    def test_complete_regex_module_with_classes(self):
        """Test module with nested classes (like regex module)."""
        _MODULE_REGISTRY.clear()

        @ml_module(
            name="regex",
            description="Regular expression operations",
            capabilities=["regex.compile"],
        )
        class RegexModule:
            @ml_function(description="Test if pattern matches")
            def test(self, pattern: str, text: str) -> bool:
                import re

                return bool(re.search(pattern, text))

            @ml_class(description="Compiled regex pattern")
            class Pattern:
                def __init__(self, pattern):
                    import re

                    self.pattern = re.compile(pattern)

                @ml_function(description="Test pattern against text")
                def test(self, text: str) -> bool:
                    return bool(self.pattern.search(text))

        # Test module registration
        metadata = get_module_metadata("regex")
        assert metadata.name == "regex"
        assert "test" in metadata.functions
        assert "Pattern" in metadata.classes

        # Test nested class functionality
        pattern_meta = metadata.classes["Pattern"]
        assert pattern_meta.description == "Compiled regex pattern"
        assert "test" in pattern_meta.methods

        # Test functionality
        instance = RegexModule()
        assert instance.test(r"\d+", "abc123") is True
        assert instance.test(r"\d+", "abc") is False

        pattern = instance.Pattern(r"[a-z]+")
        assert pattern.test("hello") is True
        assert pattern.test("123") is False
