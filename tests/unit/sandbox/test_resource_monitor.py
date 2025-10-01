"""Unit tests for sandbox resource monitoring."""

import threading
import time
from unittest.mock import Mock, patch

import psutil
import pytest

from mlpy.runtime.sandbox.resource_monitor import (
    ResourceLimitExceeded,
    ResourceLimits,
    ResourceMonitor,
    ResourceMonitorError,
)


class TestResourceLimits:
    """Test resource limits configuration."""

    def test_default_limits(self):
        """Test default resource limits."""
        limits = ResourceLimits()

        assert limits.memory_limit == 100 * 1024 * 1024  # 100MB
        assert limits.cpu_timeout == 30.0
        assert limits.file_size_limit == 10 * 1024 * 1024  # 10MB
        assert limits.temp_dir_limit == 50 * 1024 * 1024  # 50MB
        assert limits.max_file_handles == 100
        assert limits.max_threads == 10

    def test_custom_limits(self):
        """Test custom resource limits."""
        limits = ResourceLimits(
            memory_limit=256 * 1024 * 1024,  # 256MB
            cpu_timeout=60.0,
            file_size_limit=20 * 1024 * 1024,  # 20MB
            max_file_handles=200,
            max_threads=20,
        )

        assert limits.memory_limit == 256 * 1024 * 1024
        assert limits.cpu_timeout == 60.0
        assert limits.file_size_limit == 20 * 1024 * 1024
        assert limits.max_file_handles == 200
        assert limits.max_threads == 20


class TestResourceLimitExceeded:
    """Test ResourceLimitExceeded exception."""

    def test_exception_creation(self):
        """Test creating resource limit exceeded exception."""
        exc = ResourceLimitExceeded("memory", 1024 * 1024, 2 * 1024 * 1024)

        assert exc.resource_type == "memory"
        assert exc.limit == 1024 * 1024
        assert exc.current == 2 * 1024 * 1024
        assert "memory limit exceeded" in str(exc)
        assert "2097152 > 1048576" in str(exc)


class TestResourceMonitor:
    """Test resource monitor functionality."""

    def test_initialization(self):
        """Test resource monitor initialization."""
        monitor = ResourceMonitor()

        assert monitor.limits is None
        assert monitor.monitoring is False
        assert monitor.process is None
        assert monitor._monitor_thread is None
        assert monitor._usage_history == []
        assert monitor._peak_memory == 0
        assert monitor._total_cpu_time == 0.0

    def test_set_limits(self):
        """Test setting resource limits."""
        monitor = ResourceMonitor()
        limits = ResourceLimits(memory_limit=128 * 1024 * 1024)

        monitor.set_limits(limits)
        assert monitor.limits is limits
        assert monitor.limits.memory_limit == 128 * 1024 * 1024

    @patch("psutil.Process")
    def test_start_monitoring_success(self, mock_process_class):
        """Test successful monitoring start."""
        monitor = ResourceMonitor()
        limits = ResourceLimits()
        monitor.set_limits(limits)

        # Mock process
        mock_process = Mock()
        mock_process_class.return_value = mock_process

        monitor.start_monitoring(12345)

        assert monitor.monitoring is True
        assert monitor.process is mock_process
        assert monitor._monitor_thread is not None
        assert monitor._monitor_thread.is_alive()

        # Clean up
        monitor.stop_monitoring()

    @patch("psutil.Process")
    def test_start_monitoring_process_not_found(self, mock_process_class):
        """Test monitoring start with non-existent process."""
        monitor = ResourceMonitor()

        # Mock process not found
        mock_process_class.side_effect = psutil.NoSuchProcess(12345)

        with pytest.raises(ResourceMonitorError) as exc_info:
            monitor.start_monitoring(12345)

        assert "Process 12345 not found" in str(exc_info.value)

    def test_start_monitoring_already_monitoring(self):
        """Test starting monitoring when already monitoring."""
        monitor = ResourceMonitor()
        monitor.monitoring = True  # Simulate already monitoring

        with pytest.raises(ResourceMonitorError) as exc_info:
            monitor.start_monitoring(12345)

        assert "Already monitoring a process" in str(exc_info.value)

    def test_stop_monitoring(self):
        """Test stopping monitoring."""
        monitor = ResourceMonitor()

        # Start with mock monitoring state
        monitor.monitoring = True
        monitor._stop_event = threading.Event()
        monitor._monitor_thread = Mock()
        monitor._monitor_thread.is_alive.return_value = False

        monitor.stop_monitoring()

        assert monitor.monitoring is False
        assert monitor._stop_event.is_set()
        assert monitor.process is None

    def test_stop_monitoring_when_not_monitoring(self):
        """Test stopping monitoring when not currently monitoring."""
        monitor = ResourceMonitor()

        # Should not raise error
        monitor.stop_monitoring()

        assert monitor.monitoring is False

    @patch("psutil.Process")
    def test_get_current_usage(self, mock_process_class):
        """Test getting current resource usage."""
        monitor = ResourceMonitor()

        # Mock process with usage data
        mock_process = Mock()
        mock_memory_info = Mock()
        mock_memory_info.rss = 10 * 1024 * 1024  # 10MB
        mock_process.memory_info.return_value = mock_memory_info
        mock_process.cpu_percent.return_value = 15.5
        mock_process.open_files.return_value = [Mock(), Mock(), Mock()]  # 3 files
        mock_process.num_threads.return_value = 5

        monitor.process = mock_process
        monitor._start_time = time.time() - 2.0  # 2 seconds ago

        usage = monitor._get_current_usage()

        assert usage["memory"] == 10 * 1024 * 1024
        assert usage["cpu_percent"] == 15.5
        assert usage["file_handles"] == 3
        assert usage["num_threads"] == 5
        assert 1.8 < usage["elapsed_time"] < 2.2  # Should be around 2 seconds

    @patch("psutil.Process")
    def test_get_current_usage_process_gone(self, mock_process_class):
        """Test getting usage when process no longer exists."""
        monitor = ResourceMonitor()

        # Mock process that raises NoSuchProcess
        mock_process = Mock()
        mock_process.memory_info.side_effect = psutil.NoSuchProcess(12345)

        monitor.process = mock_process

        usage = monitor._get_current_usage()
        assert usage == {}

    @patch("psutil.Process")
    def test_get_current_usage_access_denied(self, mock_process_class):
        """Test getting usage with access denied."""
        monitor = ResourceMonitor()

        # Mock process with access denied for some operations
        mock_process = Mock()
        mock_memory_info = Mock()
        mock_memory_info.rss = 5 * 1024 * 1024
        mock_process.memory_info.return_value = mock_memory_info
        mock_process.cpu_percent.return_value = 10.0
        mock_process.open_files.side_effect = psutil.AccessDenied()
        mock_process.num_threads.side_effect = psutil.AccessDenied()

        monitor.process = mock_process
        monitor._start_time = time.time()

        usage = monitor._get_current_usage()

        assert usage["memory"] == 5 * 1024 * 1024
        assert usage["cpu_percent"] == 10.0
        assert usage["file_handles"] == 0  # Should default to 0 on access denied
        assert usage["num_threads"] == 0

    def test_enforce_limits_no_limits(self):
        """Test enforce limits with no limits set."""
        monitor = ResourceMonitor()

        usage = {
            "memory": 100 * 1024 * 1024,
            "elapsed_time": 60.0,
            "file_handles": 200,
            "num_threads": 50,
        }

        # Should not raise any exception
        monitor._enforce_limits(usage)

    def test_enforce_limits_memory_exceeded(self):
        """Test memory limit enforcement."""
        monitor = ResourceMonitor()
        limits = ResourceLimits(memory_limit=50 * 1024 * 1024)  # 50MB
        monitor.set_limits(limits)

        usage = {"memory": 100 * 1024 * 1024, "elapsed_time": 5.0}  # 100MB - exceeds limit

        with pytest.raises(ResourceLimitExceeded) as exc_info:
            monitor._enforce_limits(usage)

        assert exc_info.value.resource_type == "memory"
        assert exc_info.value.limit == 50 * 1024 * 1024
        assert exc_info.value.current == 100 * 1024 * 1024

    def test_enforce_limits_timeout_exceeded(self):
        """Test CPU timeout enforcement."""
        monitor = ResourceMonitor()
        limits = ResourceLimits(cpu_timeout=10.0)
        monitor.set_limits(limits)

        usage = {"memory": 10 * 1024 * 1024, "elapsed_time": 15.0}  # Exceeds 10 second limit

        with pytest.raises(ResourceLimitExceeded) as exc_info:
            monitor._enforce_limits(usage)

        assert exc_info.value.resource_type == "cpu_timeout"
        assert exc_info.value.limit == 10.0
        assert exc_info.value.current == 15.0

    def test_enforce_limits_file_handles_exceeded(self):
        """Test file handle limit enforcement."""
        monitor = ResourceMonitor()
        limits = ResourceLimits(max_file_handles=50)
        monitor.set_limits(limits)

        usage = {
            "memory": 10 * 1024 * 1024,
            "elapsed_time": 5.0,
            "file_handles": 75,  # Exceeds limit of 50
        }

        with pytest.raises(ResourceLimitExceeded) as exc_info:
            monitor._enforce_limits(usage)

        assert exc_info.value.resource_type == "file_handles"
        assert exc_info.value.limit == 50
        assert exc_info.value.current == 75

    def test_enforce_limits_threads_exceeded(self):
        """Test thread count limit enforcement."""
        monitor = ResourceMonitor()
        limits = ResourceLimits(max_threads=5)
        monitor.set_limits(limits)

        usage = {
            "memory": 10 * 1024 * 1024,
            "elapsed_time": 5.0,
            "num_threads": 10,  # Exceeds limit of 5
        }

        with pytest.raises(ResourceLimitExceeded) as exc_info:
            monitor._enforce_limits(usage)

        assert exc_info.value.resource_type == "num_threads"
        assert exc_info.value.limit == 5
        assert exc_info.value.current == 10

    def test_terminate_process(self):
        """Test process termination."""
        monitor = ResourceMonitor()

        # Mock process
        mock_process = Mock()
        mock_process.terminate.return_value = None
        mock_process.wait.return_value = None
        monitor.process = mock_process
        monitor._usage_history = []

        limit_error = ResourceLimitExceeded("memory", 1024, 2048)

        monitor._terminate_process(limit_error)

        # Should try graceful termination first
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once_with(timeout=2.0)

        # Should record violation
        assert len(monitor._usage_history) == 1
        assert monitor._usage_history[0]["event"] == "limit_exceeded"

    def test_terminate_process_force_kill(self):
        """Test forced process termination when graceful fails."""
        monitor = ResourceMonitor()

        # Mock process that doesn't terminate gracefully
        mock_process = Mock()
        mock_process.terminate.return_value = None
        mock_process.wait.side_effect = [
            psutil.TimeoutExpired(
                seconds=2.0
            ),  # Graceful termination times out (psutil API: seconds, not timeout)
            None,  # Force kill succeeds
        ]
        mock_process.kill.return_value = None
        monitor.process = mock_process
        monitor._usage_history = []

        limit_error = ResourceLimitExceeded("cpu_timeout", 10.0, 15.0)

        monitor._terminate_process(limit_error)

        # Should try graceful termination first, then force kill
        mock_process.terminate.assert_called_once()
        mock_process.kill.assert_called_once()
        assert mock_process.wait.call_count == 2

    def test_terminate_process_already_gone(self):
        """Test terminating process that's already gone."""
        monitor = ResourceMonitor()

        # Mock process that's already gone
        mock_process = Mock()
        mock_process.terminate.side_effect = psutil.NoSuchProcess(12345)
        monitor.process = mock_process
        monitor._usage_history = []

        limit_error = ResourceLimitExceeded("memory", 1024, 2048)

        # Should not raise exception
        monitor._terminate_process(limit_error)

    def test_get_usage_no_history(self):
        """Test getting usage statistics with no history."""
        monitor = ResourceMonitor()

        usage = monitor.get_usage()
        assert usage == {}

    def test_get_usage_with_history(self):
        """Test getting usage statistics with history."""
        monitor = ResourceMonitor()

        # Add some usage history
        monitor._usage_history = [
            {"memory": 10 * 1024 * 1024, "cpu_percent": 10.0, "elapsed_time": 1.0},
            {"memory": 20 * 1024 * 1024, "cpu_percent": 15.0, "elapsed_time": 2.0},
            {
                "memory": 15 * 1024 * 1024,
                "cpu_percent": 12.0,
                "elapsed_time": 3.0,
                "file_handles": 5,
                "num_threads": 3,
            },
        ]

        usage = monitor.get_usage()

        assert usage["current_memory"] == 15 * 1024 * 1024  # Latest
        assert usage["peak_memory"] == 20 * 1024 * 1024  # Maximum
        assert usage["average_memory"] == 15 * 1024 * 1024  # (10+20+15)/3
        assert usage["current_cpu"] == 12.0
        assert usage["peak_cpu"] == 15.0
        assert usage["average_cpu"] == 12.333333333333334  # (10+15+12)/3
        assert usage["file_handles"] == 5
        assert usage["num_threads"] == 3
        assert usage["elapsed_time"] == 3.0
        assert usage["samples"] == 3

    def test_get_usage_history(self):
        """Test getting full usage history."""
        monitor = ResourceMonitor()

        history_data = [
            {"memory": 10 * 1024 * 1024, "cpu_percent": 10.0},
            {"memory": 20 * 1024 * 1024, "cpu_percent": 15.0},
        ]
        monitor._usage_history = history_data

        history = monitor.get_usage_history()

        assert history == history_data
        assert history is not monitor._usage_history  # Should be a copy

    def test_reset_monitoring(self):
        """Test resetting monitoring state."""
        monitor = ResourceMonitor()

        # Set up some state
        monitor.monitoring = True
        monitor._usage_history = [{"memory": 1024}]
        monitor._peak_memory = 2048
        monitor._total_cpu_time = 10.5

        with patch.object(monitor, "stop_monitoring") as mock_stop:
            monitor.reset_monitoring()

            mock_stop.assert_called_once()

        assert monitor._usage_history == []
        assert monitor._peak_memory == 0
        assert monitor._total_cpu_time == 0.0
        assert monitor._start_time == 0.0

    def test_is_monitoring(self):
        """Test monitoring status check."""
        monitor = ResourceMonitor()

        assert monitor.is_monitoring() is False

        monitor.monitoring = True
        assert monitor.is_monitoring() is True

    def test_get_process_info(self):
        """Test getting process information."""
        monitor = ResourceMonitor()

        # No process
        assert monitor.get_process_info() is None

        # Mock process with info
        mock_process = Mock()
        mock_process.pid = 12345
        mock_process.ppid.return_value = 1234
        mock_process.name.return_value = "python"
        mock_process.status.return_value = "running"
        mock_process.create_time.return_value = 1234567890.0
        mock_process.cmdline.return_value = ["python", "script.py"]
        mock_process.cwd.return_value = "/home/user"

        monitor.process = mock_process

        info = monitor.get_process_info()

        assert info["pid"] == 12345
        assert info["ppid"] == 1234
        assert info["name"] == "python"
        assert info["status"] == "running"
        assert info["create_time"] == 1234567890.0
        assert info["cmdline"] == ["python", "script.py"]
        assert info["cwd"] == "/home/user"

    def test_get_process_info_access_denied(self):
        """Test getting process info with access denied."""
        monitor = ResourceMonitor()

        mock_process = Mock()
        mock_process.pid = 12345
        mock_process.ppid.side_effect = psutil.AccessDenied()

        monitor.process = mock_process

        info = monitor.get_process_info()
        assert info is None

    def test_format_usage_report(self):
        """Test formatting usage report."""
        monitor = ResourceMonitor()

        # No usage data
        report = monitor.format_usage_report()
        assert "No resource usage data available" in report

        # With usage data
        monitor._usage_history = [
            {
                "memory": 50 * 1024 * 1024,
                "cpu_percent": 25.0,
                "elapsed_time": 5.0,
                "file_handles": 10,
                "num_threads": 3,
            }
        ]

        report = monitor.format_usage_report()

        assert "Resource Usage Report" in report
        assert "50.0 MB" in report  # Peak memory
        assert "25.0%" in report  # Peak CPU
        assert "5.00 seconds" in report  # Execution time
        assert "File Handles: 10" in report
        assert "Threads: 3" in report

    def test_format_bytes(self):
        """Test byte formatting in report."""
        monitor = ResourceMonitor()

        # Test different byte sizes through format_usage_report
        test_cases = [
            (1023, "1023.0 B"),
            (1024, "1.0 KB"),
            (1024 * 1024, "1.0 MB"),
            (2.5 * 1024 * 1024 * 1024, "2.5 GB"),
        ]

        for bytes_val, expected in test_cases:
            monitor._usage_history = [{"memory": int(bytes_val), "cpu_percent": 0.0}]
            report = monitor.format_usage_report()
            assert expected in report


class TestResourceMonitorIntegration:
    """Integration tests for resource monitoring."""

    @patch("psutil.Process")
    def test_monitoring_lifecycle(self, mock_process_class):
        """Test complete monitoring lifecycle."""
        monitor = ResourceMonitor()
        limits = ResourceLimits(memory_limit=100 * 1024 * 1024)
        monitor.set_limits(limits)

        # Mock process with realistic behavior
        mock_process = Mock()
        mock_memory_info = Mock()
        mock_memory_info.rss = 50 * 1024 * 1024  # 50MB - under limit
        mock_process.memory_info.return_value = mock_memory_info
        mock_process.cpu_percent.return_value = 10.0
        mock_process.open_files.return_value = []
        mock_process.num_threads.return_value = 2
        mock_process_class.return_value = mock_process

        # Start monitoring
        monitor.start_monitoring(12345)
        assert monitor.is_monitoring()

        # Let it run briefly
        time.sleep(0.1)

        # Stop monitoring
        monitor.stop_monitoring()
        assert not monitor.is_monitoring()

        # Should have some usage data
        usage = monitor.get_usage()
        assert "current_memory" in usage

    def test_thread_safety(self):
        """Test resource monitor thread safety."""
        monitor = ResourceMonitor()

        errors = []

        def modify_history():
            try:
                for i in range(10):
                    monitor._usage_history.append({"memory": i * 1024, "cpu_percent": i * 0.1})
                    time.sleep(0.001)
            except Exception as e:
                errors.append(e)

        def read_usage():
            try:
                for _ in range(10):
                    usage = monitor.get_usage()
                    history = monitor.get_usage_history()
                    time.sleep(0.001)
            except Exception as e:
                errors.append(e)

        # Run concurrent operations
        threads = []
        for _ in range(2):
            threads.append(threading.Thread(target=modify_history))
            threads.append(threading.Thread(target=read_usage))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Should not have race condition errors
        assert len(errors) == 0, f"Thread safety errors: {errors}"
