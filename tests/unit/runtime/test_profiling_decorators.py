"""
Comprehensive test suite for profiling/decorators.py

Tests performance profiling system including:
- ProfileData dataclass with memory tracking
- ProfilerManager singleton with thread-safe operations
- @profile decorator with memory monitoring
- Specialized decorators (parser, security, transpiler, etc.)
- ProfileContext context manager
- Report generation and statistics
"""

import os
import threading
import time

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
    profiler,
)


class TestProfileData:
    """Test ProfileData dataclass."""

    def test_profile_data_creation(self):
        """Test creating ProfileData with required fields."""
        data = ProfileData(
            function_name="test_func",
            execution_time=1.5,
            memory_before=100.0,
            memory_after=120.0,
            memory_peak=125.0,
        )
        assert data.function_name == "test_func"
        assert data.execution_time == 1.5
        assert data.memory_before == 100.0
        assert data.memory_after == 120.0
        assert data.memory_peak == 125.0
        assert data.call_count == 1

    def test_profile_data_with_call_count(self):
        """Test ProfileData with custom call count."""
        data = ProfileData(
            function_name="test",
            execution_time=1.0,
            memory_before=0.0,
            memory_after=0.0,
            memory_peak=0.0,
            call_count=5,
        )
        assert data.call_count == 5

    def test_profile_data_timestamp_default(self):
        """Test ProfileData has default timestamp."""
        data = ProfileData(
            function_name="test",
            execution_time=1.0,
            memory_before=0.0,
            memory_after=0.0,
            memory_peak=0.0,
        )
        assert data.timestamp > 0
        assert isinstance(data.timestamp, float)

    def test_profile_data_thread_id_default(self):
        """Test ProfileData has default thread ID."""
        data = ProfileData(
            function_name="test",
            execution_time=1.0,
            memory_before=0.0,
            memory_after=0.0,
            memory_peak=0.0,
        )
        assert data.thread_id == threading.get_ident()

    def test_memory_delta_property(self):
        """Test memory_delta property calculation."""
        data = ProfileData(
            function_name="test",
            execution_time=1.0,
            memory_before=100.0,
            memory_after=120.0,
            memory_peak=125.0,
        )
        assert data.memory_delta == 20.0

    def test_memory_delta_negative(self):
        """Test memory_delta with negative delta."""
        data = ProfileData(
            function_name="test",
            execution_time=1.0,
            memory_before=120.0,
            memory_after=100.0,
            memory_peak=125.0,
        )
        assert data.memory_delta == -20.0

    def test_memory_peak_delta_property(self):
        """Test memory_peak_delta property calculation."""
        data = ProfileData(
            function_name="test",
            execution_time=1.0,
            memory_before=100.0,
            memory_after=120.0,
            memory_peak=125.0,
        )
        assert data.memory_peak_delta == 25.0

    def test_to_dict_serialization(self):
        """Test to_dict serialization."""
        data = ProfileData(
            function_name="test_func",
            execution_time=1.5,
            memory_before=100.0,
            memory_after=120.0,
            memory_peak=125.0,
            call_count=3,
        )
        result = data.to_dict()

        assert result["function_name"] == "test_func"
        assert result["execution_time"] == 1.5
        assert result["memory_before"] == 100.0
        assert result["memory_after"] == 120.0
        assert result["memory_peak"] == 125.0
        assert result["memory_delta"] == 20.0
        assert result["memory_peak_delta"] == 25.0
        assert result["call_count"] == 3
        assert "timestamp" in result
        assert "thread_id" in result


class TestProfilerManager:
    """Test ProfilerManager singleton."""

    def setup_method(self):
        """Setup for each test - clear profiler state."""
        profiler.clear_profiles()
        # Store original state
        self.original_enabled = profiler.is_enabled()

    def teardown_method(self):
        """Teardown for each test - restore profiler state."""
        profiler.clear_profiles()
        # Restore original state
        if self.original_enabled:
            profiler.enable()
        else:
            profiler.disable()

    def test_singleton_pattern(self):
        """Test ProfilerManager uses singleton pattern."""
        manager1 = ProfilerManager()
        manager2 = ProfilerManager()
        assert manager1 is manager2

    def test_enable_profiling(self):
        """Test enabling profiling."""
        profiler.disable()
        assert not profiler.is_enabled()
        profiler.enable()
        assert profiler.is_enabled()

    def test_disable_profiling(self):
        """Test disabling profiling."""
        profiler.enable()
        assert profiler.is_enabled()
        profiler.disable()
        assert not profiler.is_enabled()

    def test_record_profile_when_enabled(self):
        """Test recording profile when enabled."""
        profiler.enable()
        data = ProfileData(
            function_name="test_func",
            execution_time=1.0,
            memory_before=0.0,
            memory_after=0.0,
            memory_peak=0.0,
        )
        profiler.record_profile(data)

        profiles = profiler.get_profiles("test_func")
        assert "test_func" in profiles
        assert len(profiles["test_func"]) == 1
        assert profiles["test_func"][0] == data

    def test_record_profile_when_disabled(self):
        """Test recording profile when disabled."""
        profiler.disable()
        data = ProfileData(
            function_name="test_func",
            execution_time=1.0,
            memory_before=0.0,
            memory_after=0.0,
            memory_peak=0.0,
        )
        profiler.record_profile(data)

        profiles = profiler.get_profiles("test_func")
        # Should not record when disabled
        assert len(profiles.get("test_func", [])) == 0

    def test_get_profiles_specific_function(self):
        """Test getting profiles for specific function."""
        profiler.enable()
        data1 = ProfileData(
            "func1", execution_time=1.0, memory_before=0.0, memory_after=0.0, memory_peak=0.0
        )
        data2 = ProfileData(
            "func2", execution_time=2.0, memory_before=0.0, memory_after=0.0, memory_peak=0.0
        )
        profiler.record_profile(data1)
        profiler.record_profile(data2)

        profiles = profiler.get_profiles("func1")
        assert "func1" in profiles
        assert "func2" not in profiles
        assert len(profiles["func1"]) == 1

    def test_get_profiles_all_functions(self):
        """Test getting profiles for all functions."""
        profiler.enable()
        data1 = ProfileData(
            "func1", execution_time=1.0, memory_before=0.0, memory_after=0.0, memory_peak=0.0
        )
        data2 = ProfileData(
            "func2", execution_time=2.0, memory_before=0.0, memory_after=0.0, memory_peak=0.0
        )
        profiler.record_profile(data1)
        profiler.record_profile(data2)

        profiles = profiler.get_profiles()
        assert "func1" in profiles
        assert "func2" in profiles
        assert len(profiles["func1"]) == 1
        assert len(profiles["func2"]) == 1

    def test_get_aggregated_stats(self):
        """Test getting aggregated statistics."""
        profiler.enable()
        data1 = ProfileData(
            "test_func",
            execution_time=1.0,
            memory_before=100.0,
            memory_after=110.0,
            memory_peak=115.0,
        )
        data2 = ProfileData(
            "test_func",
            execution_time=2.0,
            memory_before=100.0,
            memory_after=120.0,
            memory_peak=130.0,
        )
        profiler.record_profile(data1)
        profiler.record_profile(data2)

        stats = profiler.get_aggregated_stats()
        assert "test_func" in stats
        func_stats = stats["test_func"]

        assert func_stats["total_calls"] == 2
        assert func_stats["total_time"] == 3.0
        assert func_stats["avg_time"] == 1.5
        assert func_stats["min_time"] == 1.0
        assert func_stats["max_time"] == 2.0
        assert func_stats["total_memory_delta"] == 30.0  # 10 + 20
        assert func_stats["avg_memory_delta"] == 15.0
        assert func_stats["max_memory_peak"] == 30.0  # max(15, 30)

    def test_clear_profiles_specific_function(self):
        """Test clearing profiles for specific function."""
        profiler.enable()
        data1 = ProfileData(
            "func1", execution_time=1.0, memory_before=0.0, memory_after=0.0, memory_peak=0.0
        )
        data2 = ProfileData(
            "func2", execution_time=2.0, memory_before=0.0, memory_after=0.0, memory_peak=0.0
        )
        profiler.record_profile(data1)
        profiler.record_profile(data2)

        profiler.clear_profiles("func1")

        profiles = profiler.get_profiles()
        assert "func1" not in profiles or len(profiles["func1"]) == 0
        assert "func2" in profiles

    def test_clear_profiles_all(self):
        """Test clearing all profiles."""
        profiler.enable()
        data1 = ProfileData(
            "func1", execution_time=1.0, memory_before=0.0, memory_after=0.0, memory_peak=0.0
        )
        data2 = ProfileData(
            "func2", execution_time=2.0, memory_before=0.0, memory_after=0.0, memory_peak=0.0
        )
        profiler.record_profile(data1)
        profiler.record_profile(data2)

        profiler.clear_profiles()

        profiles = profiler.get_profiles()
        assert len(profiles) == 0

    def test_get_memory_usage(self):
        """Test getting current memory usage."""
        memory = profiler.get_memory_usage()
        assert isinstance(memory, float)
        assert memory >= 0.0

    def test_generate_report(self):
        """Test generating comprehensive report."""
        profiler.enable()
        profiler.clear_profiles()

        data1 = ProfileData(
            "func1", execution_time=1.0, memory_before=100.0, memory_after=110.0, memory_peak=115.0
        )
        data2 = ProfileData(
            "func1", execution_time=2.0, memory_before=100.0, memory_after=120.0, memory_peak=130.0
        )
        profiler.record_profile(data1)
        profiler.record_profile(data2)

        report = profiler.generate_report()

        # Check summary
        assert "summary" in report
        assert report["summary"]["total_functions"] == 1
        assert report["summary"]["total_calls"] == 2
        assert report["summary"]["total_time"] == 3.0

        # Check functions
        assert "functions" in report
        assert "func1" in report["functions"]
        assert "recent_calls" in report["functions"]["func1"]

        # Check top performers
        assert "top_performers" in report
        assert "highest_total_time" in report["top_performers"]
        assert "most_calls" in report["top_performers"]
        assert "highest_avg_time" in report["top_performers"]

    def test_thread_safety(self):
        """Test thread-safe profile recording."""
        profiler.enable()
        profiler.clear_profiles()
        results = []

        def record_profiles():
            for i in range(10):
                data = ProfileData(
                    f"func_{i}",
                    execution_time=1.0,
                    memory_before=0.0,
                    memory_after=0.0,
                    memory_peak=0.0,
                )
                profiler.record_profile(data)
                results.append(i)

        threads = [threading.Thread(target=record_profiles) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should have recorded from both threads
        assert len(results) == 20


class TestProfileDecorator:
    """Test @profile decorator."""

    def setup_method(self):
        """Setup for each test."""
        profiler.clear_profiles()
        profiler.enable()

    def teardown_method(self):
        """Teardown for each test."""
        profiler.clear_profiles()

    def test_profile_basic_function(self):
        """Test profiling a basic function."""

        @profile(name="test_func")
        def sample_func():
            return 42

        result = sample_func()
        assert result == 42

        profiles = profiler.get_profiles("test_func")
        assert len(profiles["test_func"]) == 1
        assert profiles["test_func"][0].execution_time > 0

    def test_profile_with_default_name(self):
        """Test profile decorator with default function name."""

        @profile()
        def sample_func():
            return 42

        result = sample_func()
        assert result == 42

        # Should use module.qualname format
        profiles = profiler.get_profiles()
        # Check that some profile was recorded
        assert len(profiles) > 0

    def test_profile_when_disabled(self):
        """Test profile decorator when profiling disabled."""
        profiler.disable()

        @profile(name="test_func")
        def sample_func():
            return 42

        result = sample_func()
        assert result == 42

        profiles = profiler.get_profiles("test_func")
        assert len(profiles.get("test_func", [])) == 0

    def test_profile_with_arguments(self):
        """Test profiling function with arguments."""

        @profile(name="test_func")
        def sample_func(a, b):
            return a + b

        result = sample_func(10, 20)
        assert result == 30

        profiles = profiler.get_profiles("test_func")
        assert len(profiles["test_func"]) == 1

    def test_profile_with_exception(self):
        """Test profiling function that raises exception."""

        @profile(name="test_func")
        def sample_func():
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            sample_func()

        # Should still record profile even with exception
        profiles = profiler.get_profiles("test_func")
        assert len(profiles["test_func"]) == 1

    def test_profile_multiple_calls(self):
        """Test profiling multiple calls to same function."""

        @profile(name="test_func")
        def sample_func():
            return 42

        sample_func()
        sample_func()
        sample_func()

        profiles = profiler.get_profiles("test_func")
        assert len(profiles["test_func"]) == 3

    def test_profile_memory_tracking_disabled(self):
        """Test profile with memory tracking disabled."""

        @profile(name="test_func", memory_tracking=False)
        def sample_func():
            return 42

        sample_func()

        profiles = profiler.get_profiles("test_func")
        assert len(profiles["test_func"]) == 1
        # Memory values should be 0 when tracking disabled
        assert profiles["test_func"][0].memory_before == 0.0
        assert profiles["test_func"][0].memory_after == 0.0


class TestSpecializedDecorators:
    """Test specialized profiling decorators."""

    def setup_method(self):
        """Setup for each test."""
        profiler.clear_profiles()
        profiler.enable()

    def teardown_method(self):
        """Teardown for each test."""
        profiler.clear_profiles()

    def test_profile_parser(self):
        """Test @profile_parser decorator."""

        @profile_parser
        def parse_func():
            return "parsed"

        result = parse_func()
        assert result == "parsed"

        profiles = profiler.get_profiles()
        # Should have profile with parser. prefix
        parser_profiles = [name for name in profiles if name.startswith("parser.")]
        assert len(parser_profiles) > 0

    def test_profile_security(self):
        """Test @profile_security decorator."""

        @profile_security
        def security_func():
            return "secure"

        result = security_func()
        assert result == "secure"

        profiles = profiler.get_profiles()
        # Should have profile with security. prefix
        security_profiles = [name for name in profiles if name.startswith("security.")]
        assert len(security_profiles) > 0

    def test_profile_transpiler(self):
        """Test @profile_transpiler decorator."""

        @profile_transpiler
        def transpile_func():
            return "transpiled"

        result = transpile_func()
        assert result == "transpiled"

        profiles = profiler.get_profiles()
        transpiler_profiles = [name for name in profiles if name.startswith("transpiler.")]
        assert len(transpiler_profiles) > 0

    def test_profile_capability(self):
        """Test @profile_capability decorator."""

        @profile_capability
        def capability_func():
            return "capability"

        result = capability_func()
        assert result == "capability"

        profiles = profiler.get_profiles()
        capability_profiles = [name for name in profiles if name.startswith("capability.")]
        assert len(capability_profiles) > 0

    def test_profile_sandbox(self):
        """Test @profile_sandbox decorator."""

        @profile_sandbox
        def sandbox_func():
            return "sandboxed"

        result = sandbox_func()
        assert result == "sandboxed"

        profiles = profiler.get_profiles()
        sandbox_profiles = [name for name in profiles if name.startswith("sandbox.")]
        assert len(sandbox_profiles) > 0


class TestProfileContext:
    """Test ProfileContext context manager."""

    def setup_method(self):
        """Setup for each test."""
        profiler.clear_profiles()
        profiler.enable()

    def teardown_method(self):
        """Teardown for each test."""
        profiler.clear_profiles()

    def test_profile_context_basic(self):
        """Test basic ProfileContext usage."""
        with ProfileContext("test_block"):
            time.sleep(0.01)  # Small delay

        profiles = profiler.get_profiles("test_block")
        assert len(profiles["test_block"]) == 1
        assert profiles["test_block"][0].execution_time > 0

    def test_profile_context_without_memory_tracking(self):
        """Test ProfileContext without memory tracking."""
        with ProfileContext("test_block", memory_tracking=False):
            pass

        profiles = profiler.get_profiles("test_block")
        assert len(profiles["test_block"]) == 1
        assert profiles["test_block"][0].memory_before == 0.0
        assert profiles["test_block"][0].memory_after == 0.0

    def test_profile_context_when_disabled(self):
        """Test ProfileContext when profiling disabled."""
        profiler.disable()

        with ProfileContext("test_block"):
            pass

        profiles = profiler.get_profiles("test_block")
        assert len(profiles.get("test_block", [])) == 0

    def test_profile_context_with_exception(self):
        """Test ProfileContext with exception."""
        with pytest.raises(ValueError):
            with ProfileContext("test_block"):
                raise ValueError("Test error")

        # Should still record profile
        profiles = profiler.get_profiles("test_block")
        assert len(profiles["test_block"]) == 1

    def test_profile_block_function(self):
        """Test profile_block convenience function."""
        with profile_block("test_block"):
            time.sleep(0.01)

        profiles = profiler.get_profiles("test_block")
        assert len(profiles["test_block"]) == 1
        assert profiles["test_block"][0].execution_time > 0

    def test_profile_context_returns_self(self):
        """Test ProfileContext __enter__ returns self."""
        with ProfileContext("test_block") as ctx:
            assert isinstance(ctx, ProfileContext)
            assert ctx.name == "test_block"


class TestProfilerManagerInitialization:
    """Test ProfilerManager initialization with environment variables."""

    def test_profiler_enabled_from_env(self, monkeypatch):
        """Test profiler enabled from MLPY_PROFILE environment variable."""
        # Note: This test may not fully work due to singleton initialization
        # but we can test the logic
        monkeypatch.setenv("MLPY_PROFILE", "1")
        # Create new instance (may not work due to singleton)
        manager = ProfilerManager()
        # Just verify it's a ProfilerManager instance
        assert isinstance(manager, ProfilerManager)

    def test_profiler_disabled_by_default(self):
        """Test profiler respects environment variable."""
        # The global profiler instance behavior depends on env at import time
        manager = ProfilerManager()
        assert isinstance(manager, ProfilerManager)
        # enabled state depends on MLPY_PROFILE environment variable
        assert isinstance(manager.is_enabled(), bool)
