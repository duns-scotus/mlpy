=======================================
Standard Library Module Development
=======================================

This comprehensive guide covers creating new standard library modules for mlpy, from basic modules to advanced implementations with object access, Python bridges, and capability-based security.

.. contents:: Table of Contents
   :local:
   :depth: 3

Architecture Overview
=====================

The mlpy standard library uses a sophisticated architecture with multiple components working together:

.. code-block:: text

    ML Program
    └── import mymodule
        └── Registry System (registry.py)
            ├── Loads ML interface (mymodule.ml)
            ├── Registers Python bridge (mymodule_bridge.py)
            ├── Validates capabilities
            └── Enables object access via SafeAttributeRegistry

Components Structure
--------------------

Each standard library module consists of:

1. **ML Interface File** (`*.ml`) - ML language API definition
2. **Python Bridge** (`*_bridge.py`) - High-performance Python implementation
3. **Registry Integration** - Automatic or manual registration
4. **Object Access Control** - Safe attribute/method access (optional)
5. **Capability Requirements** - Security permissions

Registry System Deep Dive
==========================

The registry system (`src/mlpy/stdlib/registry.py`) provides centralized module management:

Core Classes
------------

.. code-block:: python

    @dataclass
    class StandardLibraryModule:
        """Module registration information."""
        name: str                        # Module identifier
        module_path: str                 # Import path
        source_file: str                 # ML source file
        capabilities_required: list[str] # Security requirements
        description: str                 # Module description
        version: str = "1.0.0"           # Module version
        python_bridge_modules: list[str] # Python dependencies

    @dataclass
    class BridgeFunction:
        """Python bridge function configuration."""
        ml_name: str                     # ML function name
        python_module: str               # Python module path
        python_function: str             # Python function name
        capabilities_required: list[str] # Function-level capabilities
        parameter_types: list[str]       # Type annotations
        return_type: str                 # Return type
        validation_function: Callable    # Input validation

Registration Methods
-------------------

**Automatic Discovery:**

.. code-block:: python

    # Place ML files in src/mlpy/stdlib/
    # Registry auto-discovers modules with metadata comments:

    // @description: Mathematical operations with security
    // @capability: read:math_constants
    // @capability: execute:calculations
    // @version: 1.0.0

**Manual Registration:**

.. code-block:: python

    def _register_core_modules(registry: StandardLibraryRegistry):
        registry.register_module(
            name="mymodule",
            source_file="mymodule.ml",
            capabilities_required=["read:data", "execute:operations"],
            description="Custom module functionality",
            python_bridge_modules=["mlpy.stdlib.mymodule_bridge"]
        )

Creating a Standard Library Module
===================================

Let's create a comprehensive example: a data analysis module with object access.

Step 1: Design the ML Interface
-------------------------------

Create `src/mlpy/stdlib/dataanalysis.ml`:

.. code-block:: ml

    // @description: Data analysis utilities with statistical functions
    // @capability: read:data_files
    // @capability: execute:calculations
    // @capability: write:analysis_results
    // @version: 1.0.0

    /**
     * ML Data Analysis Standard Library
     * Provides statistical analysis with object-oriented data structures
     */

    capability DataAnalysis {
        allow read "data_files:*";
        allow execute "calculations:*";
        allow write "analysis_results:*";
    }

    // Core statistical functions
    function mean(data: array): number {
        require capability execute:calculations;
        return __bridge_call("dataanalysis", "calculate_mean", [data]);
    }

    function median(data: array): number {
        require capability execute:calculations;
        return __bridge_call("dataanalysis", "calculate_median", [data]);
    }

    function standardDeviation(data: array): number {
        require capability execute:calculations;
        return __bridge_call("dataanalysis", "calculate_std", [data]);
    }

    // Advanced: Create data frame objects with methods
    function createDataFrame(data: array, columns: array): object {
        require capability execute:calculations;
        return __bridge_call("dataanalysis", "create_dataframe", [data, columns]);
    }

    // Statistical analysis function that returns object with methods
    function analyze(data: array): object {
        require capability execute:calculations;
        return __bridge_call("dataanalysis", "create_analysis", [data]);
    }

    // File operations with capability requirements
    function loadCSV(filename: string): object {
        require capability read:data_files;
        return __bridge_call("dataanalysis", "load_csv", [filename]);
    }

    function saveResults(analysis: object, filename: string): boolean {
        require capability write:analysis_results;
        return __bridge_call("dataanalysis", "save_analysis", [analysis, filename]);
    }

Step 2: Implement Python Bridge with Objects
--------------------------------------------

Create `src/mlpy/stdlib/dataanalysis_bridge.py`:

.. code-block:: python

    """Data analysis module with object-oriented interfaces."""

    import statistics
    import csv
    from typing import Any, List, Dict, Union
    from pathlib import Path

    from mlpy.runtime.capabilities.manager import require_capability
    from mlpy.ml.errors.exceptions import MLRuntimeError
    from mlpy.stdlib.runtime_helpers import safe_attr_access


    class DataFrame:
        """ML-compatible DataFrame with safe attribute access."""

        def __init__(self, data: List[List[Any]], columns: List[str]):
            self._data = data
            self._columns = columns
            self._validate_structure()

        def _validate_structure(self):
            """Validate data structure integrity."""
            if not self._data:
                return

            expected_cols = len(self._columns)
            for i, row in enumerate(self._data):
                if len(row) != expected_cols:
                    raise MLRuntimeError(f"Row {i} has {len(row)} values, expected {expected_cols}")

        # Properties accessible from ML code
        @property
        def columns(self) -> List[str]:
            """Get column names."""
            return self._columns.copy()

        @property
        def rows(self) -> int:
            """Get number of rows."""
            return len(self._data)

        @property
        def shape(self) -> Dict[str, int]:
            """Get dataframe shape."""
            return {"rows": len(self._data), "columns": len(self._columns)}

        # Methods accessible from ML code
        def head(self, n: int = 5) -> List[List[Any]]:
            """Get first n rows."""
            return self._data[:n]

        def tail(self, n: int = 5) -> List[List[Any]]:
            """Get last n rows."""
            return self._data[-n:] if n <= len(self._data) else self._data

        def column(self, name: str) -> List[Any]:
            """Get column data by name."""
            try:
                col_index = self._columns.index(name)
                return [row[col_index] for row in self._data]
            except ValueError:
                raise MLRuntimeError(f"Column '{name}' not found")

        def filter(self, column_name: str, condition: str, value: Any) -> 'DataFrame':
            """Filter rows based on condition."""
            col_data = self.column(column_name)
            col_index = self._columns.index(column_name)

            filtered_rows = []
            for i, row in enumerate(self._data):
                cell_value = row[col_index]

                if condition == "equals" and cell_value == value:
                    filtered_rows.append(row)
                elif condition == "greater" and isinstance(cell_value, (int, float)) and cell_value > value:
                    filtered_rows.append(row)
                elif condition == "less" and isinstance(cell_value, (int, float)) and cell_value < value:
                    filtered_rows.append(row)
                elif condition == "contains" and isinstance(cell_value, str) and value in cell_value:
                    filtered_rows.append(row)

            return DataFrame(filtered_rows, self._columns)

        def summarize(self) -> Dict[str, Any]:
            """Generate summary statistics."""
            summary = {"columns": len(self._columns), "rows": len(self._data)}

            for col_name in self._columns:
                col_data = self.column(col_name)
                numeric_data = [x for x in col_data if isinstance(x, (int, float))]

                if numeric_data:
                    summary[f"{col_name}_mean"] = statistics.mean(numeric_data)
                    summary[f"{col_name}_median"] = statistics.median(numeric_data)
                    if len(numeric_data) > 1:
                        summary[f"{col_name}_std"] = statistics.stdev(numeric_data)

            return summary


    class StatisticalAnalysis:
        """Analysis result object with computed statistics."""

        def __init__(self, data: List[Union[int, float]]):
            self._data = data
            self._computed_stats = {}
            self._compute_basic_stats()

        def _compute_basic_stats(self):
            """Pre-compute basic statistics."""
            if not self._data:
                return

            numeric_data = [x for x in self._data if isinstance(x, (int, float))]
            if not numeric_data:
                return

            self._computed_stats = {
                "count": len(numeric_data),
                "mean": statistics.mean(numeric_data),
                "median": statistics.median(numeric_data),
                "min": min(numeric_data),
                "max": max(numeric_data),
            }

            if len(numeric_data) > 1:
                self._computed_stats["std"] = statistics.stdev(numeric_data)
                self._computed_stats["variance"] = statistics.variance(numeric_data)

        # Properties accessible from ML
        @property
        def mean(self) -> float:
            return self._computed_stats.get("mean", 0.0)

        @property
        def median(self) -> float:
            return self._computed_stats.get("median", 0.0)

        @property
        def std(self) -> float:
            return self._computed_stats.get("std", 0.0)

        @property
        def count(self) -> int:
            return self._computed_stats.get("count", 0)

        # Methods accessible from ML
        def summary(self) -> Dict[str, Any]:
            """Get complete statistical summary."""
            return self._computed_stats.copy()

        def percentile(self, p: float) -> float:
            """Calculate percentile."""
            if not 0 <= p <= 100:
                raise MLRuntimeError("Percentile must be between 0 and 100")

            numeric_data = [x for x in self._data if isinstance(x, (int, float))]
            if not numeric_data:
                return 0.0

            return statistics.quantiles(numeric_data, n=100)[int(p)-1] if p > 0 else min(numeric_data)

        def zscore(self, value: float) -> float:
            """Calculate z-score for a value."""
            if self.std == 0:
                return 0.0
            return (value - self.mean) / self.std


    # Bridge function implementations
    class DataAnalysisModule:
        """Main module with bridge functions."""

        @staticmethod
        @require_capability("execute:calculations")
        def calculate_mean(data: List[Union[int, float]]) -> float:
            """Calculate arithmetic mean."""
            numeric_data = [x for x in data if isinstance(x, (int, float))]
            if not numeric_data:
                raise MLRuntimeError("No numeric data provided")
            return statistics.mean(numeric_data)

        @staticmethod
        @require_capability("execute:calculations")
        def calculate_median(data: List[Union[int, float]]) -> float:
            """Calculate median value."""
            numeric_data = [x for x in data if isinstance(x, (int, float))]
            if not numeric_data:
                raise MLRuntimeError("No numeric data provided")
            return statistics.median(numeric_data)

        @staticmethod
        @require_capability("execute:calculations")
        def calculate_std(data: List[Union[int, float]]) -> float:
            """Calculate standard deviation."""
            numeric_data = [x for x in data if isinstance(x, (int, float))]
            if len(numeric_data) < 2:
                raise MLRuntimeError("Need at least 2 numeric values for standard deviation")
            return statistics.stdev(numeric_data)

        @staticmethod
        @require_capability("execute:calculations")
        def create_dataframe(data: List[List[Any]], columns: List[str]) -> DataFrame:
            """Create DataFrame object with methods."""
            return DataFrame(data, columns)

        @staticmethod
        @require_capability("execute:calculations")
        def create_analysis(data: List[Union[int, float]]) -> StatisticalAnalysis:
            """Create analysis object with statistical methods."""
            return StatisticalAnalysis(data)

        @staticmethod
        @require_capability("read:data_files")
        def load_csv(filename: str) -> DataFrame:
            """Load CSV file into DataFrame."""
            try:
                filepath = Path(filename)
                if not filepath.exists():
                    raise MLRuntimeError(f"File {filename} does not exist")

                with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                    # Detect delimiter
                    sample = csvfile.read(1024)
                    csvfile.seek(0)
                    sniffer = csv.Sniffer()
                    delimiter = sniffer.sniff(sample).delimiter

                    reader = csv.reader(csvfile, delimiter=delimiter)
                    rows = list(reader)

                    if not rows:
                        raise MLRuntimeError("CSV file is empty")

                    # First row as headers
                    columns = rows[0]
                    data = rows[1:]

                    # Convert numeric values
                    processed_data = []
                    for row in data:
                        processed_row = []
                        for cell in row:
                            try:
                                # Try to convert to number
                                if '.' in cell:
                                    processed_row.append(float(cell))
                                else:
                                    processed_row.append(int(cell))
                            except ValueError:
                                # Keep as string
                                processed_row.append(cell)
                        processed_data.append(processed_row)

                    return DataFrame(processed_data, columns)

            except Exception as e:
                raise MLRuntimeError(f"Failed to load CSV: {e}")

        @staticmethod
        @require_capability("write:analysis_results")
        def save_analysis(analysis: StatisticalAnalysis, filename: str) -> bool:
            """Save analysis results to file."""
            try:
                summary = analysis.summary()

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Statistical Analysis Results\\n")
                    f.write("=" * 30 + "\\n\\n")

                    for key, value in summary.items():
                        f.write(f"{key}: {value}\\n")

                return True

            except Exception as e:
                raise MLRuntimeError(f"Failed to save analysis: {e}")


    # Validation functions for bridge calls
    def validate_numeric_array(args: List[Any]) -> None:
        """Validate numeric array input."""
        if len(args) != 1:
            raise ValueError("Function requires exactly 1 argument")

        data = args[0]
        if not isinstance(data, list):
            raise ValueError("Argument must be an array")

        if not data:
            raise ValueError("Array cannot be empty")

        numeric_count = sum(1 for x in data if isinstance(x, (int, float)))
        if numeric_count == 0:
            raise ValueError("Array must contain at least one numeric value")


    def validate_dataframe_creation(args: List[Any]) -> None:
        """Validate DataFrame creation arguments."""
        if len(args) != 2:
            raise ValueError("createDataFrame requires exactly 2 arguments")

        data, columns = args

        if not isinstance(data, list) or not isinstance(columns, list):
            raise ValueError("Both arguments must be arrays")

        if not columns:
            raise ValueError("Columns array cannot be empty")

        if not all(isinstance(col, str) for col in columns):
            raise ValueError("All column names must be strings")


    def validate_csv_filename(args: List[Any]) -> None:
        """Validate CSV filename."""
        if len(args) != 1:
            raise ValueError("loadCSV requires exactly 1 argument")

        filename = args[0]
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string")

        if not filename.endswith('.csv'):
            raise ValueError("File must have .csv extension")


    # Export bridge functions and validators
    DATAANALYSIS_FUNCTIONS = {
        'calculate_mean': DataAnalysisModule.calculate_mean,
        'calculate_median': DataAnalysisModule.calculate_median,
        'calculate_std': DataAnalysisModule.calculate_std,
        'create_dataframe': DataAnalysisModule.create_dataframe,
        'create_analysis': DataAnalysisModule.create_analysis,
        'load_csv': DataAnalysisModule.load_csv,
        'save_analysis': DataAnalysisModule.save_analysis,
    }

    DATAANALYSIS_VALIDATORS = {
        'calculate_mean': validate_numeric_array,
        'calculate_median': validate_numeric_array,
        'calculate_std': validate_numeric_array,
        'create_dataframe': validate_dataframe_creation,
        'create_analysis': validate_numeric_array,
        'load_csv': validate_csv_filename,
    }

Step 3: Register Safe Object Access
-----------------------------------

To enable object method/attribute access, register safe attributes in the bridge module:

.. code-block:: python

    # Add to dataanalysis_bridge.py
    from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry, SafeAttribute, AttributeAccessType

    def register_safe_attributes():
        """Register safe attributes for our custom classes."""
        registry = get_safe_registry()

        # DataFrame safe attributes
        dataframe_attributes = {
            "columns": SafeAttribute("columns", AttributeAccessType.PROPERTY, [], "Column names"),
            "rows": SafeAttribute("rows", AttributeAccessType.PROPERTY, [], "Number of rows"),
            "shape": SafeAttribute("shape", AttributeAccessType.PROPERTY, [], "DataFrame shape"),
            "head": SafeAttribute("head", AttributeAccessType.METHOD, [], "Get first n rows"),
            "tail": SafeAttribute("tail", AttributeAccessType.METHOD, [], "Get last n rows"),
            "column": SafeAttribute("column", AttributeAccessType.METHOD, [], "Get column data"),
            "filter": SafeAttribute("filter", AttributeAccessType.METHOD, [], "Filter rows"),
            "summarize": SafeAttribute("summarize", AttributeAccessType.METHOD, [], "Generate summary"),
        }
        registry.register_builtin_type(DataFrame, dataframe_attributes)

        # StatisticalAnalysis safe attributes
        analysis_attributes = {
            "mean": SafeAttribute("mean", AttributeAccessType.PROPERTY, [], "Mean value"),
            "median": SafeAttribute("median", AttributeAccessType.PROPERTY, [], "Median value"),
            "std": SafeAttribute("std", AttributeAccessType.PROPERTY, [], "Standard deviation"),
            "count": SafeAttribute("count", AttributeAccessType.PROPERTY, [], "Count of values"),
            "summary": SafeAttribute("summary", AttributeAccessType.METHOD, [], "Full summary"),
            "percentile": SafeAttribute("percentile", AttributeAccessType.METHOD, [], "Calculate percentile"),
            "zscore": SafeAttribute("zscore", AttributeAccessType.METHOD, [], "Calculate z-score"),
        }
        registry.register_builtin_type(StatisticalAnalysis, analysis_attributes)

    # Register attributes when module is imported
    register_safe_attributes()

Step 4: Registry Integration
----------------------------

Update `src/mlpy/stdlib/registry.py` to register the module:

.. code-block:: python

    def _register_core_modules(registry: StandardLibraryRegistry) -> None:
        """Register core standard library modules."""

        # ... existing modules ...

        # Data Analysis module
        registry.register_module(
            name="dataanalysis",
            source_file="dataanalysis.ml",
            capabilities_required=[
                "read:data_files",
                "execute:calculations",
                "write:analysis_results"
            ],
            description="Data analysis utilities with statistical functions",
            version="1.0.0",
            python_bridge_modules=["mlpy.stdlib.dataanalysis_bridge"]
        )

        # Register bridge functions
        dataanalysis_functions = [
            ("calculate_mean", "mlpy.stdlib.dataanalysis_bridge", "DataAnalysisModule.calculate_mean", ["execute:calculations"]),
            ("calculate_median", "mlpy.stdlib.dataanalysis_bridge", "DataAnalysisModule.calculate_median", ["execute:calculations"]),
            ("calculate_std", "mlpy.stdlib.dataanalysis_bridge", "DataAnalysisModule.calculate_std", ["execute:calculations"]),
            ("create_dataframe", "mlpy.stdlib.dataanalysis_bridge", "DataAnalysisModule.create_dataframe", ["execute:calculations"]),
            ("create_analysis", "mlpy.stdlib.dataanalysis_bridge", "DataAnalysisModule.create_analysis", ["execute:calculations"]),
            ("load_csv", "mlpy.stdlib.dataanalysis_bridge", "DataAnalysisModule.load_csv", ["read:data_files"]),
            ("save_analysis", "mlpy.stdlib.dataanalysis_bridge", "DataAnalysisModule.save_analysis", ["write:analysis_results"]),
        ]

        from mlpy.stdlib.dataanalysis_bridge import DATAANALYSIS_VALIDATORS

        for ml_name, py_module, py_func, caps in dataanalysis_functions:
            registry.register_bridge_function(
                module_name="dataanalysis",
                ml_name=ml_name,
                python_module=py_module,
                python_function=py_func,
                capabilities_required=caps,
                validation_function=DATAANALYSIS_VALIDATORS.get(ml_name)
            )

Step 5: Usage Examples
----------------------

Create `docs/examples/dataanalysis-examples.ml`:

.. code-block:: ml

    import dataanalysis;

    // Example 1: Basic statistical analysis
    function analyzeTestScores() {
        scores = [85, 92, 78, 96, 88, 79, 85, 90, 87, 93];

        // Create analysis object with methods
        analysis = dataanalysis.analyze(scores);

        // Access properties
        print("Mean: " + analysis.mean);
        print("Median: " + analysis.median);
        print("Standard Deviation: " + analysis.std);
        print("Count: " + analysis.count);

        // Call methods
        summary = analysis.summary();
        q75 = analysis.percentile(75);

        return {
            "summary": summary,
            "q75": q75,
            "analysis": analysis
        };
    }

    // Example 2: DataFrame operations with object methods
    function processCustomerData() {
        // Sample customer data
        data = [
            ["Alice", 25, 50000, "Engineering"],
            ["Bob", 30, 60000, "Marketing"],
            ["Charlie", 28, 55000, "Engineering"],
            ["Diana", 35, 70000, "Sales"],
            ["Eve", 27, 52000, "Engineering"]
        ];

        columns = ["name", "age", "salary", "department"];

        // Create DataFrame object
        df = dataanalysis.createDataFrame(data, columns);

        // Access properties using object syntax
        print("DataFrame shape: " + df.rows + " x " + df.columns.length);
        print("Columns: " + df.columns);

        // Use methods
        first_three = df.head(3);
        engineering_employees = df.filter("department", "equals", "Engineering");
        summary = df.summarize();

        // Get specific column data
        salaries = df.column("salary");
        salary_analysis = dataanalysis.analyze(salaries);

        return {
            "total_employees": df.rows,
            "engineering_count": engineering_employees.rows,
            "avg_salary": salary_analysis.mean,
            "salary_summary": summary
        };
    }

    // Example 3: CSV file processing
    function processCSVData(filename) {
        try {
            // Load CSV file into DataFrame
            data = dataanalysis.loadCSV(filename);

            print("Loaded " + data.rows + " rows with columns: " + data.columns);

            // Process numeric columns
            results = {};
            for (i = 0; i < data.columns.length; i++) {
                column_name = data.columns[i];
                column_data = data.column(column_name);

                // Check if column contains numbers
                numeric_values = [];
                for (j = 0; j < column_data.length; j++) {
                    if (typeof(column_data[j]) == "number") {
                        numeric_values.append(column_data[j]);
                    }
                }

                if (numeric_values.length > 0) {
                    analysis = dataanalysis.analyze(numeric_values);
                    results[column_name + "_mean"] = analysis.mean;
                    results[column_name + "_std"] = analysis.std;
                }
            }

            return results;

        } catch (error) {
            print("Error processing CSV: " + error);
            return null;
        }
    }

Object Access Patterns
=======================

The mlpy standard library supports safe object-oriented programming through the SafeAttributeRegistry system.

Safe Attribute Access
---------------------

Objects returned from standard library functions can have their attributes and methods accessed safely:

.. code-block:: ml

    import dataanalysis;

    // Object with properties and methods
    analysis = dataanalysis.analyze([1, 2, 3, 4, 5]);

    // Property access (generates: analysis.mean)
    mean_value = analysis.mean;

    // Method calls (generates: analysis.percentile(50))
    median_via_percentile = analysis.percentile(50);

    // Complex method calls
    summary = analysis.summary();

Transpilation to Python
-----------------------

ML object access transpiles to secure Python using runtime helpers:

.. code-block:: python

    # ML code: analysis.mean
    # Transpiles to:
    from mlpy.stdlib.runtime_helpers import safe_attr_access
    mean_value = safe_attr_access(analysis, "mean")

    # ML code: analysis.percentile(50)
    # Transpiles to:
    percentile_result = safe_attr_access(analysis, "percentile", 50)

Security Enforcement
-------------------

The SafeAttributeRegistry enforces security by:

1. **Whitelist-based Access**: Only registered attributes/methods are accessible
2. **Type-based Validation**: Different rules for different object types
3. **Capability Requirements**: Some attributes may require additional capabilities
4. **Dangerous Pattern Blocking**: Prevents access to `__*__` attributes

.. code-block:: python

    # In your bridge module
    from mlpy.ml.codegen.safe_attribute_registry import get_safe_registry, SafeAttribute, AttributeAccessType

    def register_your_class_attributes():
        registry = get_safe_registry()

        # Define safe attributes for your class
        safe_attributes = {
            "safe_property": SafeAttribute("safe_property", AttributeAccessType.PROPERTY),
            "safe_method": SafeAttribute("safe_method", AttributeAccessType.METHOD),
            "dangerous_attr": SafeAttribute("dangerous_attr", AttributeAccessType.FORBIDDEN)
        }

        registry.register_builtin_type(YourClass, safe_attributes)

Built-in Type Support
---------------------

The registry already includes comprehensive support for Python built-ins:

- **str**: 28+ safe methods (upper, lower, split, replace, etc.)
- **list**: append, extend, remove, index, count, etc.
- **dict**: keys, values, items, get, etc.
- **int/float**: Basic numeric operations

Bridge Function Patterns
=========================

Advanced Bridge Implementation
------------------------------

.. code-block:: python

    class AdvancedModule:
        """Advanced bridge patterns for complex modules."""

        @staticmethod
        @require_capability("module:advanced:computation")
        def complex_function(data: Any, options: Dict[str, Any] = None) -> Any:
            """Example of complex bridge function with options."""

            # 1. Parameter validation
            if not isinstance(data, (list, dict)):
                raise MLRuntimeError("Data must be array or object")

            options = options or {}

            # 2. Capability-based feature gating
            if options.get("use_advanced_features"):
                capability_manager = get_capability_manager()
                if not capability_manager.has_capability("module:advanced:premium"):
                    raise MLRuntimeError("Advanced features require premium capability")

            # 3. Complex processing with error handling
            try:
                result = perform_complex_operation(data, options)

                # 4. Return object with methods if needed
                if options.get("return_analysis_object"):
                    return AnalysisResult(result)
                else:
                    return result

            except Exception as e:
                # 5. Convert to ML-friendly error
                raise MLRuntimeError(f"Complex operation failed: {e}")

Capability Integration Patterns
-------------------------------

.. code-block:: python

    # Method-level capabilities
    @require_capability("file:read:csv")
    def read_csv_file(filename: str) -> DataFrame:
        """Read CSV with file access capability."""
        pass

    # Dynamic capability checking
    def flexible_operation(data: Any, mode: str) -> Any:
        """Operation that requires different capabilities based on mode."""
        capability_manager = get_capability_manager()

        if mode == "safe":
            if not capability_manager.has_capability("operation:safe"):
                raise MLRuntimeError("Safe mode requires 'operation:safe' capability")
        elif mode == "advanced":
            required_caps = ["operation:advanced", "computation:intensive"]
            for cap in required_caps:
                if not capability_manager.has_capability(cap):
                    raise MLRuntimeError(f"Advanced mode requires '{cap}' capability")

        return process_with_mode(data, mode)

Testing Standard Library Modules
=================================

Comprehensive Test Structure
----------------------------

.. code-block:: python

    """Complete test suite for standard library modules."""

    import pytest
    from mlpy.ml.transpiler import transpile_ml_code, execute_ml_code_sandbox
    from mlpy.runtime.sandbox.config import SandboxConfig
    from mlpy.runtime.capabilities.manager import CapabilityContext


    class TestDataAnalysisModule:
        """Test data analysis module functionality."""

        def test_basic_statistical_functions(self):
            """Test basic statistical calculations."""
            ml_code = '''
            import dataanalysis;

            function testStats() {
                data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

                mean = dataanalysis.mean(data);
                median = dataanalysis.median(data);
                std = dataanalysis.standardDeviation(data);

                return {
                    "mean": mean,
                    "median": median,
                    "std": std
                };
            }
            '''

            capabilities = CapabilityContext()
            capabilities.grant("execute:calculations", "execute")

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            assert result.success
            stats = result.return_value
            assert abs(stats["mean"] - 5.5) < 0.001
            assert stats["median"] == 5.5
            assert abs(stats["std"] - 3.027) < 0.01

        def test_object_method_access(self):
            """Test object-oriented interface."""
            ml_code = '''
            import dataanalysis;

            function testObjectAccess() {
                data = [10, 20, 30, 40, 50];
                analysis = dataanalysis.analyze(data);

                // Test property access
                mean = analysis.mean;
                count = analysis.count;

                // Test method calls
                summary = analysis.summary();
                q90 = analysis.percentile(90);

                return {
                    "mean": mean,
                    "count": count,
                    "summary_mean": summary.mean,
                    "q90": q90
                };
            }
            '''

            capabilities = CapabilityContext()
            capabilities.grant("execute:calculations", "execute")

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            assert result.success
            obj_result = result.return_value
            assert obj_result["mean"] == 30.0
            assert obj_result["count"] == 5
            assert obj_result["summary_mean"] == 30.0
            assert obj_result["q90"] > 40  # 90th percentile should be > 40

        def test_dataframe_operations(self):
            """Test DataFrame object functionality."""
            ml_code = '''
            import dataanalysis;

            function testDataFrame() {
                data = [
                    ["Alice", 25, 50000],
                    ["Bob", 30, 60000],
                    ["Charlie", 28, 55000]
                ];
                columns = ["name", "age", "salary"];

                df = dataanalysis.createDataFrame(data, columns);

                // Test properties
                row_count = df.rows;
                col_names = df.columns;
                shape = df.shape;

                // Test methods
                first_two = df.head(2);
                ages = df.column("age");
                high_earners = df.filter("salary", "greater", 55000);
                summary = df.summarize();

                return {
                    "rows": row_count,
                    "columns": col_names,
                    "shape": shape,
                    "first_two_count": first_two.length,
                    "ages": ages,
                    "high_earners_count": high_earners.rows,
                    "has_summary": summary != null
                };
            }
            '''

            capabilities = CapabilityContext()
            capabilities.grant("execute:calculations", "execute")

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            assert result.success
            df_result = result.return_value
            assert df_result["rows"] == 3
            assert df_result["columns"] == ["name", "age", "salary"]
            assert df_result["shape"]["rows"] == 3
            assert df_result["shape"]["columns"] == 3
            assert df_result["first_two_count"] == 2
            assert df_result["ages"] == [25, 30, 28]
            assert df_result["high_earners_count"] == 1  # Only Bob
            assert df_result["has_summary"] is True

        def test_capability_enforcement(self):
            """Test that capabilities are properly enforced."""
            ml_code = '''
            import dataanalysis;

            function testUnauthorized() {
                return dataanalysis.loadCSV("test.csv");  // Should fail
            }
            '''

            # No file read capability granted
            capabilities = CapabilityContext()
            capabilities.grant("execute:calculations", "execute")

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            assert not result.success
            assert "capability" in result.error.lower()

        def test_error_handling(self):
            """Test error handling and validation."""
            ml_code = '''
            import dataanalysis;

            function testErrorHandling() {
                try {
                    // This should fail - empty array
                    result = dataanalysis.mean([]);
                    return "should_not_reach";
                } catch (error) {
                    return "error_caught";
                }
            }
            '''

            capabilities = CapabilityContext()
            capabilities.grant("execute:calculations", "execute")

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            assert result.success
            assert result.return_value == "error_caught"

Performance Testing
-------------------

.. code-block:: python

    class TestDataAnalysisPerformance:
        """Performance tests for data analysis module."""

        def test_large_dataset_performance(self, benchmark):
            """Test performance with large datasets."""

            def setup():
                import random
                # Generate large dataset
                data = [random.randint(1, 1000) for _ in range(10000)]
                return {"data": data}

            def analysis_operation(params):
                ml_code = f'''
                import dataanalysis;

                function performAnalysis() {{
                    data = {params["data"]};
                    analysis = dataanalysis.analyze(data);
                    return analysis.summary();
                }}
                '''

                capabilities = CapabilityContext()
                capabilities.grant("execute:calculations", "execute")

                result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)
                return result.return_value

            result = benchmark.pedantic(analysis_operation, setup=setup, rounds=5)
            assert result is not None
            assert "mean" in result

Security Testing
----------------

.. code-block:: python

    class TestDataAnalysisSecurity:
        """Security tests for data analysis module."""

        def test_object_access_security(self):
            """Test that dangerous object access is blocked."""
            ml_code = '''
            import dataanalysis;

            function testDangerousAccess() {
                analysis = dataanalysis.analyze([1, 2, 3]);

                // Try to access dangerous attributes
                return analysis.__class__.__name__;  // Should fail
            }
            '''

            capabilities = CapabilityContext()
            capabilities.grant("execute:calculations", "execute")

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            assert not result.success
            assert "security" in result.error.lower() or "attribute" in result.error.lower()

        def test_input_validation_security(self):
            """Test input validation prevents attacks."""
            ml_code = '''
            import dataanalysis;

            function testMaliciousInput() {
                // Try to pass malicious data
                malicious_data = ["not", "numbers", {"attack": "vector"}];
                return dataanalysis.mean(malicious_data);
            }
            '''

            capabilities = CapabilityContext()
            capabilities.grant("execute:calculations", "execute")

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            # Should fail gracefully, not crash
            assert not result.success
            assert "numeric" in result.error.lower()

Module Development Best Practices
==================================

Code Organization
-----------------

1. **Single Responsibility**: Each module should have a clear, focused purpose
2. **Consistent Naming**: Use snake_case for Python, camelCase for ML
3. **Comprehensive Documentation**: Document every public function and class
4. **Error Handling**: Always provide meaningful error messages
5. **Security First**: Validate all inputs and require appropriate capabilities

.. code-block:: python

    # Good: Well-organized module structure
    class WellDesignedModule:
        """Clear purpose and interface."""

        @staticmethod
        @require_capability("module:operation")
        def focused_operation(validated_input: str) -> str:
            """
            Perform specific operation with clear interface.

            Args:
                validated_input: Pre-validated string input

            Returns:
                Processed result string

            Raises:
                MLRuntimeError: If operation fails
            """
            if not isinstance(validated_input, str):
                raise MLRuntimeError("Input must be a string")

            try:
                result = process_string(validated_input)
                return result
            except Exception as e:
                raise MLRuntimeError(f"Operation failed: {e}")

Performance Optimization
------------------------

1. **Lazy Loading**: Load expensive resources only when needed
2. **Caching**: Cache expensive computations with appropriate TTL
3. **Batch Operations**: Support processing multiple items efficiently
4. **Memory Management**: Clean up resources promptly
5. **Profiling**: Include performance benchmarks in tests

.. code-block:: python

    from functools import lru_cache
    import weakref

    class OptimizedModule:
        def __init__(self):
            self._cache = weakref.WeakValueDictionary()
            self._expensive_resource = None

        @lru_cache(maxsize=128)
        def cached_computation(self, input_data: str) -> str:
            """Expensive computation with caching."""
            return self._expensive_operation(input_data)

        def batch_process(self, items: List[Any]) -> List[Any]:
            """Process multiple items efficiently."""
            results = []
            with self._get_optimized_context():
                for batch in self._chunk_items(items, batch_size=100):
                    batch_results = self._process_batch(batch)
                    results.extend(batch_results)
            return results

        def _get_expensive_resource(self):
            """Lazy load expensive resource."""
            if self._expensive_resource is None:
                self._expensive_resource = load_expensive_resource()
            return self._expensive_resource

Version Management
------------------

1. **Semantic Versioning**: Use MAJOR.MINOR.PATCH
2. **Compatibility Matrix**: Document mlpy version requirements
3. **Migration Guides**: Provide clear upgrade paths
4. **Deprecation Policy**: Give advance notice for breaking changes

.. code-block:: python

    # module_info.py
    MODULE_INFO = {
        "name": "dataanalysis",
        "version": "2.1.0",
        "description": "Advanced data analysis with object-oriented interface",
        "author": "mlpy Team",
        "license": "MIT",
        "mlpy_version_required": ">=2.0.0,<3.0.0",
        "python_dependencies": [
            "statistics>=1.0.0",
            "numpy>=1.21.0;extra=='advanced'"
        ],
        "capabilities_provided": [
            "read:data_files",
            "execute:calculations",
            "write:analysis_results"
        ],
        "breaking_changes": {
            "2.0.0": "DataFrame API changed - see migration guide",
            "2.1.0": "Added new analysis methods - backward compatible"
        }
    }

This completes the comprehensive guide to developing standard library modules for mlpy, covering the registry system, object access patterns, bridge functions, capability integration, and best practices for creating production-ready modules.