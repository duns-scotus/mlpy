# ML Integration Examples

This directory contains comprehensive examples demonstrating how to integrate ML language into various Python frameworks and applications.

## Overview

These examples show how to:
- Transpile ML code to Python at runtime
- Use ML functions as callbacks in Python applications
- Integrate ML business logic with Python frameworks
- Handle async execution of ML code

## Examples

### 1. PySide6 GUI Calculator (`gui/pyside6/`)

**Description:** A Qt6 desktop calculator application with business logic written in ML.

**Key Features:**
- ML functions as GUI button callbacks
- Async ML execution using QThread
- Three tabs demonstrating different patterns:
  - Basic Calculator (synchronous callbacks)
  - Compound Interest (async calculation with progress)
  - Fibonacci (long-running calculation)

**Running:**
```bash
python examples/integration/gui/pyside6/calculator_gui.py
```

**ML Code:** `ml_calculator.ml`
- Basic arithmetic functions
- Financial calculations
- Statistical operations

---

### 2. Flask Web API (`web/flask/`)

**Description:** A RESTful API for user management and analytics with ML business logic.

**Key Features:**
- ML functions as Flask route handlers
- User validation logic in ML
- Analytics and reporting in ML
- JSON API endpoints

**Running:**
```bash
# Start the server
python examples/integration/web/flask/app.py

# In another terminal, run the test client
python examples/integration/web/flask/test_client.py
```

**Endpoints:**
- `POST /api/users/validate` - Validate user data
- `POST /api/users/score` - Calculate user engagement score
- `POST /api/analytics/cohort` - Analyze user cohorts
- `POST /api/users/search` - Search users by criteria
- `POST /api/analytics/report` - Generate analytics report

**ML Code:** `ml_api.ml`
- User validation functions
- Scoring algorithms
- Analytics and reporting functions

---

### 3. FastAPI Analytics Dashboard (`web/fastapi/`)

**Description:** A real-time analytics API with async ML execution using FastAPI.

**Key Features:**
- Async ML execution with thread pool
- Real-time event processing
- Anomaly detection
- Time-window aggregation
- Automatic OpenAPI documentation

**Running:**
```bash
# Start the server
python examples/integration/web/fastapi/app.py

# Or using uvicorn
uvicorn examples.integration.web.fastapi.app:app --reload

# In another terminal, run the test client
python examples/integration/web/fastapi/test_client.py
```

**Documentation:** Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI

**Endpoints:**
- `POST /events` - Submit new events
- `GET /events` - Retrieve stored events
- `POST /metrics` - Calculate metrics
- `POST /dashboard` - Generate dashboard summary
- `POST /anomalies` - Detect anomalies
- `POST /filter` - Filter events
- `POST /aggregate` - Aggregate by time window

**ML Code:** `ml_analytics.ml`
- Event processing functions
- Metrics calculation
- Anomaly detection
- Dashboard generation

---

## Common Patterns

### 1. Transpiling ML Code

All examples follow this pattern:

```python
from src.mlpy.ml.transpiler import MLTranspiler

# Create transpiler
transpiler = MLTranspiler()

# Read ML source code
with open("my_ml_file.ml", "r", encoding="utf-8") as f:
    ml_code = f.read()

# Transpile to Python
python_code, issues, source_map = transpiler.transpile_to_python(
    ml_code,
    source_file="my_ml_file.ml",
    strict_security=False  # For integration examples
)

# Execute transpiled code
namespace = {}
exec(python_code, namespace)

# Extract ML functions
my_function = namespace["my_function"]
```

### 2. ML Module-Level Imports

ML imports must be at the module level, not inside functions:

```ml
// Correct - imports at module level
import math;
import datetime;

function calculate() {
    return math.pow(2, 3);
}
```

```ml
// Incorrect - imports inside function
function calculate() {
    import math;  // ❌ This will fail to parse
    return math.pow(2, 3);
}
```

### 3. Available Standard Library Modules

The following ML standard library modules are available:
- `collections` - Collection utilities
- `console` - Console I/O
- `datetime` - Date and time operations
- `file` - File operations
- `functional` - Functional programming utilities
- `http` - HTTP client
- `json` - JSON encoding/decoding
- `math` - Mathematical functions
- `path` - Path manipulation
- `random` - Random number generation
- `regex` - Regular expression operations

---

## Dependencies

All integration examples require the following dependencies (already in `requirements.txt`):

```txt
PySide6>=6.6.0           # For GUI examples
Flask>=3.0.0             # For Flask example
fastapi>=0.109.0         # For FastAPI example
uvicorn>=0.27.0          # ASGI server for FastAPI
httpx>=0.26.0            # Async HTTP client for testing
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Architecture

### Integration Flow

```
ML Source Code (*.ml)
  ↓
MLTranspiler
  ↓
Python Code (in-memory)
  ↓
exec() → namespace
  ↓
Extract Functions
  ↓
Use as Python callables
```

### Async Execution (PySide6 & FastAPI)

```
ML Function Call
  ↓
Thread Pool / QThread
  ↓
Async Execution
  ↓
Signal/Callback
  ↓
Update UI / Return Response
```

---

## Best Practices

1. **Security:** Use `strict_security=False` only for trusted ML code. Production applications should enable strict security checks.

2. **Error Handling:** Always wrap ML function calls in try/except blocks to handle transpilation and execution errors gracefully.

3. **Type Conversion:** ML uses Python-compatible types, but ensure proper conversion between ML dictionaries/arrays and Python dicts/lists.

4. **Performance:** For CPU-intensive ML functions, use async execution (QThread, FastAPI's thread pool, or AsyncMLExecutor) to avoid blocking the main thread.

5. **Module Imports:** Always place import statements at the ML module level, not inside functions.

6. **Testing:** Each example includes a test client to verify functionality.

---

## Next Steps

After exploring these examples, you can:

1. **Create Your Own Integration:** Use these examples as templates for your own applications
2. **Extend ML Code:** Add more complex business logic in ML
3. **Add Authentication:** Implement authentication/authorization in the web APIs
4. **Database Integration:** Connect ML functions to databases
5. **Deploy to Production:** Package and deploy these applications

---

## Troubleshooting

### Import Errors

**Error:** `Unknown identifier 'module_name'`

**Solution:** Ensure imports are at module level:
```ml
import datetime;  // ✓ At module level

function myFunc() {
    return datetime.now();
}
```

### Transpilation Failures

**Error:** `Transpilation failed due to security issues`

**Solution:** Use `strict_security=False` for integration examples:
```python
python_code, issues, source_map = transpiler.transpile_to_python(
    ml_code, strict_security=False
)
```

### Module Not Found

**Error:** Module 'xyz' not available

**Solution:** Use correct module names from the available standard library modules list above.

---

## Contributing

To add new integration examples:

1. Create a new directory under `examples/integration/`
2. Write ML business logic (*.ml file)
3. Create Python application that transpiles and uses ML code
4. Add test client to verify functionality
5. Update this README with documentation

---

## License

These examples are part of the mlpy project and follow the same license.
