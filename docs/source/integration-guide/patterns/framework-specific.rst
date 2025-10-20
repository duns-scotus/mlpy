Framework-Specific Integration
=================================

.. note::
   **Chapter Summary:** Integrating ML with popular Python frameworks including Flask, Django, Qt/PySide6, Streamlit, and Jupyter notebooks.

This chapter provides detailed integration patterns for popular Python frameworks. You'll learn how to embed ML into web applications, desktop GUIs, data apps, and notebooks with framework-specific best practices.

----

Flask Integration
------------------

Integrate ML with Flask web applications for synchronous and asynchronous request handling.

Basic Flask Integration
~~~~~~~~~~~~~~~~~~~~~~~~

Execute ML functions in Flask route handlers.

**app.py:**

.. code-block:: python

   from flask import Flask, request, jsonify
   from mlpy import MLExecutor
   from typing import Any, Dict

   app = Flask(__name__)

   # Initialize ML executor
   ml_executor = MLExecutor()
   ml_executor.load("handlers.ml")

   @app.route('/api/process', methods=['POST'])
   def process_data():
       """Process data using ML function."""
       try:
           # Get request data
           data = request.get_json()

           # Execute ML function
           result = ml_executor.call_function("processData", data)

           return jsonify({
               "status": "success",
               "result": result
           }), 200

       except Exception as e:
           return jsonify({
               "status": "error",
               "error": str(e)
           }), 500

   @app.route('/api/validate', methods=['POST'])
   def validate_input():
       """Validate input using ML function."""
       data = request.get_json()

       result = ml_executor.call_function("validateInput", data)

       if result.get("valid"):
           return jsonify({
               "status": "valid",
               "data": result
           }), 200
       else:
           return jsonify({
               "status": "invalid",
               "errors": result.get("errors", [])
           }), 400

   @app.route('/api/calculate', methods=['POST'])
   def calculate():
       """Perform calculations using ML."""
       data = request.get_json()

       result = ml_executor.call_function("calculate", {
           "values": data.get("values", []),
           "operation": data.get("operation", "sum")
       })

       return jsonify(result), 200

   if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0', port=5000)

**handlers.ml:**

.. code-block:: ml

   function processData(data) {
       # Process input data
       let processed = {
           "input": data,
           "timestamp": new Date().toISOString(),
           "processed": true
       };

       # Add computed fields
       if (data.values) {
           processed.sum = data.values.reduce(function(a, b) {
               return a + b;
           }, 0);
           processed.count = data.values.length;
           processed.average = processed.sum / processed.count;
       }

       return processed;
   }

   function validateInput(data) {
       let errors = [];

       # Check required fields
       if (!data.name || data.name.length == 0) {
           errors.push("Name is required");
       }

       if (!data.email || data.email.indexOf("@") < 0) {
           errors.push("Valid email is required");
       }

       if (data.age && (data.age < 0 || data.age > 150)) {
           errors.push("Age must be between 0 and 150");
       }

       return {
           "valid": errors.length == 0,
           "errors": errors
       };
   }

   function calculate(params) {
       let values = params.values;
       let operation = params.operation;

       if (operation == "sum") {
           return {
               "operation": "sum",
               "result": values.reduce(function(a, b) { return a + b; }, 0)
           };
       } elif (operation == "product") {
           return {
               "operation": "product",
               "result": values.reduce(function(a, b) { return a * b; }, 1)
           };
       } elif (operation == "average") {
           let sum = values.reduce(function(a, b) { return a + b; }, 0);
           return {
               "operation": "average",
               "result": sum / values.length
           };
       }

       return {"error": "Unknown operation"};
   }

Flask with Blueprint Organization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Organize ML endpoints using Flask blueprints.

**ml_blueprint.py:**

.. code-block:: python

   from flask import Blueprint, request, jsonify
   from mlpy import MLExecutor

   # Create blueprint
   ml_api = Blueprint('ml_api', __name__, url_prefix='/api/ml')

   # Initialize executor
   executor = MLExecutor()
   executor.load("ml_functions.ml")

   @ml_api.route('/transform', methods=['POST'])
   def transform():
       """Transform data using ML."""
       data = request.get_json()
       result = executor.call_function("transform", data)
       return jsonify(result)

   @ml_api.route('/analyze', methods=['POST'])
   def analyze():
       """Analyze data using ML."""
       data = request.get_json()
       result = executor.call_function("analyze", data)
       return jsonify(result)

   @ml_api.route('/predict', methods=['POST'])
   def predict():
       """Make predictions using ML."""
       data = request.get_json()
       result = executor.call_function("predict", data)
       return jsonify(result)

**app.py:**

.. code-block:: python

   from flask import Flask
   from ml_blueprint import ml_api

   app = Flask(__name__)
   app.register_blueprint(ml_api)

   if __name__ == '__main__':
       app.run(debug=True)

Flask with Async Support
~~~~~~~~~~~~~~~~~~~~~~~~~

Use async routes with ML execution (Flask 2.0+).

.. code-block:: python

   from flask import Flask, request, jsonify
   from mlpy import AsyncMLExecutor
   import asyncio

   app = Flask(__name__)
   executor = AsyncMLExecutor()
   executor.load("async_handlers.ml")

   @app.route('/api/async-process', methods=['POST'])
   async def async_process():
       """Async endpoint using ML."""
       data = request.get_json()

       # Execute ML asynchronously
       result = await executor.call_function_async("processAsync", data)

       return jsonify({
           "status": "success",
           "result": result
       })

   @app.route('/api/batch-process', methods=['POST'])
   async def batch_process():
       """Process multiple items concurrently."""
       items = request.get_json().get("items", [])

       # Process all items concurrently
       tasks = [
           executor.call_function_async("processItem", item)
           for item in items
       ]

       results = await asyncio.gather(*tasks)

       return jsonify({
           "status": "success",
           "count": len(results),
           "results": results
       })

Flask with Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~

Comprehensive error handling for ML execution.

.. code-block:: python

   from flask import Flask, request, jsonify
   from mlpy import MLExecutor, MLExecutionError, MLSecurityError
   from functools import wraps

   app = Flask(__name__)
   executor = MLExecutor()
   executor.load("handlers.ml")

   def ml_error_handler(f):
       """Decorator for ML error handling."""
       @wraps(f)
       def decorated_function(*args, **kwargs):
           try:
               return f(*args, **kwargs)
           except MLSecurityError as e:
               return jsonify({
                   "status": "error",
                   "type": "security",
                   "message": str(e)
               }), 403
           except MLExecutionError as e:
               return jsonify({
                   "status": "error",
                   "type": "execution",
                   "message": str(e)
               }), 500
           except Exception as e:
               app.logger.error(f"Unexpected error: {e}")
               return jsonify({
                   "status": "error",
                   "type": "unexpected",
                   "message": "Internal server error"
               }), 500

       return decorated_function

   @app.route('/api/safe-process', methods=['POST'])
   @ml_error_handler
   def safe_process():
       """Process with comprehensive error handling."""
       data = request.get_json()
       result = executor.call_function("process", data)
       return jsonify({"status": "success", "result": result})

----

Django Integration
-------------------

Integrate ML with Django for full-featured web applications.

Django View Integration
~~~~~~~~~~~~~~~~~~~~~~~~

Use ML in Django class-based and function-based views.

**views.py:**

.. code-block:: python

   from django.http import JsonResponse
   from django.views import View
   from django.views.decorators.csrf import csrf_exempt
   from django.utils.decorators import method_decorator
   from mlpy import MLExecutor
   import json

   # Initialize ML executor
   ml_executor = MLExecutor()
   ml_executor.load("django_handlers.ml")

   @method_decorator(csrf_exempt, name='dispatch')
   class MLProcessView(View):
       """Process data using ML."""

       def post(self, request):
           try:
               # Parse request body
               data = json.loads(request.body)

               # Execute ML function
               result = ml_executor.call_function("processData", data)

               return JsonResponse({
                   "status": "success",
                   "result": result
               })

           except Exception as e:
               return JsonResponse({
                   "status": "error",
                   "error": str(e)
               }, status=500)

   @csrf_exempt
   def ml_validate(request):
       """Validate data using ML function."""
       if request.method == 'POST':
           data = json.loads(request.body)

           result = ml_executor.call_function("validate", data)

           if result.get("valid"):
               return JsonResponse({"status": "valid", "data": result})
           else:
               return JsonResponse({
                   "status": "invalid",
                   "errors": result.get("errors", [])
               }, status=400)

       return JsonResponse({"error": "Method not allowed"}, status=405)

**urls.py:**

.. code-block:: python

   from django.urls import path
   from . import views

   urlpatterns = [
       path('api/ml/process/', views.MLProcessView.as_view(), name='ml_process'),
       path('api/ml/validate/', views.ml_validate, name='ml_validate'),
   ]

Django with Model Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integrate ML with Django ORM models.

**models.py:**

.. code-block:: python

   from django.db import models
   from mlpy import MLExecutor
   import json

   class DataProcessor(models.Model):
       """Model that uses ML for processing."""

       name = models.CharField(max_length=100)
       input_data = models.JSONField()
       output_data = models.JSONField(null=True, blank=True)
       processed_at = models.DateTimeField(null=True, blank=True)

       ml_executor = MLExecutor()
       ml_executor.load("model_processors.ml")

       def process(self):
           """Process input data using ML."""
           result = self.ml_executor.call_function("processModelData", {
               "id": self.id,
               "name": self.name,
               "data": self.input_data
           })

           self.output_data = result
           self.processed_at = timezone.now()
           self.save()

           return result

       def validate_input(self):
           """Validate input data using ML."""
           result = self.ml_executor.call_function("validateModelData", {
               "data": self.input_data
           })

           return result.get("valid", False)

       class Meta:
           db_table = 'data_processor'

**Usage:**

.. code-block:: python

   # Create and process
   processor = DataProcessor.objects.create(
       name="Test Processor",
       input_data={"values": [1, 2, 3, 4, 5]}
   )

   # Validate
   if processor.validate_input():
       # Process
       result = processor.process()
       print(f"Processed: {result}")

Django Middleware Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ML in Django middleware for request processing.

**middleware.py:**

.. code-block:: python

   from mlpy import MLExecutor
   from django.http import JsonResponse
   import json

   class MLSecurityMiddleware:
       """Middleware for ML-based security checks."""

       def __init__(self, get_response):
           self.get_response = get_response
           self.executor = MLExecutor()
           self.executor.load("security_checks.ml")

       def __call__(self, request):
           # Pre-processing: Check request
           if request.method == 'POST':
               security_check = self.executor.call_function("checkRequest", {
                   "path": request.path,
                   "method": request.method,
                   "headers": dict(request.headers),
                   "remote_addr": request.META.get('REMOTE_ADDR')
               })

               if not security_check.get("allowed", True):
                   return JsonResponse({
                       "error": "Request blocked by security policy",
                       "reason": security_check.get("reason")
                   }, status=403)

           # Process request
           response = self.get_response(request)

           return response

**settings.py:**

.. code-block:: python

   MIDDLEWARE = [
       # ... other middleware
       'myapp.middleware.MLSecurityMiddleware',
       # ... other middleware
   ]

Django Rest Framework Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integrate ML with Django REST Framework.

**serializers.py:**

.. code-block:: python

   from rest_framework import serializers
   from mlpy import MLExecutor

   class MLProcessSerializer(serializers.Serializer):
       """Serializer with ML validation."""

       input_data = serializers.JSONField()

       ml_executor = MLExecutor()
       ml_executor.load("validators.ml")

       def validate_input_data(self, value):
           """Validate using ML function."""
           result = self.ml_executor.call_function("validateData", value)

           if not result.get("valid", False):
               raise serializers.ValidationError(
                   result.get("errors", ["Invalid data"])
               )

           return value

**views.py:**

.. code-block:: python

   from rest_framework.views import APIView
   from rest_framework.response import Response
   from rest_framework import status
   from mlpy import MLExecutor

   class MLProcessAPIView(APIView):
       """API view with ML processing."""

       def __init__(self, **kwargs):
           super().__init__(**kwargs)
           self.executor = MLExecutor()
           self.executor.load("api_handlers.ml")

       def post(self, request):
           """Process data using ML."""
           try:
               result = self.executor.call_function(
                   "processAPIData",
                   request.data
               )

               return Response({
                   "status": "success",
                   "result": result
               }, status=status.HTTP_200_OK)

           except Exception as e:
               return Response({
                   "status": "error",
                   "error": str(e)
               }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

----

Qt/PySide6 Integration
------------------------

Integrate ML with Qt desktop applications for responsive GUI applications.

Basic Qt Application with ML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute ML functions in Qt application with threading.

**main_window.py:**

.. code-block:: python

   from PySide6.QtWidgets import (
       QMainWindow, QWidget, QVBoxLayout, QPushButton,
       QTextEdit, QLabel, QProgressBar
   )
   from PySide6.QtCore import QThread, Signal, Slot
   from mlpy import MLExecutor

   class MLWorker(QThread):
       """Worker thread for ML execution."""

       finished = Signal(dict)
       error = Signal(str)
       progress = Signal(int)

       def __init__(self, ml_script, function_name, data):
           super().__init__()
           self.ml_script = ml_script
           self.function_name = function_name
           self.data = data

       def run(self):
           """Execute ML function in background thread."""
           try:
               executor = MLExecutor()
               executor.load(self.ml_script)

               self.progress.emit(50)

               result = executor.call_function(self.function_name, self.data)

               self.progress.emit(100)
               self.finished.emit(result)

           except Exception as e:
               self.error.emit(str(e))

   class MainWindow(QMainWindow):
       """Main application window with ML integration."""

       def __init__(self):
           super().__init__()
           self.setWindowTitle("ML Desktop App")
           self.setGeometry(100, 100, 800, 600)

           # Create UI
           self.setup_ui()

           # ML worker thread
           self.worker = None

       def setup_ui(self):
           """Setup user interface."""
           central_widget = QWidget()
           self.setCentralWidget(central_widget)

           layout = QVBoxLayout(central_widget)

           # Input area
           self.input_label = QLabel("Input Data:")
           layout.addWidget(self.input_label)

           self.input_text = QTextEdit()
           self.input_text.setPlaceholderText('{"values": [1, 2, 3, 4, 5]}')
           layout.addWidget(self.input_text)

           # Process button
           self.process_button = QPushButton("Process with ML")
           self.process_button.clicked.connect(self.on_process_clicked)
           layout.addWidget(self.process_button)

           # Progress bar
           self.progress_bar = QProgressBar()
           self.progress_bar.setVisible(False)
           layout.addWidget(self.progress_bar)

           # Output area
           self.output_label = QLabel("Output:")
           layout.addWidget(self.output_label)

           self.output_text = QTextEdit()
           self.output_text.setReadOnly(True)
           layout.addWidget(self.output_text)

       @Slot()
       def on_process_clicked(self):
           """Handle process button click."""
           import json

           try:
               # Parse input
               input_data = json.loads(self.input_text.toPlainText())

               # Show progress
               self.progress_bar.setVisible(True)
               self.progress_bar.setValue(0)
               self.process_button.setEnabled(False)

               # Create worker
               self.worker = MLWorker("handlers.ml", "processData", input_data)
               self.worker.finished.connect(self.on_ml_finished)
               self.worker.error.connect(self.on_ml_error)
               self.worker.progress.connect(self.on_ml_progress)

               # Start processing
               self.worker.start()

           except json.JSONDecodeError as e:
               self.output_text.setText(f"JSON Error: {e}")

       @Slot(dict)
       def on_ml_finished(self, result):
           """Handle ML execution completion."""
           import json
           self.output_text.setText(json.dumps(result, indent=2))
           self.progress_bar.setVisible(False)
           self.process_button.setEnabled(True)

       @Slot(str)
       def on_ml_error(self, error):
           """Handle ML execution error."""
           self.output_text.setText(f"Error: {error}")
           self.progress_bar.setVisible(False)
           self.process_button.setEnabled(True)

       @Slot(int)
       def on_ml_progress(self, value):
           """Update progress bar."""
           self.progress_bar.setValue(value)

**main.py:**

.. code-block:: python

   from PySide6.QtWidgets import QApplication
   from main_window import MainWindow
   import sys

   if __name__ == '__main__':
       app = QApplication(sys.argv)
       window = MainWindow()
       window.show()
       sys.exit(app.exec())

Qt with ML Model
~~~~~~~~~~~~~~~~~

Integrate ML with Qt Model/View architecture.

.. code-block:: python

   from PySide6.QtCore import QAbstractTableModel, Qt
   from mlpy import MLExecutor

   class MLDataModel(QAbstractTableModel):
       """Table model with ML data processing."""

       def __init__(self, ml_script, parent=None):
           super().__init__(parent)
           self.executor = MLExecutor()
           self.executor.load(ml_script)
           self.data_items = []
           self.headers = ["Input", "Output", "Status"]

       def rowCount(self, parent=None):
           return len(self.data_items)

       def columnCount(self, parent=None):
           return len(self.headers)

       def data(self, index, role=Qt.DisplayRole):
           if role == Qt.DisplayRole:
               item = self.data_items[index.row()]
               col = index.column()

               if col == 0:
                   return str(item.get("input", ""))
               elif col == 1:
                   return str(item.get("output", ""))
               elif col == 2:
                   return item.get("status", "Pending")

           return None

       def headerData(self, section, orientation, role=Qt.DisplayRole):
           if role == Qt.DisplayRole and orientation == Qt.Horizontal:
               return self.headers[section]
           return None

       def add_item(self, input_data):
           """Add item and process with ML."""
           row = len(self.data_items)

           self.beginInsertRows(QModelIndex(), row, row)

           item = {
               "input": input_data,
               "output": None,
               "status": "Processing"
           }
           self.data_items.append(item)

           self.endInsertRows()

           # Process with ML
           try:
               result = self.executor.call_function("processItem", input_data)
               item["output"] = result
               item["status"] = "Complete"
           except Exception as e:
               item["status"] = f"Error: {e}"

           # Update view
           self.dataChanged.emit(
               self.index(row, 0),
               self.index(row, 2)
           )

----

Streamlit Integration
----------------------

Integrate ML with Streamlit for interactive data applications.

Basic Streamlit App with ML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create interactive data app with ML processing.

**app.py:**

.. code-block:: python

   import streamlit as st
   from mlpy import MLExecutor
   import json
   import pandas as pd

   # Page configuration
   st.set_page_config(
       page_title="ML Data Processor",
       page_icon="🤖",
       layout="wide"
   )

   # Initialize ML executor
   @st.cache_resource
   def get_ml_executor():
       """Initialize and cache ML executor."""
       executor = MLExecutor()
       executor.load("streamlit_handlers.ml")
       return executor

   executor = get_ml_executor()

   # Title
   st.title("🤖 ML Data Processor")
   st.markdown("Process your data using ML functions")

   # Sidebar
   st.sidebar.header("Configuration")
   operation = st.sidebar.selectbox(
       "Select Operation",
       ["Process", "Validate", "Transform", "Analyze"]
   )

   # Main content
   col1, col2 = st.columns(2)

   with col1:
       st.header("Input")

       # Input method selection
       input_method = st.radio(
           "Input Method",
           ["JSON Editor", "File Upload", "Sample Data"]
       )

       if input_method == "JSON Editor":
           input_text = st.text_area(
               "Enter JSON data",
               value='{"values": [1, 2, 3, 4, 5]}',
               height=200
           )
       elif input_method == "File Upload":
           uploaded_file = st.file_uploader("Upload JSON file", type=['json'])
           if uploaded_file:
               input_text = uploaded_file.read().decode()
           else:
               input_text = "{}"
       else:
           sample_data = {
               "values": [10, 20, 30, 40, 50],
               "operation": "average"
           }
           input_text = json.dumps(sample_data, indent=2)
           st.code(input_text, language="json")

   with col2:
       st.header("Output")

       # Process button
       if st.button("🚀 Process with ML", type="primary"):
           try:
               # Parse input
               input_data = json.loads(input_text)

               # Show processing
               with st.spinner("Processing..."):
                   # Execute ML function
                   if operation == "Process":
                       result = executor.call_function("process", input_data)
                   elif operation == "Validate":
                       result = executor.call_function("validate", input_data)
                   elif operation == "Transform":
                       result = executor.call_function("transform", input_data)
                   else:  # Analyze
                       result = executor.call_function("analyze", input_data)

               # Display result
               st.success("✅ Processing complete!")

               # Show as JSON
               st.json(result)

               # If result contains tabular data, show as dataframe
               if "data" in result and isinstance(result["data"], list):
                   df = pd.DataFrame(result["data"])
                   st.dataframe(df)

           except json.JSONDecodeError as e:
               st.error(f"❌ JSON Error: {e}")
           except Exception as e:
               st.error(f"❌ Processing Error: {e}")

   # Footer
   st.divider()
   st.caption("Powered by mlpy ML Language")

**streamlit_handlers.ml:**

.. code-block:: ml

   function process(data) {
       return {
           "status": "processed",
           "input": data,
           "timestamp": new Date().toISOString()
       };
   }

   function validate(data) {
       let errors = [];

       if (!data.values || data.values.length == 0) {
           errors.push("Values array is required");
       }

       return {
           "valid": errors.length == 0,
           "errors": errors
       };
   }

   function transform(data) {
       if (!data.values) {
           return {"error": "No values to transform"};
       }

       return {
           "original": data.values,
           "doubled": data.values.map(function(x) { return x * 2; }),
           "squared": data.values.map(function(x) { return x * x; })
       };
   }

   function analyze(data) {
       if (!data.values) {
           return {"error": "No values to analyze"};
       }

       let values = data.values;
       let sum = values.reduce(function(a, b) { return a + b; }, 0);
       let count = values.length;
       let mean = sum / count;

       # Calculate variance
       let variance = 0;
       let i = 0;
       while (i < count) {
           let diff = values[i] - mean;
           variance = variance + (diff * diff);
           i = i + 1;
       }
       variance = variance / count;

       let stdDev = Math.sqrt(variance);

       return {
           "count": count,
           "sum": sum,
           "mean": mean,
           "variance": variance,
           "std_dev": stdDev,
           "min": Math.min(...values),
           "max": Math.max(...values)
       };
   }

Streamlit with Charts
~~~~~~~~~~~~~~~~~~~~~~

Create interactive charts from ML results.

.. code-block:: python

   import streamlit as st
   from mlpy import MLExecutor
   import plotly.graph_objects as go
   import plotly.express as px

   executor = MLExecutor()
   executor.load("analytics.ml")

   st.title("📊 ML Analytics Dashboard")

   # Data input
   st.sidebar.header("Data Input")
   data_points = st.sidebar.slider("Number of data points", 10, 100, 50)

   # Generate data using ML
   if st.sidebar.button("Generate Data"):
       result = executor.call_function("generateData", {
           "count": data_points,
           "seed": 42
       })

       # Store in session state
       st.session_state.data = result

   # Display charts if data exists
   if 'data' in st.session_state:
       data = st.session_state.data

       # Analyze data
       analysis = executor.call_function("analyzeTimeSeries", data)

       # Display metrics
       col1, col2, col3, col4 = st.columns(4)
       col1.metric("Mean", f"{analysis['mean']:.2f}")
       col2.metric("Std Dev", f"{analysis['std_dev']:.2f}")
       col3.metric("Min", f"{analysis['min']:.2f}")
       col4.metric("Max", f"{analysis['max']:.2f}")

       # Line chart
       st.subheader("Time Series")
       fig = go.Figure()
       fig.add_trace(go.Scatter(
           y=data['values'],
           mode='lines+markers',
           name='Values'
       ))
       st.plotly_chart(fig, use_container_width=True)

       # Histogram
       st.subheader("Distribution")
       fig = px.histogram(x=data['values'], nbins=20)
       st.plotly_chart(fig, use_container_width=True)

Streamlit with Caching
~~~~~~~~~~~~~~~~~~~~~~~~

Optimize ML execution with Streamlit caching.

.. code-block:: python

   import streamlit as st
   from mlpy import MLExecutor

   @st.cache_resource
   def get_executor():
       """Cache ML executor initialization."""
       executor = MLExecutor()
       executor.load("expensive_operations.ml")
       return executor

   @st.cache_data
   def process_data(data, _executor):
       """Cache expensive ML operations."""
       return _executor.call_function("expensiveOperation", data)

   st.title("Cached ML Processing")

   executor = get_executor()

   # Input
   input_data = st.text_input("Enter data", value="test")

   # Process (cached)
   if st.button("Process"):
       with st.spinner("Processing..."):
           result = process_data(input_data, executor)
           st.json(result)
           st.info("Result cached for future use")

----

Jupyter Notebook Integration
------------------------------

Integrate ML with Jupyter notebooks for interactive data analysis.

Basic Notebook Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute ML functions in Jupyter cells.

.. code-block:: python

   # Cell 1: Setup
   from mlpy import MLExecutor
   import pandas as pd
   import matplotlib.pyplot as plt

   # Initialize ML executor
   ml = MLExecutor()
   ml.load("notebook_functions.ml")

   print("✅ ML executor initialized")

.. code-block:: python

   # Cell 2: Process Data
   data = {
       "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
       "operation": "statistics"
   }

   result = ml.call_function("analyzeData", data)

   # Display results
   print("Analysis Results:")
   for key, value in result.items():
       print(f"  {key}: {value}")

.. code-block:: python

   # Cell 3: Visualize
   # Generate data using ML
   chart_data = ml.call_function("generateChartData", {"points": 50})

   # Plot
   plt.figure(figsize=(10, 6))
   plt.plot(chart_data['x'], chart_data['y'], marker='o')
   plt.title("ML-Generated Data")
   plt.xlabel("X Values")
   plt.ylabel("Y Values")
   plt.grid(True)
   plt.show()

.. code-block:: python

   # Cell 4: DataFrame Integration
   # Transform data using ML
   transformed = ml.call_function("transformForDataFrame", data)

   # Create DataFrame
   df = pd.DataFrame(transformed['data'])
   display(df)

   # Statistical summary
   display(df.describe())

IPython Magic Commands
~~~~~~~~~~~~~~~~~~~~~~~

Create custom IPython magic for ML execution.

**ml_magic.py:**

.. code-block:: python

   from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
   from mlpy import MLExecutor
   import json

   @magics_class
   class MLMagics(Magics):
       """Custom magic commands for ML execution."""

       def __init__(self, shell):
           super().__init__(shell)
           self.executor = MLExecutor()

       @line_magic
       def mlload(self, line):
           """Load ML script: %mlload script.ml"""
           self.executor.load(line.strip())
           return f"Loaded: {line}"

       @line_magic
       def mlcall(self, line):
           """Call ML function: %mlcall functionName {"data": "value"}"""
           parts = line.split(None, 1)
           function_name = parts[0]
           data = json.loads(parts[1]) if len(parts) > 1 else {}

           result = self.executor.call_function(function_name, data)
           return result

       @cell_magic
       def mlprocess(self, line, cell):
           """Process cell content with ML function.

           Usage:
           %%mlprocess processFunction
           {"data": "value"}
           """
           function_name = line.strip()
           data = json.loads(cell)

           result = self.executor.call_function(function_name, data)
           return result

   # Register magic
   def load_ipython_extension(ipython):
       ipython.register_magics(MLMagics)

**Usage in Notebook:**

.. code-block:: python

   # Load the extension
   %load_ext ml_magic

   # Load ML script
   %mlload functions.ml

   # Call ML function
   %mlcall processData {"values": [1, 2, 3]}

   # Use cell magic
   %%mlprocess transformData
   {
       "input": [1, 2, 3, 4, 5],
       "operation": "double"
   }

Notebook with Interactive Widgets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create interactive ML interfaces with ipywidgets.

.. code-block:: python

   from mlpy import MLExecutor
   import ipywidgets as widgets
   from IPython.display import display, clear_output

   # Initialize
   ml = MLExecutor()
   ml.load("interactive_functions.ml")

   # Create widgets
   input_text = widgets.Textarea(
       value='{"values": [1, 2, 3, 4, 5]}',
       placeholder='Enter JSON data',
       description='Input:',
       layout=widgets.Layout(width='100%', height='100px')
   )

   function_dropdown = widgets.Dropdown(
       options=['process', 'validate', 'transform', 'analyze'],
       value='process',
       description='Function:',
   )

   process_button = widgets.Button(
       description='Process with ML',
       button_style='success',
       icon='play'
   )

   output_area = widgets.Output()

   def on_process_clicked(b):
       """Handle button click."""
       with output_area:
           clear_output()
           try:
               import json
               data = json.loads(input_text.value)
               result = ml.call_function(function_dropdown.value, data)

               print("✅ Processing complete!")
               print(json.dumps(result, indent=2))

           except Exception as e:
               print(f"❌ Error: {e}")

   process_button.on_click(on_process_clicked)

   # Display interface
   display(widgets.VBox([
       input_text,
       function_dropdown,
       process_button,
       output_area
   ]))

----

Best Practices
---------------

Flask Best Practices
~~~~~~~~~~~~~~~~~~~~~

**1. Use Application Factory Pattern:**

.. code-block:: python

   def create_app(config=None):
       app = Flask(__name__)

       # Initialize ML executor once
       executor = MLExecutor()
       executor.load("handlers.ml")

       # Store in app context
       app.ml_executor = executor

       # Register blueprints
       from .ml_routes import ml_bp
       app.register_blueprint(ml_bp)

       return app

**2. Handle ML Errors Gracefully:**

.. code-block:: python

   @app.errorhandler(MLExecutionError)
   def handle_ml_error(e):
       return jsonify({"error": str(e)}), 500

**3. Use Request Hooks for Cleanup:**

.. code-block:: python

   @app.teardown_request
   def cleanup(exception=None):
       # Clean up ML resources if needed
       pass

Django Best Practices
~~~~~~~~~~~~~~~~~~~~~~

**1. Use Django Settings for ML Configuration:**

.. code-block:: python

   # settings.py
   ML_SCRIPTS_DIR = os.path.join(BASE_DIR, 'ml_scripts')
   ML_CACHE_ENABLED = True

   # views.py
   from django.conf import settings

   executor = MLExecutor()
   executor.load(os.path.join(settings.ML_SCRIPTS_DIR, 'handlers.ml'))

**2. Use Django Signals for ML Events:**

.. code-block:: python

   from django.db.models.signals import post_save
   from django.dispatch import receiver

   @receiver(post_save, sender=MyModel)
   def process_with_ml(sender, instance, **kwargs):
       executor.call_function("processModel", {
           "id": instance.id,
           "data": instance.data
       })

**3. Cache ML Executors:**

.. code-block:: python

   from django.core.cache import cache

   def get_ml_executor():
       executor = cache.get('ml_executor')
       if not executor:
           executor = MLExecutor()
           executor.load('handlers.ml')
           cache.set('ml_executor', executor, timeout=3600)
       return executor

Qt Best Practices
~~~~~~~~~~~~~~~~~~

**1. Always Use Worker Threads:**

Never block the GUI thread with ML execution.

.. code-block:: python

   # Good: Use worker thread
   worker = MLWorker("script.ml", "function", data)
   worker.finished.connect(self.on_finished)
   worker.start()

   # Bad: Block GUI thread
   # result = executor.call_function("function", data)  # DON'T DO THIS

**2. Proper Resource Cleanup:**

.. code-block:: python

   def closeEvent(self, event):
       """Clean up on window close."""
       if self.worker and self.worker.isRunning():
           self.worker.quit()
           self.worker.wait()
       event.accept()

**3. Use Signals for Communication:**

.. code-block:: python

   # Define custom signals
   class MLWorker(QThread):
       progress_updated = Signal(int, str)
       data_ready = Signal(dict)

       def run(self):
           self.progress_updated.emit(25, "Loading...")
           # ... processing ...
           self.data_ready.emit(result)

Streamlit Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Cache ML Executors:**

.. code-block:: python

   @st.cache_resource
   def get_ml_executor():
       executor = MLExecutor()
       executor.load("handlers.ml")
       return executor

**2. Cache Expensive Operations:**

.. code-block:: python

   @st.cache_data
   def expensive_ml_operation(data, _executor):
       return _executor.call_function("expensive", data)

**3. Use Session State for Persistence:**

.. code-block:: python

   if 'ml_results' not in st.session_state:
       st.session_state.ml_results = []

   result = executor.call_function("process", data)
   st.session_state.ml_results.append(result)

Jupyter Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~

**1. Initialize Once:**

.. code-block:: python

   # First cell: Setup
   if 'ml_executor' not in globals():
       ml_executor = MLExecutor()
       ml_executor.load("functions.ml")

**2. Use Display Functions:**

.. code-block:: python

   from IPython.display import display, Markdown, JSON

   # Display formatted output
   display(Markdown("## Results"))
   display(JSON(result))

**3. Create Reusable Functions:**

.. code-block:: python

   def ml_process(data, function_name="process"):
       """Reusable ML processing function."""
       result = ml_executor.call_function(function_name, data)
       display(JSON(result))
       return result

----

Common Pitfalls
----------------

1. Blocking GUI Thread (Qt)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** ML execution blocks UI updates.

**Solution:** Always use worker threads.

.. code-block:: python

   # Wrong
   def on_click(self):
       result = self.executor.call_function("slow", data)  # Blocks!
       self.update_ui(result)

   # Right
   def on_click(self):
       worker = MLWorker("script.ml", "slow", data)
       worker.finished.connect(self.update_ui)
       worker.start()  # Non-blocking

2. Memory Leaks (All Frameworks)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** ML executors not properly cleaned up.

**Solution:** Implement proper cleanup.

.. code-block:: python

   # Flask
   @app.teardown_appcontext
   def cleanup(exception=None):
       # Clean up resources
       pass

   # Django
   from django.core.signals import request_finished

   @receiver(request_finished)
   def cleanup(sender, **kwargs):
       # Clean up resources
       pass

3. Not Caching ML Executors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Creating new executor for each request.

**Solution:** Cache and reuse executors.

.. code-block:: python

   # Streamlit
   @st.cache_resource
   def get_executor():
       return MLExecutor()

   # Flask
   def create_app():
       app = Flask(__name__)
       app.ml_executor = MLExecutor()  # Reuse
       return app

----

Troubleshooting
----------------

Framework-Specific Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Flask: "Working outside of application context"**

.. code-block:: python

   # Solution: Use application context
   with app.app_context():
       result = executor.call_function("process", data)

**Django: "Apps aren't loaded yet"**

.. code-block:: python

   # Solution: Initialize in AppConfig
   from django.apps import AppConfig

   class MyAppConfig(AppConfig):
       def ready(self):
           self.ml_executor = MLExecutor()
           self.ml_executor.load("handlers.ml")

**Qt: "Cannot create children for a parent in a different thread"**

.. code-block:: python

   # Solution: Create executor in worker thread
   class MLWorker(QThread):
       def run(self):
           executor = MLExecutor()  # Create here, not in __init__
           executor.load(self.script)

**Streamlit: "DuplicateWidgetID"**

.. code-block:: python

   # Solution: Use unique keys
   st.button("Process", key=f"process_{index}")

----

Summary
--------

Framework-specific integration enables ML to work seamlessly with popular Python frameworks:

**Web Frameworks:**
- Flask: Lightweight REST APIs with ML
- Django: Full-featured web applications with ORM integration

**Desktop:**
- Qt/PySide6: Responsive GUI applications with worker threads

**Data Apps:**
- Streamlit: Interactive data applications with caching

**Notebooks:**
- Jupyter: Interactive data analysis with custom magic commands

**Key Principles:**
- Never block the main/GUI thread
- Cache ML executors for performance
- Implement proper error handling
- Clean up resources properly
- Use framework-specific patterns

Each framework has unique requirements, but the core ML integration patterns remain consistent.

----

Next: :doc:`../data/marshalling` - Deep dive into data marshalling between Python and ML
