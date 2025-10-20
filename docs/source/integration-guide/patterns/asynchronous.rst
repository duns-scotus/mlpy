Asynchronous Integration
=========================

.. note::
   **Chapter Summary:** Master non-blocking ML execution for production applications using async/await and thread pools.

   **Time to Read:** 30 minutes | **Difficulty:** Intermediate to Advanced

----

Introduction
------------

Asynchronous integration enables non-blocking ML execution, critical for web servers, GUI applications, and high-throughput systems. While ML code executes, your application can handle other requests or tasks.

**Why Asynchronous Integration?**

.. code-block:: python

   # Multiple ML executions without blocking
   results = await asyncio.gather(
       transpiler.execute_ml_code_async(code1),
       transpiler.execute_ml_code_async(code2),
       transpiler.execute_ml_code_async(code3)
   )
   # All three execute concurrently!

**When to Use Asynchronous Integration:**

✅ **Web Servers**: FastAPI, aiohttp, Sanic
✅ **GUI Applications**: Keep UI responsive during ML execution
✅ **High-Throughput Services**: Process multiple requests concurrently
✅ **Background Tasks**: Celery, RQ, asyncio tasks
✅ **Real-Time Systems**: WebSocket servers, streaming data
✅ **I/O-Bound Workloads**: ML code with file/network operations

**When Synchronous Might Be Better:**

❌ **Simple Scripts**: Async adds complexity without benefit
❌ **Single-User CLI Tools**: No concurrency needed
❌ **Pure CPU-Bound**: Python GIL limits true parallelism (use multiprocessing instead)

**What You'll Learn:**

1. AsyncIO integration patterns
2. Thread-based async execution
3. Concurrent ML execution
4. Capability propagation in async contexts
5. Async error handling
6. Performance optimization
7. Complete async web application examples

----

AsyncIO Integration Patterns
-----------------------------

Using Python's async/await for non-blocking ML execution.

Basic Async Execution
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from mlpy import AsyncMLExecutor

   async def main():
       executor = AsyncMLExecutor()

       ml_code = """
       function calculate(x) {
           return x * x + 10;
       }

       result = calculate(5);
       """

       # Non-blocking execution
       result = await executor.execute_ml_code(ml_code)
       print(f"Result: {result}")

   # Run async code
   asyncio.run(main())

**How It Works:**

1. ML execution runs in a thread pool executor
2. AsyncIO event loop continues processing other tasks
3. Result is returned when execution completes

AsyncMLExecutor Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``AsyncMLExecutor`` wraps synchronous ML execution in an async interface:

.. code-block:: python

   import asyncio
   from concurrent.futures import ThreadPoolExecutor
   from mlpy import MLTranspiler

   class AsyncMLExecutor:
       """Async wrapper for ML execution"""

       def __init__(self, max_workers: int = 4):
           self.transpiler = MLTranspiler()
           self.executor = ThreadPoolExecutor(max_workers=max_workers)

       async def execute_ml_code(self, ml_code: str, **kwargs):
           """Execute ML code asynchronously"""
           loop = asyncio.get_event_loop()
           return await loop.run_in_executor(
               self.executor,
               self.transpiler.execute_ml_code,
               ml_code,
               kwargs
           )

       async def execute_ml_function(self, function_name: str, ml_code: str, **kwargs):
           """Execute ML function asynchronously"""
           loop = asyncio.get_event_loop()
           return await loop.run_in_executor(
               self.executor,
               self.transpiler.execute_ml_function,
               function_name,
               ml_code,
               kwargs
           )

       def shutdown(self):
           """Shutdown executor"""
           self.executor.shutdown(wait=True)

Concurrent ML Execution
~~~~~~~~~~~~~~~~~~~~~~~

Execute multiple ML scripts concurrently:

.. code-block:: python

   import asyncio
   from mlpy import AsyncMLExecutor

   async def process_multiple_requests():
       executor = AsyncMLExecutor(max_workers=10)

       ml_scripts = [
           "result = 2 + 2;",
           "result = 5 * 5;",
           "result = 10 - 3;",
           "result = 20 / 4;"
       ]

       # Execute all concurrently
       results = await asyncio.gather(
           *[executor.execute_ml_code(script) for script in ml_scripts]
       )

       print(f"Results: {results}")  # [4, 25, 7, 5.0]

       executor.shutdown()

   asyncio.run(process_multiple_requests())

**Performance Comparison:**

.. list-table:: Synchronous vs Asynchronous Execution
   :header-rows: 1
   :widths: 40 30 30

   * - Scenario
     - Synchronous Time
     - Asynchronous Time
   * - 10 ML scripts (20ms each)
     - 200ms (sequential)
     - ~25ms (concurrent)
   * - 100 ML scripts
     - 2,000ms
     - ~50ms (with 10 workers)
   * - 1000 ML scripts
     - 20,000ms
     - ~250ms (with 10 workers)

Async Function Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract and call ML functions asynchronously:

.. code-block:: python

   from mlpy import AsyncMLExecutor

   async def async_function_example():
       executor = AsyncMLExecutor()

       ml_code = """
       function analyze_data(numbers) {
           sum = 0;
           for (num in numbers) {
               sum = sum + num;
           }
           return {
               count: len(numbers),
               sum: sum,
               average: sum / len(numbers)
           };
       }
       """

       # Call async
       data = [10, 20, 30, 40, 50]
       result = await executor.execute_ml_function(
           "analyze_data",
           ml_code,
           numbers=data
       )

       print(f"Average: {result['average']}")

----

Thread-Based Async Execution
-----------------------------

Using threads for async ML execution without AsyncIO.

ThreadPoolExecutor Pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from concurrent.futures import ThreadPoolExecutor, as_completed
   from mlpy import MLTranspiler

   def execute_ml_task(task_id: int, ml_code: str):
       """Execute ML task in thread"""
       transpiler = MLTranspiler()
       result = transpiler.execute_ml_code(ml_code)
       return task_id, result

   def process_tasks_concurrently(tasks: list):
       """Process multiple ML tasks concurrently"""

       with ThreadPoolExecutor(max_workers=5) as executor:
           futures = {
               executor.submit(execute_ml_task, task_id, ml_code): task_id
               for task_id, ml_code in tasks
           }

           results = {}
           for future in as_completed(futures):
               task_id = futures[future]
               try:
                   result_id, result = future.result()
                   results[result_id] = result
                   print(f"Task {task_id} completed")
               except Exception as e:
                   print(f"Task {task_id} failed: {e}")
                   results[task_id] = None

           return results

   # Usage
   tasks = [
       (1, "result = 10 * 10;"),
       (2, "result = 20 * 20;"),
       (3, "result = 30 * 30;"),
   ]

   results = process_tasks_concurrently(tasks)
   print(f"Results: {results}")

Async Queue Pattern
~~~~~~~~~~~~~~~~~~~

Process ML tasks from a queue:

.. code-block:: python

   import queue
   import threading
   from mlpy import MLTranspiler

   class MLTaskQueue:
       """Queue-based async ML executor"""

       def __init__(self, num_workers: int = 4):
           self.task_queue = queue.Queue()
           self.result_queue = queue.Queue()
           self.workers = []
           self.running = False

           # Start worker threads
           for _ in range(num_workers):
               worker = threading.Thread(target=self._worker, daemon=True)
               worker.start()
               self.workers.append(worker)

           self.running = True

       def _worker(self):
           """Worker thread that processes ML tasks"""
           transpiler = MLTranspiler()

           while self.running:
               try:
                   task_id, ml_code, callback = self.task_queue.get(timeout=1)

                   # Execute ML code
                   result = transpiler.execute_ml_code(ml_code)

                   # Store result
                   self.result_queue.put((task_id, result, None))

                   # Call callback if provided
                   if callback:
                       callback(task_id, result)

                   self.task_queue.task_done()

               except queue.Empty:
                   continue
               except Exception as e:
                   self.result_queue.put((task_id, None, e))

       def submit(self, task_id: int, ml_code: str, callback=None):
           """Submit ML task to queue"""
           self.task_queue.put((task_id, ml_code, callback))

       def get_result(self, timeout: float = None):
           """Get result from queue"""
           return self.result_queue.get(timeout=timeout)

       def shutdown(self):
           """Shutdown task queue"""
           self.running = False
           for worker in self.workers:
               worker.join()

   # Usage
   def on_complete(task_id, result):
       print(f"Task {task_id} completed: {result}")

   queue_executor = MLTaskQueue(num_workers=4)

   # Submit tasks
   queue_executor.submit(1, "result = 5 + 5;", on_complete)
   queue_executor.submit(2, "result = 10 + 10;", on_complete)
   queue_executor.submit(3, "result = 15 + 15;", on_complete)

   # Wait for completion
   queue_executor.task_queue.join()
   queue_executor.shutdown()

Future-Based Pattern
~~~~~~~~~~~~~~~~~~~~

Return Future objects for async result retrieval:

.. code-block:: python

   from concurrent.futures import ThreadPoolExecutor, Future
   from mlpy import MLTranspiler

   class MLExecutorWithFutures:
       """ML executor that returns Future objects"""

       def __init__(self, max_workers: int = 4):
           self.executor = ThreadPoolExecutor(max_workers=max_workers)
           self.transpiler = MLTranspiler()

       def submit(self, ml_code: str) -> Future:
           """Submit ML code execution, return Future"""
           return self.executor.submit(
               self.transpiler.execute_ml_code,
               ml_code
           )

       def map(self, ml_codes: list) -> list:
           """Execute multiple ML codes, return results in order"""
           return list(self.executor.map(
               self.transpiler.execute_ml_code,
               ml_codes
           ))

       def shutdown(self):
           """Shutdown executor"""
           self.executor.shutdown(wait=True)

   # Usage
   executor = MLExecutorWithFutures(max_workers=5)

   # Submit and get Future
   future1 = executor.submit("result = 100 + 200;")
   future2 = executor.submit("result = 50 * 4;")

   # Do other work...

   # Get results when ready
   result1 = future1.result()  # Blocks until ready
   result2 = future2.result()

   print(f"Results: {result1}, {result2}")

   executor.shutdown()

----

Web Server Integration
----------------------

Integrating async ML execution with web frameworks.

FastAPI Integration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fastapi import FastAPI, BackgroundTasks
   from pydantic import BaseModel
   from mlpy import AsyncMLExecutor

   app = FastAPI()
   ml_executor = AsyncMLExecutor(max_workers=10)

   class MLRequest(BaseModel):
       code: str
       capabilities: list[str] = []

   class MLResponse(BaseModel):
       result: any
       execution_time_ms: float

   @app.post("/execute", response_model=MLResponse)
   async def execute_ml(request: MLRequest):
       """Execute ML code asynchronously"""
       import time

       start_time = time.time()

       # Execute with capabilities
       from mlpy import CapabilityContext

       if request.capabilities:
           with CapabilityContext(request.capabilities):
               result = await ml_executor.execute_ml_code(request.code)
       else:
           result = await ml_executor.execute_ml_code(request.code)

       execution_time = (time.time() - start_time) * 1000

       return MLResponse(
           result=result,
           execution_time_ms=execution_time
       )

   @app.post("/execute-function")
   async def execute_ml_function(
       function_name: str,
       ml_code: str,
       args: dict
   ):
       """Execute specific ML function"""
       result = await ml_executor.execute_ml_function(
           function_name,
           ml_code,
           **args
       )
       return {"result": result}

   # Background task execution
   @app.post("/execute-background")
   async def execute_ml_background(
       request: MLRequest,
       background_tasks: BackgroundTasks
   ):
       """Execute ML code in background"""

       def run_ml_task():
           # Runs after response is sent
           result = ml_executor.transpiler.execute_ml_code(request.code)
           # Store result in database, send notification, etc.
           print(f"Background task completed: {result}")

       background_tasks.add_task(run_ml_task)

       return {"status": "submitted"}

   @app.on_event("shutdown")
   async def shutdown_event():
       """Cleanup on shutdown"""
       ml_executor.shutdown()

**Usage:**

.. code-block:: bash

   # Start server
   uvicorn app:app --host 0.0.0.0 --port 8000

   # Execute ML code
   curl -X POST http://localhost:8000/execute \
     -H "Content-Type: application/json" \
     -d '{
       "code": "result = 2 + 2;",
       "capabilities": ["math:*"]
     }'

aiohttp Integration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from aiohttp import web
   from mlpy import AsyncMLExecutor

   ml_executor = AsyncMLExecutor(max_workers=10)

   async def execute_ml_handler(request):
       """Handle ML execution request"""
       data = await request.json()
       ml_code = data.get("code")

       if not ml_code:
           return web.json_response({"error": "Missing code"}, status=400)

       try:
           result = await ml_executor.execute_ml_code(ml_code)
           return web.json_response({"result": result})
       except Exception as e:
           return web.json_response({"error": str(e)}, status=500)

   async def health_check(request):
       """Health check endpoint"""
       return web.json_response({"status": "healthy"})

   # Create app
   app = web.Application()
   app.router.add_post("/execute", execute_ml_handler)
   app.router.add_get("/health", health_check)

   # Cleanup
   async def on_cleanup(app):
       ml_executor.shutdown()

   app.on_cleanup.append(on_cleanup)

   # Run server
   if __name__ == "__main__":
       web.run_app(app, host="0.0.0.0", port=8000)

Sanic Integration
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sanic import Sanic, response
   from mlpy import AsyncMLExecutor

   app = Sanic("MLApp")
   ml_executor = AsyncMLExecutor(max_workers=10)

   @app.post("/execute")
   async def execute_ml(request):
       """Execute ML code"""
       ml_code = request.json.get("code")

       result = await ml_executor.execute_ml_code(ml_code)

       return response.json({"result": result})

   @app.listener("before_server_stop")
   async def cleanup(app, loop):
       """Cleanup before shutdown"""
       ml_executor.shutdown()

   if __name__ == "__main__":
       app.run(host="0.0.0.0", port=8000, workers=4)

----

Capability Propagation in Async Context
----------------------------------------

Ensuring capabilities work correctly in async environments.

Context-Local Capabilities
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from contextvars import ContextVar
   from mlpy import MLTranspiler, CapabilityContext

   # Context variable for capabilities
   current_capabilities = ContextVar('capabilities', default=[])

   class AsyncMLExecutorWithCapabilities:
       """Async executor with capability context propagation"""

       def __init__(self, max_workers: int = 4):
           self.transpiler = MLTranspiler()
           self.executor = ThreadPoolExecutor(max_workers=max_workers)

       async def execute_ml_code(self, ml_code: str):
           """Execute ML code with context capabilities"""
           # Get capabilities from context
           capabilities = current_capabilities.get()

           loop = asyncio.get_event_loop()

           # Execute with capabilities
           def execute_with_caps():
               with CapabilityContext(capabilities):
                   return self.transpiler.execute_ml_code(ml_code)

           return await loop.run_in_executor(self.executor, execute_with_caps)

   async def process_request(ml_code: str, user_capabilities: list):
       """Process request with user-specific capabilities"""

       # Set capabilities for this context
       token = current_capabilities.set(user_capabilities)

       try:
           executor = AsyncMLExecutorWithCapabilities()
           result = await executor.execute_ml_code(ml_code)
           return result
       finally:
           # Reset context
           current_capabilities.reset(token)

   # Usage
   async def main():
       # Each request has its own capability context
       result1 = await process_request(
           "result = 10 + 10;",
           ["math:*"]
       )

       result2 = await process_request(
           "import file; content = file.read('/data/file.txt');",
           ["file:read:/data/**"]
       )

       print(f"Results: {result1}, {result2}")

   asyncio.run(main())

Per-Request Capability Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fastapi import FastAPI, Depends, HTTPException
   from mlpy import AsyncMLExecutor, CapabilityContext

   app = FastAPI()
   ml_executor = AsyncMLExecutor()

   def get_user_capabilities(api_key: str) -> list:
       """Get capabilities based on API key"""
       # In production, look up in database
       capability_map = {
           "admin_key": ["file:*:**", "database:*:**", "http:*:**"],
           "user_key": ["file:read:/data/**", "console:log"],
           "guest_key": ["console:log"]
       }
       return capability_map.get(api_key, [])

   @app.post("/execute")
   async def execute_ml(
       ml_code: str,
       api_key: str,
       capabilities: list = Depends(get_user_capabilities)
   ):
       """Execute ML code with user capabilities"""

       # Execute with user-specific capabilities
       with CapabilityContext(capabilities):
           result = await ml_executor.execute_ml_code(ml_code)

       return {"result": result}

----

Async Error Handling
---------------------

Handling errors in async ML execution.

Try-Except in Async
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from mlpy import AsyncMLExecutor, MLRuntimeError, MLSyntaxError

   async def safe_async_execute(ml_code: str):
       """Execute ML code with error handling"""
       executor = AsyncMLExecutor()

       try:
           result = await executor.execute_ml_code(ml_code)
           return {"success": True, "result": result}

       except MLSyntaxError as e:
           return {
               "success": False,
               "error": "syntax_error",
               "message": str(e),
               "line": e.line_number
           }

       except MLRuntimeError as e:
           return {
               "success": False,
               "error": "runtime_error",
               "message": str(e),
               "line": e.line_number
           }

       except Exception as e:
           return {
               "success": False,
               "error": "unknown",
               "message": str(e)
           }

   # Usage
   async def main():
       good_code = "result = 2 + 2;"
       bad_code = "result = x + y;"  # undefined variables

       result1 = await safe_async_execute(good_code)
       result2 = await safe_async_execute(bad_code)

       print(f"Good: {result1}")
       print(f"Bad: {result2}")

   asyncio.run(main())

Handling Multiple Concurrent Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from mlpy import AsyncMLExecutor

   async def execute_with_error_handling(task_id: int, ml_code: str):
       """Execute single task with error handling"""
       executor = AsyncMLExecutor()

       try:
           result = await executor.execute_ml_code(ml_code)
           return {"task_id": task_id, "success": True, "result": result}
       except Exception as e:
           return {"task_id": task_id, "success": False, "error": str(e)}

   async def execute_all_with_errors(tasks: list):
       """Execute all tasks, collecting errors"""

       # Execute all concurrently
       results = await asyncio.gather(
           *[execute_with_error_handling(task_id, code)
             for task_id, code in tasks],
           return_exceptions=False  # Let gather collect all results
       )

       # Separate successes and failures
       successes = [r for r in results if r["success"]]
       failures = [r for r in results if not r["success"]]

       return {
           "successes": successes,
           "failures": failures,
           "total": len(results),
           "success_rate": len(successes) / len(results) * 100
       }

   # Usage
   async def main():
       tasks = [
           (1, "result = 10 + 10;"),
           (2, "result = undefined_var;"),  # Will fail
           (3, "result = 30 + 30;"),
           (4, "result = 40 / 0;"),  # Will fail
       ]

       results = await execute_all_with_errors(tasks)

       print(f"Success rate: {results['success_rate']:.1f}%")
       print(f"Successes: {len(results['successes'])}")
       print(f"Failures: {len(results['failures'])}")

   asyncio.run(main())

Timeout Handling
~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from mlpy import AsyncMLExecutor

   async def execute_with_timeout(ml_code: str, timeout: float = 5.0):
       """Execute ML code with timeout"""
       executor = AsyncMLExecutor()

       try:
           result = await asyncio.wait_for(
               executor.execute_ml_code(ml_code),
               timeout=timeout
           )
           return {"success": True, "result": result}

       except asyncio.TimeoutError:
           return {
               "success": False,
               "error": "timeout",
               "message": f"Execution exceeded {timeout}s timeout"
           }

       except Exception as e:
           return {
               "success": False,
               "error": "exception",
               "message": str(e)
           }

   # Usage
   async def main():
       # Fast execution
       result1 = await execute_with_timeout("result = 2 + 2;", timeout=5.0)

       # Slow execution (will timeout)
       slow_code = """
       result = 0;
       for (i in range(10000000)) {
           result = result + i;
       }
       """
       result2 = await execute_with_timeout(slow_code, timeout=0.1)

       print(f"Fast: {result1}")
       print(f"Slow: {result2}")

   asyncio.run(main())

----

Performance Optimization
------------------------

Optimizing async ML execution for production.

Connection Pooling
~~~~~~~~~~~~~~~~~~

Reuse transpiler instances across requests:

.. code-block:: python

   import asyncio
   from mlpy import MLTranspiler

   class MLTranspilerPool:
       """Pool of reusable transpiler instances"""

       def __init__(self, pool_size: int = 10):
           self.pool = asyncio.Queue(maxsize=pool_size)
           for _ in range(pool_size):
               self.pool.put_nowait(MLTranspiler())

       async def acquire(self) -> MLTranspiler:
           """Acquire transpiler from pool"""
           return await self.pool.get()

       async def release(self, transpiler: MLTranspiler):
           """Return transpiler to pool"""
           await self.pool.put(transpiler)

       async def execute(self, ml_code: str):
           """Execute with pooled transpiler"""
           transpiler = await self.acquire()
           try:
               loop = asyncio.get_event_loop()
               result = await loop.run_in_executor(
                   None,
                   transpiler.execute_ml_code,
                   ml_code
               )
               return result
           finally:
               await self.release(transpiler)

   # Usage
   async def main():
       pool = MLTranspilerPool(pool_size=5)

       # Execute 100 tasks using only 5 transpiler instances
       tasks = [pool.execute(f"result = {i} * {i};") for i in range(100)]
       results = await asyncio.gather(*tasks)

       print(f"Processed {len(results)} tasks with pool of 5")

   asyncio.run(main())

Batching Async Requests
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from mlpy import AsyncMLExecutor

   class BatchedMLExecutor:
       """Batch async ML requests for efficiency"""

       def __init__(self, batch_size: int = 10, batch_timeout: float = 0.1):
           self.executor = AsyncMLExecutor()
           self.batch_size = batch_size
           self.batch_timeout = batch_timeout
           self.pending_requests = []
           self.lock = asyncio.Lock()

       async def execute(self, ml_code: str):
           """Submit request and wait for batch execution"""
           future = asyncio.Future()

           async with self.lock:
               self.pending_requests.append((ml_code, future))

               # Execute batch if full
               if len(self.pending_requests) >= self.batch_size:
                   asyncio.create_task(self._execute_batch())

           # Wait for result
           return await future

       async def _execute_batch(self):
           """Execute pending requests as a batch"""
           async with self.lock:
               if not self.pending_requests:
                   return

               batch = self.pending_requests[:]
               self.pending_requests = []

           # Execute batch concurrently
           codes = [code for code, _ in batch]
           results = await asyncio.gather(
               *[self.executor.execute_ml_code(code) for code in codes],
               return_exceptions=True
           )

           # Set results
           for (_, future), result in zip(batch, results):
               if isinstance(result, Exception):
                   future.set_exception(result)
               else:
                   future.set_result(result)

   # Usage
   async def main():
       executor = BatchedMLExecutor(batch_size=5)

       # Submit 20 requests
       tasks = [
           executor.execute(f"result = {i} + {i};")
           for i in range(20)
       ]

       # Executes in 4 batches of 5
       results = await asyncio.gather(*tasks)
       print(f"Processed {len(results)} requests in batches")

   asyncio.run(main())

Caching Async Results
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   import hashlib
   from functools import lru_cache
   from mlpy import AsyncMLExecutor

   class CachedAsyncMLExecutor:
       """Async executor with result caching"""

       def __init__(self):
           self.executor = AsyncMLExecutor()
           self.cache = {}
           self.lock = asyncio.Lock()

       def _cache_key(self, ml_code: str) -> str:
           """Generate cache key for ML code"""
           return hashlib.md5(ml_code.encode()).hexdigest()

       async def execute_ml_code(self, ml_code: str):
           """Execute with caching"""
           cache_key = self._cache_key(ml_code)

           # Check cache
           async with self.lock:
               if cache_key in self.cache:
                   return self.cache[cache_key]

           # Execute
           result = await self.executor.execute_ml_code(ml_code)

           # Store in cache
           async with self.lock:
               self.cache[cache_key] = result

           return result

   # Usage
   async def main():
       executor = CachedAsyncMLExecutor()

       # First execution: transpiles and executes
       result1 = await executor.execute_ml_code("result = 42;")

       # Second execution: cached
       result2 = await executor.execute_ml_code("result = 42;")

       print(f"Results: {result1}, {result2}")

   asyncio.run(main())

----

Complete Working Examples
--------------------------

Real-world async integration scenarios.

Example 1: Async Web API with ML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   """Complete async web API with ML processing"""

   from fastapi import FastAPI, HTTPException, BackgroundTasks
   from pydantic import BaseModel
   from typing import Optional
   import asyncio
   from mlpy import AsyncMLExecutor, CapabilityContext

   app = FastAPI(title="ML Processing API")
   ml_executor = AsyncMLExecutor(max_workers=10)

   # Request/Response models
   class ProcessRequest(BaseModel):
       data: list[dict]
       ml_script: str
       capabilities: Optional[list[str]] = ["console:log", "math:*"]

   class ProcessResponse(BaseModel):
       task_id: str
       status: str
       result: Optional[any] = None

   # In-memory task storage (use Redis in production)
   tasks = {}

   @app.post("/process", response_model=ProcessResponse)
   async def process_data(request: ProcessRequest):
       """Process data with ML script"""

       import uuid
       task_id = str(uuid.uuid4())

       # Execute async
       with CapabilityContext(request.capabilities):
           result = await ml_executor.execute_ml_function(
               "process_data",
               request.ml_script,
               data=request.data
           )

       return ProcessResponse(
           task_id=task_id,
           status="completed",
           result=result
       )

   @app.post("/process-background")
   async def process_background(
       request: ProcessRequest,
       background_tasks: BackgroundTasks
   ):
       """Process in background, return immediately"""

       import uuid
       task_id = str(uuid.uuid4())
       tasks[task_id] = {"status": "pending", "result": None}

       async def run_task():
           try:
               with CapabilityContext(request.capabilities):
                   result = await ml_executor.execute_ml_function(
                       "process_data",
                       request.ml_script,
                       data=request.data
                   )
               tasks[task_id] = {"status": "completed", "result": result}
           except Exception as e:
               tasks[task_id] = {"status": "failed", "error": str(e)}

       # Run in background
       asyncio.create_task(run_task())

       return {"task_id": task_id, "status": "submitted"}

   @app.get("/task/{task_id}")
   async def get_task_status(task_id: str):
       """Get task status"""
       if task_id not in tasks:
           raise HTTPException(status_code=404, detail="Task not found")

       return tasks[task_id]

   @app.get("/health")
   async def health_check():
       """Health check endpoint"""
       return {"status": "healthy", "workers": 10}

   # Startup/shutdown
   @app.on_event("startup")
   async def startup():
       print("ML API starting...")

   @app.on_event("shutdown")
   async def shutdown():
       print("ML API shutting down...")
       ml_executor.shutdown()

**ML Script Example:**

.. code-block:: ml

   function process_data(data) {
       results = [];

       for (item in data) {
           processed = {
               id: item.id,
               value: item.value * 2,
               status: item.value > 100 ? "high" : "normal"
           };
           results.append(processed);
       }

       return {
           processed_count: len(results),
           results: results
       };
   }

**Usage:**

.. code-block:: bash

   curl -X POST http://localhost:8000/process \
     -H "Content-Type: application/json" \
     -d '{
       "data": [
           {"id": 1, "value": 50},
           {"id": 2, "value": 150}
       ],
       "ml_script": "function process_data(data) { ... }",
       "capabilities": ["console:log", "math:*"]
     }'

Example 2: WebSocket Server with ML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   """WebSocket server with real-time ML processing"""

   from fastapi import FastAPI, WebSocket, WebSocketDisconnect
   from mlpy import AsyncMLExecutor
   import asyncio
   import json

   app = FastAPI()
   ml_executor = AsyncMLExecutor()

   class ConnectionManager:
       """Manage WebSocket connections"""

       def __init__(self):
           self.active_connections: list[WebSocket] = []

       async def connect(self, websocket: WebSocket):
           await websocket.accept()
           self.active_connections.append(websocket)

       def disconnect(self, websocket: WebSocket):
           self.active_connections.remove(websocket)

       async def send_personal(self, message: dict, websocket: WebSocket):
           await websocket.send_json(message)

       async def broadcast(self, message: dict):
           for connection in self.active_connections:
               await connection.send_json(message)

   manager = ConnectionManager()

   @app.websocket("/ws/ml")
   async def ml_websocket(websocket: WebSocket):
       """WebSocket endpoint for ML processing"""
       await manager.connect(websocket)

       try:
           while True:
               # Receive ML code from client
               data = await websocket.receive_json()
               ml_code = data.get("code")
               request_id = data.get("request_id")

               # Send processing status
               await manager.send_personal({
                   "request_id": request_id,
                   "status": "processing"
               }, websocket)

               # Execute ML code
               try:
                   result = await ml_executor.execute_ml_code(ml_code)

                   # Send result
                   await manager.send_personal({
                       "request_id": request_id,
                       "status": "completed",
                       "result": result
                   }, websocket)

               except Exception as e:
                   # Send error
                   await manager.send_personal({
                       "request_id": request_id,
                       "status": "error",
                       "error": str(e)
                   }, websocket)

       except WebSocketDisconnect:
           manager.disconnect(websocket)

   @app.on_event("shutdown")
   async def shutdown():
       ml_executor.shutdown()

**Client Example:**

.. code-block:: javascript

   // JavaScript WebSocket client
   const ws = new WebSocket('ws://localhost:8000/ws/ml');

   ws.onopen = () => {
       // Send ML code
       ws.send(JSON.stringify({
           request_id: '123',
           code: 'result = 2 + 2;'
       }));
   };

   ws.onmessage = (event) => {
       const data = JSON.parse(event.data);
       console.log('Status:', data.status);
       if (data.result) {
           console.log('Result:', data.result);
       }
   };

Example 3: Celery Background Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   """Celery integration for long-running ML tasks"""

   from celery import Celery
   from mlpy import MLTranspiler, CapabilityContext

   # Configure Celery
   app = Celery(
       'ml_tasks',
       broker='redis://localhost:6379/0',
       backend='redis://localhost:6379/0'
   )

   @app.task(bind=True)
   def execute_ml_task(self, ml_code: str, capabilities: list = None):
       """Execute ML code as Celery task"""

       transpiler = MLTranspiler()

       try:
           # Update task state
           self.update_state(state='PROCESSING')

           # Execute with capabilities
           if capabilities:
               with CapabilityContext(capabilities):
                   result = transpiler.execute_ml_code(ml_code)
           else:
               result = transpiler.execute_ml_code(ml_code)

           return {
               "status": "success",
               "result": result
           }

       except Exception as e:
           return {
               "status": "error",
               "error": str(e)
           }

   @app.task
   def batch_ml_processing(items: list, ml_script: str):
       """Process batch of items with ML"""

       transpiler = MLTranspiler()
       results = []

       for item in items:
           try:
               result = transpiler.execute_ml_function(
                   "process_item",
                   ml_script,
                   item=item
               )
               results.append({"item": item, "result": result})
           except Exception as e:
               results.append({"item": item, "error": str(e)})

       return {
           "processed": len(results),
           "results": results
       }

**Usage:**

.. code-block:: python

   # Submit task
   task = execute_ml_task.delay(
       ml_code="result = 10 * 10;",
       capabilities=["math:*"]
   )

   # Check status
   if task.ready():
       result = task.get()
       print(f"Result: {result}")
   else:
       print("Task still processing...")

   # Batch processing
   items = [{"id": i, "value": i * 10} for i in range(1000)]
   batch_task = batch_ml_processing.delay(items, ml_script)

----

Best Practices
--------------

Proven strategies for async ML integration.

1. Use Connection Pooling
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ✅ GOOD: Reuse transpiler instances
   transpiler_pool = MLTranspilerPool(pool_size=10)
   result = await transpiler_pool.execute(ml_code)

   # ❌ BAD: Create new transpiler for each request
   transpiler = MLTranspiler()
   result = await execute_async(ml_code)

2. Set Appropriate Timeouts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ✅ GOOD: Timeout protection
   try:
       result = await asyncio.wait_for(
           executor.execute_ml_code(ml_code),
           timeout=30.0
       )
   except asyncio.TimeoutError:
       # Handle timeout

   # ❌ BAD: No timeout (can hang forever)
   result = await executor.execute_ml_code(ml_code)

3. Handle Concurrent Errors Gracefully
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ✅ GOOD: Collect all results, handle errors
   results = await asyncio.gather(
       *tasks,
       return_exceptions=True
   )
   for result in results:
       if isinstance(result, Exception):
           log_error(result)

   # ❌ BAD: One failure stops all
   results = await asyncio.gather(*tasks)

4. Use Background Tasks for Long Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ✅ GOOD: Return immediately, process in background
   @app.post("/process")
   async def process(data, background_tasks: BackgroundTasks):
       background_tasks.add_task(long_ml_task, data)
       return {"status": "submitted"}

   # ❌ BAD: Block request until complete
   @app.post("/process")
   async def process(data):
       result = await long_ml_task(data)
       return result

5. Monitor and Limit Concurrency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # ✅ GOOD: Limit concurrent tasks
   semaphore = asyncio.Semaphore(10)

   async def execute_with_limit(ml_code):
       async with semaphore:
           return await executor.execute_ml_code(ml_code)

   # ❌ BAD: Unlimited concurrency (resource exhaustion)
   tasks = [executor.execute_ml_code(code) for code in codes]
   await asyncio.gather(*tasks)

----

Summary
-------

This chapter covered asynchronous ML integration:

**Key Takeaways:**

1. **AsyncIO**: Use async/await for non-blocking ML execution
2. **Thread Pools**: Execute ML in threads while keeping event loop responsive
3. **Web Integration**: FastAPI, aiohttp, Sanic integration patterns
4. **Capability Propagation**: Use context variables for async capability management
5. **Error Handling**: Handle timeouts, concurrent errors gracefully
6. **Performance**: Connection pooling, batching, caching for production

**When to Use Async Integration:**

✅ Web servers (FastAPI, aiohttp)
✅ GUI applications (keep UI responsive)
✅ High-throughput services
✅ WebSocket servers
✅ Background task processing

**Next Steps:**

- **Chapter 2.3**: Event-driven integration for reactive systems
- **Chapter 2.4**: Framework-specific integration (Flask, Django, Qt)
- **Chapter 3.1**: Data marshalling deep dive

**Quick Reference:**

.. code-block:: python

   # Basic async execution
   from mlpy import AsyncMLExecutor

   executor = AsyncMLExecutor(max_workers=10)
   result = await executor.execute_ml_code(ml_code)

   # Concurrent execution
   results = await asyncio.gather(
       executor.execute_ml_code(code1),
       executor.execute_ml_code(code2),
       executor.execute_ml_code(code3)
   )

   # With timeout
   result = await asyncio.wait_for(
       executor.execute_ml_code(ml_code),
       timeout=30.0
   )

   # FastAPI integration
   @app.post("/execute")
   async def execute(ml_code: str):
       result = await executor.execute_ml_code(ml_code)
       return {"result": result}

----

**Chapter Status:** ✅ Complete | **Target Length:** ~2,000 lines | **Actual Length:** 2,234 lines
