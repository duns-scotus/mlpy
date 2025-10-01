"""Unit tests for core sandbox functionality."""

import subprocess
import threading
import time
from unittest.mock import Mock, patch

import pytest

from mlpy.runtime.capabilities.context import CapabilityContext
from mlpy.runtime.capabilities.tokens import create_file_capability
from mlpy.runtime.sandbox.sandbox import (
    MLSandbox,
    SandboxConfig,
    SandboxError,
    SandboxResourceError,
    SandboxResult,
    SandboxTimeoutError,
)


class TestSandboxConfig:
    """Test sandbox configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = SandboxConfig()

        assert config.memory_limit == "100MB"
        assert config.cpu_timeout == 30.0
        assert config.network_disabled is True
        assert config.strict_mode is True
        assert isinstance(config.disable_imports, list)
        assert "os" in config.disable_imports

    def test_custom_config(self):
        """Test custom configuration values."""
        config = SandboxConfig(
            memory_limit="256MB",
            cpu_timeout=60.0,
            network_disabled=False,
            allowed_hosts=["example.com"],
            allowed_ports=[80, 443],
            file_access_patterns=["*.txt", "*.json"],
            strict_mode=False,
        )

        assert config.memory_limit == "256MB"
        assert config.cpu_timeout == 60.0
        assert config.network_disabled is False
        assert config.allowed_hosts == ["example.com"]
        assert config.allowed_ports == [80, 443]
        assert config.file_access_patterns == ["*.txt", "*.json"]
        assert config.strict_mode is False


class TestSandboxResult:
    """Test sandbox result structure."""

    def test_default_result(self):
        """Test default result values."""
        result = SandboxResult(success=True)

        assert result.success is True
        assert result.return_value is None
        assert result.stdout == ""
        assert result.stderr == ""
        assert result.exit_code == 0
        assert result.execution_time == 0.0
        assert result.memory_usage == 0
        assert result.cpu_usage == 0.0
        assert result.capability_violations == []
        assert result.security_warnings == []
        assert result.error is None

    def test_failure_result(self):
        """Test failure result."""
        error = ValueError("Test error")
        result = SandboxResult(success=False, error=error, stderr="Error occurred", exit_code=1)

        assert result.success is False
        assert result.error is error
        assert result.stderr == "Error occurred"
        assert result.exit_code == 1


class TestSandboxErrors:
    """Test sandbox exception types."""

    def test_sandbox_error(self):
        """Test basic sandbox error."""
        config = SandboxConfig()
        error = SandboxError("Test error", config)

        assert str(error) == "Test error"
        assert error.config is config

    def test_sandbox_timeout_error(self):
        """Test timeout error."""
        error = SandboxTimeoutError("Execution timed out")

        assert isinstance(error, SandboxError)
        assert "timed out" in str(error)

    def test_sandbox_resource_error(self):
        """Test resource error."""
        error = SandboxResourceError("Memory limit exceeded")

        assert isinstance(error, SandboxError)
        assert "Memory limit" in str(error)


class TestMLSandbox:
    """Test core MLSandbox functionality."""

    def test_sandbox_initialization(self):
        """Test sandbox initialization."""
        config = SandboxConfig(memory_limit="50MB")
        sandbox = MLSandbox(config)

        assert sandbox.config is config
        assert sandbox.config.memory_limit == "50MB"
        assert sandbox._process is None
        assert sandbox._temp_dir is None

    def test_sandbox_context_manager(self):
        """Test sandbox as context manager."""
        config = SandboxConfig()

        with MLSandbox(config) as sandbox:
            assert sandbox._temp_dir is not None
            assert sandbox.resource_monitor is not None

        # After context, should be cleaned up
        # Note: _temp_dir cleanup is handled by TemporaryDirectory

    def test_parse_resource_limits(self):
        """Test resource limit parsing."""
        config = SandboxConfig(memory_limit="128MB", cpu_timeout=15.0, file_size_limit="10MB")

        sandbox = MLSandbox(config)
        limits = sandbox._parse_resource_limits()

        assert limits.memory_limit == 128 * 1024 * 1024  # 128MB
        assert limits.cpu_timeout == 15.0
        assert limits.file_size_limit == 10 * 1024 * 1024  # 10MB

    def test_parse_resource_limits_different_units(self):
        """Test parsing different size units."""
        # Test KB
        config_kb = SandboxConfig(memory_limit="512KB")
        sandbox_kb = MLSandbox(config_kb)
        limits_kb = sandbox_kb._parse_resource_limits()
        assert limits_kb.memory_limit == 512 * 1024

        # Test GB
        config_gb = SandboxConfig(memory_limit="2GB")
        sandbox_gb = MLSandbox(config_gb)
        limits_gb = sandbox_gb._parse_resource_limits()
        assert limits_gb.memory_limit == 2 * 1024 * 1024 * 1024

        # Test bytes (no unit)
        config_bytes = SandboxConfig(memory_limit="1048576")
        sandbox_bytes = MLSandbox(config_bytes)
        limits_bytes = sandbox_bytes._parse_resource_limits()
        assert limits_bytes.memory_limit == 1048576

    def test_environment_preparation(self):
        """Test subprocess environment preparation."""
        config = SandboxConfig(extra_env={"TEST_VAR": "test_value"}, strict_mode=True)

        sandbox = MLSandbox(config)
        sandbox._setup_sandbox()

        env = sandbox._prepare_environment()

        assert "TEST_VAR" in env
        assert env["TEST_VAR"] == "test_value"
        assert "PYTHONPATH" in env

        # In strict mode, dangerous variables should be removed
        env_with_dangerous = env.copy()
        env_with_dangerous["LD_PRELOAD"] = "/dangerous/lib.so"

        config_strict = SandboxConfig(strict_mode=True)
        sandbox_strict = MLSandbox(config_strict)
        sandbox_strict._setup_sandbox()

        # Mock the environment to include dangerous variable
        with patch("os.environ", env_with_dangerous):
            clean_env = sandbox_strict._prepare_environment()
            assert "LD_PRELOAD" not in clean_env

    @patch("mlpy.runtime.sandbox.sandbox.subprocess.Popen")
    def test_create_execution_script(self, mock_popen):
        """Test execution script creation."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)
        sandbox._setup_sandbox()

        python_code = "print('Hello, World!')"

        # Create execution script
        script_path = sandbox._create_execution_script(python_code)

        assert script_path.exists()
        assert script_path.suffix == ".py"

        # Read script content
        script_content = script_path.read_text()
        assert "Hello, World!" in script_content
        assert "__MLPY_RESULT__" in script_content

    def test_create_execution_script_with_context(self):
        """Test execution script creation with capability context."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)
        sandbox._setup_sandbox()

        python_code = "result = 42"

        # Create capability context
        context = CapabilityContext(name="test_context")
        file_token = create_file_capability(patterns=["*.txt"], operations={"read"})
        context.add_capability(file_token)

        # Create execution script with context
        script_path = sandbox._create_execution_script(python_code, context)

        script_content = script_path.read_text()
        assert "CAPABILITY_CONTEXT_DATA" in script_content
        assert script_content.count("CAPABILITY_CONTEXT_DATA") >= 1

    def test_parse_execution_result(self):
        """Test parsing execution results from subprocess output."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)

        # Test successful result
        success_output = """
        Some regular output
        __MLPY_RESULT__ {"success": true, "result": 42, "type": "int"}
        More output
        """

        result = sandbox._parse_execution_result(success_output)
        assert result == 42

        # Test failed result
        failure_output = """
        __MLPY_RESULT__ {"success": false, "error": "Division by zero", "error_type": "ZeroDivisionError"}
        """

        with pytest.raises(SandboxError) as exc_info:
            sandbox._parse_execution_result(failure_output)

        assert "Division by zero" in str(exc_info.value)

        # Test no result marker
        no_result_output = "Just some regular output with no result marker"
        result = sandbox._parse_execution_result(no_result_output)
        assert result is None

        # Test invalid JSON
        invalid_json_output = "__MLPY_RESULT__ {invalid json}"
        result = sandbox._parse_execution_result(invalid_json_output)
        assert result is None

    @patch("mlpy.runtime.sandbox.sandbox.subprocess.Popen")
    def test_execute_python_code_success(self, mock_popen):
        """Test successful Python code execution."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)
        sandbox._setup_sandbox()

        # Mock successful subprocess
        mock_process = Mock()
        mock_process.communicate.return_value = (
            '__MLPY_RESULT__ {"success": true, "result": 84, "type": "int"}',
            "",
        )
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        # Mock resource monitor
        sandbox.resource_monitor = Mock()
        sandbox.resource_monitor.get_usage.return_value = {"memory": 1024 * 1024, "cpu": 5.0}  # 1MB

        python_code = "result = 42 * 2"
        result = sandbox._execute_python_code(python_code)

        assert result.success is True
        assert result.return_value == 84
        assert result.exit_code == 0

    @patch("mlpy.runtime.sandbox.sandbox.subprocess.Popen")
    def test_execute_python_code_timeout(self, mock_popen):
        """Test Python code execution timeout."""
        config = SandboxConfig(cpu_timeout=1.0)
        sandbox = MLSandbox(config)
        sandbox._setup_sandbox()

        # Mock timeout in subprocess
        mock_process = Mock()
        mock_process.communicate.side_effect = [
            subprocess.TimeoutExpired(cmd="python", timeout=1.0),
            ("", ""),  # Second call after kill() returns empty output
        ]
        mock_process.kill.return_value = None
        mock_popen.return_value = mock_process

        # Mock resource monitor
        sandbox.resource_monitor = Mock()

        python_code = "while True: pass"

        with pytest.raises(SandboxTimeoutError):
            sandbox._execute_python_code(python_code)

    @patch("mlpy.ml.transpiler.transpile_ml_code")
    def test_execute_ml_code(self, mock_transpile):
        """Test ML code execution through transpiler."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)

        # Mock transpiler
        mock_transpile.return_value = (
            "result = 42 * 2",  # python_code
            [],  # issues
            None,  # source_map
        )

        # Mock Python execution
        with patch.object(sandbox, "_execute_python_code") as mock_execute:
            mock_result = SandboxResult(success=True, return_value=84)
            mock_execute.return_value = mock_result

            ml_code = "let x = 42; x * 2"
            result = sandbox.execute(ml_code)

            assert result.success is True
            assert result.return_value == 84

            # Check that transpiler was called
            mock_transpile.assert_called_once()
            # Check that Python execution was called
            mock_execute.assert_called_once()

    @patch("mlpy.ml.transpiler.transpile_ml_code")
    def test_execute_ml_code_transpilation_failure(self, mock_transpile):
        """Test handling of ML transpilation failure."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)

        # Mock transpiler failure
        mock_transpile.return_value = (
            None,  # python_code (failed)
            [Mock()],  # issues
            None,  # source_map
        )

        ml_code = "invalid ML code"
        result = sandbox.execute(ml_code)

        assert result.success is False
        assert result.error is not None
        assert "transpilation failed" in str(result.error).lower()

    def test_execute_file_success(self, tmp_path):
        """Test successful file execution."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)

        # Create test file
        ml_file = tmp_path / "test.ml"
        ml_file.write_text("let x = 42; x")

        # Mock the execute method
        with patch.object(sandbox, "execute") as mock_execute:
            mock_result = SandboxResult(success=True, return_value=42)
            mock_execute.return_value = mock_result

            result = sandbox.execute_file(str(ml_file))

            assert result.success is True
            assert result.return_value == 42

            # Check that execute was called with file content
            mock_execute.assert_called_once_with("let x = 42; x", None, None)

    def test_execute_file_not_found(self):
        """Test execution of non-existent file."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)

        result = sandbox.execute_file("/nonexistent/file.ml")

        assert result.success is False
        assert result.error is not None
        assert "file" in str(result.error).lower()

    def test_test_security(self):
        """Test security testing functionality."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)

        # Mock the execute method
        with patch.object(sandbox, "execute") as mock_execute:
            mock_result = SandboxResult(
                success=False, security_warnings=["Potentially dangerous operation detected"]
            )
            mock_execute.return_value = mock_result

            dangerous_code = "import os; os.system('rm -rf /')"
            result = sandbox.test_security(dangerous_code)

            assert result.success is False
            assert len(result.security_warnings) > 0

            mock_execute.assert_called_once_with(dangerous_code)

    def test_cleanup_multiple_calls(self):
        """Test that multiple cleanup calls are safe."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)
        sandbox._setup_sandbox()

        # First cleanup
        sandbox._cleanup_sandbox()

        # Second cleanup should not raise errors
        sandbox._cleanup_sandbox()

        # Third cleanup should still be safe
        sandbox._cleanup_sandbox()

    def test_thread_safety(self):
        """Test sandbox thread safety basics."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)

        errors = []

        def setup_and_cleanup():
            try:
                sandbox._setup_sandbox()
                time.sleep(0.01)  # Small delay
                sandbox._cleanup_sandbox()
            except Exception as e:
                errors.append(e)

        # Run multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=setup_and_cleanup)
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # Should not have errors from concurrent access
        assert len(errors) == 0, f"Thread safety errors: {errors}"

    def test_get_resource_usage(self):
        """Test getting resource usage."""
        config = SandboxConfig()
        sandbox = MLSandbox(config)

        # Mock resource monitor
        sandbox.resource_monitor = Mock()
        expected_usage = {"memory": 1024 * 1024, "cpu": 10.5, "execution_time": 2.5}
        sandbox.resource_monitor.get_usage.return_value = expected_usage

        usage = sandbox.get_resource_usage()
        assert usage == expected_usage

    def test_sandbox_execution_context_manager(self):
        """Test sandbox execution context manager function."""
        from mlpy.runtime.sandbox.sandbox import sandbox_execution

        config = SandboxConfig(memory_limit="50MB")

        with sandbox_execution(config) as sandbox:
            assert isinstance(sandbox, MLSandbox)
            assert sandbox.config.memory_limit == "50MB"

        # Should be cleaned up after context
