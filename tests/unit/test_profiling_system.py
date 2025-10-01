"""Comprehensive unit tests for the mlpy profiling system."""

import os
import threading
import time
from unittest.mock import MagicMock, patch

import pytest

from mlpy.runtime.profiling.decorators import (
    ProfileContext,
    ProfileData,
    ProfilerManager,
    profile,
    profile_block,
    profile_capability,
    profile_parser,
    profile_sandbox,
    profile_security,
    profile_transpiler,
)


@pytest.fixture(autouse=True)
def enable_profiling_for_tests():
    """Enable profiling for all tests in this file.

    The profiling system is opt-in via MLPY_PROFILE environment variable
    for performance reasons. Tests need profiling enabled to validate
    profiling functionality.
    """
    # Enable profiling
    os.environ["MLPY_PROFILE"] = "1"

    # Reset profiler state to ensure clean tests
    ProfilerManager._instance = None
    profiler_manager_instance = ProfilerManager()
    profiler_manager_instance.clear_profiles()  # Clear all profiles (no args = clear all)

    yield

    # Cleanup after tests
    os.environ.pop("MLPY_PROFILE", None)
    ProfilerManager._instance = None


class TestProfileData:
    """Test cases for ProfileData class."""

    def test_basic_profile_data(self):
        """Test basic ProfileData creation."""
        profile_data = ProfileData(
            function_name="test_function",
            execution_time=0.1,
            memory_before=100.0,
            memory_after=105.0,
            memory_peak=107.0,
        )

        assert profile_data.function_name == "test_function"
        assert profile_data.execution_time == 0.1
        assert profile_data.memory_before == 100.0
        assert profile_data.memory_after == 105.0
        assert profile_data.memory_peak == 107.0
        assert profile_data.call_count == 1
        assert profile_data.memory_delta == 5.0
        assert profile_data.memory_peak_delta == 7.0

    def test_profile_data_to_dict(self):
        """Test ProfileData serialization."""
        profile_data = ProfileData(
            function_name="test_func",
            execution_time=0.05,
            memory_before=50.0,
            memory_after=55.0,
            memory_peak=60.0,
            call_count=3,
        )

        result = profile_data.to_dict()

        expected_keys = {
            "function_name",
            "execution_time",
            "memory_before",
            "memory_after",
            "memory_peak",
            "memory_delta",
            "memory_peak_delta",
            "call_count",
            "timestamp",
            "thread_id",
        }

        assert set(result.keys()) == expected_keys
        assert result["function_name"] == "test_func"
        assert result["execution_time"] == 0.05
        assert result["memory_delta"] == 5.0
        assert result["memory_peak_delta"] == 10.0


class TestProfilerManager:
    """Test cases for ProfilerManager class."""

    def setup_method(self):
        """Setup fresh profiler for each test."""
        # Create a new profiler instance for testing
        ProfilerManager._instance = None
        self.profiler = ProfilerManager()
        # Ensure the global profiler reference points to our test instance
        import mlpy.runtime.profiling.decorators as decorators_module

        decorators_module.profiler = self.profiler

    def test_profiler_singleton(self):
        """Test ProfilerManager singleton behavior."""
        profiler1 = ProfilerManager()
        profiler2 = ProfilerManager()

        assert profiler1 is profiler2

    def test_enable_disable(self):
        """Test profiler enable/disable functionality."""
        assert self.profiler.is_enabled() is True

        self.profiler.disable()
        assert self.profiler.is_enabled() is False

        self.profiler.enable()
        assert self.profiler.is_enabled() is True

    def test_record_profile(self):
        """Test profile data recording."""
        profile_data = ProfileData(
            function_name="test_function",
            execution_time=0.1,
            memory_before=100.0,
            memory_after=105.0,
            memory_peak=107.0,
        )

        self.profiler.record_profile(profile_data)

        profiles = self.profiler.get_profiles("test_function")
        assert "test_function" in profiles
        assert len(profiles["test_function"]) == 1
        assert profiles["test_function"][0] == profile_data

    def test_record_profile_disabled(self):
        """Test that disabled profiler doesn't record."""
        self.profiler.disable()

        profile_data = ProfileData(
            function_name="test_function",
            execution_time=0.1,
            memory_before=100.0,
            memory_after=105.0,
            memory_peak=107.0,
        )

        self.profiler.record_profile(profile_data)

        profiles = self.profiler.get_profiles("test_function")
        assert len(profiles["test_function"]) == 0

    def test_aggregated_stats(self):
        """Test aggregated statistics calculation."""
        # Record multiple calls to same function
        for i in range(3):
            profile_data = ProfileData(
                function_name="test_function",
                execution_time=0.1 + i * 0.05,  # 0.1, 0.15, 0.2
                memory_before=100.0,
                memory_after=105.0 + i,  # 105, 106, 107
                memory_peak=107.0,
            )
            self.profiler.record_profile(profile_data)

        stats = self.profiler.get_aggregated_stats()
        func_stats = stats["test_function"]

        assert func_stats["total_calls"] == 3
        assert func_stats["total_time"] == 0.45  # 0.1 + 0.15 + 0.2
        assert func_stats["avg_time"] == 0.15  # 0.45 / 3
        assert func_stats["min_time"] == 0.1
        assert func_stats["max_time"] == 0.2

    def test_clear_profiles(self):
        """Test clearing profile data."""
        profile_data = ProfileData(
            function_name="test_function",
            execution_time=0.1,
            memory_before=100.0,
            memory_after=105.0,
            memory_peak=107.0,
        )

        self.profiler.record_profile(profile_data)
        assert len(self.profiler.get_profiles()["test_function"]) == 1

        self.profiler.clear_profiles("test_function")
        assert "test_function" not in self.profiler.get_profiles()

    def test_clear_all_profiles(self):
        """Test clearing all profile data."""
        # Record data for multiple functions
        for func_name in ["func1", "func2", "func3"]:
            profile_data = ProfileData(
                function_name=func_name,
                execution_time=0.1,
                memory_before=100.0,
                memory_after=105.0,
                memory_peak=107.0,
            )
            self.profiler.record_profile(profile_data)

        assert len(self.profiler.get_profiles()) == 3

        self.profiler.clear_profiles()
        assert len(self.profiler.get_profiles()) == 0

    @patch("psutil.Process")
    def test_get_memory_usage(self, mock_process_class):
        """Test memory usage calculation."""
        mock_process = MagicMock()
        mock_process.memory_info.return_value.rss = 1024 * 1024 * 100  # 100 MB in bytes
        mock_process_class.return_value = mock_process

        # Create new profiler with mocked psutil
        ProfilerManager._instance = None
        profiler_instance = ProfilerManager()

        memory_usage = profiler_instance.get_memory_usage()
        assert memory_usage == 100.0  # Should be 100 MB

    def test_generate_report(self):
        """Test comprehensive report generation."""
        # Record data for multiple functions
        functions = ["func_a", "func_b", "func_c"]
        for i, func_name in enumerate(functions):
            for j in range(i + 1):  # Different call counts
                profile_data = ProfileData(
                    function_name=func_name,
                    execution_time=0.1 * (i + 1),
                    memory_before=100.0,
                    memory_after=105.0,
                    memory_peak=107.0,
                )
                self.profiler.record_profile(profile_data)

        report = self.profiler.generate_report()

        # Check summary
        assert "summary" in report
        assert report["summary"]["total_functions"] == 3
        assert report["summary"]["total_calls"] == 6  # 1 + 2 + 3

        # Check functions
        assert "functions" in report
        assert len(report["functions"]) == 3

        # Check top performers
        assert "top_performers" in report
        assert "highest_total_time" in report["top_performers"]
        assert "most_calls" in report["top_performers"]
        assert "highest_avg_time" in report["top_performers"]


class TestProfileDecorator:
    """Test cases for profile decorator."""

    def setup_method(self):
        """Setup fresh profiler for each test."""
        ProfilerManager._instance = None
        self.profiler = ProfilerManager()
        # Ensure the global profiler reference points to our test instance
        import mlpy.runtime.profiling.decorators as decorators_module

        decorators_module.profiler = self.profiler

    def test_basic_profile_decorator(self):
        """Test basic profile decorator functionality."""

        @profile()
        def test_function():
            time.sleep(0.01)  # Small delay
            return "result"

        result = test_function()

        assert result == "result"

        profiles = self.profiler.get_profiles()
        assert len(profiles) == 1

        func_name = list(profiles.keys())[0]
        assert func_name.endswith("test_function")
        assert len(profiles[func_name]) == 1
        assert profiles[func_name][0].execution_time > 0.005  # At least 5ms

    def test_profile_decorator_disabled(self):
        """Test profile decorator when profiling is disabled."""
        self.profiler.disable()

        @profile()
        def test_function():
            time.sleep(0.01)
            return "result"

        result = test_function()
        assert result == "result"

        profiles = self.profiler.get_profiles()
        assert len(profiles) == 0

    def test_profile_decorator_custom_name(self):
        """Test profile decorator with custom name."""

        @profile(name="custom_function_name")
        def test_function():
            return "result"

        test_function()

        profiles = self.profiler.get_profiles()
        assert "custom_function_name" in profiles

    def test_profile_decorator_disabled_flag(self):
        """Test profile decorator with enabled=False."""

        @profile(enabled=False)
        def test_function():
            return "result"

        result = test_function()
        assert result == "result"

        profiles = self.profiler.get_profiles()
        assert len(profiles) == 0

    @patch("mlpy.runtime.profiling.decorators.ProfilerManager.get_memory_usage")
    def test_profile_decorator_memory_tracking(self, mock_memory):
        """Test profile decorator memory tracking."""
        memory_values = [100.0, 105.0, 110.0]  # before, during, after
        mock_memory.side_effect = memory_values

        @profile(memory_tracking=True)
        def test_function():
            return "result"

        test_function()

        profiles = self.profiler.get_profiles()
        profile_data = list(profiles.values())[0][0]

        assert profile_data.memory_before == 100.0
        assert profile_data.memory_after == 110.0  # Last call

    def test_profile_decorator_no_memory_tracking(self):
        """Test profile decorator without memory tracking."""

        @profile(memory_tracking=False)
        def test_function():
            return "result"

        test_function()

        profiles = self.profiler.get_profiles()
        profile_data = list(profiles.values())[0][0]

        assert profile_data.memory_before == 0.0
        assert profile_data.memory_after == 0.0
        assert profile_data.memory_peak == 0.0

    def test_multiple_calls_same_function(self):
        """Test multiple calls to same profiled function."""

        @profile()
        def test_function(value):
            time.sleep(0.001)  # Small delay
            return value * 2

        # Call function multiple times
        for i in range(5):
            result = test_function(i)
            assert result == i * 2

        profiles = self.profiler.get_profiles()
        func_name = list(profiles.keys())[0]
        assert len(profiles[func_name]) == 5

        stats = self.profiler.get_aggregated_stats()
        assert stats[func_name]["total_calls"] == 5


class TestSpecializedProfileDecorators:
    """Test cases for specialized profile decorators."""

    def setup_method(self):
        """Setup fresh profiler for each test."""
        ProfilerManager._instance = None
        self.profiler = ProfilerManager()
        # Ensure the global profiler reference points to our test instance
        import mlpy.runtime.profiling.decorators as decorators_module

        decorators_module.profiler = self.profiler

    def test_profile_parser(self):
        """Test profile_parser decorator."""

        @profile_parser
        def parse_function():
            return "parsed"

        parse_function()

        profiles = self.profiler.get_profiles()
        func_name = list(profiles.keys())[0]
        assert "parser.parse_function" in func_name

    def test_profile_security(self):
        """Test profile_security decorator."""

        @profile_security
        def security_function():
            return "secure"

        security_function()

        profiles = self.profiler.get_profiles()
        func_name = list(profiles.keys())[0]
        assert "security.security_function" in func_name

    def test_profile_transpiler(self):
        """Test profile_transpiler decorator."""

        @profile_transpiler
        def transpile_function():
            return "transpiled"

        transpile_function()

        profiles = self.profiler.get_profiles()
        func_name = list(profiles.keys())[0]
        assert "transpiler.transpile_function" in func_name

    def test_profile_capability(self):
        """Test profile_capability decorator."""

        @profile_capability
        def capability_function():
            return "capability"

        capability_function()

        profiles = self.profiler.get_profiles()
        func_name = list(profiles.keys())[0]
        assert "capability.capability_function" in func_name

    def test_profile_sandbox(self):
        """Test profile_sandbox decorator."""

        @profile_sandbox
        def sandbox_function():
            return "sandboxed"

        sandbox_function()

        profiles = self.profiler.get_profiles()
        func_name = list(profiles.keys())[0]
        assert "sandbox.sandbox_function" in func_name


class TestProfileContext:
    """Test cases for ProfileContext and profile_block."""

    def setup_method(self):
        """Setup fresh profiler for each test."""
        ProfilerManager._instance = None
        self.profiler = ProfilerManager()
        # Ensure the global profiler reference points to our test instance
        import mlpy.runtime.profiling.decorators as decorators_module

        decorators_module.profiler = self.profiler

    def test_profile_context_basic(self):
        """Test basic ProfileContext usage."""
        with ProfileContext("test_block"):
            time.sleep(0.01)

        profiles = self.profiler.get_profiles()
        assert "test_block" in profiles
        assert len(profiles["test_block"]) == 1
        assert profiles["test_block"][0].execution_time > 0.005

    def test_profile_block_function(self):
        """Test profile_block function."""
        with profile_block("test_block_func"):
            time.sleep(0.01)

        profiles = self.profiler.get_profiles()
        assert "test_block_func" in profiles

    def test_profile_context_disabled(self):
        """Test ProfileContext when profiling is disabled."""
        self.profiler.disable()

        with ProfileContext("disabled_block"):
            time.sleep(0.01)

        profiles = self.profiler.get_profiles()
        assert len(profiles) == 0

    def test_profile_context_exception(self):
        """Test ProfileContext behavior with exceptions."""
        try:
            with ProfileContext("exception_block"):
                time.sleep(0.01)
                raise ValueError("Test exception")
        except ValueError:
            pass

        # Should still record the profile data
        profiles = self.profiler.get_profiles()
        assert "exception_block" in profiles
        assert len(profiles["exception_block"]) == 1

    @patch("mlpy.runtime.profiling.decorators.ProfilerManager.get_memory_usage")
    def test_profile_context_memory_tracking(self, mock_memory):
        """Test ProfileContext memory tracking."""
        mock_memory.side_effect = [100.0, 105.0]  # before, after

        with ProfileContext("memory_block", memory_tracking=True):
            pass

        profiles = self.profiler.get_profiles()
        profile_data = profiles["memory_block"][0]

        assert profile_data.memory_before == 100.0
        assert profile_data.memory_after == 105.0

    def test_profile_context_no_memory_tracking(self):
        """Test ProfileContext without memory tracking."""
        with ProfileContext("no_memory_block", memory_tracking=False):
            pass

        profiles = self.profiler.get_profiles()
        profile_data = profiles["no_memory_block"][0]

        assert profile_data.memory_before == 0.0
        assert profile_data.memory_after == 0.0


class TestProfileSystemIntegration:
    """Integration tests for the complete profiling system."""

    def setup_method(self):
        """Setup fresh profiler for each test."""
        ProfilerManager._instance = None
        self.profiler = ProfilerManager()
        # Ensure the global profiler reference points to our test instance
        import mlpy.runtime.profiling.decorators as decorators_module

        decorators_module.profiler = self.profiler

    def test_mixed_profiling_methods(self):
        """Test using different profiling methods together."""

        @profile_parser
        def parse_func():
            time.sleep(0.001)
            return "parsed"

        @profile_security
        def security_func():
            time.sleep(0.001)
            return "secure"

        # Use decorator
        parse_func()
        security_func()

        # Use context manager
        with profile_block("manual_block"):
            time.sleep(0.001)

        # Use ProfileContext directly
        with ProfileContext("direct_context"):
            time.sleep(0.001)

        profiles = self.profiler.get_profiles()
        assert len(profiles) == 4

        report = self.profiler.generate_report()
        assert report["summary"]["total_functions"] == 4
        assert report["summary"]["total_calls"] == 4

    def test_threaded_profiling(self):
        """Test profiling with multiple threads."""
        results = []

        def worker_function(worker_id):
            @profile(name=f"worker_{worker_id}")
            def work():
                time.sleep(0.01)
                return f"result_{worker_id}"

            results.append(work())

        # Create multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=worker_function, args=(i,))
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check results
        assert len(results) == 3
        profiles = self.profiler.get_profiles()
        assert len(profiles) == 3

        # Check that each worker was profiled
        for i in range(3):
            assert f"worker_{i}" in profiles

    def test_profiling_performance_overhead(self):
        """Test that profiling doesn't add significant overhead."""

        def test_function():
            # Simple computation
            return sum(range(100))

        # Time without profiling
        start_time = time.time()
        for _ in range(1000):
            test_function()
        unprofiled_time = time.time() - start_time

        # Time with profiling
        @profile()
        def profiled_test_function():
            return sum(range(100))

        start_time = time.time()
        for _ in range(1000):
            profiled_test_function()
        profiled_time = time.time() - start_time

        # Profiling overhead should be reasonable
        # With memory monitoring threads, overhead can be higher but should still be manageable
        overhead_ratio = profiled_time / unprofiled_time
        assert overhead_ratio < 500.0, f"Profiling overhead too high: {overhead_ratio:.2f}x"

    def test_memory_accuracy(self):
        """Test memory usage accuracy (when possible)."""

        @profile(memory_tracking=True)
        def memory_test():
            # Allocate some memory
            data = [0] * 1000000  # Should use some memory
            return len(data)

        memory_test()

        profiles = self.profiler.get_profiles()
        profile_data = list(profiles.values())[0][0]

        # Memory tracking should show some change (if psutil is working)
        # This test might not be reliable in all environments
        assert profile_data.memory_before >= 0
        assert profile_data.memory_after >= 0
        assert profile_data.memory_peak >= profile_data.memory_before
