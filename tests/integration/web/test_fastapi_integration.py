"""
Automated test for FastAPI integration example.
Verifies that the FastAPI app works correctly with the sys.modules fix.
"""

import sys
from pathlib import Path
import time
import threading
import requests

# Add mlpy to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("FASTAPI INTEGRATION TEST")
print("=" * 80)

# Import FastAPI app
from examples.integration.web.fastapi.app import create_app

print("\n[Step 1] Initializing FastAPI with ML backend")
print("-" * 80)

try:
    app = create_app()
    print(f"[OK] FastAPI app initialized successfully")
except Exception as e:
    print(f"[FAIL] Failed to initialize FastAPI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Start FastAPI server in background thread
print("\n[Step 2] Starting FastAPI server")
print("-" * 80)

def run_server():
    import uvicorn
    try:
        uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")
    except Exception as e:
        print(f"Server error: {e}")

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Wait for server to start
time.sleep(3)
print("[OK] FastAPI server started on http://127.0.0.1:8001")

# Test endpoints
print("\n[Step 3] Testing FastAPI Endpoints")
print("-" * 80)

base_url = "http://127.0.0.1:8001"
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
        print(f"  Executor workers: {data.get('executor_workers')}")
        test_results.append(("Health Check", True))
    else:
        print(f"[FAIL] Health check failed: {response.status_code}")
        test_results.append(("Health Check", False))
except Exception as e:
    print(f"[FAIL] Health check error: {e}")
    test_results.append(("Health Check", False))

# Test 2: Process event
print("\n[Test 2] Process Event Endpoint")
try:
    event = {
        "id": "test-001",
        "type": "user_action",
        "user_id": "user123",
        "data": {"action": "login", "platform": "web"}
    }
    response = requests.post(f"{base_url}/events/process", json=event, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Event processing passed")
        print(f"  Success: {data.get('success')}")
        if data.get('event'):
            print(f"  Event ID: {data['event'].get('id')}")
            print(f"  Category: {data['event'].get('category')}")
        test_results.append(("Process Event", True))
    else:
        print(f"[FAIL] Event processing failed: {response.status_code}")
        print(f"  Response: {response.text}")
        test_results.append(("Process Event", False))
except Exception as e:
    print(f"[FAIL] Event processing error: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("Process Event", False))

# Test 3: Submit and retrieve events
print("\n[Test 3] Submit Event and Retrieve")
try:
    # Submit event
    event = {
        "id": "test-002",
        "type": "purchase",
        "user_id": "user456",
        "data": {"amount": 99.99, "product": "widget"}
    }
    response = requests.post(f"{base_url}/events", json=event, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Event submission passed")
        print(f"  Success: {data.get('success')}")

        # Retrieve events
        response2 = requests.get(f"{base_url}/events?limit=10", timeout=5)
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"[OK] Event retrieval passed")
            print(f"  Total events: {data2.get('total')}")
            test_results.append(("Submit/Retrieve Events", True))
        else:
            print(f"[FAIL] Event retrieval failed: {response2.status_code}")
            test_results.append(("Submit/Retrieve Events", False))
    else:
        print(f"[FAIL] Event submission failed: {response.status_code}")
        test_results.append(("Submit/Retrieve Events", False))
except Exception as e:
    print(f"[FAIL] Submit/retrieve error: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("Submit/Retrieve Events", False))

# Test 4: Calculate metrics
print("\n[Test 4] Calculate Metrics Endpoint")
try:
    # Clear events first
    requests.delete(f"{base_url}/events", timeout=5)

    # Submit some events
    events_data = [
        {"id": "e1", "type": "user_action", "user_id": "u1", "data": {"score": 100}},
        {"id": "e2", "type": "error", "user_id": "u2", "data": {"error": "timeout"}},
        {"id": "e3", "type": "purchase", "user_id": "u1", "data": {"amount": 50}}
    ]

    for event in events_data:
        requests.post(f"{base_url}/events", json=event, timeout=10)

    # Calculate metrics
    response = requests.post(f"{base_url}/metrics", json=None, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Metrics calculation passed")
        print(f"  Total events: {data.get('total_events')}")
        print(f"  By type: {data.get('by_type')}")
        test_results.append(("Calculate Metrics", True))
    else:
        print(f"[FAIL] Metrics calculation failed: {response.status_code}")
        test_results.append(("Calculate Metrics", False))
except Exception as e:
    print(f"[FAIL] Metrics calculation error: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("Calculate Metrics", False))

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
    print("\n[SUCCESS] All FastAPI integration tests passed!")
    print("The sys.modules fix is working correctly with FastAPI integration.")
    sys.exit(0)
else:
    print(f"\n[FAILURE] {total - passed} test(s) failed")
    sys.exit(1)
