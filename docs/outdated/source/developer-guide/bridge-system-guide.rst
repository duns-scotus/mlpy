====================
Bridge System Guide
====================

The bridge system enables seamless interoperability between ML and Python code while maintaining security guarantees. This guide covers advanced bridge patterns, custom bridge development, and performance optimization techniques.

Bridge System Architecture
===========================

The bridge system consists of four main components:

.. code-block:: text

    ┌─────────────────┐    ┌─────────────────┐
    │   ML Runtime    │◄──►│  Bridge Registry │
    │   Environment   │    │                 │
    └─────────────────┘    └─────────────────┘
             │                        │
             ▼                        ▼
    ┌─────────────────┐    ┌─────────────────┐
    │ Type Marshalling│◄──►│ Python Runtime  │
    │   & Validation  │    │   Environment   │
    └─────────────────┘    └─────────────────┘

Core Bridge Components
======================

Bridge Function Registration
----------------------------

**File**: ``src/mlpy/stdlib/registry.py``

Bridge functions connect ML function calls to Python implementations:

.. code-block:: python

    @dataclass
    class BridgeFunction:
        """Configuration for a Python-ML bridge function."""
        ml_name: str                              # ML function name
        python_module: str                        # Python module path
        python_function: str                      # Python function name
        capabilities_required: list[str]          # Required capabilities
        parameter_types: list[str] = None         # Type annotations
        return_type: str = None                   # Return type annotation
        validation_function: Callable = None     # Custom validation
        async_mode: bool = False                  # Async execution support
        batch_support: bool = False               # Batch operation support
        timeout_seconds: float = None            # Execution timeout
        memory_limit_mb: int = None              # Memory limit
        cache_results: bool = False               # Result caching
        audit_calls: bool = True                 # Audit logging

**Advanced Registration Example**:

.. code-block:: python

    def register_advanced_bridge():
        """Register advanced bridge function with full configuration."""

        def validate_ml_request(args: list) -> None:
            """Custom validation for ML function arguments."""
            if len(args) != 2:
                raise ValidationError("Function requires exactly 2 arguments")

            data, options = args
            if not isinstance(data, (str, list, dict)):
                raise ValidationError("First argument must be data structure")

            if not isinstance(options, dict):
                raise ValidationError("Second argument must be options object")

            # Validate options structure
            required_keys = {'format', 'encoding'}
            if not required_keys.issubset(options.keys()):
                raise ValidationError(f"Options must contain: {required_keys}")

        registry.register_bridge_function(
            module_name="data_processing",
            ml_name="processAdvancedData",
            python_module="mymodule.data_processor",
            python_function="process_advanced_data",
            capabilities_required=[
                "data:read:structured",
                "data:write:processed",
                "system:cpu:intensive"
            ],
            parameter_types=["Union[str, list, dict]", "dict"],
            return_type="ProcessingResult",
            validation_function=validate_ml_request,
            async_mode=True,
            batch_support=True,
            timeout_seconds=30.0,
            memory_limit_mb=512,
            cache_results=True,
            audit_calls=True
        )

Type Marshalling System
=======================

**File**: ``src/mlpy/runtime/bridge/marshalling.py``

The marshalling system handles data conversion between ML and Python types:

Core Type Mappings
------------------

.. code-block:: python

    class TypeMarshaller:
        """Advanced type marshalling with validation and optimization."""

        # Core type mapping
        ML_TO_PYTHON_TYPES = {
            'string': str,
            'number': (int, float),
            'boolean': bool,
            'array': list,
            'object': dict,
            'null': type(None)
        }

        PYTHON_TO_ML_TYPES = {v: k for k, v in ML_TO_PYTHON_TYPES.items()}

        def __init__(self):
            self.conversion_cache = {}
            self.custom_converters = {}
            self.validation_rules = {}

        def python_to_ml(self, value: Any, target_type: str = None) -> Any:
            """Convert Python value to ML-compatible format."""

            # Check cache first
            cache_key = (id(value), target_type)
            if cache_key in self.conversion_cache:
                return self.conversion_cache[cache_key]

            result = self._convert_python_to_ml(value, target_type)

            # Cache result if beneficial
            if self._should_cache(value):
                self.conversion_cache[cache_key] = result

            return result

        def _convert_python_to_ml(self, value: Any, target_type: str = None) -> Any:
            """Core Python to ML conversion logic."""

            # Handle None
            if value is None:
                return None

            # Handle primitive types
            if isinstance(value, (int, float)):
                if target_type == "string":
                    return str(value)
                return value

            elif isinstance(value, str):
                if target_type == "number":
                    try:
                        return int(value) if value.isdigit() else float(value)
                    except ValueError:
                        raise TypeConversionError(f"Cannot convert '{value}' to number")
                return value

            elif isinstance(value, bool):
                if target_type == "string":
                    return "true" if value else "false"
                elif target_type == "number":
                    return 1 if value else 0
                return value

            # Handle collections
            elif isinstance(value, (list, tuple)):
                return [self.python_to_ml(item, self._get_element_type(target_type))
                       for item in value]

            elif isinstance(value, dict):
                return {str(k): self.python_to_ml(v, self._get_value_type(target_type))
                       for k, v in value.items()}

            # Handle custom objects
            elif hasattr(value, '__dict__'):
                return self._convert_custom_object(value, target_type)

            else:
                raise TypeConversionError(f"Unsupported Python type: {type(value)}")

        def ml_to_python(self, value: Any, target_type: type = None) -> Any:
            """Convert ML value to Python format with type hints."""

            if value is None:
                return None

            # Handle ML-specific structures
            if isinstance(value, dict) and '__ml_type__' in value:
                return self._convert_ml_object(value, target_type)

            # Handle collections with type preservation
            elif isinstance(value, dict):
                if target_type and hasattr(target_type, '__annotations__'):
                    # Convert to typed object
                    return self._create_typed_object(value, target_type)
                else:
                    return {k: self.ml_to_python(v) for k, v in value.items()}

            elif isinstance(value, list):
                element_type = self._get_list_element_type(target_type)
                return [self.ml_to_python(item, element_type) for item in value]

            else:
                return value

        def register_custom_converter(self,
                                    python_type: type,
                                    to_ml: Callable,
                                    from_ml: Callable):
            """Register custom type converter."""
            self.custom_converters[python_type] = {
                'to_ml': to_ml,
                'from_ml': from_ml
            }

Advanced Bridge Patterns
========================

Async Bridge Functions
----------------------

Support for asynchronous operations in bridge functions:

.. code-block:: python

    class AsyncBridge:
        """Asynchronous bridge function support."""

        def __init__(self):
            self.async_executor = AsyncExecutor()
            self.pending_operations = {}

        async def call_async_bridge(self,
                                  function_name: str,
                                  args: list,
                                  context: CapabilityContext) -> Any:
            """Execute async bridge function with capability validation."""

            bridge_func = self.get_bridge_function(function_name)

            # Validate capabilities
            await self.validate_async_capabilities(bridge_func.capabilities_required, context)

            # Create async execution context
            async_context = AsyncExecutionContext(
                function_name=function_name,
                capabilities=context,
                timeout=bridge_func.timeout_seconds,
                memory_limit=bridge_func.memory_limit_mb
            )

            try:
                # Execute async function
                future = self.async_executor.submit(
                    bridge_func.python_function,
                    *args,
                    context=async_context
                )

                # Monitor execution
                result = await self.monitor_async_execution(future, async_context)

                return result

            except asyncio.TimeoutError:
                raise BridgeExecutionError("Async operation timed out")
            except MemoryError:
                raise BridgeExecutionError("Async operation exceeded memory limit")

**ML Async Usage**:

.. code-block:: ml

    // ML code using async bridge functions
    import http

    async function fetchUserData(userId: number): object {
        let response = await http.get("https://api.example.com/users/" + userId)
        return response.json()
    }

    async function processMultipleUsers(userIds: array): array {
        let promises = []
        for (let id in userIds) {
            promises.push(fetchUserData(id))
        }
        return await Promise.all(promises)
    }

Batch Bridge Operations
-----------------------

Optimize performance with batch processing:

.. code-block:: python

    class BatchBridge:
        """Batch operation support for bridge functions."""

        def __init__(self):
            self.batch_queue = {}
            self.batch_timers = {}
            self.batch_config = {
                'max_batch_size': 100,
                'max_wait_time': 0.1,  # 100ms
                'min_batch_size': 5
            }

        def call_batch_bridge(self,
                             function_name: str,
                             args: list,
                             context: CapabilityContext) -> Any:
            """Execute bridge function with batching optimization."""

            if not self.is_batchable(function_name):
                return self.call_single_bridge(function_name, args, context)

            # Add to batch queue
            batch_id = self.get_batch_id(function_name, context)
            if batch_id not in self.batch_queue:
                self.batch_queue[batch_id] = []
                self.schedule_batch_execution(batch_id)

            # Create future for result
            future = asyncio.Future()
            self.batch_queue[batch_id].append({
                'args': args,
                'future': future,
                'timestamp': time.time()
            })

            # Check if batch should execute immediately
            if len(self.batch_queue[batch_id]) >= self.batch_config['max_batch_size']:
                self.execute_batch_immediately(batch_id)

            return future

        async def execute_batch(self, batch_id: str):
            """Execute batched operations."""
            if batch_id not in self.batch_queue:
                return

            batch_items = self.batch_queue.pop(batch_id)
            if not batch_items:
                return

            try:
                # Extract arguments for batch processing
                batch_args = [item['args'] for item in batch_items]

                # Execute batch function
                bridge_func = self.get_bridge_function_for_batch(batch_id)
                batch_results = await bridge_func.batch_function(batch_args)

                # Distribute results to futures
                for item, result in zip(batch_items, batch_results):
                    item['future'].set_result(result)

            except Exception as e:
                # Set error on all futures
                for item in batch_items:
                    item['future'].set_exception(e)

**ML Batch Usage**:

.. code-block:: ml

    // ML code using batch operations
    import image_processing

    function processBatchImages(imageUrls: array): array {
        // This will be automatically batched for efficiency
        let results = []
        for (let url in imageUrls) {
            results.push(image_processing.resize(url, {width: 200, height: 200}))
        }
        return results
    }

Callback Bridge System
======================

Enable ML functions to call Python callbacks and vice versa:

.. code-block:: python

    class CallbackBridge:
        """Bidirectional callback support between ML and Python."""

        def __init__(self):
            self.ml_callbacks = {}
            self.python_callbacks = {}
            self.callback_contexts = {}

        def register_ml_callback(self,
                               callback_name: str,
                               ml_function: str,
                               capabilities: list[str]):
            """Register ML function as Python-callable callback."""

            def callback_wrapper(*args, **kwargs):
                # Convert arguments to ML format
                ml_args = self.marshaller.python_to_ml(args)

                # Validate capabilities
                context = self.get_callback_context(callback_name)
                for cap in capabilities:
                    if not context.check(cap, "execute"):
                        raise CallbackSecurityError(f"Missing capability: {cap}")

                # Execute ML function
                try:
                    result = self.ml_runtime.call_function(ml_function, ml_args)
                    return self.marshaller.ml_to_python(result)
                except Exception as e:
                    raise CallbackExecutionError(f"ML callback failed: {e}")

            self.ml_callbacks[callback_name] = callback_wrapper

        def register_python_callback(self,
                                   callback_name: str,
                                   python_function: Callable,
                                   capabilities: list[str]):
            """Register Python function as ML-callable callback."""

            def ml_callable_wrapper(args: list) -> Any:
                # Validate capabilities
                for cap in capabilities:
                    if not self.current_capability_context.check(cap, "execute"):
                        raise CallbackSecurityError(f"Missing capability: {cap}")

                # Convert arguments from ML format
                python_args = [self.marshaller.ml_to_python(arg) for arg in args]

                # Execute Python function
                try:
                    result = python_function(*python_args)
                    return self.marshaller.python_to_ml(result)
                except Exception as e:
                    raise CallbackExecutionError(f"Python callback failed: {e}")

            self.python_callbacks[callback_name] = ml_callable_wrapper

**Callback Usage Examples**:

.. code-block:: python

    # Python side - register ML callback
    def process_data_with_ml_validation(data):
        # ML function validates data format
        is_valid = bridge.call_ml_callback('validate_data_format', data)

        if is_valid:
            return process_complex_data(data)
        else:
            raise ValueError("Invalid data format")

.. code-block:: ml

    // ML side - register Python callback
    import data_processing

    function processWithPythonOptimization(dataset: array): array {
        // Use Python's optimized processing for large datasets
        return data_processing.optimized_process(dataset)
    }

Error Handling and Recovery
===========================

Bridge Error Types
-------------------

.. code-block:: python

    class BridgeError(Exception):
        """Base class for bridge-related errors."""
        pass

    class TypeConversionError(BridgeError):
        """Error in type marshalling/conversion."""
        pass

    class CapabilityError(BridgeError):
        """Insufficient capabilities for bridge operation."""
        pass

    class ValidationError(BridgeError):
        """Bridge function validation failed."""
        pass

    class ExecutionTimeoutError(BridgeError):
        """Bridge function execution timed out."""
        pass

    class ResourceLimitError(BridgeError):
        """Bridge function exceeded resource limits."""
        pass

Error Recovery Strategies
-------------------------

.. code-block:: python

    class BridgeErrorHandler:
        """Sophisticated error handling for bridge operations."""

        def __init__(self):
            self.retry_strategies = {}
            self.fallback_functions = {}
            self.error_metrics = {}

        def handle_bridge_error(self,
                              error: BridgeError,
                              context: BridgeContext) -> RecoveryAction:
            """Determine appropriate error recovery action."""

            if isinstance(error, ExecutionTimeoutError):
                return self.handle_timeout_error(error, context)
            elif isinstance(error, CapabilityError):
                return self.handle_capability_error(error, context)
            elif isinstance(error, TypeConversionError):
                return self.handle_conversion_error(error, context)
            elif isinstance(error, ResourceLimitError):
                return self.handle_resource_error(error, context)
            else:
                return RecoveryAction.PROPAGATE_ERROR

        def handle_timeout_error(self,
                               error: ExecutionTimeoutError,
                               context: BridgeContext) -> RecoveryAction:
            """Handle execution timeout with retry logic."""

            # Check if retry is appropriate
            if context.retry_count < 3:
                # Exponential backoff
                delay = 2 ** context.retry_count
                return RecoveryAction.RETRY_AFTER_DELAY(delay)

            # Try fallback function if available
            if context.function_name in self.fallback_functions:
                return RecoveryAction.USE_FALLBACK

            # Give up
            return RecoveryAction.PROPAGATE_ERROR

Performance Optimization
========================

Caching Strategies
------------------

.. code-block:: python

    class BridgeCache:
        """Intelligent caching for bridge function results."""

        def __init__(self):
            self.result_cache = {}
            self.cache_stats = {}
            self.cache_policies = {}

        def get_cached_result(self,
                            function_name: str,
                            args_hash: str) -> tuple[bool, Any]:
            """Get cached result if available and valid."""

            cache_key = f"{function_name}:{args_hash}"

            if cache_key not in self.result_cache:
                return False, None

            cache_entry = self.result_cache[cache_key]

            # Check TTL
            if time.time() > cache_entry['expires_at']:
                del self.result_cache[cache_key]
                return False, None

            # Update access stats
            cache_entry['access_count'] += 1
            cache_entry['last_accessed'] = time.time()

            self.cache_stats[function_name]['hits'] += 1
            return True, cache_entry['result']

        def cache_result(self,
                        function_name: str,
                        args_hash: str,
                        result: Any,
                        ttl_seconds: int = 300):
            """Cache function result with TTL."""

            if not self.should_cache_result(function_name, result):
                return

            cache_key = f"{function_name}:{args_hash}"

            self.result_cache[cache_key] = {
                'result': result,
                'created_at': time.time(),
                'expires_at': time.time() + ttl_seconds,
                'access_count': 0,
                'last_accessed': time.time()
            }

            # Update cache stats
            if function_name not in self.cache_stats:
                self.cache_stats[function_name] = {'hits': 0, 'misses': 0}

            # Evict old entries if cache is full
            self.evict_if_necessary()

Connection Pooling
------------------

.. code-block:: python

    class BridgeConnectionPool:
        """Connection pooling for resource-intensive bridge operations."""

        def __init__(self, max_connections: int = 10):
            self.max_connections = max_connections
            self.active_connections = {}
            self.connection_pool = {}
            self.connection_stats = {}

        @contextmanager
        def get_connection(self, resource_type: str):
            """Get pooled connection for resource type."""

            if resource_type not in self.connection_pool:
                self.connection_pool[resource_type] = []

            pool = self.connection_pool[resource_type]

            # Try to get existing connection
            connection = None
            while pool:
                candidate = pool.pop()
                if self.is_connection_healthy(candidate):
                    connection = candidate
                    break

            # Create new connection if needed
            if connection is None:
                connection = self.create_connection(resource_type)

            try:
                self.active_connections[id(connection)] = {
                    'resource_type': resource_type,
                    'acquired_at': time.time()
                }
                yield connection
            finally:
                # Return connection to pool
                del self.active_connections[id(connection)]
                if len(pool) < self.max_connections:
                    pool.append(connection)
                else:
                    self.close_connection(connection)

Security Considerations
=======================

Capability Validation
---------------------

.. code-block:: python

    class BridgeSecurityValidator:
        """Security validation for bridge operations."""

        def __init__(self):
            self.security_policies = {}
            self.audit_logger = SecurityAuditLogger()

        def validate_bridge_call(self,
                                function_name: str,
                                args: list,
                                context: CapabilityContext) -> ValidationResult:
            """Comprehensive security validation."""

            validation_result = ValidationResult()

            # 1. Capability validation
            bridge_func = self.get_bridge_function(function_name)
            for cap in bridge_func.capabilities_required:
                if not context.check(cap, "execute"):
                    validation_result.add_violation(
                        CapabilityViolation(f"Missing capability: {cap}")
                    )

            # 2. Argument validation
            if bridge_func.validation_function:
                try:
                    bridge_func.validation_function(args)
                except Exception as e:
                    validation_result.add_violation(
                        ArgumentValidationViolation(str(e))
                    )

            # 3. Rate limiting
            if self.is_rate_limited(function_name, context):
                validation_result.add_violation(
                    RateLimitViolation("Function call rate limit exceeded")
                )

            # 4. Resource usage validation
            if self.would_exceed_resource_limits(function_name, args):
                validation_result.add_violation(
                    ResourceLimitViolation("Operation would exceed resource limits")
                )

            # 5. Audit logging
            self.audit_logger.log_bridge_call_attempt(
                function_name, args, context, validation_result
            )

            return validation_result

Sandboxed Execution
-------------------

.. code-block:: python

    class SandboxedBridge:
        """Execute bridge functions in isolated sandbox."""

        def __init__(self):
            self.sandbox_configs = {}
            self.sandbox_pool = SandboxPool()

        def execute_in_sandbox(self,
                             function_name: str,
                             args: list,
                             context: CapabilityContext) -> Any:
            """Execute bridge function in isolated environment."""

            config = self.get_sandbox_config(function_name)

            with self.sandbox_pool.get_sandbox(config) as sandbox:
                try:
                    # Prepare sandbox environment
                    sandbox.set_capabilities(context)
                    sandbox.set_resource_limits(config.resource_limits)
                    sandbox.install_monitoring()

                    # Execute function
                    result = sandbox.execute_function(function_name, args)

                    # Validate result
                    if not self.validate_sandbox_result(result):
                        raise SandboxSecurityError("Invalid result from sandbox")

                    return result

                except SandboxTimeoutError:
                    raise BridgeExecutionError("Sandbox execution timed out")
                except SandboxResourceError as e:
                    raise ResourceLimitError(f"Sandbox resource limit: {e}")

This comprehensive bridge system guide provides the foundation for building sophisticated, secure, and high-performance interoperability between ML and Python code.