# FastAPI ML Integration Example

Demonstrates how to integrate ML code execution into FastAPI web applications using `AsyncMLExecutor`.

## Features

- **Non-blocking Execution**: ML code runs in background threads without blocking the main event loop
- **Concurrent Requests**: Handle multiple ML execution requests simultaneously (4 workers by default)
- **Timeout Support**: Prevent long-running ML scripts from hanging the API
- **Context Variables**: Pass data from HTTP requests into ML code execution context
- **Error Handling**: Graceful error handling with proper HTTP status codes
- **Performance Optimized**: Single executor instance reused across all requests

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install mlpy (from project root):
```bash
cd /path/to/mlpy
pip install -e .
```

## Running the Example

Start the FastAPI server:
```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --reload
```

The API will be available at:
- **Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### POST /execute

Execute arbitrary ML code with optional context and timeout.

**Request:**
```json
{
  "code": "result = x + y;",
  "timeout": 5.0,
  "context": {
    "x": 10,
    "y": 20
  }
}
```

**Response:**
```json
{
  "success": true,
  "value": 30,
  "error": null,
  "execution_time": 0.023,
  "transpile_time": 0.012
}
```

**Example ML Code:**

Simple calculation:
```ml
result = 2 + 2;
```

With loops:
```ml
sum = 0;
i = 1;
while (i <= 100) {
    sum = sum + i;
    i = i + 1;
}
result = sum;
```

With context variables:
```ml
// Assumes context: {"numbers": [1, 2, 3, 4, 5]}
sum = 0;
for (n in numbers) {
    sum = sum + n;
}
result = sum;
```

### GET /calculate

Simple calculation endpoint with predefined operations.

**Examples:**
```bash
# Addition
curl "http://localhost:8000/calculate?operation=add&a=10&b=5"

# Multiplication
curl "http://localhost:8000/calculate?operation=multiply&a=7&b=6"

# Power (2^8)
curl "http://localhost:8000/calculate?operation=power&a=2&b=8"
```

**Response:**
```json
{
  "operation": "add",
  "a": 10,
  "b": 5,
  "result": 15,
  "execution_time_ms": 12.5
}
```

### GET /health

Health check endpoint that tests ML executor.

**Response:**
```json
{
  "status": "healthy",
  "executor": {
    "max_workers": 4,
    "strict_security": false
  },
  "test_execution": {
    "success": true,
    "execution_time_ms": 8.2
  }
}
```

## Testing with curl

Execute ML code:
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "result = 2 + 2;",
    "timeout": 5.0
  }'
```

With context variables:
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "result = x * y;",
    "context": {"x": 7, "y": 6},
    "timeout": 5.0
  }'
```

## Testing with Python

```python
import httpx
import asyncio

async def test_api():
    async with httpx.AsyncClient() as client:
        # Simple execution
        response = await client.post(
            "http://localhost:8000/execute",
            json={
                "code": "result = 2 + 2;",
                "timeout": 5.0
            }
        )
        print(response.json())

        # With context
        response = await client.post(
            "http://localhost:8000/execute",
            json={
                "code": "result = x + y;",
                "context": {"x": 10, "y": 20},
                "timeout": 5.0
            }
        )
        print(response.json())

asyncio.run(test_api())
```

## Performance Considerations

1. **Executor Reuse**: Single `AsyncMLExecutor` instance is created at startup and reused across all requests for better performance

2. **Worker Pool**: Default 4 workers allows handling 4 concurrent ML executions. Adjust based on your needs:
   ```python
   executor = AsyncMLExecutor(max_workers=8)
   ```

3. **Timeouts**: Always specify reasonable timeouts to prevent resource exhaustion:
   ```python
   result = await executor.execute(code, timeout=5.0)
   ```

4. **Security**: For production, consider enabling strict security:
   ```python
   executor = AsyncMLExecutor(strict_security=True)
   ```

## Production Deployment

For production deployment, use a proper ASGI server:

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn + Uvicorn workers
gunicorn app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Architecture

```
┌─────────────────┐
│  FastAPI        │
│  (async/await)  │
└────────┬────────┘
         │
         │ HTTP Request
         ▼
┌─────────────────┐
│  /execute       │
│  endpoint       │
└────────┬────────┘
         │
         │ await executor.execute()
         ▼
┌─────────────────┐
│ AsyncMLExecutor │
│  (ThreadPool)   │
└────────┬────────┘
         │
         │ Background thread
         ▼
┌─────────────────┐
│  ML Transpiler  │
│  + Execution    │
└─────────────────┘
```

## Error Handling

The API handles various error scenarios:

1. **Invalid ML Syntax**:
```json
{
  "success": false,
  "error": "Parse error: unexpected token...",
  "value": null
}
```

2. **Timeout**:
```json
{
  "success": false,
  "error": "Execution timeout after 5.0 seconds",
  "value": null
}
```

3. **Runtime Error**:
```json
{
  "success": false,
  "error": "name 'undefined_variable' is not defined",
  "value": null
}
```

## Next Steps

- Add authentication/authorization
- Implement rate limiting
- Add request logging and monitoring
- Create custom ML function libraries
- Add caching for frequently executed ML scripts

## Related Examples

- **Tkinter Integration**: See `examples/integration/tkinter/` for GUI integration
- **Flask Integration**: Similar patterns apply to Flask applications
