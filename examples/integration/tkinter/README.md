# Tkinter ML Integration Example

Demonstrates how to integrate async ML code execution into Tkinter GUI applications, keeping the UI responsive during ML execution.

## Features

- **Non-blocking Execution**: ML code runs asynchronously without freezing the GUI
- **Responsive UI**: Users can interact with the application while ML code executes
- **Real-time Status**: Progress and status updates during execution
- **Error Handling**: Graceful error display in GUI
- **Example Programs**: Pre-loaded ML code examples for testing
- **Async/Tk Bridge**: Seamless integration between asyncio and Tkinter's event loop

## Installation

1. **Python 3.12+** is required (tkinter is built-in)

2. Install mlpy (from project root):
```bash
cd /path/to/mlpy
pip install -e .
```

## Running the Example

Simply run:
```bash
python app.py
```

## Application Features

### Code Editor

- **Syntax-aware** text editor for ML code
- **Scrollable** for long programs
- **Example loading** with one-click buttons

### Execution Controls

- **Execute Button**: Run ML code asynchronously
- **Timeout Setting**: Configure execution timeout (0.5-30 seconds)
- **Clear Output**: Clear results display
- **Status Display**: Real-time execution status

### Results Display

- **Execution Status**: Success or failure indication
- **Result Value**: Output from ML code execution
- **Timing Metrics**: Transpile time, execution time, total time
- **Error Messages**: Detailed error information on failure
- **History**: Multiple execution results displayed (newest first)

### Example Programs

Four pre-loaded example programs:

1. **Simple Math**: Basic arithmetic operations with object results
2. **Fibonacci**: Recursive Fibonacci sequence calculation
3. **Array Processing**: Sum of squares of even numbers
4. **Factorial**: Recursive factorial calculation with multiple values

## How It Works

### Architecture

```
┌─────────────────┐
│  Tkinter GUI    │
│  (Main Thread)  │
└────────┬────────┘
         │
         │ User clicks "Execute"
         ▼
┌─────────────────┐
│  Async Loop     │
│  (Background    │
│   Thread)       │
└────────┬────────┘
         │
         │ asyncio.run_coroutine_threadsafe()
         ▼
┌─────────────────┐
│ AsyncMLExecutor │
│  (ThreadPool)   │
└────────┬────────┘
         │
         │ Background execution
         ▼
┌─────────────────┐
│  ML Transpiler  │
│  + Execution    │
└────────┬────────┘
         │
         │ Result ready
         ▼
┌─────────────────┐
│  root.after()   │
│  Update GUI     │
└─────────────────┘
```

### Key Integration Pattern

The example uses a background thread running an asyncio event loop:

```python
# 1. Start async event loop in background thread
def start_async_loop(self):
    def run_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    self.loop = asyncio.new_event_loop()
    self.loop_thread = threading.Thread(
        target=run_loop,
        args=(self.loop,),
        daemon=True
    )
    self.loop_thread.start()

# 2. Execute ML code asynchronously
def execute_code(self):
    ml_code = self.code_editor.get("1.0", tk.END).strip()
    asyncio.run_coroutine_threadsafe(
        self._execute_async(ml_code),
        self.loop
    )

# 3. Update GUI from main thread
async def _execute_async(self, ml_code: str):
    result = await self.executor.execute(ml_code, timeout=timeout)
    self.root.after(0, self._display_result, result, total_time)
```

## Example ML Code

### Simple Calculation
```ml
sum = 0;
i = 1;
while (i <= 100) {
    sum = sum + i;
    i = i + 1;
}
result = sum;  // 5050
```

### With Functions
```ml
function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

result = factorial(10);  // 3628800
```

### Array Operations
```ml
numbers = [1, 2, 3, 4, 5];
doubled = [];

for (n in numbers) {
    doubled = doubled + [n * 2];
}

result = doubled;  // [2, 4, 6, 8, 10]
```

### Object Results
```ml
a = 10;
b = 20;

result = {
    sum: a + b,
    product: a * b,
    difference: b - a
};
```

## Performance Considerations

### UI Responsiveness

- ML execution runs in background threads via `AsyncMLExecutor`
- Tkinter's main thread remains free to process UI events
- Users can interact with the application during ML execution

### Threading Model

```
Main Thread (Tkinter):
  - UI event handling
  - Widget updates
  - User interactions

Background Thread (Asyncio):
  - Async event loop
  - ML executor scheduling
  - Non-blocking execution

Worker Threads (ThreadPool):
  - ML code transpilation
  - Python code execution
  - Actual computation
```

### Timeout Protection

Always set reasonable timeouts to prevent hanging:
```python
result = await executor.execute(ml_code, timeout=5.0)
```

## Common Patterns

### Pattern 1: Simple Execution

```python
# Execute ML code and display result
async def _execute_async(self, ml_code: str):
    result = await self.executor.execute(ml_code, timeout=5.0)
    self.root.after(0, self._display_result, result)
```

### Pattern 2: With Context Variables

```python
# Pass GUI values to ML code
async def execute_with_context(self):
    context = {
        'input_value': self.input_var.get(),
        'multiplier': self.multiplier_var.get()
    }

    ml_code = "result = input_value * multiplier;"
    result = await self.executor.execute(ml_code, context=context)
    self.root.after(0, self._update_output, result)
```

### Pattern 3: Progress Updates

```python
# Show progress during execution
async def execute_with_progress(self, ml_code: str):
    self.root.after(0, self.progress_bar.start)

    result = await self.executor.execute(ml_code, timeout=10.0)

    self.root.after(0, self.progress_bar.stop)
    self.root.after(0, self._display_result, result)
```

## Error Handling

The application handles various error scenarios:

1. **Parse Errors**: Invalid ML syntax
2. **Runtime Errors**: Execution failures
3. **Timeouts**: Long-running code exceeding timeout
4. **Unexpected Errors**: Caught and displayed gracefully

All errors are displayed in the results pane with detailed information.

## Extending the Example

### Add Custom Examples

```python
def example_custom(self):
    code = """// Your custom ML code
result = 42;
"""
    self.code_editor.delete("1.0", tk.END)
    self.code_editor.insert("1.0", code)

# Add button in setup_ui()
ttk.Button(
    examples_frame,
    text="Custom",
    command=self.example_custom
).pack(side=tk.LEFT, padx=5)
```

### Add Context Variable Inputs

```python
# Add entry widgets
self.x_var = tk.IntVar(value=10)
ttk.Entry(control_frame, textvariable=self.x_var).pack()

# Use in execution
context = {'x': self.x_var.get()}
result = await self.executor.execute(ml_code, context=context)
```

### Add Result Visualization

```python
# Display result as graph (requires matplotlib)
def _display_result(self, result):
    if isinstance(result.value, list):
        # Plot array as graph
        self.plot_array(result.value)
```

## Troubleshooting

### Issue: GUI Freezes
**Solution**: Ensure ML execution uses `asyncio.run_coroutine_threadsafe()` to run in background loop

### Issue: Results Not Displaying
**Solution**: Always update GUI using `self.root.after(0, callback)` from async code

### Issue: Timeout Not Working
**Solution**: Check that timeout value is properly passed to `executor.execute()`

## Related Examples

- **FastAPI Integration**: See `examples/integration/fastapi/` for web API integration
- **Flask Integration**: Similar async patterns apply
- **PyQt Integration**: Similar threading patterns with PyQt event loop

## Next Steps

- Add syntax highlighting for ML code
- Implement code completion
- Add debugging features (breakpoints, step execution)
- Create custom ML function libraries
- Add result visualization (charts, graphs)
