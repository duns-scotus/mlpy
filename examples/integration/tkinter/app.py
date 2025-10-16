"""Tkinter Integration Example - Async ML Execution in GUI

Demonstrates:
- Non-blocking ML code execution in Tkinter GUI
- Keeping UI responsive during ML execution
- Progress updates and status display
- Error handling in GUI context
- Threading integration with Tk event loop

Requirements:
    - Python 3.12+ (tkinter is built-in)
    - mlpy installed

Run:
    python app.py
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import asyncio
import threading
from typing import Optional
import time

# Import ML async executor
from mlpy.integration import AsyncMLExecutor, AsyncMLResult


class AsyncMLApp:
    """Tkinter application with async ML code execution.

    Bridges asyncio event loop with Tkinter's mainloop to enable
    non-blocking ML execution while keeping the GUI responsive.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ML Code Executor - Async Integration")
        self.root.geometry("900x700")

        # Create ML executor (reused across executions)
        self.executor = AsyncMLExecutor(
            max_workers=2,
            strict_security=False
        )

        # Async event loop (runs in background thread)
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.loop_thread: Optional[threading.Thread] = None

        # Setup GUI components
        self.setup_ui()

        # Start async event loop in background
        self.start_async_loop()

        # Cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        """Setup UI components."""
        # Title
        title_label = tk.Label(
            self.root,
            text="ML Code Executor",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Code editor section
        code_frame = ttk.LabelFrame(main_frame, text="ML Code", padding="10")
        code_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.code_editor = scrolledtext.ScrolledText(
            code_frame,
            wrap=tk.WORD,
            height=10,
            font=("Courier New", 10)
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # Insert example ML code
        example_code = """// Example ML code - try editing and clicking Execute!
sum = 0;
i = 1;
while (i <= 100) {
    sum = sum + i;
    i = i + 1;
}
result = sum;
"""
        self.code_editor.insert("1.0", example_code)

        # Control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # Timeout setting
        ttk.Label(control_frame, text="Timeout (seconds):").pack(side=tk.LEFT, padx=(0, 5))
        self.timeout_var = tk.DoubleVar(value=5.0)
        timeout_spin = ttk.Spinbox(
            control_frame,
            from_=0.5,
            to=30.0,
            increment=0.5,
            textvariable=self.timeout_var,
            width=10
        )
        timeout_spin.pack(side=tk.LEFT, padx=(0, 20))

        # Execute button
        self.execute_btn = ttk.Button(
            control_frame,
            text="Execute ML Code",
            command=self.execute_code
        )
        self.execute_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Clear button
        clear_btn = ttk.Button(
            control_frame,
            text="Clear Output",
            command=self.clear_output
        )
        clear_btn.pack(side=tk.LEFT)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            control_frame,
            textvariable=self.status_var,
            font=("Arial", 9, "italic")
        )
        status_label.pack(side=tk.RIGHT)

        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Execution Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)

        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            height=10,
            font=("Courier New", 10),
            bg="#f0f0f0"
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Examples buttons
        examples_frame = ttk.LabelFrame(main_frame, text="Example ML Programs", padding="10")
        examples_frame.pack(fill=tk.X, pady=(10, 0))

        examples = [
            ("Simple Math", self.example_simple_math),
            ("Fibonacci", self.example_fibonacci),
            ("Array Processing", self.example_array),
            ("Factorial", self.example_factorial)
        ]

        for text, command in examples:
            ttk.Button(
                examples_frame,
                text=text,
                command=command,
                width=15
            ).pack(side=tk.LEFT, padx=5)

    def start_async_loop(self):
        """Start asyncio event loop in background thread."""
        def run_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self.loop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(target=run_loop, args=(self.loop,), daemon=True)
        self.loop_thread.start()

    def execute_code(self):
        """Execute ML code asynchronously."""
        # Get code from editor
        ml_code = self.code_editor.get("1.0", tk.END).strip()

        if not ml_code:
            messagebox.showwarning("Empty Code", "Please enter ML code to execute")
            return

        # Disable execute button during execution
        self.execute_btn.config(state=tk.DISABLED)
        self.status_var.set("Executing...")

        # Schedule async execution in the background event loop
        asyncio.run_coroutine_threadsafe(
            self._execute_async(ml_code),
            self.loop
        )

    async def _execute_async(self, ml_code: str):
        """Execute ML code asynchronously (runs in background thread)."""
        try:
            timeout = self.timeout_var.get()
            start_time = time.perf_counter()

            # Execute ML code (non-blocking)
            result = await self.executor.execute(ml_code, timeout=timeout)

            total_time = time.perf_counter() - start_time

            # Update GUI from main thread
            self.root.after(0, self._display_result, result, total_time)

        except Exception as e:
            # Update GUI with error from main thread
            self.root.after(0, self._display_error, str(e))

    def _display_result(self, result: AsyncMLResult, total_time: float):
        """Display execution result in GUI (runs in main thread)."""
        # Build result text
        lines = []
        lines.append("=" * 70)
        lines.append(f"Execution Status: {'SUCCESS' if result.success else 'FAILED'}")
        lines.append("-" * 70)

        if result.success:
            lines.append(f"Result Value: {result.value}")
        else:
            lines.append(f"Error: {result.error}")

        lines.append("-" * 70)
        lines.append(f"Transpile Time: {result.transpile_time * 1000:.2f} ms")
        lines.append(f"Execution Time: {result.execution_time * 1000:.2f} ms")
        lines.append(f"Total Time:     {total_time * 1000:.2f} ms")
        lines.append("=" * 70)
        lines.append("")

        # Insert results (newest at top)
        self.results_text.insert("1.0", "\n".join(lines) + "\n")

        # Update status
        status_msg = "Success" if result.success else "Failed"
        self.status_var.set(f"{status_msg} ({total_time * 1000:.1f} ms)")

        # Re-enable execute button
        self.execute_btn.config(state=tk.NORMAL)

    def _display_error(self, error_message: str):
        """Display error in GUI (runs in main thread)."""
        lines = []
        lines.append("=" * 70)
        lines.append("UNEXPECTED ERROR")
        lines.append("-" * 70)
        lines.append(error_message)
        lines.append("=" * 70)
        lines.append("")

        self.results_text.insert("1.0", "\n".join(lines) + "\n")
        self.status_var.set("Error occurred")
        self.execute_btn.config(state=tk.NORMAL)

    def clear_output(self):
        """Clear results output."""
        self.results_text.delete("1.0", tk.END)
        self.status_var.set("Output cleared")

    # Example ML programs
    def example_simple_math(self):
        """Load simple math example."""
        code = """// Simple arithmetic operations
a = 10;
b = 20;
sum = a + b;
product = a * b;
difference = b - a;
quotient = b / a;

result = {
    sum: sum,
    product: product,
    difference: difference,
    quotient: quotient
};
"""
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert("1.0", code)

    def example_fibonacci(self):
        """Load Fibonacci example."""
        code = """// Calculate Fibonacci sequence
function fibonacci(n) {
    if (n <= 1) {
        return n;
    }

    a = 0;
    b = 1;
    i = 2;

    while (i <= n) {
        temp = a + b;
        a = b;
        b = temp;
        i = i + 1;
    }

    return b;
}

// Calculate first 10 Fibonacci numbers
sequence = [];
i = 0;
while (i < 10) {
    sequence = sequence + [fibonacci(i)];
    i = i + 1;
}

result = sequence;
"""
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert("1.0", code)

    def example_array(self):
        """Load array processing example."""
        code = """// Array processing - sum of squares of even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

sum_of_squares = 0;
for (n in numbers) {
    // Check if even (remainder is 0)
    remainder = n - (n / 2) * 2;
    if (remainder == 0) {
        square = n * n;
        sum_of_squares = sum_of_squares + square;
    }
}

result = sum_of_squares;  // 2^2 + 4^2 + 6^2 + 8^2 + 10^2 = 220
"""
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert("1.0", code)

    def example_factorial(self):
        """Load factorial example."""
        code = """// Calculate factorial using recursion
function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// Calculate factorials from 1 to 10
factorials = {};
i = 1;
while (i <= 10) {
    fact = factorial(i);
    factorials["f" + str(i)] = fact;
    i = i + 1;
}

result = factorials;
"""
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert("1.0", code)

    def on_closing(self):
        """Cleanup on window close."""
        # Shutdown executor
        self.executor.shutdown(wait=False)

        # Stop async event loop
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

        # Close window
        self.root.destroy()


def main():
    """Main entry point."""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  Tkinter ML Integration Example                           ║
    ║                                                            ║
    ║  Non-blocking ML code execution in Tkinter GUI            ║
    ║  - Edit ML code in the editor                             ║
    ║  - Click "Execute ML Code" to run                         ║
    ║  - UI remains responsive during execution                 ║
    ║  - Try the example programs!                              ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    root = tk.Tk()
    app = AsyncMLApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
