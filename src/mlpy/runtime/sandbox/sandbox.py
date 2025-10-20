"""Core MLSandbox class for secure subprocess-based ML code execution."""

import base64
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..capabilities.context import CapabilityContext
from ..capabilities.tokens import CapabilityToken
from .context_serializer import CapabilityContextSerializer
from .resource_monitor import ResourceLimits, ResourceMonitor


@dataclass
class SandboxConfig:
    """Configuration for sandbox execution."""

    # Resource limits
    memory_limit: str = "100MB"  # e.g., "100MB", "1GB"
    cpu_timeout: float = 30.0  # seconds
    file_size_limit: str = "10MB"
    temp_dir_limit: str = "50MB"

    # Network settings
    network_disabled: bool = True
    allowed_hosts: list[str] = field(default_factory=list)
    allowed_ports: list[int] = field(default_factory=list)

    # File system access
    file_access_patterns: list[str] = field(default_factory=list)
    read_only_mode: bool = False

    # Python execution settings
    python_executable: str | None = None
    extra_env: dict[str, str] = field(default_factory=dict)

    # Security settings
    disable_imports: list[str] = field(
        default_factory=lambda: ["os", "subprocess", "sys", "importlib", "__builtins__"]
    )
    strict_mode: bool = True


@dataclass
class SandboxResult:
    """Result of sandbox code execution."""

    # Execution results
    success: bool
    return_value: Any = None
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0

    # Resource usage
    execution_time: float = 0.0
    memory_usage: int = 0  # bytes
    cpu_usage: float = 0.0  # percentage

    # Security info
    capability_violations: list[str] = field(default_factory=list)
    security_warnings: list[str] = field(default_factory=list)

    # Error info
    error: Exception | None = None
    error_traceback: str | None = None


class SandboxError(Exception):
    """Base exception for sandbox execution errors."""

    def __init__(self, message: str, config: SandboxConfig | None = None):
        super().__init__(message)
        self.config = config


class SandboxTimeoutError(SandboxError):
    """Exception raised when sandbox execution times out."""

    pass


class SandboxResourceError(SandboxError):
    """Exception raised when resource limits are exceeded."""

    pass


class MLSandbox:
    """Secure subprocess-based sandbox for ML code execution."""

    def __init__(self, config: SandboxConfig | None = None):
        """Initialize the sandbox with configuration."""
        self.config = config or SandboxConfig()
        self.resource_monitor = ResourceMonitor()
        self.context_serializer = CapabilityContextSerializer()
        self._process: subprocess.Popen | None = None
        self._temp_dir: tempfile.TemporaryDirectory | None = None
        self._lock = threading.Lock()

    def __enter__(self):
        """Context manager entry."""
        self._setup_sandbox()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self._cleanup_sandbox()

    def _setup_sandbox(self) -> None:
        """Set up the sandbox environment."""
        # Create temporary directory for sandbox execution
        self._temp_dir = tempfile.TemporaryDirectory(prefix="mlpy_sandbox_")

        # Set up resource monitoring
        limits = self._parse_resource_limits()
        self.resource_monitor.set_limits(limits)

    def _cleanup_sandbox(self) -> None:
        """Clean up sandbox resources."""
        with self._lock:
            # Terminate any running process
            if self._process and self._process.poll() is None:
                try:
                    self._process.terminate()
                    self._process.wait(timeout=5.0)
                except (subprocess.TimeoutExpired, OSError):
                    # Force kill if termination fails
                    try:
                        self._process.kill()
                        self._process.wait(timeout=2.0)
                    except (subprocess.TimeoutExpired, OSError):
                        pass  # Process cleanup will be handled by OS

            # Clean up temporary directory
            if self._temp_dir:
                try:
                    self._temp_dir.cleanup()
                except OSError:
                    pass  # Best effort cleanup

    def _parse_resource_limits(self) -> ResourceLimits:
        """Parse resource limits from config."""

        def parse_size(size_str: str) -> int:
            """Parse size string like '100MB' to bytes."""
            size_str = size_str.strip().upper()

            if size_str.endswith("KB"):
                return int(size_str[:-2]) * 1024
            elif size_str.endswith("MB"):
                return int(size_str[:-2]) * 1024 * 1024
            elif size_str.endswith("GB"):
                return int(size_str[:-2]) * 1024 * 1024 * 1024
            else:
                return int(size_str)  # Assume bytes

        return ResourceLimits(
            memory_limit=parse_size(self.config.memory_limit),
            cpu_timeout=self.config.cpu_timeout,
            file_size_limit=parse_size(self.config.file_size_limit),
            temp_dir_limit=parse_size(self.config.temp_dir_limit),
        )

    def execute(
        self,
        ml_code: str,
        capabilities: list[CapabilityToken] | None = None,
        context: CapabilityContext | None = None,
    ) -> SandboxResult:
        """Execute ML code in the sandbox with capabilities."""
        start_time = time.time()

        try:
            # Prepare capability context
            if context is None and capabilities:
                from ..capabilities.manager import get_capability_manager

                manager = get_capability_manager()
                context = manager.create_context(name="sandbox_execution")

                for token in capabilities:
                    context.add_capability(token)

            # Transpile ML code to Python
            python_code = self._transpile_ml_code(ml_code)

            # Execute in subprocess
            result = self._execute_python_code(python_code, context)

            # Update timing
            result.execution_time = time.time() - start_time

            return result

        except SandboxTimeoutError as e:
            return SandboxResult(
                success=False, error=e, execution_time=time.time() - start_time, stderr=str(e)
            )

        except Exception as e:
            return SandboxResult(
                success=False,
                error=e,
                execution_time=time.time() - start_time,
                stderr=str(e),
                error_traceback=self._get_traceback(),
            )

    def _transpile_ml_code(self, ml_code: str) -> str:
        """Transpile ML code to Python using the transpiler."""
        from ...ml.transpiler import transpile_ml_code

        python_code, issues, _ = transpile_ml_code(
            ml_code,
            source_file="<sandbox>",
            strict_security=self.config.strict_mode,
            generate_source_maps=False,
        )

        if python_code is None:
            # Collect error messages from issues
            error_messages = [str(issue.error) for issue in issues]
            raise SandboxError(f"ML transpilation failed: {'; '.join(error_messages)}")

        return python_code

    def _execute_python_code(
        self, python_code: str, context: CapabilityContext | None = None
    ) -> SandboxResult:
        """Execute Python code in isolated subprocess."""

        # Create execution script
        script_path = self._create_execution_script(python_code, context)

        # Prepare subprocess environment
        env = self._prepare_environment()

        # Start resource monitoring
        monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
        monitor_thread.start()

        try:
            # Execute subprocess
            with self._lock:
                self._process = subprocess.Popen(
                    [self.config.python_executable or sys.executable, str(script_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=env,
                    cwd=self._temp_dir.name,
                    preexec_fn=self._setup_subprocess_limits if os.name != "nt" else None,
                )

            # Wait for completion with timeout
            try:
                stdout, stderr = self._process.communicate(timeout=self.config.cpu_timeout)
                exit_code = self._process.returncode

            except subprocess.TimeoutExpired:
                self._process.kill()
                stdout, stderr = self._process.communicate()
                raise SandboxTimeoutError(
                    f"Execution timed out after {self.config.cpu_timeout} seconds"
                )

            # Get resource usage
            resource_usage = self.resource_monitor.get_usage()

            # Parse result
            return_value = self._parse_execution_result(stdout)

            return SandboxResult(
                success=(exit_code == 0),
                return_value=return_value,
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                memory_usage=resource_usage.get("memory", 0),
                cpu_usage=resource_usage.get("cpu", 0.0),
            )

        finally:
            # Stop resource monitoring
            self.resource_monitor.stop_monitoring()

    def _create_execution_script(
        self, python_code: str, context: CapabilityContext | None = None
    ) -> Path:
        """Create the Python script to execute in subprocess."""
        script_template = '''#!/usr/bin/env python3
"""MLPy Sandbox Execution Script"""

import sys
import json as _stdlib_json
import traceback
import base64
import pickle
from pathlib import Path
from typing import Any, Optional

# Import mlpy runtime modules for safe execution (before any user code)
# This must be at module level to avoid UnboundLocalError when user code
# contains imports that might shadow built-in modules
sys.path.insert(0, {runtime_path!r})

# Capability context data (serialized)
CAPABILITY_CONTEXT_DATA = {context_data}

def setup_capabilities():
    """Set up capability context in subprocess."""
    if CAPABILITY_CONTEXT_DATA and CAPABILITY_CONTEXT_DATA != "None":
        try:
            # Import capability system
            from mlpy.runtime.sandbox.context_serializer import CapabilityContextSerializer
            from mlpy.runtime.capabilities.context import set_current_context

            # Deserialize capability context
            serializer = CapabilityContextSerializer()
            context = serializer.deserialize_from_subprocess(CAPABILITY_CONTEXT_DATA)

            # Activate context in subprocess
            set_current_context(context)

        except Exception as e:
            print(f"Warning: Failed to set up capabilities: {{e}}", file=sys.stderr)

def main():
    """Main execution function."""
    try:
        # Set up security context
        setup_capabilities()

        # Execute the user code
        result = None
        exec_globals = {{
            "__name__": "__main__",
            "__file__": "<sandbox>",
        }}

        # Execute the transpiled Python code
{code_block}

        # Output result in JSON format
        output = {{
            "success": True,
            "result": result,
            "type": str(type(result).__name__) if result is not None else None
        }}

        print("__MLPY_RESULT__", _stdlib_json.dumps(output, default=str))

    except Exception as e:
        error_output = {{
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc()
        }}

        print("__MLPY_RESULT__", _stdlib_json.dumps(error_output, default=str))
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

        # Serialize capability context for subprocess
        context_data = "None"
        if context:
            try:
                serialized = self.context_serializer.serialize_for_subprocess(context)
                context_data = f'"{serialized}"'
            except Exception as e:
                # Use None if serialization fails
                import sys
                print(f"Warning: Failed to serialize context: {e}", file=sys.stderr)
                pass

        # Prepare code block (indented for exec)
        code_lines = python_code.split("\n")
        indented_code = "\n".join(f"        {line}" for line in code_lines)

        # Get runtime path
        runtime_path = str(Path(__file__).parent.parent)

        # Format script
        script_content = script_template.format(
            context_data=context_data, runtime_path=runtime_path, code_block=indented_code
        )

        # Write script to temp file
        script_path = Path(self._temp_dir.name) / "sandbox_execution.py"
        script_path.write_text(script_content, encoding="utf-8")

        return script_path

    def _prepare_environment(self) -> dict[str, str]:
        """Prepare subprocess environment variables."""
        env = os.environ.copy()

        # Add custom environment variables
        env.update(self.config.extra_env)

        # Set Python path to include mlpy runtime
        python_path = env.get("PYTHONPATH", "")
        runtime_path = str(Path(__file__).parent.parent.parent)

        if python_path:
            env["PYTHONPATH"] = f"{runtime_path}:{python_path}"
        else:
            env["PYTHONPATH"] = runtime_path

        # Security: Limit subprocess environment
        if self.config.strict_mode:
            # Remove potentially dangerous environment variables
            dangerous_vars = ["LD_PRELOAD", "DYLD_INSERT_LIBRARIES", "PYTHONSTARTUP"]
            for var in dangerous_vars:
                env.pop(var, None)

        return env

    def _setup_subprocess_limits(self) -> None:
        """Set up resource limits for subprocess (Unix only)."""
        if os.name == "nt":
            return  # Not supported on Windows

        import resource

        limits = self._parse_resource_limits()

        # Set memory limit
        if limits.memory_limit > 0:
            resource.setrlimit(resource.RLIMIT_AS, (limits.memory_limit, limits.memory_limit))

        # Set CPU time limit
        if limits.cpu_timeout > 0:
            cpu_limit = int(limits.cpu_timeout) + 5  # Add buffer
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))

        # Set file size limit
        if limits.file_size_limit > 0:
            resource.setrlimit(
                resource.RLIMIT_FSIZE, (limits.file_size_limit, limits.file_size_limit)
            )

    def _monitor_resources(self) -> None:
        """Monitor resource usage during execution."""
        if self._process:
            self.resource_monitor.start_monitoring(self._process.pid)

    def _parse_execution_result(self, stdout: str) -> Any:
        """Parse execution result from subprocess output."""
        lines = stdout.split("\n")

        # Look for result marker
        for line in lines:
            line = line.strip()  # Strip whitespace to handle indented output
            if line.startswith("__MLPY_RESULT__"):
                try:
                    result_json = line[len("__MLPY_RESULT__") :].strip()
                    result_data = json.loads(result_json)

                    if result_data.get("success", False):
                        return result_data.get("result")
                    else:
                        # Execution failed
                        error_msg = result_data.get("error", "Unknown error")
                        traceback_msg = result_data.get("traceback", "")
                        if traceback_msg:
                            raise SandboxError(f"Code execution failed: {error_msg}\n\nTraceback:\n{traceback_msg}")
                        else:
                            raise SandboxError(f"Code execution failed: {error_msg}")

                except json.JSONDecodeError:
                    pass

        # No result found, return None
        return None

    def _get_traceback(self) -> str:
        """Get current exception traceback."""
        import traceback

        return traceback.format_exc()

    def execute_file(
        self,
        ml_file_path: str,
        capabilities: list[CapabilityToken] | None = None,
        context: CapabilityContext | None = None,
    ) -> SandboxResult:
        """Execute ML code from file in the sandbox."""
        try:
            path = Path(ml_file_path)
            ml_code = path.read_text(encoding="utf-8")

            return self.execute(ml_code, capabilities, context)

        except Exception as e:
            return SandboxResult(
                success=False, error=e, stderr=f"Failed to read file {ml_file_path}: {str(e)}"
            )

    def test_security(self, test_code: str) -> SandboxResult:
        """Test security by executing potentially dangerous code."""
        # This should be safe due to sandbox isolation
        return self.execute(test_code)

    def get_resource_usage(self) -> dict[str, Any]:
        """Get current resource usage information."""
        return self.resource_monitor.get_usage()


@contextmanager
def sandbox_execution(config: SandboxConfig | None = None):
    """Context manager for convenient sandbox execution."""
    sandbox = MLSandbox(config)

    try:
        yield sandbox
    finally:
        sandbox._cleanup_sandbox()
