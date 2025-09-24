"""Resource monitoring and limits enforcement for sandbox execution."""

import threading
import time
from dataclasses import dataclass
from typing import Any

import psutil


@dataclass
class ResourceLimits:
    """Resource limits configuration."""

    memory_limit: int = 100 * 1024 * 1024  # 100MB in bytes
    cpu_timeout: float = 30.0  # seconds
    file_size_limit: int = 10 * 1024 * 1024  # 10MB in bytes
    temp_dir_limit: int = 50 * 1024 * 1024  # 50MB in bytes
    max_file_handles: int = 100
    max_threads: int = 10


class ResourceMonitorError(Exception):
    """Exception raised for resource monitoring errors."""

    pass


class ResourceLimitExceeded(ResourceMonitorError):
    """Exception raised when resource limits are exceeded."""

    def __init__(self, resource_type: str, limit: Any, current: Any):
        self.resource_type = resource_type
        self.limit = limit
        self.current = current
        super().__init__(f"{resource_type} limit exceeded: {current} > {limit}")


class ResourceMonitor:
    """Monitor resource usage for sandbox processes."""

    def __init__(self):
        """Initialize the resource monitor."""
        self.limits: ResourceLimits | None = None
        self.monitoring = False
        self.process: psutil.Process | None = None
        self._monitor_thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()

        # Resource usage tracking
        self._usage_history: list[dict[str, Any]] = []
        self._peak_memory = 0
        self._total_cpu_time = 0.0
        self._start_time = 0.0

    def set_limits(self, limits: ResourceLimits) -> None:
        """Set resource limits for monitoring."""
        with self._lock:
            self.limits = limits

    def start_monitoring(self, pid: int) -> None:
        """Start monitoring a process by PID."""
        with self._lock:
            if self.monitoring:
                raise ResourceMonitorError("Already monitoring a process")

            try:
                self.process = psutil.Process(pid)
                self.monitoring = True
                self._start_time = time.time()
                self._stop_event.clear()

                # Start monitoring thread
                self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
                self._monitor_thread.start()

            except psutil.NoSuchProcess:
                raise ResourceMonitorError(f"Process {pid} not found")

    def stop_monitoring(self) -> None:
        """Stop resource monitoring."""
        with self._lock:
            if not self.monitoring:
                return

            self.monitoring = False
            self._stop_event.set()

            # Wait for monitor thread to finish
            if self._monitor_thread and self._monitor_thread.is_alive():
                self._monitor_thread.join(timeout=2.0)

            self.process = None

    def _monitor_loop(self) -> None:
        """Main monitoring loop running in separate thread."""
        check_interval = 0.1  # Check every 100ms

        while not self._stop_event.is_set() and self.monitoring:
            try:
                self._check_resources()
                time.sleep(check_interval)

            except psutil.NoSuchProcess:
                # Process ended
                break

            except ResourceLimitExceeded as e:
                # Resource limit exceeded - terminate process
                self._terminate_process(e)
                break

            except Exception:
                # Other errors - continue monitoring
                time.sleep(check_interval)

    def _check_resources(self) -> None:
        """Check resource usage against limits."""
        if not self.process or not self.limits:
            return

        # Get current usage
        usage = self._get_current_usage()

        # Record usage history
        with self._lock:
            self._usage_history.append({"timestamp": time.time(), **usage})

            # Update peaks
            self._peak_memory = max(self._peak_memory, usage["memory"])

        # Check limits
        self._enforce_limits(usage)

    def _get_current_usage(self) -> dict[str, Any]:
        """Get current resource usage."""
        if not self.process:
            return {}

        try:
            # Memory usage
            memory_info = self.process.memory_info()
            memory_usage = memory_info.rss  # Resident Set Size

            # CPU usage (percentage)
            cpu_percent = self.process.cpu_percent()

            # Number of open file handles
            try:
                file_handles = len(self.process.open_files())
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                file_handles = 0

            # Number of threads
            try:
                num_threads = self.process.num_threads()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                num_threads = 0

            # Execution time
            elapsed_time = time.time() - self._start_time

            return {
                "memory": memory_usage,
                "cpu_percent": cpu_percent,
                "file_handles": file_handles,
                "num_threads": num_threads,
                "elapsed_time": elapsed_time,
            }

        except psutil.NoSuchProcess:
            return {}

    def _enforce_limits(self, usage: dict[str, Any]) -> None:
        """Enforce resource limits."""
        if not self.limits:
            return

        # Check memory limit
        if self.limits.memory_limit > 0 and usage.get("memory", 0) > self.limits.memory_limit:
            raise ResourceLimitExceeded("memory", self.limits.memory_limit, usage["memory"])

        # Check CPU timeout
        if self.limits.cpu_timeout > 0 and usage.get("elapsed_time", 0) > self.limits.cpu_timeout:
            raise ResourceLimitExceeded(
                "cpu_timeout", self.limits.cpu_timeout, usage["elapsed_time"]
            )

        # Check file handles
        if (
            self.limits.max_file_handles > 0
            and usage.get("file_handles", 0) > self.limits.max_file_handles
        ):
            raise ResourceLimitExceeded(
                "file_handles", self.limits.max_file_handles, usage["file_handles"]
            )

        # Check thread count
        if self.limits.max_threads > 0 and usage.get("num_threads", 0) > self.limits.max_threads:
            raise ResourceLimitExceeded(
                "num_threads", self.limits.max_threads, usage["num_threads"]
            )

    def _terminate_process(self, limit_error: ResourceLimitExceeded) -> None:
        """Terminate process due to resource limit violation."""
        if not self.process:
            return

        try:
            # Try graceful termination first
            self.process.terminate()

            # Wait briefly for graceful shutdown
            try:
                self.process.wait(timeout=2.0)
            except psutil.TimeoutExpired:
                # Force kill if graceful termination fails
                self.process.kill()
                self.process.wait(timeout=1.0)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass  # Process already gone or we can't kill it

        # Record the violation
        with self._lock:
            self._usage_history.append(
                {
                    "timestamp": time.time(),
                    "event": "limit_exceeded",
                    "limit_type": limit_error.resource_type,
                    "limit": limit_error.limit,
                    "current": limit_error.current,
                }
            )

    def get_usage(self) -> dict[str, Any]:
        """Get current or final resource usage statistics."""
        with self._lock:
            if not self._usage_history:
                return {}

            # Get latest usage
            latest = self._usage_history[-1]

            # Calculate statistics
            memory_values = [
                entry.get("memory", 0) for entry in self._usage_history if "memory" in entry
            ]

            cpu_values = [
                entry.get("cpu_percent", 0.0)
                for entry in self._usage_history
                if "cpu_percent" in entry
            ]

            return {
                "current_memory": latest.get("memory", 0),
                "peak_memory": max(memory_values) if memory_values else 0,
                "average_memory": sum(memory_values) / len(memory_values) if memory_values else 0,
                "current_cpu": latest.get("cpu_percent", 0.0),
                "average_cpu": sum(cpu_values) / len(cpu_values) if cpu_values else 0.0,
                "peak_cpu": max(cpu_values) if cpu_values else 0.0,
                "file_handles": latest.get("file_handles", 0),
                "num_threads": latest.get("num_threads", 0),
                "elapsed_time": latest.get("elapsed_time", 0.0),
                "samples": len(self._usage_history),
                "monitoring_active": self.monitoring,
            }

    def get_usage_history(self) -> list[dict[str, Any]]:
        """Get full usage history for analysis."""
        with self._lock:
            return self._usage_history.copy()

    def reset_monitoring(self) -> None:
        """Reset monitoring state and clear history."""
        with self._lock:
            self.stop_monitoring()
            self._usage_history.clear()
            self._peak_memory = 0
            self._total_cpu_time = 0.0
            self._start_time = 0.0

    def is_monitoring(self) -> bool:
        """Check if currently monitoring a process."""
        return self.monitoring

    def get_process_info(self) -> dict[str, Any] | None:
        """Get detailed process information."""
        if not self.process:
            return None

        try:
            return {
                "pid": self.process.pid,
                "ppid": self.process.ppid(),
                "name": self.process.name(),
                "status": self.process.status(),
                "create_time": self.process.create_time(),
                "cmdline": self.process.cmdline(),
                "cwd": self.process.cwd(),
                "username": self.process.username() if hasattr(self.process, "username") else None,
            }

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    def format_usage_report(self) -> str:
        """Format a human-readable usage report."""
        usage = self.get_usage()

        if not usage:
            return "No resource usage data available"

        def format_bytes(bytes_val: int) -> str:
            """Format bytes as human-readable string."""
            for unit in ["B", "KB", "MB", "GB"]:
                if bytes_val < 1024.0:
                    return f"{bytes_val:.1f} {unit}"
                bytes_val /= 1024.0
            return f"{bytes_val:.1f} TB"

        report_lines = [
            "=== Resource Usage Report ===",
            f"Peak Memory: {format_bytes(usage.get('peak_memory', 0))}",
            f"Average Memory: {format_bytes(usage.get('average_memory', 0))}",
            f"Peak CPU: {usage.get('peak_cpu', 0.0):.1f}%",
            f"Average CPU: {usage.get('average_cpu', 0.0):.1f}%",
            f"File Handles: {usage.get('file_handles', 0)}",
            f"Threads: {usage.get('num_threads', 0)}",
            f"Execution Time: {usage.get('elapsed_time', 0.0):.2f} seconds",
            f"Monitoring Samples: {usage.get('samples', 0)}",
        ]

        return "\n".join(report_lines)
