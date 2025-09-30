"""Performance profiling decorators for mlpy components."""

import functools
import os
import threading
import time
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Optional, TypeVar

import psutil

F = TypeVar("F", bound=Callable[..., Any])


@dataclass
class ProfileData:
    """Performance profiling data for a function call."""

    function_name: str
    execution_time: float
    memory_before: float
    memory_after: float
    memory_peak: float
    call_count: int = 1
    timestamp: float = field(default_factory=time.time)
    thread_id: int = field(default_factory=lambda: threading.get_ident())

    @property
    def memory_delta(self) -> float:
        """Memory usage difference in MB."""
        return self.memory_after - self.memory_before

    @property
    def memory_peak_delta(self) -> float:
        """Peak memory increase in MB."""
        return self.memory_peak - self.memory_before

    def to_dict(self) -> dict[str, Any]:
        """Convert profile data to dictionary."""
        return {
            "function_name": self.function_name,
            "execution_time": self.execution_time,
            "memory_before": self.memory_before,
            "memory_after": self.memory_after,
            "memory_peak": self.memory_peak,
            "memory_delta": self.memory_delta,
            "memory_peak_delta": self.memory_peak_delta,
            "call_count": self.call_count,
            "timestamp": self.timestamp,
            "thread_id": self.thread_id,
        }


class ProfilerManager:
    """Global profiler manager for collecting performance data."""

    _instance: Optional["ProfilerManager"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "ProfilerManager":
        """Singleton pattern for global profiler."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize profiler manager."""
        if hasattr(self, "_initialized") and self._initialized:
            return

        self._profiles: dict[str, list[ProfileData]] = defaultdict(list)
        self._aggregated: dict[str, dict[str, Any]] = {}
        # Profiling is opt-in via MLPY_PROFILE environment variable
        self._enabled = os.environ.get("MLPY_PROFILE", "0").lower() in ("1", "true", "yes", "on")
        self._lock = threading.RLock()
        self._process = psutil.Process(os.getpid())
        self._initialized = True

    def enable(self) -> None:
        """Enable profiling."""
        self._enabled = True

    def disable(self) -> None:
        """Disable profiling."""
        self._enabled = False

    def is_enabled(self) -> bool:
        """Check if profiling is enabled."""
        return self._enabled

    def record_profile(self, profile_data: ProfileData) -> None:
        """Record profile data."""
        if not self._enabled:
            return

        with self._lock:
            self._profiles[profile_data.function_name].append(profile_data)
            self._update_aggregated(profile_data)

    def _update_aggregated(self, profile_data: ProfileData) -> None:
        """Update aggregated statistics."""
        func_name = profile_data.function_name

        if func_name not in self._aggregated:
            self._aggregated[func_name] = {
                "total_calls": 0,
                "total_time": 0.0,
                "avg_time": 0.0,
                "min_time": float("inf"),
                "max_time": 0.0,
                "total_memory_delta": 0.0,
                "avg_memory_delta": 0.0,
                "max_memory_peak": 0.0,
            }

        stats = self._aggregated[func_name]
        stats["total_calls"] += 1
        stats["total_time"] += profile_data.execution_time
        stats["avg_time"] = stats["total_time"] / stats["total_calls"]
        stats["min_time"] = min(stats["min_time"], profile_data.execution_time)
        stats["max_time"] = max(stats["max_time"], profile_data.execution_time)
        stats["total_memory_delta"] += profile_data.memory_delta
        stats["avg_memory_delta"] = stats["total_memory_delta"] / stats["total_calls"]
        stats["max_memory_peak"] = max(stats["max_memory_peak"], profile_data.memory_peak_delta)

    def get_profiles(self, function_name: str | None = None) -> dict[str, list[ProfileData]]:
        """Get profile data for a specific function or all functions."""
        with self._lock:
            if function_name:
                return {function_name: self._profiles.get(function_name, [])}
            return dict(self._profiles)

    def get_aggregated_stats(self) -> dict[str, dict[str, Any]]:
        """Get aggregated statistics for all profiled functions."""
        with self._lock:
            return dict(self._aggregated)

    def clear_profiles(self, function_name: str | None = None) -> None:
        """Clear profile data."""
        with self._lock:
            if function_name:
                self._profiles.pop(function_name, None)
                self._aggregated.pop(function_name, None)
            else:
                self._profiles.clear()
                self._aggregated.clear()

    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            return self._process.memory_info().rss / 1024 / 1024
        except Exception:
            return 0.0

    def generate_report(self) -> dict[str, Any]:
        """Generate comprehensive profiling report."""
        with self._lock:
            report = {
                "summary": {
                    "total_functions": len(self._aggregated),
                    "total_calls": sum(stats["total_calls"] for stats in self._aggregated.values()),
                    "total_time": sum(stats["total_time"] for stats in self._aggregated.values()),
                },
                "functions": {},
                "top_performers": {},
            }

            # Add function details
            for func_name, stats in self._aggregated.items():
                report["functions"][func_name] = {
                    **stats,
                    "recent_calls": [
                        profile.to_dict()
                        for profile in self._profiles[func_name][-5:]  # Last 5 calls
                    ],
                }

            # Top performers by different metrics
            if self._aggregated:
                sorted_by_time = sorted(
                    self._aggregated.items(), key=lambda x: x[1]["total_time"], reverse=True
                )
                sorted_by_calls = sorted(
                    self._aggregated.items(), key=lambda x: x[1]["total_calls"], reverse=True
                )
                sorted_by_avg_time = sorted(
                    self._aggregated.items(), key=lambda x: x[1]["avg_time"], reverse=True
                )

                report["top_performers"] = {
                    "highest_total_time": sorted_by_time[:5],
                    "most_calls": sorted_by_calls[:5],
                    "highest_avg_time": sorted_by_avg_time[:5],
                }

            return report


# Global profiler instance
profiler = ProfilerManager()


def profile(
    name: str | None = None,
    enabled: bool = True,
    memory_tracking: bool = True,
) -> Callable[[F], F]:
    """Decorator for profiling function performance.

    Args:
        name: Custom name for the profiled function
        enabled: Whether profiling is enabled for this function
        memory_tracking: Whether to track memory usage

    Returns:
        Decorated function with profiling
    """

    def decorator(func: F) -> F:
        if not enabled or not profiler.is_enabled():
            return func

        profile_name = name or f"{func.__module__}.{func.__qualname__}"

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not profiler.is_enabled():
                return func(*args, **kwargs)

            # Memory tracking
            memory_before = profiler.get_memory_usage() if memory_tracking else 0.0
            memory_peak = memory_before
            stop_monitoring = threading.Event()

            def memory_monitor() -> None:
                nonlocal memory_peak
                while not stop_monitoring.is_set():
                    current_memory = profiler.get_memory_usage()
                    memory_peak = max(memory_peak, current_memory)
                    if stop_monitoring.wait(0.001):  # Check every 1ms or until stopped
                        break

            # Start memory monitoring in background
            monitor_thread = None
            if memory_tracking:
                monitor_thread = threading.Thread(target=memory_monitor, daemon=True)
                monitor_thread.start()

            # Execute function with timing
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                execution_time = end_time - start_time

                # Stop memory monitoring
                if monitor_thread:
                    stop_monitoring.set()  # Signal the monitor thread to stop
                    monitor_thread.join(timeout=0.1)  # Wait for thread to finish (increased timeout)

                memory_after = profiler.get_memory_usage() if memory_tracking else 0.0

                # Record profile data
                profile_data = ProfileData(
                    function_name=profile_name,
                    execution_time=execution_time,
                    memory_before=memory_before,
                    memory_after=memory_after,
                    memory_peak=memory_peak,
                )

                profiler.record_profile(profile_data)

        return wrapper

    return decorator


def profile_parser(func: F) -> F:
    """Specialized profiling decorator for parser functions."""
    return profile(name=f"parser.{func.__name__}", memory_tracking=True)(func)


def profile_security(func: F) -> F:
    """Specialized profiling decorator for security analysis functions."""
    return profile(name=f"security.{func.__name__}", memory_tracking=False)(func)


def profile_transpiler(func: F) -> F:
    """Specialized profiling decorator for transpiler functions."""
    return profile(name=f"transpiler.{func.__name__}", memory_tracking=True)(func)


def profile_capability(func: F) -> F:
    """Specialized profiling decorator for capability system functions."""
    return profile(name=f"capability.{func.__name__}", memory_tracking=False)(func)


def profile_sandbox(func: F) -> F:
    """Specialized profiling decorator for sandbox functions."""
    return profile(name=f"sandbox.{func.__name__}", memory_tracking=True)(func)


# Context manager for profiling code blocks
class ProfileContext:
    """Context manager for profiling code blocks."""

    def __init__(self, name: str, memory_tracking: bool = True) -> None:
        """Initialize profile context.

        Args:
            name: Name for the profiled block
            memory_tracking: Whether to track memory usage
        """
        self.name = name
        self.memory_tracking = memory_tracking
        self.start_time: float = 0.0
        self.memory_before: float = 0.0
        self.memory_peak: float = 0.0

    def __enter__(self) -> "ProfileContext":
        """Enter profiling context."""
        if profiler.is_enabled():
            self.start_time = time.perf_counter()
            if self.memory_tracking:
                self.memory_before = profiler.get_memory_usage()
                self.memory_peak = self.memory_before
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit profiling context and record data."""
        if profiler.is_enabled():
            end_time = time.perf_counter()
            execution_time = end_time - self.start_time

            memory_after = profiler.get_memory_usage() if self.memory_tracking else 0.0

            profile_data = ProfileData(
                function_name=self.name,
                execution_time=execution_time,
                memory_before=self.memory_before,
                memory_after=memory_after,
                memory_peak=self.memory_peak,
            )

            profiler.record_profile(profile_data)


def profile_block(name: str, memory_tracking: bool = True) -> ProfileContext:
    """Create a profiling context manager for code blocks.

    Args:
        name: Name for the profiled block
        memory_tracking: Whether to track memory usage

    Returns:
        ProfileContext for use with 'with' statement
    """
    return ProfileContext(name, memory_tracking)
