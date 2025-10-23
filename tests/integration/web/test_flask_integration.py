"""
Automated test for Flask integration example.
Verifies that the Flask API works correctly with the sys.modules fix.
"""

import sys
from pathlib import Path
import time
import threading
import requests

# Add mlpy to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("FLASK INTEGRATION TEST")
print("=" * 80)

# Import Flask app
from examples.integration.web.flask.app import MLFlaskAPI

print("\n[Step 1] Initializing Flask API with ML backend")
print("-" * 80)

try:
    ml_file = Path(__file__).parent / "examples/integration/web/flask/ml_api.ml"
    api = MLFlaskAPI(ml_file)
    print(f"[OK] Flask API initialized successfully")
    print(f"  ML functions loaded: {len(api.ml_functions)}")
    print(f"  Functions: {list(api.ml_functions.keys())}")
except Exception as e:
    print(f"[FAIL] Failed to initialize Flask API: {e}")
    sys.exit(1)

# Start Flask server in background thread
print("\n[Step 2] Starting Flask server")
print("-" * 80)

server_ready = threading.Event()

def run_server():
    try:
        api.run(debug=False, host="127.0.0.1", port=5001, use_reloader=False)
    except Exception as e:
        print(f"Server error: {e}")

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Wait for server to start
time.sleep(2)
print("[OK] Flask server started on http://127.0.0.1:5001")

# Test endpoints
print("\n[Step 3] Testing Flask API Endpoints")
print("-" * 80)

base_url = "http://127.0.0.1:5001"
test_results = []

# Test 1: Health check
print("\n[Test 1] Health Check")
try:
    response = requests.get(f"{base_url}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Health check passed")
        print(f"  Status: {data.get('status')}")
        print(f"  ML functions loaded: {data.get('ml_functions_loaded')}")
        test_results.append(("Health Check", True))
    else:
        print(f"[FAIL] Health check failed: {response.status_code}")
        test_results.append(("Health Check", False))
except Exception as e:
    print(f"[FAIL] Health check error: {e}")
    test_results.append(("Health Check", False))

# Test 2: Validate user
print("\n[Test 2] Validate User Endpoint")
try:
    test_user = {
        "username": "john_doe",
        "email": "john@example.com",
        "age": 25
    }
    response = requests.post(f"{base_url}/api/users/validate", json=test_user, timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] User validation passed")
        print(f"  Valid: {data.get('valid')}")
        print(f"  Message: {data.get('message')}")
        test_results.append(("Validate User", True))
    else:
        print(f"[FAIL] User validation failed: {response.status_code}")
        print(f"  Response: {response.text}")
        test_results.append(("Validate User", False))
except Exception as e:
    print(f"[FAIL] User validation error: {e}")
    test_results.append(("Validate User", False))

# Test 3: Calculate user score
print("\n[Test 3] Calculate User Score Endpoint")
try:
    activity_data = {
        "posts": 10,
        "comments": 50,
        "likes_received": 100,
        "days_active": 30
    }
    response = requests.post(f"{base_url}/api/users/score", json=activity_data, timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Score calculation passed")
        print(f"  Score: {data.get('score')}")
        print(f"  Level: {data.get('level')}")
        test_results.append(("Calculate Score", True))
    else:
        print(f"[FAIL] Score calculation failed: {response.status_code}")
        test_results.append(("Calculate Score", False))
except Exception as e:
    print(f"[FAIL] Score calculation error: {e}")
    test_results.append(("Calculate Score", False))

# Test 4: Search users
print("\n[Test 4] Search Users Endpoint")
try:
    search_data = {
        "users": [
            {"username": "alice", "age": 25, "score": 450},
            {"username": "bob", "age": 30, "score": 300},
            {"username": "charlie", "age": 20, "score": 500}
        ],
        "criteria": {
            "min_score": 400
        }
    }
    response = requests.post(f"{base_url}/api/users/search", json=search_data, timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] User search passed")
        print(f"  Results found: {data.get('count')}")
        print(f"  Users: {[u.get('username') for u in data.get('results', [])]}")
        test_results.append(("Search Users", True))
    else:
        print(f"[FAIL] User search failed: {response.status_code}")
        test_results.append(("Search Users", False))
except Exception as e:
    print(f"[FAIL] User search error: {e}")
    test_results.append(("Search Users", False))

# Summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

passed = sum(1 for _, result in test_results if result)
total = len(test_results)

for test_name, result in test_results:
    status = "[OK]" if result else "[FAIL]"
    print(f"  {status} {test_name}")

print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

if passed == total:
    print("\n[SUCCESS] All Flask integration tests passed!")
    print("The sys.modules fix is working correctly with Flask integration.")
    sys.exit(0)
else:
    print(f"\n[FAILURE] {total - passed} test(s) failed")
    sys.exit(1)
