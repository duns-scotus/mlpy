"""FastAPI Integration Example - Async ML Execution in Web APIs

Demonstrates:
- Non-blocking ML code execution in FastAPI endpoints
- Context variable passing from HTTP requests
- Timeout handling for long-running ML scripts
- Error handling and validation
- Performance optimization with executor reuse

Requirements:
    pip install fastapi uvicorn

Run:
    uvicorn app:app --reload

Then visit:
    http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging

# Import ML async executor
from mlpy.integration import AsyncMLExecutor, AsyncMLResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ML Code Execution API",
    description="Execute ML code asynchronously via REST API",
    version="1.0.0"
)

# Create single executor instance (reused across requests for performance)
# Using 4 workers allows handling 4 concurrent ML executions
executor = AsyncMLExecutor(
    max_workers=4,
    strict_security=False  # Adjust based on your security requirements
)


# Request models
class MLExecutionRequest(BaseModel):
    """Request to execute ML code."""
    code: str = Field(..., description="ML source code to execute", min_length=1)
    timeout: Optional[float] = Field(5.0, description="Timeout in seconds", gt=0, le=30)
    context: Optional[Dict[str, Any]] = Field(None, description="Context variables for ML code")

    class Config:
        schema_extra = {
            "example": {
                "code": "result = x + y;",
                "timeout": 5.0,
                "context": {"x": 10, "y": 20}
            }
        }


class MLExecutionResponse(BaseModel):
    """Response from ML code execution."""
    success: bool
    value: Any = None
    error: Optional[str] = None
    execution_time: float
    transpile_time: float


# Endpoints
@app.get("/")
async def root():
    """API information."""
    return {
        "name": "ML Code Execution API",
        "version": "1.0.0",
        "endpoints": {
            "/execute": "Execute ML code (POST)",
            "/calculate": "Simple calculation endpoint (GET)",
            "/health": "Health check (GET)"
        }
    }


@app.post("/execute", response_model=MLExecutionResponse)
async def execute_ml_code(request: MLExecutionRequest):
    """Execute ML code asynchronously.

    Example ML code:
    ```ml
    // Simple calculation
    result = 2 + 2;

    // With context variables
    result = x * y;

    // Complex calculation
    sum = 0;
    i = 1;
    while (i <= 10) {
        sum = sum + i;
        i = i + 1;
    }
    result = sum;
    ```
    """
    try:
        logger.info(f"Executing ML code (timeout={request.timeout}s)")

        # Execute ML code asynchronously (non-blocking)
        result = await executor.execute(
            request.code,
            timeout=request.timeout,
            context=request.context
        )

        logger.info(f"ML execution completed: success={result.success}, time={result.execution_time:.3f}s")

        return MLExecutionResponse(
            success=result.success,
            value=result.value,
            error=result.error,
            execution_time=result.execution_time,
            transpile_time=result.transpile_time
        )

    except Exception as e:
        logger.exception("Unexpected error during ML execution")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/calculate")
async def calculate(
    operation: str = Query(..., description="Operation: add, multiply, power"),
    a: float = Query(..., description="First operand"),
    b: float = Query(..., description="Second operand")
):
    """Simple calculation endpoint using ML code.

    Examples:
        /calculate?operation=add&a=10&b=5
        /calculate?operation=multiply&a=7&b=6
        /calculate?operation=power&a=2&b=8
    """
    # Generate ML code based on operation
    ml_code_map = {
        "add": "result = a + b;",
        "multiply": "result = a * b;",
        "power": """
            result = 1;
            i = 0;
            while (i < b) {
                result = result * a;
                i = i + 1;
            }
        """,
        "subtract": "result = a - b;",
        "divide": """
            if (b == 0) {
                throw {message: "Division by zero", type: "MathError"};
            }
            result = a / b;
        """
    }

    if operation not in ml_code_map:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid operation. Supported: {', '.join(ml_code_map.keys())}"
        )

    try:
        # Execute ML code with context
        result = await executor.execute(
            ml_code_map[operation],
            timeout=2.0,
            context={"a": a, "b": b}
        )

        if not result.success:
            raise HTTPException(status_code=400, detail=result.error)

        return {
            "operation": operation,
            "a": a,
            "b": b,
            "result": result.value,
            "execution_time_ms": result.execution_time * 1000
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Calculation error")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    # Test executor with simple ML code
    try:
        result = await executor.execute("result = 42;", timeout=1.0)

        return {
            "status": "healthy" if result.success else "degraded",
            "executor": {
                "max_workers": executor.max_workers,
                "strict_security": executor.strict_security
            },
            "test_execution": {
                "success": result.success,
                "execution_time_ms": result.execution_time * 1000
            }
        }
    except Exception as e:
        logger.exception("Health check failed")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down ML executor")
    executor.shutdown(wait=True)


# Example usage and testing
if __name__ == "__main__":
    import uvicorn

    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  FastAPI ML Integration Example                           ║
    ║                                                            ║
    ║  Starting server on http://localhost:8000                 ║
    ║  API Documentation: http://localhost:8000/docs            ║
    ║                                                            ║
    ║  Example requests:                                         ║
    ║  1. GET  /calculate?operation=add&a=10&b=5                ║
    ║  2. POST /execute                                          ║
    ║     Body: {"code": "result = 2 + 2;"}                     ║
    ║  3. GET  /health                                           ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
