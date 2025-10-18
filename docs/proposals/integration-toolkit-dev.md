# ML Integration Toolkit: Development & Operations Guide

**Document Version:** 1.1
**Date:** October 2025
**Status:** Selective Implementation - ~40% Essential Subset
**Last Updated:** January 19, 2026
**Author:** Architecture Team
**Related Document:** [integration-toolkit.md](./integration-toolkit.md) - Core Architecture & Production Deployment (✅ COMPLETE)

---

## Executive Summary

This document provides guidance for **developing, testing, debugging, and monitoring** ML integrations using the Integration Toolkit. It complements the core Integration Toolkit proposal (✅ now complete) by focusing on operational tooling and development workflows.

**Implementation Status: Selective (~40% Essential Subset)**

Based on current adoption stage and user needs, this proposal recommends implementing approximately 40% of the originally planned features:

✅ **IMPLEMENT NOW (Essential):**
- **Section 2:** Advanced Testing Utilities - Full implementation for quality assurance
- **Section 3:** REPL Development Workflow - Core commands only (.async, .callback, .caps, .benchmark)
- **Section 4:** CLI Tools - Minimal subset (validate, benchmark)

⏸️ **DEFERRED (Until User Demand):**
- **Section 1:** Debugging Integration Code - Complex async debugging features
- **Section 5:** Observability and Monitoring - Enterprise-grade monitoring (Prometheus, OpenTelemetry)

**Rationale for Selective Implementation:**
- Integration Toolkit (Proposal #3) is newly complete; prioritize validation tooling
- Testing utilities are essential for quality assurance and confidence
- Advanced debugging and enterprise monitoring can wait for production adoption feedback
- Avoid dependency creep (structlog, prometheus_client, opentelemetry) before validation

**Target Audience:**
- **Developers** building ML-integrated applications
- **QA Engineers** testing integration code
- **DevOps Engineers** (deferred: enterprise monitoring)
- **Integration Architects** designing development workflows

**What This Document Covers:**
- ⏸️ **Debugging:** Source maps, breakpoints, trace correlation (DEFERRED - complex features)
- ✅ **Testing:** Integration test utilities, mocking frameworks, performance benchmarking (ESSENTIAL)
- ✅ **Development:** Enhanced REPL with async/callback testing commands (CORE ONLY)
- ✅ **CLI Tools:** Validation and benchmarking utilities (MINIMAL)
- ⏸️ **Monitoring:** Prometheus metrics, distributed tracing, structured logging (DEFERRED)

**Prerequisites:**
- Familiarity with the core Integration Toolkit architecture (see `integration-toolkit.md`)
- Understanding of async/await patterns in Python
- Basic knowledge of mlpy's capability-based security model

---

## Table of Contents

1. ⏸️ [Debugging Integration Code](#1-debugging-integration-code) - **DEFERRED**
2. ✅ [Advanced Testing Utilities](#2-advanced-testing-utilities) - **ESSENTIAL - IMPLEMENT FULLY**
3. ✅ [REPL Development Workflow](#3-repl-development-workflow) - **CORE COMMANDS ONLY**
4. ✅ [CLI Tools for Integration](#4-cli-tools-for-integration) - **MINIMAL SUBSET**
5. ⏸️ [Observability and Monitoring](#5-observability-and-monitoring) - **DEFERRED**

---

## Implementation Roadmap

### Phase 1: Essential Testing Infrastructure (Week 1)
**Priority: HIGH - Implement Now**

- ✅ **Section 2.1-2.3:** Integration testing framework (`IntegrationTestHelper`, mock environments)
- ✅ **Section 2.4:** Performance testing utilities
- ✅ **Section 2.5:** Testing best practices documentation

**Deliverables:**
- `src/mlpy/integration/testing/test_utilities.py`
- `src/mlpy/integration/testing/mocks.py`
- `src/mlpy/integration/testing/performance.py`
- Test examples for async execution and callbacks

### Phase 2: Developer Experience Tools (Week 2)
**Priority: MEDIUM - Implement Core Features Only**

- ✅ **Section 3.1-3.2:** Core REPL commands (.async, .callback, .caps, .grant, .benchmark)
- ✅ **Section 4.1:** CLI validate and benchmark commands
- ⏸️ **Section 3.3-3.4:** Session management and complex debugging (DEFERRED)
- ⏸️ **Section 4.2:** Project configuration (use existing mlpy.json patterns)

**Deliverables:**
- Enhanced `IntegrationREPL` with 5 core commands
- `mlpy integration validate` CLI command
- `mlpy integration benchmark` CLI command

### Deferred Until Adoption (Future Phases)
**Priority: LOW - Wait for User Demand**

- ⏸️ **Section 1:** All debugging features (async source maps, breakpoints, DAP integration)
- ⏸️ **Section 5:** All observability features (Prometheus, OpenTelemetry, structured logging)
- ⏸️ **Advanced REPL:** Session management, complex state inspection
- ⏸️ **Advanced CLI:** create-callback code generation, separate integration REPL

---

## 1. Debugging Integration Code

**⏸️ IMPLEMENTATION STATUS: DEFERRED**

**Rationale:** The debugging features in this section are over-engineered for the current adoption stage. Complex async source mapping, breakpoint instrumentation, and DAP integration add significant complexity without demonstrated user need.

**Essential Subset (Keep):**
- Simple REPL commands: `.trace <execution_id>`, `.inspect <variable>`
- Basic execution history tracking

**Deferred Features:**
- `AsyncExecutionSourceMap` with parent stack tracking
- Breakpoint instrumentation in code generation
- `BreakpointManager` with hit callbacks
- DAP (Debug Adapter Protocol) integration
- Complex source map correlation across async boundaries

**When to Implement:** After users report debugging challenges with async ML execution and provide specific use cases.

---

### 1.1 The Debugging Challenge (DEFERRED)

Debugging ML code executed through the Integration Toolkit presents unique challenges:

**Core Problems:**
1. ML code executes in async contexts (thread pools, event loops)
2. Callbacks are invoked from Python event handlers
3. Source maps must bridge Python → ML → Python boundaries
4. REPL sessions maintain state across multiple executions
5. Async execution loses stack trace context

**Requirements:**
- Step-through debugging in async-executed ML code
- Breakpoint support in callbacks
- State inspection during REPL execution
- Trace correlation across language boundaries
- Integration with existing DAP debugger

### 1.2 Source Map Integration with Async Execution

The Integration Toolkit extends source map generation to support async execution contexts:

**Enhanced Source Map Structure:**
```python
@dataclass
class AsyncExecutionSourceMap:
    """Source map for async-executed ML code"""

    # Standard source map data
    ml_source: str
    python_source: str
    mappings: List[SourceMapping]

    # Async execution context
    execution_id: str  # Unique ID for this execution
    thread_id: int  # Thread pool worker ID
    parent_stack: List[FrameInfo]  # Python call stack before ML execution

    # Timing and performance
    submit_time: float
    start_time: float
    end_time: Optional[float]

    # Result tracking
    result: Optional[Any]
    exception: Optional[Exception]
```

**Implementation:**
```python
# src/mlpy/integration/debug/async_source_mapper.py

class AsyncSourceMapper:
    """Source map management for async ML execution"""

    def __init__(self):
        self._maps: Dict[str, AsyncExecutionSourceMap] = {}
        self._active_executions: Dict[str, asyncio.Task] = {}
        self._lock = threading.Lock()

    def create_map(
        self,
        ml_code: str,
        execution_id: str,
        parent_stack: Optional[List[FrameInfo]] = None
    ) -> AsyncExecutionSourceMap:
        """Create source map for async execution"""

        # Capture parent stack if not provided
        if parent_stack is None:
            parent_stack = self._capture_stack()

        # Generate Python code and mappings
        transpiler = MLTranspiler()
        result = transpiler.transpile(ml_code, source_map=True)

        # Create async-aware source map
        source_map = AsyncExecutionSourceMap(
            ml_source=ml_code,
            python_source=result.python_code,
            mappings=result.source_map.mappings,
            execution_id=execution_id,
            thread_id=threading.get_ident(),
            parent_stack=parent_stack,
            submit_time=time.time(),
            start_time=0.0,
            end_time=None,
            result=None,
            exception=None
        )

        with self._lock:
            self._maps[execution_id] = source_map

        return source_map

    def update_execution_start(self, execution_id: str):
        """Mark execution start time"""
        with self._lock:
            if execution_id in self._maps:
                self._maps[execution_id].start_time = time.time()

    def update_execution_end(
        self,
        execution_id: str,
        result: Optional[Any] = None,
        exception: Optional[Exception] = None
    ):
        """Mark execution completion"""
        with self._lock:
            if execution_id in self._maps:
                source_map = self._maps[execution_id]
                source_map.end_time = time.time()
                source_map.result = result
                source_map.exception = exception

    def get_map(self, execution_id: str) -> Optional[AsyncExecutionSourceMap]:
        """Retrieve source map by execution ID"""
        with self._lock:
            return self._maps.get(execution_id)

    def _capture_stack(self) -> List[FrameInfo]:
        """Capture current Python call stack"""
        stack = []
        for frame_info in inspect.stack()[2:]:  # Skip this method and caller
            stack.append(FrameInfo(
                filename=frame_info.filename,
                lineno=frame_info.lineno,
                function=frame_info.function,
                code_context=frame_info.code_context
            ))
        return stack
```

**Integration with AsyncMLExecutor:**
```python
# Enhanced async_ml_execute with source map support

async def async_ml_execute(
    ml_code: str,
    timeout: Optional[float] = None,
    context: Optional[Dict[str, Any]] = None,
    enable_debugging: bool = False,  # NEW
    **executor_kwargs
) -> AsyncMLResult:
    """Execute ML code asynchronously with debugging support"""

    executor = get_async_executor(**executor_kwargs)
    execution_id = str(uuid.uuid4())

    # Create source map if debugging enabled
    source_map = None
    if enable_debugging:
        mapper = AsyncSourceMapper.get_instance()
        source_map = mapper.create_map(ml_code, execution_id)

    try:
        # Execute with source map tracking
        if source_map:
            mapper.update_execution_start(execution_id)

        result = await executor.execute(
            ml_code,
            timeout=timeout,
            context=context,
            execution_id=execution_id  # Pass for tracing
        )

        if source_map:
            mapper.update_execution_end(execution_id, result=result)

        return AsyncMLResult(
            success=True,
            result=result,
            execution_id=execution_id,
            source_map=source_map  # Include in result
        )

    except Exception as e:
        if source_map:
            mapper.update_execution_end(execution_id, exception=e)
        raise
```

### 1.3 Breakpoint Support in Async ML Code

**Challenge:** Traditional breakpoints don't work in thread pool executed code.

**Solution:** Instrumentation-based breakpoints with event notifications:

```python
# src/mlpy/integration/debug/breakpoint_manager.py

class BreakpointManager:
    """Manage breakpoints for async-executed ML code"""

    def __init__(self):
        self._breakpoints: Dict[str, Set[int]] = {}  # file -> line numbers
        self._hit_callbacks: List[Callable] = []
        self._lock = threading.Lock()

    def add_breakpoint(self, ml_file: str, line: int):
        """Add breakpoint at ML source location"""
        with self._lock:
            if ml_file not in self._breakpoints:
                self._breakpoints[ml_file] = set()
            self._breakpoints[ml_file].add(line)

    def remove_breakpoint(self, ml_file: str, line: int):
        """Remove breakpoint"""
        with self._lock:
            if ml_file in self._breakpoints:
                self._breakpoints[ml_file].discard(line)

    def register_hit_callback(self, callback: Callable):
        """Register callback for breakpoint hits"""
        self._hit_callbacks.append(callback)

    def check_breakpoint(
        self,
        execution_id: str,
        ml_file: str,
        ml_line: int,
        local_vars: Dict[str, Any]
    ) -> bool:
        """Check if breakpoint is hit, return True if should pause"""

        with self._lock:
            if ml_file in self._breakpoints and ml_line in self._breakpoints[ml_file]:
                # Breakpoint hit!
                for callback in self._hit_callbacks:
                    try:
                        callback(BreakpointHitEvent(
                            execution_id=execution_id,
                            ml_file=ml_file,
                            ml_line=ml_line,
                            local_vars=local_vars,
                            timestamp=time.time()
                        ))
                    except Exception as e:
                        logger.error(f"Breakpoint callback error: {e}")

                return True

        return False
```

**Integration with Code Generation:**
```python
# Enhanced Python generator injects breakpoint checks

class PythonGeneratorWithBreakpoints(PythonGenerator):
    """Python generator with breakpoint instrumentation"""

    def visit_statement(self, node: ASTNode) -> ast.stmt:
        """Wrap statements with breakpoint checks"""

        # Generate normal statement
        py_stmt = super().visit_statement(node)

        if not self.enable_breakpoints:
            return py_stmt

        # Inject breakpoint check before statement
        check_call = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='__mlpy_check_breakpoint__', ctx=ast.Load()),
                args=[
                    ast.Constant(value=self.current_file),
                    ast.Constant(value=node.line),
                    ast.Call(
                        func=ast.Name(id='locals', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    )
                ],
                keywords=[]
            )
        )

        # Return both check and statement
        return [check_call, py_stmt]
```

### 1.4 Debugging ML Callbacks

**Challenge:** Callbacks are invoked from Python event handlers, losing context.

**Solution:** Callback wrapper with debugging support:

```python
# src/mlpy/integration/debug/callback_debugger.py

class CallbackDebugWrapper:
    """Debug-aware callback wrapper"""

    def __init__(
        self,
        session: REPLSession,
        function_name: str,
        enable_debugging: bool = True
    ):
        self.session = session
        self.function_name = function_name
        self.enable_debugging = enable_debugging
        self.breakpoint_manager = BreakpointManager.get_instance()

    def __call__(self, *args, **kwargs) -> Any:
        """Execute callback with debugging support"""

        execution_id = str(uuid.uuid4())

        if self.enable_debugging:
            # Create source map for callback execution
            mapper = AsyncSourceMapper.get_instance()
            ml_code = f"{self.function_name}({self._format_args(args, kwargs)});"
            source_map = mapper.create_map(ml_code, execution_id)
            mapper.update_execution_start(execution_id)

        try:
            # Execute callback through REPL
            result = self.session.call_function(
                self.function_name,
                args,
                kwargs,
                execution_id=execution_id  # Pass for tracing
            )

            if self.enable_debugging:
                mapper.update_execution_end(execution_id, result=result)

            return result

        except Exception as e:
            if self.enable_debugging:
                mapper.update_execution_end(execution_id, exception=e)
            raise

# Enhanced ml_callback with debugging support
def ml_callback(
    session: REPLSession,
    function_name: str,
    enable_debugging: bool = False,  # NEW
    **kwargs
) -> Callable:
    """Create ML callback with optional debugging support"""

    if enable_debugging:
        return CallbackDebugWrapper(session, function_name, enable_debugging=True)
    else:
        # Use lightweight wrapper for production
        return _create_lightweight_callback(session, function_name, **kwargs)
```

### 1.5 REPL Debugging Commands

**Interactive Debugging from REPL:**

```python
# Enhanced REPL with debugging commands

class DebugREPL(REPLSession):
    """REPL with debugging capabilities"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.breakpoint_manager = BreakpointManager.get_instance()
        self.source_mapper = AsyncSourceMapper.get_instance()
        self.register_debug_commands()

    def register_debug_commands(self):
        """Register debugging commands"""

        self.add_command('.break', self.cmd_set_breakpoint,
                        "Set breakpoint: .break <file>:<line>")
        self.add_command('.clear', self.cmd_clear_breakpoint,
                        "Clear breakpoint: .clear <file>:<line>")
        self.add_command('.list', self.cmd_list_breakpoints,
                        "List all breakpoints")
        self.add_command('.trace', self.cmd_show_trace,
                        "Show execution trace: .trace <execution_id>")
        self.add_command('.inspect', self.cmd_inspect_state,
                        "Inspect session state: .inspect [variable]")
        self.add_command('.async', self.cmd_list_async,
                        "List active async executions")

    def cmd_set_breakpoint(self, args: List[str]):
        """Set breakpoint: .break file.ml:42"""
        if not args:
            print("Usage: .break <file>:<line>")
            return

        try:
            file_line = args[0]
            ml_file, line_str = file_line.split(':')
            line = int(line_str)

            self.breakpoint_manager.add_breakpoint(ml_file, line)
            print(f"Breakpoint set at {ml_file}:{line}")
        except ValueError:
            print("Invalid breakpoint format. Use: .break <file>:<line>")

    def cmd_show_trace(self, args: List[str]):
        """Show execution trace: .trace <execution_id>"""
        if not args:
            print("Usage: .trace <execution_id>")
            return

        execution_id = args[0]
        source_map = self.source_mapper.get_map(execution_id)

        if not source_map:
            print(f"No trace found for execution {execution_id}")
            return

        # Display comprehensive trace
        print(f"\n=== Execution Trace: {execution_id} ===")
        print(f"Thread: {source_map.thread_id}")
        print(f"Submit time: {source_map.submit_time}")
        print(f"Start time: {source_map.start_time}")
        print(f"Duration: {(source_map.end_time or time.time()) - source_map.start_time:.3f}s")

        print("\n--- Python Call Stack Before ML Execution ---")
        for frame in source_map.parent_stack:
            print(f"  {frame.filename}:{frame.lineno} in {frame.function}")

        print("\n--- ML Source Code ---")
        print(source_map.ml_source)

        if source_map.exception:
            print("\n--- Exception ---")
            print(f"{type(source_map.exception).__name__}: {source_map.exception}")
        elif source_map.result is not None:
            print("\n--- Result ---")
            print(repr(source_map.result))

    def cmd_inspect_state(self, args: List[str]):
        """Inspect REPL session state"""
        if not args:
            # Show all variables
            print("\n=== Session Variables ===")
            for name, value in self.variables.items():
                print(f"{name}: {type(value).__name__} = {repr(value)[:50]}")
        else:
            # Show specific variable
            var_name = args[0]
            if var_name in self.variables:
                value = self.variables[var_name]
                print(f"\n{var_name}: {type(value).__name__}")
                print(f"Value: {repr(value)}")
                if hasattr(value, '__dict__'):
                    print(f"Attributes: {list(value.__dict__.keys())}")
            else:
                print(f"Variable '{var_name}' not found")

    def cmd_list_async(self, args: List[str]):
        """List active async executions"""
        active = self.source_mapper._active_executions

        if not active:
            print("No active async executions")
            return

        print("\n=== Active Async Executions ===")
        for execution_id, task in active.items():
            source_map = self.source_mapper.get_map(execution_id)
            if source_map:
                duration = time.time() - source_map.submit_time
                print(f"{execution_id[:8]}: {duration:.2f}s - {source_map.ml_source[:50]}")
```

**Usage Example:**
```python
# Start debug-enabled REPL
repl = DebugREPL()

# Set breakpoints
repl.execute(".break validator.ml:25")
repl.execute(".break validator.ml:42")

# Execute code
repl.execute("let result = validate_order(order);")

# Inspect state when breakpoint hits
repl.execute(".inspect result")
repl.execute(".inspect order")

# Show execution trace
repl.execute(".trace abc123-execution-id")
```

### 1.6 DAP Debugger Integration

**Integration with VS Code Debug Adapter Protocol:**

```python
# src/mlpy/integration/debug/dap_integration.py

class MLIntegrationDebugAdapter:
    """DAP adapter for ML Integration Toolkit debugging"""

    def __init__(self, dap_server: DebugAdapterServer):
        self.dap = dap_server
        self.breakpoint_manager = BreakpointManager.get_instance()
        self.source_mapper = AsyncSourceMapper.get_instance()

        # Register breakpoint hit callback
        self.breakpoint_manager.register_hit_callback(self._on_breakpoint_hit)

    def _on_breakpoint_hit(self, event: BreakpointHitEvent):
        """Handle breakpoint hit event from async execution"""

        # Get source map for this execution
        source_map = self.source_mapper.get_map(event.execution_id)
        if not source_map:
            return

        # Convert ML line to Python line
        py_line = self._ml_to_python_line(source_map, event.ml_line)

        # Send DAP stopped event
        self.dap.send_event('stopped', {
            'reason': 'breakpoint',
            'threadId': source_map.thread_id,
            'allThreadsStopped': False
        })

        # Provide stack trace when requested
        self.dap.register_stack_trace_provider(
            source_map.thread_id,
            lambda: self._build_stack_trace(source_map, event)
        )

    def _build_stack_trace(
        self,
        source_map: AsyncExecutionSourceMap,
        event: BreakpointHitEvent
    ) -> List[Dict]:
        """Build DAP stack trace from source map"""

        frames = []

        # Add ML frame
        frames.append({
            'id': 1,
            'name': f'ML: {event.ml_file}',
            'source': {
                'name': event.ml_file,
                'path': event.ml_file,
                'sourceReference': 0
            },
            'line': event.ml_line,
            'column': 1
        })

        # Add Python frames from parent stack
        for i, frame_info in enumerate(source_map.parent_stack):
            frames.append({
                'id': i + 2,
                'name': frame_info.function,
                'source': {
                    'name': os.path.basename(frame_info.filename),
                    'path': frame_info.filename,
                    'sourceReference': 0
                },
                'line': frame_info.lineno,
                'column': 1
            })

        return frames
```

### 1.7 Debugging Best Practices

**1. Enable Debugging in Development Only:**
```python
# Development
result = await async_ml_execute(
    ml_code,
    enable_debugging=True  # Full debugging support
)

# Production
result = await async_ml_execute(
    ml_code,
    enable_debugging=False  # No overhead
)
```

**2. Use Execution IDs for Trace Correlation:**
```python
# Track async execution
result = await async_ml_execute(ml_code, enable_debugging=True)
print(f"Execution ID: {result.execution_id}")

# Later, inspect trace
repl.execute(f".trace {result.execution_id}")
```

**3. Set Conditional Breakpoints:**
```python
# Set breakpoint with condition
self.breakpoint_manager.add_breakpoint(
    'validator.ml',
    42,
    condition=lambda vars: vars.get('price', 0) > 1000
)
```

**4. Debugging Callbacks:**
```python
# Enable debugging for specific callback
validate = ml_callback(
    session,
    'validate_order',
    enable_debugging=True  # Debug this callback
)

# Use in event handler
button.config(command=lambda: validate(order))
```

**5. REPL Debugging Workflow:**
```python
# 1. Start debug REPL
repl = DebugREPL()

# 2. Load ML code
repl.execute("import validator;")

# 3. Set breakpoints
repl.execute(".break validator.ml:25")

# 4. Execute function
repl.execute("validate_order(test_order);")

# 5. When breakpoint hits, inspect
repl.execute(".inspect test_order")
repl.execute(".trace <execution_id>")
```

---

## 2. Advanced Testing Utilities

**✅ IMPLEMENTATION STATUS: ESSENTIAL - IMPLEMENT FULLY**

**Rationale:** Testing utilities are critical for validating the Integration Toolkit (Proposal #3). They provide confidence in async execution, callback functionality, and capability propagation. This is foundational infrastructure for quality assurance.

**Implementation Priority: HIGH**

**All Features in This Section:**
- ✅ **Section 2.1:** Integration testing framework (IntegrationTestHelper)
- ✅ **Section 2.2:** Mock execution environments
- ✅ **Section 2.3:** Integration test examples
- ✅ **Section 2.4:** Performance testing utilities
- ✅ **Section 2.5:** Testing best practices

**Deliverables:**
- `src/mlpy/integration/testing/test_utilities.py`
- `src/mlpy/integration/testing/mocks.py`
- `src/mlpy/integration/testing/performance.py`
- Comprehensive test examples for async and callback scenarios

**Estimated Implementation:** 3-4 days

---

### 2.1 Integration Testing Framework

The Integration Toolkit provides comprehensive testing utilities for async execution, callbacks, and capability propagation:

**Core Testing Infrastructure:**

```python
# src/mlpy/integration/testing/test_utilities.py

class IntegrationTestHelper:
    """Utilities for testing ML Integration Toolkit"""

    def __init__(self):
        self.mock_repl_sessions = []
        self.captured_async_executions = []
        self.capability_violations = []

    def create_test_repl(
        self,
        capabilities: Optional[Set[CapabilityToken]] = None
    ) -> REPLSession:
        """Create REPL session with test configuration"""

        session = REPLSession(
            enable_debugging=True,
            capture_metrics=True
        )

        if capabilities:
            cap_manager = get_capability_manager()
            cap_manager.set_context(CapabilityContext(
                capabilities=capabilities,
                context_id=str(uuid.uuid4()),
                parent_context_id=None,
                execution_type='repl',
                thread_id=threading.get_ident(),
                created_at=time.time()
            ))

        self.mock_repl_sessions.append(session)
        return session

    async def assert_async_execution(
        self,
        ml_code: str,
        expected_result: Any,
        timeout: float = 5.0,
        capabilities: Optional[Set[CapabilityToken]] = None
    ):
        """Assert async execution produces expected result"""

        result = await async_ml_execute(
            ml_code,
            timeout=timeout,
            capabilities=capabilities,
            enable_debugging=True
        )

        self.captured_async_executions.append({
            'ml_code': ml_code,
            'result': result,
            'execution_id': result.execution_id
        })

        assert result.success, f"Execution failed: {result.error}"
        assert result.result == expected_result, \
            f"Expected {expected_result}, got {result.result}"

    def assert_callback_works(
        self,
        session: REPLSession,
        function_name: str,
        args: tuple,
        expected_result: Any,
        capabilities: Optional[Set[CapabilityToken]] = None
    ):
        """Assert callback executes correctly"""

        callback = ml_callback(
            session,
            function_name,
            capabilities=capabilities,
            enable_debugging=True
        )

        result = callback(*args)
        assert result == expected_result, \
            f"Expected {expected_result}, got {result}"

    def assert_capability_violation(
        self,
        ml_code: str,
        required_capability: CapabilityToken,
        available_capabilities: Optional[Set[CapabilityToken]] = None
    ):
        """Assert that capability violation is raised"""

        async def execute():
            await async_ml_execute(
                ml_code,
                capabilities=available_capabilities or set()
            )

        # Should raise CapabilityViolationError
        with pytest.raises(CapabilityViolationError) as exc_info:
            asyncio.run(execute())

        assert str(required_capability) in str(exc_info.value)

    def cleanup(self):
        """Clean up test resources"""
        for session in self.mock_repl_sessions:
            session.close()
        self.mock_repl_sessions.clear()
        self.captured_async_executions.clear()
        self.capability_violations.clear()
```

### 2.2 Mock Execution Environment

**Mocking External Dependencies:**

```python
# src/mlpy/integration/testing/mocks.py

class MockAsyncExecutor:
    """Mock async executor for testing"""

    def __init__(self):
        self.executions = []
        self.should_fail = False
        self.execution_delay = 0.0

    async def execute(
        self,
        ml_code: str,
        timeout: Optional[float] = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Any:
        """Mock execution"""

        execution_record = {
            'ml_code': ml_code,
            'timeout': timeout,
            'context': context,
            'timestamp': time.time()
        }
        self.executions.append(execution_record)

        if self.execution_delay > 0:
            await asyncio.sleep(self.execution_delay)

        if self.should_fail:
            raise RuntimeError("Mock execution failure")

        # Return mock result
        return {"status": "success", "mock": True}

class MockREPLSession:
    """Mock REPL session for testing"""

    def __init__(self):
        self.variables = {}
        self.executed_lines = []
        self.function_calls = []

    def execute(self, ml_code: str):
        """Mock execution"""
        self.executed_lines.append(ml_code)
        return {"executed": True}

    def call_function(
        self,
        function_name: str,
        args: tuple,
        kwargs: dict,
        **options
    ) -> Any:
        """Mock function call"""
        call_record = {
            'function_name': function_name,
            'args': args,
            'kwargs': kwargs,
            'timestamp': time.time()
        }
        self.function_calls.append(call_record)

        # Return mock result based on function name
        if function_name == 'validate_order':
            return {'valid': True}
        elif function_name == 'calculate_total':
            return 100.50
        else:
            return None

class MockCapabilityManager:
    """Mock capability manager for testing"""

    def __init__(self):
        self.contexts = []
        self.violations = []

    def set_context(self, context: CapabilityContext):
        """Mock set context"""
        self.contexts.append(context)

    def get_context(self) -> Optional[CapabilityContext]:
        """Mock get context"""
        return self.contexts[-1] if self.contexts else None

    def record_violation(self, violation: CapabilityViolation):
        """Mock record violation"""
        self.violations.append(violation)
```

### 2.3 Integration Test Examples

**Test Suite for Async Execution:**

```python
# tests/integration/test_async_ml_execution.py

class TestAsyncMLExecution:
    """Test async ML execution"""

    @pytest.fixture
    def test_helper(self):
        helper = IntegrationTestHelper()
        yield helper
        helper.cleanup()

    async def test_simple_async_execution(self, test_helper):
        """Test basic async execution"""

        ml_code = "let result = 2 + 2; result;"

        await test_helper.assert_async_execution(
            ml_code,
            expected_result=4,
            timeout=5.0
        )

    async def test_async_execution_with_timeout(self, test_helper):
        """Test async execution respects timeout"""

        ml_code = """
        let count = 0;
        while (count < 1000000) {
            count = count + 1;
        }
        count;
        """

        with pytest.raises(asyncio.TimeoutError):
            await async_ml_execute(ml_code, timeout=0.1)

    async def test_concurrent_async_executions(self, test_helper):
        """Test multiple concurrent async executions"""

        tasks = []
        for i in range(10):
            ml_code = f"let result = {i} * 2; result;"
            task = async_ml_execute(ml_code, timeout=5.0)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        assert len(results) == 10
        for i, result in enumerate(results):
            assert result.result == i * 2

    async def test_async_execution_with_capabilities(self, test_helper):
        """Test async execution with capability propagation"""

        file_cap = CapabilityToken('file:read', pattern='/data/*')

        ml_code = '''
        import file;
        let content = file.read_file("/data/test.csv");
        '''

        # Should work with capability
        await test_helper.assert_async_execution(
            ml_code,
            expected_result="test data",
            capabilities={file_cap}
        )

        # Should fail without capability
        test_helper.assert_capability_violation(
            ml_code,
            required_capability=file_cap,
            available_capabilities=set()
        )
```

**Test Suite for Callbacks:**

```python
# tests/integration/test_ml_callbacks.py

class TestMLCallbacks:
    """Test ML callback integration"""

    @pytest.fixture
    def test_helper(self):
        helper = IntegrationTestHelper()
        yield helper
        helper.cleanup()

    def test_basic_callback(self, test_helper):
        """Test basic callback functionality"""

        session = test_helper.create_test_repl()
        session.execute("let double = (x) => x * 2;")

        callback = ml_callback(session, 'double')
        result = callback(5)

        assert result == 10

    def test_callback_with_multiple_args(self, test_helper):
        """Test callback with multiple arguments"""

        session = test_helper.create_test_repl()
        session.execute("let add = (a, b) => a + b;")

        callback = ml_callback(session, 'add')
        result = callback(3, 7)

        assert result == 10

    def test_callback_with_capabilities(self, test_helper):
        """Test callback capability inheritance"""

        network_cap = CapabilityToken('network:http', pattern='api.example.com')

        session = test_helper.create_test_repl(capabilities={network_cap})
        session.execute('''
        import http;
        let fetch_data = (url) => http.get(url);
        ''')

        test_helper.assert_callback_works(
            session,
            'fetch_data',
            ('https://api.example.com/data',),
            expected_result={'data': 'mock response'},
            capabilities={network_cap}
        )

    def test_callback_error_handling(self, test_helper):
        """Test callback error handling"""

        session = test_helper.create_test_repl()
        session.execute("let divide = (a, b) => a / b;")

        error_handler_called = False
        error_message = None

        def error_handler(e):
            nonlocal error_handler_called, error_message
            error_handler_called = True
            error_message = str(e)
            return {"error": "Division error"}

        callback = ml_callback(
            session,
            'divide',
            error_handler=error_handler
        )

        result = callback(10, 0)  # Division by zero

        assert error_handler_called
        assert "division" in error_message.lower() or "zero" in error_message.lower()
        assert result == {"error": "Division error"}
```

### 2.4 Performance Testing Utilities

**Benchmark Async Execution:**

```python
# src/mlpy/integration/testing/performance.py

class PerformanceTester:
    """Performance testing utilities for Integration Toolkit"""

    def __init__(self):
        self.metrics = []

    async def benchmark_async_execution(
        self,
        ml_code: str,
        iterations: int = 100
    ) -> Dict[str, float]:
        """Benchmark async execution performance"""

        execution_times = []

        for _ in range(iterations):
            start = time.perf_counter()
            await async_ml_execute(ml_code, timeout=30.0)
            end = time.perf_counter()
            execution_times.append(end - start)

        return {
            'mean': statistics.mean(execution_times),
            'median': statistics.median(execution_times),
            'std_dev': statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
            'min': min(execution_times),
            'max': max(execution_times),
            'iterations': iterations
        }

    async def benchmark_concurrent_executions(
        self,
        ml_code: str,
        concurrency: int = 10
    ) -> Dict[str, float]:
        """Benchmark concurrent execution performance"""

        start = time.perf_counter()

        tasks = [async_ml_execute(ml_code, timeout=30.0) for _ in range(concurrency)]
        await asyncio.gather(*tasks)

        end = time.perf_counter()
        total_time = end - start

        return {
            'total_time': total_time,
            'avg_per_execution': total_time / concurrency,
            'throughput': concurrency / total_time,
            'concurrency': concurrency
        }

    def benchmark_callback_overhead(
        self,
        session: REPLSession,
        function_name: str,
        args: tuple,
        iterations: int = 1000
    ) -> Dict[str, float]:
        """Benchmark callback overhead"""

        callback = ml_callback(session, function_name)

        execution_times = []
        for _ in range(iterations):
            start = time.perf_counter()
            callback(*args)
            end = time.perf_counter()
            execution_times.append(end - start)

        return {
            'mean': statistics.mean(execution_times),
            'median': statistics.median(execution_times),
            'overhead_ms': statistics.mean(execution_times) * 1000,
            'iterations': iterations
        }

# Usage
async def test_performance():
    tester = PerformanceTester()

    # Benchmark async execution
    results = await tester.benchmark_async_execution(
        "let result = 2 + 2; result;",
        iterations=100
    )
    print(f"Async execution: {results['mean']*1000:.2f}ms avg")

    # Benchmark concurrent executions
    results = await tester.benchmark_concurrent_executions(
        "let result = 2 + 2; result;",
        concurrency=50
    )
    print(f"Throughput: {results['throughput']:.2f} executions/sec")
```

### 2.5 Testing Best Practices

**1. Use IntegrationTestHelper for Comprehensive Tests:**
```python
@pytest.fixture
def integration_helper():
    helper = IntegrationTestHelper()
    yield helper
    helper.cleanup()

async def test_full_integration(integration_helper):
    # Test async execution
    await integration_helper.assert_async_execution(
        "2 + 2",
        expected_result=4
    )

    # Test callbacks
    session = integration_helper.create_test_repl()
    session.execute("let add = (a, b) => a + b;")
    integration_helper.assert_callback_works(
        session, 'add', (3, 5), expected_result=8
    )
```

**2. Mock External Dependencies:**
```python
def test_with_mock_executor(monkeypatch):
    mock_executor = MockAsyncExecutor()
    mock_executor.execution_delay = 0.1

    monkeypatch.setattr('mlpy.integration.async_executor', mock_executor)

    # Test with controlled executor behavior
    result = await async_ml_execute("test code")
    assert mock_executor.executions[0]['ml_code'] == "test code"
```

**3. Test Capability Propagation:**
```python
async def test_capability_propagation():
    helper = IntegrationTestHelper()

    file_cap = CapabilityToken('file:read', pattern='/data/*')

    # Test async inherits capabilities
    await helper.assert_async_execution(
        "import file; file.read_file('/data/test.csv');",
        expected_result="data",
        capabilities={file_cap}
    )

    # Test violation detection
    helper.assert_capability_violation(
        "import file; file.read_file('/etc/passwd');",
        required_capability=CapabilityToken('file:read', pattern='/etc/passwd'),
        available_capabilities={file_cap}
    )
```

---

## 3. REPL Development Workflow

**✅ IMPLEMENTATION STATUS: CORE COMMANDS ONLY**

**Rationale:** Enhanced REPL commands for testing async execution and callbacks are valuable for development. However, complex session management and debugging workflows can be deferred until demonstrated need.

**Implementation Priority: MEDIUM**

**Features to Implement:**
- ✅ **Section 3.1:** Core REPL commands only:
  - `.async <code>` - Execute code asynchronously
  - `.callback <function>` - Create and test callbacks
  - `.caps` - Show current capabilities
  - `.grant <capability>` - Grant capability for testing
  - `.benchmark <code>` - Quick performance check

**Features to Defer:**
- ⏸️ **Section 3.2:** Full IntegrationREPL class with 12+ commands
- ⏸️ **Section 3.3:** REPLSessionManager for long-running sessions
- ⏸️ **Section 3.4:** Complex interactive debugging workflow
- ⏸️ Advanced commands: `.await`, `.revoke`, `.test`, `.call`

**Deliverables:**
- 5 core commands added to existing REPL (extend `src/mlpy/cli/repl.py`)
- Simple implementation without heavyweight session management
- Documentation for core commands

**Estimated Implementation:** 2-3 days

---

### 3.1 Enhanced REPL for Integration Development (CORE COMMANDS ONLY)

The Integration Toolkit provides an enhanced REPL experience for developing and testing ML integrations:

**IntegrationREPL Features:**

```python
# src/mlpy/integration/repl/integration_repl.py

class IntegrationREPL(REPLSession):
    """Enhanced REPL for integration development"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Integration-specific features
        self.async_executor = None
        self.registered_callbacks = {}
        self.capability_context = None

        # Register integration commands
        self.register_integration_commands()

    def register_integration_commands(self):
        """Register commands for integration development"""

        # Async execution commands
        self.add_command('.async', self.cmd_async_execute,
                        "Execute code asynchronously: .async <code>")
        self.add_command('.await', self.cmd_await_execution,
                        "Wait for async execution: .await <execution_id>")

        # Callback management
        self.add_command('.callback', self.cmd_create_callback,
                        "Create callback: .callback <function_name>")
        self.add_command('.callbacks', self.cmd_list_callbacks,
                        "List registered callbacks")
        self.add_command('.call', self.cmd_invoke_callback,
                        "Invoke callback: .call <callback_name> <args>")

        # Capability management
        self.add_command('.caps', self.cmd_show_capabilities,
                        "Show current capabilities")
        self.add_command('.grant', self.cmd_grant_capability,
                        "Grant capability: .grant <capability>")
        self.add_command('.revoke', self.cmd_revoke_capability,
                        "Revoke capability: .revoke <capability>")

        # Integration testing
        self.add_command('.test', self.cmd_run_integration_test,
                        "Run integration test: .test <test_name>")
        self.add_command('.benchmark', self.cmd_benchmark,
                        "Benchmark code: .benchmark <code>")

        # Module management
        self.add_command('.reload', self.cmd_reload_module,
                        "Reload module: .reload <module_name>")
        self.add_command('.modules', self.cmd_list_modules,
                        "List loaded modules")

    async def cmd_async_execute(self, args: List[str]):
        """Execute code asynchronously"""
        if not args:
            print("Usage: .async <ML code>")
            return

        ml_code = ' '.join(args)

        if not self.async_executor:
            self.async_executor = get_async_executor()

        try:
            result = await async_ml_execute(
                ml_code,
                timeout=30.0,
                enable_debugging=True
            )

            print(f"Execution ID: {result.execution_id}")
            print(f"Result: {result.result}")

        except Exception as e:
            print(f"Async execution failed: {e}")

    def cmd_create_callback(self, args: List[str]):
        """Create callback for ML function"""
        if not args:
            print("Usage: .callback <function_name> [<alias>]")
            return

        function_name = args[0]
        alias = args[1] if len(args) > 1 else function_name

        callback = ml_callback(
            self,
            function_name,
            enable_debugging=True
        )

        self.registered_callbacks[alias] = callback
        print(f"Callback '{alias}' created for function '{function_name}'")
        print(f"Usage: .call {alias} <args>")

    def cmd_list_callbacks(self, args: List[str]):
        """List registered callbacks"""
        if not self.registered_callbacks:
            print("No callbacks registered")
            return

        print("\n=== Registered Callbacks ===")
        for alias, callback in self.registered_callbacks.items():
            print(f"  {alias}: {callback.function_name}")

    def cmd_invoke_callback(self, args: List[str]):
        """Invoke registered callback"""
        if not args:
            print("Usage: .call <callback_name> <args>")
            return

        callback_name = args[0]
        callback_args = args[1:]

        if callback_name not in self.registered_callbacks:
            print(f"Callback '{callback_name}' not found")
            return

        callback = self.registered_callbacks[callback_name]

        try:
            # Parse arguments (simple parsing for demo)
            parsed_args = [eval(arg) for arg in callback_args]
            result = callback(*parsed_args)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Callback invocation failed: {e}")

    def cmd_show_capabilities(self, args: List[str]):
        """Show current capabilities"""
        cap_manager = get_capability_manager()
        context = cap_manager.get_context()

        if not context or not context.capabilities:
            print("No capabilities granted")
            return

        print("\n=== Current Capabilities ===")
        for cap in context.capabilities:
            print(f"  {cap.capability_type}: {cap.pattern}")

    def cmd_grant_capability(self, args: List[str]):
        """Grant capability for testing"""
        if not args:
            print("Usage: .grant <capability_type>:<pattern>")
            print("Example: .grant file:read:/data/*")
            return

        try:
            cap_str = args[0]
            cap_type, pattern = cap_str.split(':')

            cap = CapabilityToken(cap_type, pattern=pattern)

            cap_manager = get_capability_manager()
            context = cap_manager.get_context()

            if context:
                context.capabilities.add(cap)
            else:
                # Create new context
                context = CapabilityContext(
                    capabilities={cap},
                    context_id=str(uuid.uuid4()),
                    parent_context_id=None,
                    execution_type='repl',
                    thread_id=threading.get_ident(),
                    created_at=time.time()
                )
                cap_manager.set_context(context)

            print(f"Granted capability: {cap_type}:{pattern}")

        except ValueError:
            print("Invalid capability format. Use: <type>:<pattern>")

    async def cmd_benchmark(self, args: List[str]):
        """Benchmark code execution"""
        if not args:
            print("Usage: .benchmark <ML code>")
            return

        ml_code = ' '.join(args)
        tester = PerformanceTester()

        print(f"Benchmarking: {ml_code}")
        print("Running 100 iterations...")

        results = await tester.benchmark_async_execution(ml_code, iterations=100)

        print("\n=== Benchmark Results ===")
        print(f"Mean: {results['mean']*1000:.3f}ms")
        print(f"Median: {results['median']*1000:.3f}ms")
        print(f"Std Dev: {results['std_dev']*1000:.3f}ms")
        print(f"Min: {results['min']*1000:.3f}ms")
        print(f"Max: {results['max']*1000:.3f}ms")

    def cmd_reload_module(self, args: List[str]):
        """Reload module"""
        if not args:
            print("Usage: .reload <module_name>")
            return

        module_name = args[0]

        try:
            # Reload module in module registry
            registry = ModuleRegistry.get_instance()
            registry.reload_module(module_name)
            print(f"Module '{module_name}' reloaded")
        except Exception as e:
            print(f"Reload failed: {e}")
```

### 3.2 Interactive Integration Development (DEFERRED)

**Development Workflow:**

```python
# Example interactive session

# 1. Start IntegrationREPL
$ python -m mlpy.integration.repl

mlpy integration> .help
Available commands:
  .async       Execute code asynchronously
  .await       Wait for async execution
  .callback    Create callback for ML function
  .callbacks   List registered callbacks
  .call        Invoke callback
  .caps        Show current capabilities
  .grant       Grant capability
  .benchmark   Benchmark code execution
  .reload      Reload module
  .modules     List loaded modules

# 2. Grant capabilities for testing
mlpy integration> .grant file:read:/data/*
Granted capability: file:read:/data/*

mlpy integration> .grant network:http:api.example.com
Granted capability: network:http:api.example.com

# 3. Define ML functions
mlpy integration> let process_data = (file) => {
...     import file;
...     import http;
...     let data = file.read_file(file);
...     let result = http.post("https://api.example.com/process", data);
...     result;
... };

# 4. Test async execution
mlpy integration> .async process_data("/data/test.csv")
Execution ID: abc123
Result: {"status": "processed", "rows": 100}

# 5. Create callback
mlpy integration> .callback process_data data_processor
Callback 'data_processor' created for function 'process_data'
Usage: .call data_processor <args>

# 6. Test callback
mlpy integration> .call data_processor "/data/test.csv"
Result: {"status": "processed", "rows": 100}

# 7. Benchmark performance
mlpy integration> .benchmark process_data("/data/small.csv")
Benchmarking: process_data("/data/small.csv")
Running 100 iterations...

=== Benchmark Results ===
Mean: 42.315ms
Median: 41.892ms
Std Dev: 5.123ms
Min: 38.142ms
Max: 58.912ms

# 8. Check loaded modules
mlpy integration> .modules
=== Loaded Modules ===
  file: /path/to/mlpy/stdlib/file_bridge.py
  http: /path/to/mlpy/stdlib/http_bridge.py
  string: /path/to/mlpy/stdlib/string_bridge.py

# 9. Reload modified module
mlpy integration> .reload http
Module 'http' reloaded
```

### 3.3 REPL Session Management (DEFERRED)

**Managing Long-Running Sessions:**

```python
# src/mlpy/integration/repl/session_manager.py

class REPLSessionManager:
    """Manage multiple REPL sessions"""

    def __init__(self):
        self.sessions: Dict[str, IntegrationREPL] = {}
        self._lock = threading.Lock()

    def create_session(
        self,
        session_id: Optional[str] = None,
        capabilities: Optional[Set[CapabilityToken]] = None
    ) -> IntegrationREPL:
        """Create new REPL session"""

        if session_id is None:
            session_id = str(uuid.uuid4())

        with self._lock:
            if session_id in self.sessions:
                raise ValueError(f"Session {session_id} already exists")

            session = IntegrationREPL()

            if capabilities:
                cap_manager = get_capability_manager()
                cap_manager.set_context(CapabilityContext(
                    capabilities=capabilities,
                    context_id=session_id,
                    parent_context_id=None,
                    execution_type='repl',
                    thread_id=threading.get_ident(),
                    created_at=time.time()
                ))

            self.sessions[session_id] = session
            return session

    def get_session(self, session_id: str) -> Optional[IntegrationREPL]:
        """Get existing session"""
        with self._lock:
            return self.sessions.get(session_id)

    def close_session(self, session_id: str):
        """Close and remove session"""
        with self._lock:
            if session_id in self.sessions:
                session = self.sessions[session_id]
                session.close()
                del self.sessions[session_id]

    def list_sessions(self) -> List[Dict]:
        """List all active sessions"""
        with self._lock:
            return [
                {
                    'session_id': session_id,
                    'variables': len(session.variables),
                    'callbacks': len(session.registered_callbacks)
                }
                for session_id, session in self.sessions.items()
            ]

# Usage
manager = REPLSessionManager()

# Create session with capabilities
file_cap = CapabilityToken('file:read', pattern='/data/*')
session = manager.create_session(
    session_id='dev-session-1',
    capabilities={file_cap}
)

# Use session
session.execute("import file;")
session.execute("let data = file.read_file('/data/test.csv');")

# Later, retrieve session
session = manager.get_session('dev-session-1')

# Close when done
manager.close_session('dev-session-1')
```

### 3.4 REPL Debugging Workflow (DEFERRED)

**Step-by-Step Debugging:**

```python
# Interactive debugging session

# 1. Start debug-enabled REPL
mlpy integration> .debug on
Debug mode enabled

# 2. Set breakpoints
mlpy integration> .break validator.ml:25
Breakpoint set at validator.ml:25

# 3. Execute code
mlpy integration> import validator; validator.validate_order(order);
Breakpoint hit at validator.ml:25

# 4. Inspect state
mlpy integration> .inspect order
order: Object
Value: {'id': 123, 'total': 150.00, 'items': [{'id': 1, 'price': 50.00}]}
Attributes: ['id', 'total', 'items']

# 5. Continue execution
mlpy integration> .continue
Execution completed
Result: {'valid': true, 'warnings': []}

# 6. Show trace
mlpy integration> .trace last
=== Execution Trace ===
Thread: 12345
Duration: 0.342s

--- Python Call Stack ---
  repl.py:123 in execute
  validator.ml:25 in validate_order

--- ML Source Code ---
import validator;
validator.validate_order(order);

--- Result ---
{'valid': true, 'warnings': []}
```

---

## 4. CLI Tools for Integration

**✅ IMPLEMENTATION STATUS: MINIMAL SUBSET**

**Rationale:** Some CLI tools are useful for validation and performance testing. However, code generation tools and separate integration REPL are unnecessary.

**Implementation Priority: MEDIUM**

**Features to Implement:**
- ✅ **`mlpy integration validate`** - Validate Integration Toolkit setup
  - Check module registry status
  - Check async executor availability
  - Check capability manager readiness
- ✅ **`mlpy integration benchmark <file.ml>`** - Benchmark ML file execution
  - Support `--iterations` and `--concurrency` flags
  - Simple performance reporting

**Features to Defer:**
- ⏸️ **`mlpy integration execute`** - Redundant with existing `mlpy run --async`
- ⏸️ **`mlpy integration create-callback`** - Low value code generation
- ⏸️ **`mlpy integration repl`** - Use main REPL with enhanced commands instead
- ⏸️ **Section 4.2:** Complex project configuration (use existing `mlpy.json` patterns)

**Deliverables:**
- 2 CLI commands: `validate` and `benchmark`
- Minimal implementation extending existing CLI infrastructure
- Documentation for new commands

**Estimated Implementation:** 1-2 days

---

### 4.1 Integration CLI Commands (MINIMAL SUBSET)

The Integration Toolkit extends the mlpy CLI with integration-specific commands:

**CLI Commands:**

```python
# src/mlpy/integration/cli/commands.py

@cli.group()
def integration():
    """Integration Toolkit commands"""
    pass

@integration.command()
@click.argument('ml_file', type=click.Path(exists=True))
@click.option('--async', 'use_async', is_flag=True, help='Execute asynchronously')
@click.option('--timeout', type=float, default=30.0, help='Execution timeout')
@click.option('--capabilities', multiple=True, help='Grant capabilities')
def execute(ml_file: str, use_async: bool, timeout: float, capabilities: tuple):
    """Execute ML file with Integration Toolkit"""

    # Read ML code
    with open(ml_file, 'r') as f:
        ml_code = f.read()

    # Parse capabilities
    caps = set()
    for cap_str in capabilities:
        cap_type, pattern = cap_str.split(':')
        caps.add(CapabilityToken(cap_type, pattern=pattern))

    # Execute
    if use_async:
        result = asyncio.run(async_ml_execute(
            ml_code,
            timeout=timeout,
            capabilities=caps
        ))
    else:
        transpiler = MLTranspiler()
        result = transpiler.execute(ml_code, capabilities=caps)

    click.echo(f"Result: {result}")

@integration.command()
@click.argument('ml_file', type=click.Path(exists=True))
@click.option('--iterations', type=int, default=100, help='Number of iterations')
@click.option('--concurrency', type=int, default=1, help='Concurrent executions')
def benchmark(ml_file: str, iterations: int, concurrency: int):
    """Benchmark ML file execution"""

    with open(ml_file, 'r') as f:
        ml_code = f.read()

    tester = PerformanceTester()

    if concurrency > 1:
        results = asyncio.run(tester.benchmark_concurrent_executions(
            ml_code,
            concurrency=concurrency
        ))
        click.echo(f"Throughput: {results['throughput']:.2f} executions/sec")
        click.echo(f"Total time: {results['total_time']:.3f}s")
    else:
        results = asyncio.run(tester.benchmark_async_execution(
            ml_code,
            iterations=iterations
        ))
        click.echo(f"Mean: {results['mean']*1000:.3f}ms")
        click.echo(f"Median: {results['median']*1000:.3f}ms")

@integration.command()
@click.argument('function_name')
@click.option('--session-file', type=click.Path(exists=True), help='REPL session file')
def create_callback(function_name: str, session_file: str):
    """Create Python callback for ML function"""

    # Load session
    if session_file:
        session = REPLSession()
        with open(session_file, 'r') as f:
            for line in f:
                session.execute(line.strip())
    else:
        session = REPLSession()

    # Create callback
    callback = ml_callback(session, function_name)

    # Generate Python code
    callback_code = f"""
# Generated callback for ML function '{function_name}'
from mlpy.integration import ml_callback, REPLSession

session = REPLSession()
# Load your ML code here

{function_name}_callback = ml_callback(session, '{function_name}')

# Use in your application:
# result = {function_name}_callback(arg1, arg2)
"""

    output_file = f"{function_name}_callback.py"
    with open(output_file, 'w') as f:
        f.write(callback_code)

    click.echo(f"Callback code written to {output_file}")

@integration.command()
def validate():
    """Validate Integration Toolkit setup"""

    click.echo("Validating Integration Toolkit...")

    # Check module registry
    try:
        registry = ModuleRegistry.get_instance()
        modules = registry.list_modules()
        click.echo(f"✓ Module registry: {len(modules)} modules loaded")
    except Exception as e:
        click.echo(f"✗ Module registry error: {e}")
        return

    # Check async executor
    try:
        executor = get_async_executor()
        click.echo(f"✓ Async executor: Ready")
    except Exception as e:
        click.echo(f"✗ Async executor error: {e}")
        return

    # Check capability system
    try:
        cap_manager = get_capability_manager()
        click.echo(f"✓ Capability manager: Ready")
    except Exception as e:
        click.echo(f"✗ Capability manager error: {e}")
        return

    click.echo("\nIntegration Toolkit is properly configured!")

@integration.command()
def repl():
    """Start Integration REPL"""

    repl = IntegrationREPL()
    repl.run()
```

**Usage Examples:**

```bash
# Execute ML file asynchronously
$ mlpy integration execute myapp.ml --async --timeout 60.0

# Execute with capabilities
$ mlpy integration execute myapp.ml \
    --capabilities file:read:/data/* \
    --capabilities network:http:api.example.com

# Benchmark ML file
$ mlpy integration benchmark process_data.ml --iterations 1000
Mean: 42.5ms
Median: 41.8ms

# Benchmark with concurrency
$ mlpy integration benchmark process_data.ml --concurrency 50
Throughput: 125.32 executions/sec
Total time: 0.399s

# Create callback
$ mlpy integration create-callback validate_order --session-file session.ml
Callback code written to validate_order_callback.py

# Validate setup
$ mlpy integration validate
Validating Integration Toolkit...
✓ Module registry: 12 modules loaded
✓ Async executor: Ready
✓ Capability manager: Ready

Integration Toolkit is properly configured!

# Start Integration REPL
$ mlpy integration repl
mlpy integration> .help
...
```

### 4.2 Project Configuration (DEFERRED - Use Existing mlpy.json)

**mlpy.integration.yaml:**

```yaml
# Integration Toolkit configuration

# Async execution settings
async:
  max_workers: 10
  default_timeout: 30.0
  enable_debugging: false

# Capability defaults
capabilities:
  default_capabilities:
    - type: file
      action: read
      pattern: ./data/*
    - type: network
      action: http
      pattern: api.example.com

# REPL settings
repl:
  history_file: .mlpy_integration_history
  auto_save: true
  enable_debugging: true

# Module paths
modules:
  extension_paths:
    - ./custom_modules
    - /usr/local/lib/mlpy/modules

# Monitoring
monitoring:
  enable_metrics: true
  metrics_port: 9090
  enable_tracing: false
```

**Loading Configuration:**

```python
# src/mlpy/integration/config.py

class IntegrationConfig:
    """Integration Toolkit configuration"""

    @staticmethod
    def load_from_file(config_file: str) -> Dict:
        """Load configuration from YAML file"""

        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        return config

    @staticmethod
    def apply_config(config: Dict):
        """Apply configuration to Integration Toolkit"""

        # Configure async executor
        if 'async' in config:
            async_config = config['async']
            executor = get_async_executor(
                max_workers=async_config.get('max_workers', 10)
            )

        # Configure default capabilities
        if 'capabilities' in config:
            caps_config = config['capabilities']
            default_caps = set()
            for cap_def in caps_config.get('default_capabilities', []):
                cap = CapabilityToken(
                    cap_def['type'],
                    action=cap_def.get('action'),
                    pattern=cap_def.get('pattern')
                )
                default_caps.add(cap)

        # Configure module paths
        if 'modules' in config:
            modules_config = config['modules']
            registry = ModuleRegistry.get_instance()
            for path in modules_config.get('extension_paths', []):
                registry.add_extension_path(path)

# Usage
config = IntegrationConfig.load_from_file('mlpy.integration.yaml')
IntegrationConfig.apply_config(config)
```

---

## 5. Observability and Monitoring

**⏸️ IMPLEMENTATION STATUS: DEFERRED**

**Rationale:** Enterprise-grade monitoring with Prometheus, OpenTelemetry, and structured logging adds significant dependencies and complexity. This should wait until the Integration Toolkit sees production deployments and users request these features.

**Implementation Priority: LOW - Wait for Adoption**

**All Features in This Section Deferred:**
- ⏸️ **Section 5.1:** Prometheus metrics collection
- ⏸️ **Section 5.2:** OpenTelemetry distributed tracing
- ⏸️ **Section 5.3:** Structured logging with structlog
- ⏸️ **Section 5.4:** Health check endpoints

**Concerns:**
- **Dependency Creep:** Adds `prometheus_client`, `opentelemetry`, `structlog` dependencies
- **Premature Optimization:** Enterprise monitoring before production usage
- **Maintenance Burden:** Complex infrastructure to maintain without user demand

**When to Implement:**
- After Integration Toolkit has production deployments
- When users explicitly request monitoring capabilities
- When there's demonstrated need for observability at scale

**Simple Alternative (Now):**
- Basic logging with Python's standard `logging` module
- Simple execution time tracking in existing code
- Performance metrics from Section 2.4 testing utilities

---

### 5.1 Metrics Collection (DEFERRED)

**Prometheus Metrics:**

```python
# src/mlpy/integration/monitoring/metrics.py

from prometheus_client import Counter, Histogram, Gauge

# Async execution metrics
async_executions_total = Counter(
    'mlpy_async_executions_total',
    'Total async ML executions',
    ['status']
)

async_execution_duration = Histogram(
    'mlpy_async_execution_duration_seconds',
    'Async execution duration',
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0]
)

active_async_executions = Gauge(
    'mlpy_active_async_executions',
    'Currently active async executions'
)

# Callback metrics
callback_invocations_total = Counter(
    'mlpy_callback_invocations_total',
    'Total callback invocations',
    ['function_name', 'status']
)

callback_duration = Histogram(
    'mlpy_callback_duration_seconds',
    'Callback execution duration',
    ['function_name']
)

# Capability metrics
capability_violations_total = Counter(
    'mlpy_capability_violations_total',
    'Total capability violations',
    ['capability_type']
)

# REPL session metrics
repl_sessions_active = Gauge(
    'mlpy_repl_sessions_active',
    'Active REPL sessions'
)

# Instrumented async execution
async def async_ml_execute_instrumented(
    ml_code: str,
    **kwargs
) -> AsyncMLResult:
    """Async execution with metrics"""

    active_async_executions.inc()

    start = time.time()
    status = 'success'

    try:
        result = await async_ml_execute(ml_code, **kwargs)
        return result

    except Exception as e:
        status = 'error'
        raise

    finally:
        duration = time.time() - start
        async_execution_duration.observe(duration)
        async_executions_total.labels(status=status).inc()
        active_async_executions.dec()
```

### 5.2 Distributed Tracing (DEFERRED)

**OpenTelemetry Integration:**

```python
# src/mlpy/integration/monitoring/tracing.py

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.instrumentation.auto_instrumentation import sitecustomize

tracer = trace.get_tracer(__name__)

async def async_ml_execute_traced(
    ml_code: str,
    **kwargs
) -> AsyncMLResult:
    """Async execution with distributed tracing"""

    with tracer.start_as_current_span("async_ml_execute") as span:
        # Add attributes
        span.set_attribute("ml.code_length", len(ml_code))
        span.set_attribute("ml.timeout", kwargs.get('timeout', 'none'))

        execution_id = str(uuid.uuid4())
        span.set_attribute("ml.execution_id", execution_id)

        try:
            result = await async_ml_execute(ml_code, **kwargs)

            span.set_attribute("ml.result_type", type(result.result).__name__)
            span.set_status(Status(StatusCode.OK))

            return result

        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise

def ml_callback_traced(
    session: REPLSession,
    function_name: str,
    **kwargs
) -> Callable:
    """Create traced callback"""

    base_callback = ml_callback(session, function_name, **kwargs)

    def traced_callback(*args, **cb_kwargs):
        with tracer.start_as_current_span("ml_callback") as span:
            span.set_attribute("ml.function_name", function_name)
            span.set_attribute("ml.args_count", len(args))

            try:
                result = base_callback(*args, **cb_kwargs)
                span.set_status(Status(StatusCode.OK))
                return result

            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    return traced_callback
```

### 5.3 Structured Logging (DEFERRED)

**Production Logging:**

```python
# src/mlpy/integration/monitoring/logging_config.py

import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage
async def async_ml_execute_logged(ml_code: str, **kwargs) -> AsyncMLResult:
    """Async execution with structured logging"""

    execution_id = str(uuid.uuid4())

    logger.info(
        "async_execution_started",
        execution_id=execution_id,
        code_length=len(ml_code),
        timeout=kwargs.get('timeout')
    )

    start = time.time()

    try:
        result = await async_ml_execute(ml_code, **kwargs)

        logger.info(
            "async_execution_completed",
            execution_id=execution_id,
            duration=time.time() - start,
            result_type=type(result.result).__name__
        )

        return result

    except Exception as e:
        logger.error(
            "async_execution_failed",
            execution_id=execution_id,
            duration=time.time() - start,
            error=str(e),
            error_type=type(e).__name__
        )
        raise
```

### 5.4 Health Checks (DEFERRED)

**Production Health Monitoring:**

```python
# src/mlpy/integration/monitoring/health.py

class HealthChecker:
    """Health check for Integration Toolkit"""

    async def check_health(self) -> Dict[str, Any]:
        """Comprehensive health check"""

        health = {
            'status': 'healthy',
            'timestamp': time.time(),
            'checks': {}
        }

        # Check async executor
        try:
            executor = get_async_executor()
            health['checks']['async_executor'] = {
                'status': 'healthy',
                'max_workers': executor._max_workers
            }
        except Exception as e:
            health['status'] = 'unhealthy'
            health['checks']['async_executor'] = {
                'status': 'unhealthy',
                'error': str(e)
            }

        # Check module registry
        try:
            registry = ModuleRegistry.get_instance()
            modules = registry.list_modules()
            health['checks']['module_registry'] = {
                'status': 'healthy',
                'modules_loaded': len(modules)
            }
        except Exception as e:
            health['status'] = 'unhealthy'
            health['checks']['module_registry'] = {
                'status': 'unhealthy',
                'error': str(e)
            }

        # Check REPL session pool
        try:
            pool = REPLSessionPool.get_instance()
            health['checks']['repl_pool'] = {
                'status': 'healthy',
                'pool_size': pool.pool_size,
                'active_sessions': pool.active_sessions
            }
        except Exception as e:
            health['status'] = 'unhealthy'
            health['checks']['repl_pool'] = {
                'status': 'unhealthy',
                'error': str(e)
            }

        return health

# FastAPI integration
@app.get("/health")
async def health_check():
    checker = HealthChecker()
    health = await checker.check_health()

    status_code = 200 if health['status'] == 'healthy' else 503
    return JSONResponse(content=health, status_code=status_code)
```

---


## Conclusion

This Development & Operations Guide provides **selective** tooling for building, testing, and validating ML-integrated applications using the Integration Toolkit. Based on current adoption stage, **~40% of features are recommended for immediate implementation**.

**Recommended Implementation (~40% Essential Subset):**

✅ **1. Testing Infrastructure (ESSENTIAL)** - Full implementation
   - Advanced testing utilities with integration test helpers
   - Mock environments for async and callback testing
   - Performance benchmarking utilities
   - **Estimated:** 3-4 days

✅ **2. Core REPL Commands** - 5 essential commands only
   - `.async`, `.callback`, `.caps`, `.grant`, `.benchmark`
   - Simple integration without complex session management
   - **Estimated:** 2-3 days

✅ **3. Minimal CLI Tools** - Validation and benchmarking
   - `mlpy integration validate` - Setup verification
   - `mlpy integration benchmark` - Performance testing
   - **Estimated:** 1-2 days

**Total Essential Implementation: 6-9 days (1-2 weeks)**

---

**Deferred Features (Until User Demand):**

⏸️ **4. Advanced Debugging** - Complex async debugging features
   - AsyncExecutionSourceMap, breakpoint instrumentation, DAP integration
   - **Defer until:** Users report debugging challenges with specific use cases

⏸️ **5. Enterprise Observability** - Production monitoring
   - Prometheus metrics, OpenTelemetry tracing, structured logging
   - **Defer until:** Integration Toolkit has production deployments

---

**Simplified Development Workflow:**

```
Development → Testing → Validation
     ↓           ↓          ↓
  5 REPL      Test       CLI
  Commands    Helpers    Validate
```

**What's Ready Now:**
- ✅ Core Integration Toolkit operational (Proposal #3 complete)
- ✅ Testing utilities provide quality assurance foundation
- ✅ Core REPL commands enable interactive development
- ✅ CLI validation ensures proper setup
- ⏸️ Advanced debugging and monitoring deferred pending adoption

**Next Steps:**
1. ✅ Review the core Integration Toolkit proposal ([integration-toolkit.md](./integration-toolkit.md)) - COMPLETE
2. Implement Section 2 (Testing Utilities) - Essential for quality assurance
3. Implement Section 3 (Core REPL Commands) - Valuable for development
4. Implement Section 4 (Minimal CLI) - Useful for validation
5. Defer Sections 1 and 5 until production adoption demonstrates need

---

**Related Documents:**
- [integration-toolkit.md](./integration-toolkit.md) - Core Architecture & Production Deployment (✅ COMPLETE)
- [next-steps.md](./next-steps.md) - Implementation Roadmap (✅ Phases 1-3 Complete)
- [integration-patterns-analysis.md](../integration-patterns-analysis.md) - Integration Patterns Analysis

---

**Document Summary:**

This proposal has been evaluated and updated to reflect a **selective implementation approach** based on current adoption stage:

- **40% Essential Features:** Testing utilities, core REPL commands, minimal CLI tools
- **60% Deferred Features:** Advanced debugging, enterprise observability
- **Implementation Timeline:** 1-2 weeks for essential subset
- **Rationale:** Prioritize quality assurance and validation; defer complex features until user demand demonstrates need

**Status:** Ready for selective implementation (Sections 2, 3 core, 4 minimal)

**Document End**
