===============
Runtime Systems
===============

mlpy's runtime systems provide secure execution environments and capability-based access control. These systems ensure that ML programs run safely while maintaining high performance and providing rich debugging capabilities.

Architecture Overview
=====================

The runtime consists of four interconnected systems:

.. code-box:: text

    ┌─────────────────────┐    ┌─────────────────────┐
    │   Capability        │────│   Sandbox           │
    │   Manager           │    │   Execution         │
    └─────────────────────┘    └─────────────────────┘
             │                          │
             │                          │
    ┌─────────────────────┐    ┌─────────────────────┐
    │   Standard Library  │────│   Performance       │
    │   Bridge System     │    │   Monitoring        │
    └─────────────────────┘    └─────────────────────┘

Capability Management System
============================

**File**: ``src/mlpy/runtime/capabilities/manager.py``

The capability system implements fine-grained access control using capability tokens.

Core Components
---------------

**Capability Tokens**::

    @dataclass
    class CapabilityToken:
        resource_pattern: str
        permission_type: str
        granted_by: str
        expires_at: datetime | None
        restrictions: dict[str, Any]
        metadata: dict[str, Any]

        def matches(self, resource: str, permission: str) -> bool:
            return (
                self.matches_pattern(resource) and
                self.permission_type == permission and
                not self.is_expired()
            )

**Capability Context**::

    class CapabilityContext:
        def __init__(self, parent: CapabilityContext | None = None):
            self.parent = parent
            self.tokens: list[CapabilityToken] = []
            self.restrictions: dict[str, Any] = {}
            self.audit_log: list[CapabilityAuditEvent] = []

        def grant(self, pattern: str, permission: str, **kwargs) -> CapabilityToken:
            token = CapabilityToken(
                resource_pattern=pattern,
                permission_type=permission,
                granted_by=self.get_current_context(),
                expires_at=kwargs.get('expires_at'),
                restrictions=kwargs.get('restrictions', {}),
                metadata=kwargs.get('metadata', {})
            )

            self.tokens.append(token)
            self.audit_grant(token)
            return token

        def check(self, resource: str, permission: str) -> bool:
            # Check local tokens first
            for token in self.tokens:
                if token.matches(resource, permission):
                    self.audit_access(token, resource, permission, success=True)
                    return True

            # Check parent context
            if self.parent:
                return self.parent.check(resource, permission)

            self.audit_access(None, resource, permission, success=False)
            return False

Resource Pattern Matching
-------------------------

Capability patterns support flexible resource matching::

    # File system patterns
    "file:/home/user/*.txt"        # Specific directory and extension
    "file:/home/user/**"           # Recursive directory access
    "file:temp:*"                  # Temporary file access

    # Network patterns
    "http://api.example.com/*"     # Specific domain API access
    "https://*.trusted-domain.com" # Wildcard subdomain access

    # System patterns
    "system:time:read"             # System time access
    "system:random:*"              # All random operations

**Pattern Matching Implementation**::

    def matches_pattern(self, pattern: str, resource: str) -> bool:
        if pattern == "*":
            return True
        elif pattern.endswith("**"):
            prefix = pattern[:-2]
            return resource.startswith(prefix)
        elif pattern.endswith("*"):
            prefix = pattern[:-1]
            return resource.startswith(prefix) and "/" not in resource[len(prefix):]
        else:
            return pattern == resource

Capability Inheritance
---------------------

Child contexts inherit capabilities with restrictions::

    def create_child_context(self, restrictions: dict = None) -> CapabilityContext:
        child = CapabilityContext(parent=self)

        # Apply additional restrictions
        if restrictions:
            child.restrictions.update(restrictions)

        # Filter inherited capabilities based on restrictions
        for token in self.tokens:
            if self.token_allowed_in_child(token, restrictions):
                restricted_token = token.with_restrictions(restrictions)
                child.tokens.append(restricted_token)

        return child

Performance Optimization
------------------------

The capability system uses several optimization strategies:

**Capability Caching**::

    class CapabilityCache:
        def __init__(self, max_size: int = 1000):
            self._cache: dict[str, bool] = {}
            self._access_times: dict[str, float] = {}
            self.max_size = max_size

        def check_cached(self, resource: str, permission: str) -> bool | None:
            cache_key = f"{resource}:{permission}"

            if cache_key in self._cache:
                self._access_times[cache_key] = time.time()
                return self._cache[cache_key]

            return None

        def cache_result(self, resource: str, permission: str, result: bool):
            if len(self._cache) >= self.max_size:
                self._evict_oldest()

            cache_key = f"{resource}:{permission}"
            self._cache[cache_key] = result
            self._access_times[cache_key] = time.time()

Sandbox Execution System
=========================

**File**: ``src/mlpy/runtime/sandbox/executor.py``

The sandbox provides process-level isolation with resource monitoring.

Sandbox Configuration
---------------------

**Configuration Options**::

    @dataclass
    class SandboxConfig:
        max_memory_mb: int = 100
        max_cpu_time_seconds: float = 5.0
        max_wall_time_seconds: float = 10.0
        max_file_size_mb: int = 10
        max_open_files: int = 20
        allow_network: bool = False
        allowed_imports: set[str] = field(default_factory=set)
        temp_dir: str | None = None
        environment_vars: dict[str, str] = field(default_factory=dict)

**Resource Monitoring**::

    class ResourceMonitor:
        def __init__(self, config: SandboxConfig):
            self.config = config
            self.start_time = time.time()
            self.peak_memory = 0
            self.files_opened = 0

        def check_limits(self):
            # Memory check
            current_memory = psutil.Process().memory_info().rss // (1024 * 1024)
            if current_memory > self.config.max_memory_mb:
                raise ResourceLimitError(f"Memory limit exceeded: {current_memory}MB")

            # Time check
            elapsed = time.time() - self.start_time
            if elapsed > self.config.max_wall_time_seconds:
                raise ResourceLimitError(f"Wall time limit exceeded: {elapsed:.2f}s")

Process Isolation
-----------------

**Subprocess Management**::

    class SandboxExecutor:
        def execute(self, code: str, config: SandboxConfig) -> SandboxResult:
            # Create isolated environment
            env = self.create_sandbox_environment(config)

            # Prepare execution script
            script_path = self.write_execution_script(code, config)

            # Execute with resource limits
            try:
                result = subprocess.run(
                    [sys.executable, script_path],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=config.max_wall_time_seconds,
                    cwd=config.temp_dir
                )

                return SandboxResult(
                    success=result.returncode == 0,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    exit_code=result.returncode,
                    execution_time=self.get_execution_time(),
                    memory_usage=self.get_memory_usage(),
                    capabilities_used=self.get_capabilities_used()
                )

            except subprocess.TimeoutExpired:
                return SandboxResult(
                    success=False,
                    error="Execution timeout exceeded",
                    execution_time=config.max_wall_time_seconds
                )

**Security Restrictions**::

    def create_sandbox_environment(self, config: SandboxConfig) -> dict[str, str]:
        env = {
            # Minimal environment
            'PATH': '/usr/bin:/bin',
            'PYTHONPATH': self.get_safe_python_path(),
            'TMPDIR': config.temp_dir,

            # Security restrictions
            'PYTHONDONTWRITEBYTECODE': '1',
            'PYTHONHASHSEED': '0',
            'MLPY_SANDBOX_MODE': '1',
            'MLPY_CAPABILITY_CONTEXT': self.serialize_capabilities()
        }

        # Add user-specified environment variables (filtered)
        for key, value in config.environment_vars.items():
            if self.is_safe_env_var(key, value):
                env[key] = value

        return env

Standard Library Bridge System
==============================

**File**: ``src/mlpy/stdlib/registry.py``

The bridge system enables secure interoperability between ML and Python code.

Bridge Architecture
-------------------

**Function Registration**::

    class BridgeRegistry:
        def register_function(
            self,
            ml_name: str,
            python_func: Callable,
            capabilities: list[str],
            validator: Callable | None = None
        ):
            bridge_func = BridgeFunction(
                ml_name=ml_name,
                python_function=python_func,
                capabilities_required=capabilities,
                parameter_validator=validator
            )

            self.functions[ml_name] = bridge_func

**Secure Function Calls**::

    def call_bridge_function(
        self,
        name: str,
        args: list,
        capability_context: CapabilityContext
    ) -> Any:
        if name not in self.functions:
            raise FunctionNotFoundError(f"Bridge function '{name}' not registered")

        bridge_func = self.functions[name]

        # Check capabilities
        for cap in bridge_func.capabilities_required:
            if not capability_context.check(cap, "execute"):
                raise InsufficientCapabilitiesError(
                    f"Missing capability: {cap}"
                )

        # Validate arguments
        if bridge_func.parameter_validator:
            bridge_func.parameter_validator(args)

        # Execute with monitoring
        try:
            with self.execution_monitor():
                result = bridge_func.python_function(*args)
                return self.sanitize_result(result)
        except Exception as e:
            raise BridgeFunctionError(f"Error in bridge function '{name}': {e}")

Type Marshalling
---------------

**Python ↔ ML Data Conversion**::

    class TypeMarshaller:
        def python_to_ml(self, value: Any) -> Any:
            if isinstance(value, dict):
                return {k: self.python_to_ml(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [self.python_to_ml(item) for item in value]
            elif isinstance(value, (int, float, str, bool)):
                return value
            elif value is None:
                return None
            else:
                # Complex objects need special handling
                return self.serialize_complex_object(value)

        def ml_to_python(self, value: Any) -> Any:
            # Inverse transformation
            if isinstance(value, dict) and '__mlpy_type__' in value:
                return self.deserialize_complex_object(value)
            elif isinstance(value, dict):
                return {k: self.ml_to_python(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [self.ml_to_python(item) for item in value]
            else:
                return value

**Callback Handling**::

    class CallbackManager:
        def register_callback(self, ml_func_name: str, python_callback: Callable):
            wrapped_callback = self.wrap_callback_with_security(python_callback)
            self.callbacks[ml_func_name] = wrapped_callback

        def wrap_callback_with_security(self, callback: Callable) -> Callable:
            def secure_wrapper(*args, **kwargs):
                # Validate callback context
                if not self.validate_callback_context():
                    raise SecurityError("Callback invoked from invalid context")

                # Check callback capabilities
                required_caps = self.get_callback_capabilities(callback)
                for cap in required_caps:
                    if not self.current_capability_context.check(cap, "execute"):
                        raise InsufficientCapabilitiesError(f"Callback missing capability: {cap}")

                # Execute with monitoring
                with self.callback_monitor(callback):
                    return callback(*args, **kwargs)

            return secure_wrapper

Performance Monitoring System
=============================

**File**: ``src/mlpy/runtime/profiling/monitor.py``

Real-time performance monitoring and profiling for ML program execution.

Execution Profiling
-------------------

**Performance Metrics Collection**::

    class ExecutionProfiler:
        def __init__(self):
            self.metrics = {
                'compilation_time': 0.0,
                'security_analysis_time': 0.0,
                'execution_time': 0.0,
                'memory_peak': 0,
                'capability_checks': 0,
                'bridge_calls': 0
            }

        @contextmanager
        def profile_stage(self, stage_name: str):
            start_time = time.perf_counter()
            start_memory = self.get_memory_usage()

            try:
                yield
            finally:
                end_time = time.perf_counter()
                end_memory = self.get_memory_usage()

                self.metrics[f'{stage_name}_time'] = end_time - start_time
                self.metrics[f'{stage_name}_memory'] = end_memory - start_memory

**Real-time Monitoring**::

    class RuntimeMonitor:
        def __init__(self, sampling_interval: float = 0.1):
            self.sampling_interval = sampling_interval
            self.is_monitoring = False
            self.samples: list[RuntimeSample] = []

        def start_monitoring(self):
            self.is_monitoring = True
            threading.Thread(target=self._monitor_loop, daemon=True).start()

        def _monitor_loop(self):
            while self.is_monitoring:
                sample = RuntimeSample(
                    timestamp=time.time(),
                    memory_mb=self.get_memory_usage_mb(),
                    cpu_percent=psutil.cpu_percent(),
                    active_capabilities=len(self.get_active_capabilities()),
                    bridge_call_rate=self.get_bridge_call_rate()
                )

                self.samples.append(sample)
                time.sleep(self.sampling_interval)

Resource Leak Detection
----------------------

**Memory Leak Detection**::

    class MemoryLeakDetector:
        def __init__(self):
            self.baseline_objects = {}
            self.growth_threshold = 1000  # objects

        def establish_baseline(self):
            self.baseline_objects = self.count_objects_by_type()

        def check_for_leaks(self) -> list[MemoryLeak]:
            current_objects = self.count_objects_by_type()
            leaks = []

            for obj_type, current_count in current_objects.items():
                baseline_count = self.baseline_objects.get(obj_type, 0)
                growth = current_count - baseline_count

                if growth > self.growth_threshold:
                    leak = MemoryLeak(
                        object_type=obj_type,
                        baseline_count=baseline_count,
                        current_count=current_count,
                        growth=growth
                    )
                    leaks.append(leak)

            return leaks

Error Handling and Recovery
===========================

**Graceful Degradation**::

    class RuntimeErrorHandler:
        def handle_capability_error(self, error: CapabilityError) -> RecoveryAction:
            if error.severity == "low":
                # Log warning and continue with restricted functionality
                self.log_security_warning(error)
                return RecoveryAction.CONTINUE_RESTRICTED
            else:
                # Terminate execution for security
                self.log_security_violation(error)
                return RecoveryAction.TERMINATE_SECURE

        def handle_resource_limit_error(self, error: ResourceLimitError) -> RecoveryAction:
            # Attempt cleanup and retry with stricter limits
            self.cleanup_resources()

            if self.retry_count < 3:
                return RecoveryAction.RETRY_WITH_LOWER_LIMITS
            else:
                return RecoveryAction.TERMINATE_WITH_ERROR

**State Recovery**::

    class StateManager:
        def create_checkpoint(self) -> StateCheckpoint:
            return StateCheckpoint(
                capability_context=self.capability_context.copy(),
                variable_state=self.get_variable_snapshot(),
                resource_state=self.get_resource_snapshot(),
                timestamp=time.time()
            )

        def restore_from_checkpoint(self, checkpoint: StateCheckpoint):
            self.capability_context.restore(checkpoint.capability_context)
            self.restore_variable_state(checkpoint.variable_state)
            self.restore_resource_state(checkpoint.resource_state)

Integration with IDE and Debugging Tools
=========================================

**Debug Information Provider**::

    class DebugInfoProvider:
        def get_runtime_state(self) -> RuntimeState:
            return RuntimeState(
                active_capabilities=self.capability_context.get_active_tokens(),
                variable_scope=self.get_current_scope(),
                call_stack=self.get_call_stack(),
                resource_usage=self.get_resource_usage(),
                security_violations=self.get_recent_violations()
            )

        def set_breakpoint(self, file: str, line: int):
            self.breakpoints.add((file, line))

        def should_break_here(self, file: str, line: int) -> bool:
            return (file, line) in self.breakpoints

**IDE Integration Protocol**::

    class IDEBridge:
        def handle_ide_request(self, request: IDERequest) -> IDEResponse:
            if request.type == "get_capabilities":
                return IDEResponse(
                    type="capabilities",
                    data=self.get_available_capabilities()
                )
            elif request.type == "validate_code":
                return self.validate_code_request(request.data)
            elif request.type == "security_analysis":
                return self.run_security_analysis(request.data)

This runtime system architecture provides the foundation for secure, high-performance ML program execution while maintaining the flexibility needed for diverse application scenarios.