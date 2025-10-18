"""
PySide6 GUI Calculator with ML Backend
Demonstrates ML functions as GUI callbacks with async execution
"""

import sys
from pathlib import Path

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QGroupBox,
    QMessageBox,
)

# Add mlpy to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.mlpy.ml.transpiler import MLTranspiler


class MLWorkerThread(QThread):
    """Worker thread for async ML execution to avoid blocking GUI"""

    result_ready = Signal(object)
    error_occurred = Signal(str)

    def __init__(self, ml_function, *args):
        super().__init__()
        self.ml_function = ml_function
        self.args = args

    def run(self):
        """Execute ML function in background thread"""
        try:
            result = self.ml_function(*self.args)
            self.result_ready.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))


class BasicCalculatorTab(QWidget):
    """Basic calculator demonstrating simple ML callbacks"""

    def __init__(self, ml_functions):
        super().__init__()
        self.ml_functions = ml_functions
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input fields
        input_group = QGroupBox("Inputs")
        input_layout = QVBoxLayout()

        self.num1_input = QLineEdit()
        self.num1_input.setPlaceholderText("Enter first number")
        input_layout.addWidget(QLabel("Number 1:"))
        input_layout.addWidget(self.num1_input)

        self.num2_input = QLineEdit()
        self.num2_input.setPlaceholderText("Enter second number")
        input_layout.addWidget(QLabel("Number 2:"))
        input_layout.addWidget(self.num2_input)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Operation buttons
        button_layout = QHBoxLayout()
        operations = [
            ("Add", "add"),
            ("Subtract", "subtract"),
            ("Multiply", "multiply"),
            ("Divide", "divide"),
        ]

        for label, op in operations:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, o=op: self.calculate(o))
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)

        # Result display
        self.result_label = QLabel("Result: -")
        self.result_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate(self, operation):
        """Execute ML calculation"""
        try:
            # Get inputs
            num1 = float(self.num1_input.text())
            num2 = float(self.num2_input.text())

            # Get ML function
            ml_func = self.ml_functions.get(operation)
            if not ml_func:
                self.result_label.setText(f"Error: Unknown operation '{operation}'")
                return

            # Execute ML function (synchronous for simple operations)
            result = ml_func(num1, num2)

            # Display result
            if result is None:
                self.result_label.setText("Result: Error (Division by zero)")
                self.result_label.setStyleSheet("color: red; font-size: 18px;")
            else:
                self.result_label.setText(f"Result: {result}")
                self.result_label.setStyleSheet("color: green; font-size: 18px; font-weight: bold;")

        except ValueError:
            self.result_label.setText("Error: Invalid number format")
            self.result_label.setStyleSheet("color: red; font-size: 18px;")
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
            self.result_label.setStyleSheet("color: red; font-size: 18px;")


class CompoundInterestTab(QWidget):
    """Compound interest calculator with async execution"""

    def __init__(self, ml_functions):
        super().__init__()
        self.ml_functions = ml_functions
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input group
        input_group = QGroupBox("Investment Details")
        input_layout = QVBoxLayout()

        self.principal_input = QLineEdit()
        self.principal_input.setPlaceholderText("e.g., 10000")
        input_layout.addWidget(QLabel("Principal Amount:"))
        input_layout.addWidget(self.principal_input)

        self.rate_input = QLineEdit()
        self.rate_input.setPlaceholderText("e.g., 5.5 (for 5.5%)")
        input_layout.addWidget(QLabel("Annual Interest Rate (%):"))
        input_layout.addWidget(self.rate_input)

        self.years_input = QLineEdit()
        self.years_input.setPlaceholderText("e.g., 10")
        input_layout.addWidget(QLabel("Number of Years:"))
        input_layout.addWidget(self.years_input)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Calculate button
        self.calc_button = QPushButton("Calculate Compound Interest")
        self.calc_button.clicked.connect(self.calculate)
        layout.addWidget(self.calc_button)

        # Result display
        result_group = QGroupBox("Results")
        result_layout = QVBoxLayout()

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMaximumHeight(150)
        result_layout.addWidget(self.result_text)

        result_group.setLayout(result_layout)
        layout.addWidget(result_group)

        self.setLayout(layout)

    def calculate(self):
        """Calculate compound interest using ML function"""
        try:
            # Get inputs
            principal = float(self.principal_input.text())
            rate = float(self.rate_input.text())
            years = int(self.years_input.text())

            # Disable button during calculation
            self.calc_button.setEnabled(False)
            self.result_text.setText("Calculating...")

            # Get ML function
            ml_func = self.ml_functions.get("calculate_compound_interest")

            # Execute in background thread (for demonstration of async pattern)
            self.worker = MLWorkerThread(ml_func, principal, rate, years)
            self.worker.result_ready.connect(self.on_result)
            self.worker.error_occurred.connect(self.on_error)
            self.worker.finished.connect(self.on_finished)
            self.worker.start()

        except ValueError:
            self.result_text.setText("Error: Invalid input format")
            self.calc_button.setEnabled(True)
        except Exception as e:
            self.result_text.setText(f"Error: {str(e)}")
            self.calc_button.setEnabled(True)

    def on_result(self, result):
        """Handle calculation result"""
        if result:
            output = f"""
Compound Interest Calculation Results:
=====================================
Principal Amount: ${result['principal']:,.2f}
Interest Rate: {result['rate']}%
Investment Period: {result['years']} years

Final Amount: ${result['amount']:,.2f}
Interest Earned: ${result['interest']:,.2f}
Total Return: {(result['interest'] / result['principal'] * 100):.2f}%
"""
            self.result_text.setText(output)
        else:
            self.result_text.setText("Error: Calculation returned null")

    def on_error(self, error_msg):
        """Handle calculation error"""
        self.result_text.setText(f"Error: {error_msg}")

    def on_finished(self):
        """Re-enable button when calculation completes"""
        self.calc_button.setEnabled(True)


class FibonacciTab(QWidget):
    """Fibonacci calculator demonstrating long-running calculations"""

    def __init__(self, ml_functions):
        super().__init__()
        self.ml_functions = ml_functions
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Calculate Fibonacci number:"))
        self.n_input = QLineEdit()
        self.n_input.setPlaceholderText("e.g., 30")
        input_layout.addWidget(self.n_input)
        layout.addLayout(input_layout)

        # Calculate button
        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate)
        layout.addWidget(self.calc_button)

        # Result
        self.result_label = QLabel("Result: -")
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.result_label)

        # Status
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-style: italic; color: gray;")
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.setLayout(layout)

    def calculate(self):
        """Calculate Fibonacci number"""
        try:
            n = int(self.n_input.text())

            if n < 0:
                self.result_label.setText("Error: Please enter a non-negative number")
                return

            # Disable button
            self.calc_button.setEnabled(False)
            self.status_label.setText("Calculating... (GUI remains responsive)")

            # Get ML function
            ml_func = self.ml_functions.get("fibonacci")

            # Execute in background
            self.worker = MLWorkerThread(ml_func, n)
            self.worker.result_ready.connect(self.on_result)
            self.worker.error_occurred.connect(self.on_error)
            self.worker.finished.connect(self.on_finished)
            self.worker.start()

        except ValueError:
            self.result_label.setText("Error: Invalid number format")
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")

    def on_result(self, result):
        """Display result"""
        self.result_label.setText(f"Fibonacci Result: {result}")
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")
        self.status_label.setText("✓ Calculation complete")

    def on_error(self, error_msg):
        """Display error"""
        self.result_label.setText(f"Error: {error_msg}")
        self.result_label.setStyleSheet("font-size: 16px; color: red;")
        self.status_label.setText("")

    def on_finished(self):
        """Re-enable button"""
        self.calc_button.setEnabled(True)


class CalculatorMainWindow(QMainWindow):
    """Main window with tabbed interface"""

    def __init__(self):
        super().__init__()
        self.ml_functions = {}
        self.init_ml()
        self.init_ui()

    def init_ml(self):
        """Initialize ML transpiler and load functions"""
        try:
            # Get ML file path
            ml_file = Path(__file__).parent / "ml_calculator.ml"

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
                "add",
                "subtract",
                "multiply",
                "divide",
                "calculate_compound_interest",
                "fibonacci",
                "calculate_statistics",
            ]

            for func_name in function_names:
                if func_name in namespace:
                    self.ml_functions[func_name] = namespace[func_name]

        except Exception as e:
            QMessageBox.critical(
                self, "ML Initialization Error", f"Failed to load ML functions:\n{str(e)}"
            )
            sys.exit(1)

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("ML Calculator - PySide6 Integration Demo")
        self.setMinimumSize(600, 500)

        # Central widget with tabs
        tabs = QTabWidget()

        # Create tabs
        tabs.addTab(BasicCalculatorTab(self.ml_functions), "Basic Calculator")
        tabs.addTab(CompoundInterestTab(self.ml_functions), "Compound Interest")
        tabs.addTab(FibonacciTab(self.ml_functions), "Fibonacci")

        self.setCentralWidget(tabs)

        # Status bar
        self.statusBar().showMessage("Ready - ML functions loaded successfully")


def main():
    """Run the application"""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    # Create and show main window
    window = CalculatorMainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
