"""
FastAPI Real-Time Analytics with ML Backend
Demonstrates async ML execution with FastAPI
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Add mlpy to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.mlpy.ml.transpiler import MLTranspiler
from src.mlpy.runtime.capabilities import CapabilityContext


# Pydantic models for request/response
class Event(BaseModel):
    id: str
    type: str
    user_id: Optional[str] = None
    data: Dict[str, Any] = {}


class ProcessEventResponse(BaseModel):
    success: bool
    event: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class MetricsResponse(BaseModel):
    total_events: int
    by_type: Dict[str, int]
    by_category: Dict[str, int]
    high_priority: int


class FilterRequest(BaseModel):
    events: List[Dict[str, Any]]
    filters: Dict[str, Any]


class DashboardRequest(BaseModel):
    events: List[Dict[str, Any]]
    time_range: str = "last_hour"


class AggregateRequest(BaseModel):
    events: List[Dict[str, Any]]
    window_size: int = 10


# In-memory event store (for demonstration)
event_store: List[Dict[str, Any]] = []


class MLAnalyticsAPI:
    """FastAPI powered by async ML analytics"""

    def __init__(self, ml_file: Path):
        self.app = FastAPI(
            title="ML Analytics API",
            description="Real-time analytics with async ML processing",
            version="1.0.0"
        )
        self.ml_functions = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.max_workers = 4
        self.init_ml(ml_file)
        self.setup_routes()

    def _call_with_capabilities(self, func_name, capabilities, *args):
        """Helper to call ML function with capability context in thread pool"""
        with CapabilityContext() as ctx:
            for cap in capabilities:
                ctx.add_capability(cap)
            return self.ml_functions[func_name](*args)

    def init_ml(self, ml_file: Path):
        """Initialize ML transpiler and load functions"""
        try:
            # Transpile ML code
            transpiler = MLTranspiler()
            with open(ml_file, "r", encoding="utf-8") as f:
                ml_code = f.read()

            python_code, issues, source_map = transpiler.transpile_to_python(
                ml_code, source_file=str(ml_file), strict_security=False
            )

            if issues:
                raise Exception(f"ML transpilation issues: {issues}")

            # Execute transpiled code to get ML functions
            namespace = {}
            exec(python_code, namespace)

            # Extract ML functions (no wrapping needed - they're already Python functions)
            function_names = [
                "process_event",
                "calculate_metrics",
                "detect_anomalies",
                "generate_dashboard",
                "filter_events",
                "aggregate_by_window",
            ]

            for func_name in function_names:
                if func_name in namespace:
                    self.ml_functions[func_name] = namespace[func_name]

            print(f"Loaded {len(self.ml_functions)} ML functions with ThreadPoolExecutor")

        except Exception as e:
            print(f"Error loading ML functions: {e}")
            raise

    def setup_routes(self):
        """Setup FastAPI routes with async ML execution"""

        @self.app.get("/")
        async def root():
            """API information"""
            return {
                "name": "ML Analytics API",
                "version": "1.0.0",
                "description": "Real-time analytics with async ML processing",
                "docs": "/docs",
                "endpoints": {
                    "POST /events": "Submit new event",
                    "GET /events": "Get all events",
                    "POST /events/process": "Process single event",
                    "POST /metrics": "Calculate metrics",
                    "POST /dashboard": "Generate dashboard",
                    "POST /anomalies": "Detect anomalies",
                    "POST /filter": "Filter events",
                    "POST /aggregate": "Aggregate by time window",
                }
            }

        @self.app.post("/events", response_model=ProcessEventResponse)
        async def submit_event(event: Event, background_tasks: BackgroundTasks):
            """Submit a new event for processing (async)"""
            try:
                # Convert Pydantic model to dict
                event_dict = event.dict()

                # Process event asynchronously with datetime capability
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self._call_with_capabilities,
                    "process_event",
                    ["datetime.now"],
                    event_dict
                )

                if result["success"]:
                    # Store processed event
                    processed_event = result["event"]
                    event_store.append(processed_event)

                return ProcessEventResponse(**result)

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/events")
        async def get_events(limit: int = 100):
            """Get recent events"""
            return {
                "total": len(event_store),
                "events": event_store[-limit:] if len(event_store) > limit else event_store
            }

        @self.app.delete("/events")
        async def clear_events():
            """Clear all events (for testing)"""
            event_store.clear()
            return {"message": "All events cleared", "count": 0}

        @self.app.post("/events/process", response_model=ProcessEventResponse)
        async def process_single_event(event: Event):
            """Process a single event without storing"""
            try:
                event_dict = event.dict()

                # Async execution with datetime capability
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self._call_with_capabilities,
                    "process_event",
                    ["datetime.now"],
                    event_dict
                )

                return ProcessEventResponse(**result)

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/metrics", response_model=MetricsResponse)
        async def calculate_metrics(events: Optional[List[Dict[str, Any]]] = None):
            """Calculate metrics for events (async)"""
            try:
                # Use stored events if none provided
                events_to_analyze = events if events is not None else event_store

                if not events_to_analyze:
                    return MetricsResponse(
                        total_events=0,
                        by_type={},
                        by_category={},
                        high_priority=0
                    )

                # Async execution
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self.ml_functions["calculate_metrics"],
                    events_to_analyze
                )

                return MetricsResponse(**result)

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/dashboard")
        async def generate_dashboard(request: DashboardRequest):
            """Generate dashboard summary (async)"""
            try:
                # Use stored events if none provided
                events = request.events if request.events else event_store

                if not events:
                    raise HTTPException(status_code=400, detail="No events available")

                # Async execution
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self.ml_functions["generate_dashboard"],
                    events,
                    request.time_range
                )

                return result

            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/anomalies")
        async def detect_anomalies(
            events: Optional[List[Dict[str, Any]]] = None,
            threshold: float = 10.0
        ):
            """Detect anomalies in event stream (async)"""
            try:
                events_to_analyze = events if events is not None else event_store

                if not events_to_analyze:
                    raise HTTPException(status_code=400, detail="No events to analyze")

                # Async execution
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self.ml_functions["detect_anomalies"],
                    events_to_analyze,
                    threshold
                )

                return result

            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/filter")
        async def filter_events(request: FilterRequest):
            """Filter events by criteria (async)"""
            try:
                # Async execution
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self.ml_functions["filter_events"],
                    request.events,
                    request.filters
                )

                return {
                    "filtered_events": result,
                    "count": len(result)
                }

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/aggregate")
        async def aggregate_by_window(request: AggregateRequest):
            """Aggregate events by time window (async)"""
            try:
                # Async execution
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self.ml_functions["aggregate_by_window"],
                    request.events,
                    request.window_size
                )

                return {
                    "windows": result,
                    "window_count": len(result)
                }

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/health")
        async def health():
            """Health check"""
            return {
                "status": "healthy",
                "ml_functions_loaded": len(self.ml_functions),
                "executor_workers": self.max_workers,
                "stored_events": len(event_store)
            }

    def get_app(self):
        """Get the FastAPI app instance"""
        return self.app


def create_app() -> FastAPI:
    """Factory function to create the FastAPI app"""
    ml_file = Path(__file__).parent / "ml_analytics.ml"
    api = MLAnalyticsAPI(ml_file)
    return api.get_app()


# Create app instance for uvicorn
app = create_app()


if __name__ == "__main__":
    import uvicorn

    print("Starting ML-powered FastAPI Analytics API...")
    print("API documentation: http://127.0.0.1:8000/docs")
    print("OpenAPI spec: http://127.0.0.1:8000/openapi.json")

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
