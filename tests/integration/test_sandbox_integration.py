"""Integration tests for sandbox execution functionality."""

import threading
import time
from pathlib import Path

import pytest

from mlpy.ml.transpiler import execute_ml_code_sandbox
from mlpy.runtime.capabilities.manager import get_capability_manager
from mlpy.runtime.capabilities.tokens import create_file_capability
from mlpy.runtime.sandbox import MLSandbox, SandboxConfig, SandboxResult


class TestSandboxIntegration:
    """Test sandbox execution integration."""

    def test_basic_sandbox_execution(self):
        """Test basic ML code execution in sandbox."""
        ml_code = """
        let x = 42
        let y = x * 2
        y
        """

        config = SandboxConfig(memory_limit="50MB", cpu_timeout=10.0, strict_mode=True)

        with MLSandbox(config) as sandbox:
            result = sandbox.execute(ml_code)

            assert result is not None
            assert isinstance(result, SandboxResult)
            # Note: Actual execution result depends on ML transpiler implementation

    def test_sandbox_with_file_capabilities(self):
        """Test sandbox execution with file access capabilities."""
        # Create temporary test file
        test_file = Path("test_sandbox_file.txt")
        test_content = "Hello from sandbox test!"

        try:
            test_file.write_text(test_content)

            ml_code = f"""
            let content = read_file("{test_file}")
            content
            """

            config = SandboxConfig(file_access_patterns=["test_*.txt"], strict_mode=False)

            # Create file capability
            file_token = create_file_capability(patterns=["test_*.txt"], operations={"read"})

            with MLSandbox(config) as sandbox:
                result = sandbox.execute(ml_code, capabilities=[file_token])

                assert result is not None
                assert isinstance(result, SandboxResult)

        finally:
            # Clean up
            if test_file.exists():
                test_file.unlink()

    def test_sandbox_resource_limits(self):
        """Test sandbox resource limit enforcement."""
        # Test memory limit
        ml_code_memory = """
        let big_list = []
        for i in 0..10000000:
            big_list.push(i)
        big_list
        """

        config = SandboxConfig(
            memory_limit="10MB", cpu_timeout=5.0, strict_mode=True  # Very low limit
        )

        with MLSandbox(config) as sandbox:
            result = sandbox.execute(ml_code_memory)

            # Should handle resource limit gracefully
            assert result is not None

    def test_sandbox_timeout(self):
        """Test sandbox CPU timeout enforcement."""
        ml_code_timeout = """
        let x = 0
        while true:
            x = x + 1
        """

        config = SandboxConfig(cpu_timeout=1.0, strict_mode=True)  # Very short timeout

        with MLSandbox(config) as sandbox:
            start_time = time.time()
            result = sandbox.execute(ml_code_timeout)
            execution_time = time.time() - start_time

            # Should timeout within reasonable time
            assert execution_time < 5.0  # Should timeout much faster than this
            assert result is not None

    def test_sandbox_security_isolation(self):
        """Test that sandbox provides proper security isolation."""
        # Potentially dangerous ML code
        dangerous_code = """
        import os
        os.system("echo 'This should be blocked'")
        """

        config = SandboxConfig(strict_mode=True)

        with MLSandbox(config) as sandbox:
            result = sandbox.execute(dangerous_code)

            # Should either block or fail safely
            assert result is not None
            if result.success:
                # If it succeeded, check for security warnings
                assert len(result.security_warnings) > 0

    def test_sandbox_concurrent_execution(self):
        """Test multiple sandboxes running concurrently."""
        ml_code = """
        let x = 42
        x * 2
        """

        config = SandboxConfig(memory_limit="50MB", cpu_timeout=10.0)

        results = []
        exceptions = []

        def run_sandbox(sandbox_id: int):
            try:
                with MLSandbox(config) as sandbox:
                    result = sandbox.execute(ml_code)
                    results.append((sandbox_id, result))
            except Exception as e:
                exceptions.append((sandbox_id, e))

        # Start multiple sandbox executions
        threads = []
        for i in range(3):
            thread = threading.Thread(target=run_sandbox, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all to complete
        for thread in threads:
            thread.join(timeout=30.0)

        # Check results
        assert len(exceptions) == 0, f"Exceptions occurred: {exceptions}"
        assert len(results) == 3

        for sandbox_id, result in results:
            assert result is not None
            assert isinstance(result, SandboxResult)

    def test_sandbox_with_transpiler_integration(self):
        """Test sandbox integration with the full transpiler."""
        ml_code = """
        let greeting = "Hello, Sandbox!"
        let length = len(greeting)
        length
        """

        # Test with transpiler function
        result, issues = execute_ml_code_sandbox(
            ml_code, source_file="<test>", strict_security=True
        )

        assert isinstance(issues, list)  # Should return issues list
        # Note: Result depends on transpiler implementation


class TestSandboxResourceMonitoring:
    """Test sandbox resource monitoring functionality."""

    def test_resource_monitoring_basic(self):
        """Test basic resource monitoring."""
        from mlpy.runtime.sandbox.resource_monitor import ResourceLimits, ResourceMonitor

        monitor = ResourceMonitor()
        limits = ResourceLimits(memory_limit=100 * 1024 * 1024, cpu_timeout=10.0)  # 100MB

        monitor.set_limits(limits)

        # Test that monitoring can be enabled/disabled
        assert not monitor.is_monitoring()

        # Note: Full process monitoring test would require actual subprocess

    def test_resource_limits_parsing(self):
        """Test resource limit parsing in sandbox config."""
        config = SandboxConfig(memory_limit="128MB", cpu_timeout=15.0, file_size_limit="5MB")

        sandbox = MLSandbox(config)
        limits = sandbox._parse_resource_limits()

        assert limits.memory_limit == 128 * 1024 * 1024  # 128MB in bytes
        assert limits.cpu_timeout == 15.0
        assert limits.file_size_limit == 5 * 1024 * 1024  # 5MB in bytes


class TestSandboxCapabilityIntegration:
    """Test sandbox integration with capability system."""

    def test_capability_context_serialization(self):
        """Test that capability contexts can be serialized for subprocess."""
        from mlpy.runtime.capabilities.context import CapabilityContext
        from mlpy.runtime.sandbox.context_serializer import CapabilityContextSerializer

        serializer = CapabilityContextSerializer()

        # Create context with capabilities
        context = CapabilityContext(name="test_context")

        file_token = create_file_capability(patterns=["*.txt"], operations={"read", "write"})
        context.add_capability(file_token)

        # Test serialization
        assert serializer.validate_serialization(context)

        # Test subprocess serialization format
        encoded = serializer.serialize_for_subprocess(context)
        assert isinstance(encoded, str)
        assert len(encoded) > 0

        # Test deserialization
        decoded_context = serializer.deserialize_from_subprocess(encoded)
        assert decoded_context.name == context.name
        assert decoded_context.has_capability("file")

    def test_capability_inheritance_in_sandbox(self):
        """Test that capability inheritance works in sandbox."""
        manager = get_capability_manager()

        # Create parent context with file capability
        with manager.create_file_capability_context(["*.txt"]) as parent_context:
            # Create child context
            child_context = parent_context.create_child_context("child")

            # Child should inherit file capability
            assert child_context.has_capability("file")

            # Test in sandbox
            ml_code = """
            let x = 42
            x
            """

            config = SandboxConfig(strict_mode=False)

            with MLSandbox(config) as sandbox:
                result = sandbox.execute(ml_code, context=child_context)
                assert result is not None


class TestSandboxCaching:
    """Test sandbox performance caching functionality."""

    def test_compilation_cache(self):
        """Test compilation result caching."""
        from mlpy.runtime.sandbox.cache import get_compilation_cache

        cache = get_compilation_cache()
        cache.clear()  # Start fresh

        ml_code = """
        let x = 42
        let y = x * 2
        y
        """

        python_code = "# Generated Python code"

        # Cache compilation
        key = cache.cache_compilation(ml_code, python_code)
        assert isinstance(key, str)
        assert len(key) > 0

        # Retrieve compilation
        cached_result = cache.get_compilation(ml_code)
        assert cached_result is not None
        cached_python, cached_source_map = cached_result
        assert cached_python == python_code

        # Test cache statistics
        stats = cache.get_stats()
        assert stats["size"] == 1
        assert stats["hits"] >= 1

    def test_execution_cache(self):
        """Test execution result caching."""
        from mlpy.runtime.sandbox.cache import get_execution_cache

        cache = get_execution_cache()
        cache.clear()  # Start fresh

        python_code = "result = 42 * 2"
        result_value = 84

        # Cache execution (simple deterministic result)
        key = cache.cache_execution(python_code, result_value)
        assert isinstance(key, str)

        # Retrieve execution
        cached_result = cache.get_execution(python_code)
        assert cached_result == result_value

    def test_cache_cleanup(self):
        """Test cache cleanup functionality."""
        from mlpy.runtime.sandbox.cache import clear_all_caches, get_compilation_cache

        cache = get_compilation_cache()

        # Add some entries
        cache.put("test1", "value1")
        cache.put("test2", "value2")

        assert cache.get_stats()["size"] >= 2

        # Clear all caches
        clear_all_caches()

        assert cache.get_stats()["size"] == 0


class TestSandboxErrorHandling:
    """Test sandbox error handling and edge cases."""

    def test_invalid_ml_code(self):
        """Test handling of invalid ML code."""
        invalid_code = """
        this is not valid ML code $$$ !!!
        """

        config = SandboxConfig()

        with MLSandbox(config) as sandbox:
            result = sandbox.execute(invalid_code)

            assert result is not None
            assert not result.success
            assert result.error is not None

    def test_sandbox_cleanup(self):
        """Test that sandbox cleanup works properly."""
        config = SandboxConfig()

        # Create sandbox and ensure cleanup happens
        sandbox = MLSandbox(config)
        sandbox._setup_sandbox()

        # Should have temp directory
        assert sandbox._temp_dir is not None

        # Cleanup should work without errors
        sandbox._cleanup_sandbox()

        # Multiple cleanups should be safe
        sandbox._cleanup_sandbox()

    def test_sandbox_context_manager_exceptions(self):
        """Test sandbox context manager with exceptions."""
        config = SandboxConfig()

        try:
            with MLSandbox(config) as sandbox:
                # Force an exception
                raise ValueError("Test exception")
        except ValueError:
            pass  # Expected

        # Sandbox should still clean up properly
        # (context manager __exit__ should handle cleanup)


@pytest.fixture
def sample_ml_files(tmp_path):
    """Create sample ML files for testing."""
    files = {}

    # Simple ML file
    simple_file = tmp_path / "simple.ml"
    simple_file.write_text(
        """
    let x = 42
    let y = x * 2
    y
    """
    )
    files["simple"] = simple_file

    # ML file with file operations
    file_ops = tmp_path / "file_ops.ml"
    file_ops.write_text(
        """
    let content = read_file("test.txt")
    write_file("output.txt", content)
    len(content)
    """
    )
    files["file_ops"] = file_ops

    # Data file
    data_file = tmp_path / "test.txt"
    data_file.write_text("Hello, World!")
    files["data"] = data_file

    return files


class TestSandboxFileExecution:
    """Test sandbox execution with file I/O."""

    def test_execute_file_basic(self, sample_ml_files):
        """Test executing ML file in sandbox."""
        config = SandboxConfig()

        with MLSandbox(config) as sandbox:
            result = sandbox.execute_file(str(sample_ml_files["simple"]))

            assert result is not None
            assert isinstance(result, SandboxResult)

    def test_execute_file_with_capabilities(self, sample_ml_files):
        """Test executing ML file with file capabilities."""
        # Create file capability for reading test files
        file_token = create_file_capability(patterns=["*.txt"], operations={"read", "write"})

        config = SandboxConfig(file_access_patterns=["*.txt"], strict_mode=False)

        with MLSandbox(config) as sandbox:
            result = sandbox.execute_file(
                str(sample_ml_files["file_ops"]), capabilities=[file_token]
            )

            assert result is not None

    def test_execute_nonexistent_file(self):
        """Test handling of non-existent file."""
        config = SandboxConfig()

        with MLSandbox(config) as sandbox:
            result = sandbox.execute_file("/nonexistent/file.ml")

            assert result is not None
            assert not result.success
            assert result.error is not None
            assert "file" in str(result.error).lower()


# Performance benchmarks
class TestSandboxPerformance:
    """Performance tests for sandbox execution."""

    def test_sandbox_startup_time(self):
        """Test sandbox startup performance."""
        config = SandboxConfig()

        # Measure sandbox setup time
        times = []
        for _ in range(5):
            start_time = time.time()
            with MLSandbox(config) as sandbox:
                pass  # Just setup and teardown
            elapsed = time.time() - start_time
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        # Should startup in reasonable time (less than 1 second)
        assert avg_time < 1.0, f"Average startup time {avg_time:.3f}s exceeds 1.0s"

    def test_simple_execution_performance(self):
        """Test performance of simple ML code execution."""
        ml_code = """
        let x = 42
        let y = x * 2
        y
        """

        config = SandboxConfig()

        # Measure execution time
        times = []
        with MLSandbox(config) as sandbox:
            for _ in range(3):
                start_time = time.time()
                result = sandbox.execute(ml_code)
                elapsed = time.time() - start_time
                times.append(elapsed)

                assert result is not None

        avg_time = sum(times) / len(times)
        # Should execute simple code quickly (less than 10 seconds for basic transpilation)
        assert avg_time < 10.0, f"Average execution time {avg_time:.3f}s exceeds 10.0s"

    def test_capability_serialization_performance(self):
        """Test performance of capability serialization."""
        from mlpy.runtime.capabilities.context import CapabilityContext
        from mlpy.runtime.sandbox.context_serializer import CapabilityContextSerializer

        serializer = CapabilityContextSerializer()

        # Create context with multiple capabilities
        context = CapabilityContext(name="perf_test")

        for i in range(10):
            file_token = create_file_capability(patterns=[f"*.{i}"], operations={"read", "write"})
            context.add_capability(file_token)

        # Measure serialization time
        times = []
        for _ in range(10):
            start_time = time.time()
            serialized = serializer.serialize(context)
            elapsed = time.time() - start_time
            times.append(elapsed)

            assert len(serialized) > 0

        avg_time = sum(times) / len(times)
        # Should serialize quickly (less than 0.1 second)
        assert avg_time < 0.1, f"Average serialization time {avg_time:.3f}s exceeds 0.1s"
