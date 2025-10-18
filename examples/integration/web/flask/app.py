"""
Flask Web API with ML Backend
Demonstrates ML functions as Flask route handlers
"""

import sys
from pathlib import Path
from flask import Flask, request, jsonify

# Add mlpy to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.mlpy.ml.transpiler import MLTranspiler


class MLFlaskAPI:
    """Flask API powered by ML business logic"""

    def __init__(self, ml_file: Path):
        self.app = Flask(__name__)
        self.ml_functions = {}
        self.init_ml(ml_file)
        self.setup_routes()

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
                "validate_user",
                "calculate_user_score",
                "analyze_cohort",
                "search_users",
                "generate_report",
                "generate_recommendations",
            ]

            for func_name in function_names:
                if func_name in namespace:
                    self.ml_functions[func_name] = namespace[func_name]

            print(f"✓ Loaded {len(self.ml_functions)} ML functions")

        except Exception as e:
            print(f"Error loading ML functions: {e}")
            raise

    def setup_routes(self):
        """Setup Flask routes using ML callbacks"""

        @self.app.route("/")
        def index():
            """API information endpoint"""
            return jsonify(
                {
                    "name": "ML-Powered User API",
                    "version": "1.0",
                    "description": "User management and analytics API with ML backend",
                    "endpoints": {
                        "POST /api/users/validate": "Validate user data",
                        "POST /api/users/score": "Calculate user score",
                        "POST /api/analytics/cohort": "Analyze user cohort",
                        "POST /api/users/search": "Search users",
                        "POST /api/analytics/report": "Generate analytics report",
                    },
                }
            )

        @self.app.route("/api/users/validate", methods=["POST"])
        def validate_user():
            """Validate user data using ML validation logic"""
            try:
                user_data = request.json
                if not user_data:
                    return jsonify({"error": "No user data provided"}), 400

                # Call ML validation function
                validation_result = self.ml_functions["validate_user"](user_data)

                if validation_result["valid"]:
                    return jsonify(
                        {"valid": True, "message": "User data is valid"}
                    ), 200
                else:
                    return jsonify(
                        {"valid": False, "errors": validation_result["errors"]}
                    ), 400

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/users/score", methods=["POST"])
        def calculate_score():
            """Calculate user score using ML scoring algorithm"""
            try:
                activity_data = request.json
                if not activity_data:
                    return jsonify({"error": "No activity data provided"}), 400

                # Call ML scoring function
                score_result = self.ml_functions["calculate_user_score"](
                    activity_data
                )

                return jsonify(score_result), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/analytics/cohort", methods=["POST"])
        def analyze_cohort():
            """Analyze user cohort using ML analytics"""
            try:
                users = request.json.get("users", [])
                if not users:
                    return jsonify({"error": "No users provided"}), 400

                # Call ML cohort analysis function
                analysis_result = self.ml_functions["analyze_cohort"](users)

                if analysis_result is None:
                    return jsonify({"error": "Analysis failed - no data"}), 400

                return jsonify(analysis_result), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/users/search", methods=["POST"])
        def search_users():
            """Search users using ML filtering logic"""
            try:
                data = request.json
                users = data.get("users", [])
                criteria = data.get("criteria", {})

                if not users:
                    return jsonify({"error": "No users provided"}), 400

                # Call ML search function
                search_results = self.ml_functions["search_users"](users, criteria)

                return jsonify({"results": search_results, "count": len(search_results)}), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/analytics/report", methods=["POST"])
        def generate_report():
            """Generate analytics report using ML report generation"""
            try:
                data = request.json
                users = data.get("users", [])
                time_period = data.get("period", "current")

                if not users:
                    return jsonify({"error": "No users provided"}), 400

                # Call ML report generation function
                report = self.ml_functions["generate_report"](users, time_period)

                if not report.get("success", False):
                    return jsonify({"error": report.get("error", "Report generation failed")}), 400

                return jsonify(report), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/health")
        def health():
            """Health check endpoint"""
            return jsonify(
                {
                    "status": "healthy",
                    "ml_functions_loaded": len(self.ml_functions),
                    "functions": list(self.ml_functions.keys()),
                }
            )

    def run(self, **kwargs):
        """Run the Flask application"""
        self.app.run(**kwargs)


def main():
    """Run the API server"""
    # Get ML file path
    ml_file = Path(__file__).parent / "ml_api.ml"

    # Create API instance
    api = MLFlaskAPI(ml_file)

    # Run server
    print("Starting ML-powered Flask API...")
    print("API documentation available at http://127.0.0.1:5000/")
    print("Health check at http://127.0.0.1:5000/health")
    api.run(debug=True, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
