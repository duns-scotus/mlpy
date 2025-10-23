"""
Test client for ML-powered FastAPI Analytics
Demonstrates async interaction with ML-backed endpoints
"""

import asyncio
import httpx
from pprint import pprint
import random
import time


class AsyncAPIClient:
    """Async client for testing the ML FastAPI"""

    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    async def test_health(self):
        """Test health check endpoint"""
        print("\n" + "=" * 60)
        print("TEST 0: Health Check")
        print("=" * 60)

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/health")
            print(f"Status: {response.status_code}")
            pprint(response.json())

    async def test_process_event(self):
        """Test single event processing"""
        print("\n" + "=" * 60)
        print("TEST 1: Process Single Event")
        print("=" * 60)

        event = {
            "id": "evt_001",
            "type": "page_view",
            "user_id": "user_123",
            "data": {"page": "/home", "duration": 45}
        }

        print(f"\nProcessing event: {event['type']}")
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/events/process", json=event)
            print(f"Status: {response.status_code}")
            pprint(response.json())

    async def test_submit_multiple_events(self):
        """Test submitting multiple events concurrently"""
        print("\n" + "=" * 60)
        print("TEST 2: Submit Multiple Events (Async)")
        print("=" * 60)

        # Create varied events
        events = [
            {"id": f"evt_{i:03d}", "type": random.choice(["page_view", "purchase", "error"]),
             "user_id": f"user_{random.randint(1, 10):03d}",
             "data": {"value": random.randint(1, 100)}}
            for i in range(20)
        ]

        print(f"\nSubmitting {len(events)} events concurrently...")
        start_time = time.time()

        async with httpx.AsyncClient() as client:
            # Submit all events concurrently
            tasks = [
                client.post(f"{self.base_url}/events", json=event)
                for event in events
            ]
            responses = await asyncio.gather(*tasks)

        elapsed = time.time() - start_time
        print(f"Submitted {len(events)} events in {elapsed:.2f}s")
        print(f"Average: {elapsed/len(events)*1000:.2f}ms per event")

        success_count = sum(1 for r in responses if r.status_code == 200)
        print(f"Success: {success_count}/{len(events)}")

    async def test_metrics(self):
        """Test metrics calculation"""
        print("\n" + "=" * 60)
        print("TEST 3: Calculate Metrics")
        print("=" * 60)

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/metrics")
            print(f"Status: {response.status_code}")
            pprint(response.json())

    async def test_dashboard(self):
        """Test dashboard generation"""
        print("\n" + "=" * 60)
        print("TEST 4: Generate Dashboard")
        print("=" * 60)

        async with httpx.AsyncClient() as client:
            # Get stored events first
            events_response = await client.get(f"{self.base_url}/events")
            events = events_response.json()["events"]

            if not events:
                print("No events stored, submitting sample events first...")
                await self.test_submit_multiple_events()
                events_response = await client.get(f"{self.base_url}/events")
                events = events_response.json()["events"]

            # Generate dashboard
            response = await client.post(
                f"{self.base_url}/dashboard",
                json={"events": events, "time_range": "test_period"}
            )
            print(f"Status: {response.status_code}")
            pprint(response.json())

    async def test_anomaly_detection(self):
        """Test anomaly detection"""
        print("\n" + "=" * 60)
        print("TEST 5: Anomaly Detection")
        print("=" * 60)

        async with httpx.AsyncClient() as client:
            # Get stored events
            events_response = await client.get(f"{self.base_url}/events")
            events = events_response.json()["events"]

            if not events:
                print("No events to analyze")
                return

            # Detect anomalies
            response = await client.post(
                f"{self.base_url}/anomalies",
                params={"threshold": 5.0}
            )
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"\nAnomaly Count: {result['anomaly_count']}")
            print(f"Clean: {result['clean']}")
            if result['anomalies']:
                print("\nDetected Anomalies:")
                for anomaly in result['anomalies'][:5]:  # Show first 5
                    print(f"  - {anomaly}")

    async def test_filtering(self):
        """Test event filtering"""
        print("\n" + "=" * 60)
        print("TEST 6: Event Filtering")
        print("=" * 60)

        async with httpx.AsyncClient() as client:
            # Get stored events
            events_response = await client.get(f"{self.base_url}/events")
            events = events_response.json()["events"]

            if not events:
                print("No events to filter")
                return

            # Filter for high priority events
            print("\n1. Filtering for high priority events (priority >= 4):")
            response = await client.post(
                f"{self.base_url}/filter",
                json={
                    "events": events,
                    "filters": {"min_priority": 4}
                }
            )
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Found {result['count']} high priority events")

            # Filter by type
            print("\n2. Filtering for 'purchase' events:")
            response = await client.post(
                f"{self.base_url}/filter",
                json={
                    "events": events,
                    "filters": {"type": "purchase"}
                }
            )
            result = response.json()
            print(f"Found {result['count']} purchase events")

    async def test_aggregation(self):
        """Test time window aggregation"""
        print("\n" + "=" * 60)
        print("TEST 7: Time Window Aggregation")
        print("=" * 60)

        async with httpx.AsyncClient() as client:
            # Get stored events
            events_response = await client.get(f"{self.base_url}/events")
            events = events_response.json()["events"]

            if not events:
                print("No events to aggregate")
                return

            # Aggregate by windows of 5 events
            response = await client.post(
                f"{self.base_url}/aggregate",
                json={
                    "events": events,
                    "window_size": 5
                }
            )
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"\nCreated {result['window_count']} time windows")
            print("\nWindow Summary:")
            for window in result['windows']:
                print(f"  Window {window['window_id']}: {window['event_count']} events")

    async def test_concurrent_operations(self):
        """Test multiple concurrent operations"""
        print("\n" + "=" * 60)
        print("TEST 8: Concurrent Operations")
        print("=" * 60)

        print("\nRunning metrics, dashboard, and anomaly detection concurrently...")
        start_time = time.time()

        async with httpx.AsyncClient(timeout=30.0) as client:
            # Get events first
            events_response = await client.get(f"{self.base_url}/events")
            events = events_response.json()["events"]

            if not events:
                print("No events available")
                return

            # Run multiple operations concurrently
            tasks = [
                client.post(f"{self.base_url}/metrics"),
                client.post(f"{self.base_url}/dashboard",
                           json={"events": events, "time_range": "concurrent_test"}),
                client.post(f"{self.base_url}/anomalies", params={"threshold": 10.0}),
            ]

            responses = await asyncio.gather(*tasks)

        elapsed = time.time() - start_time
        print(f"\nCompleted 3 operations in {elapsed:.2f}s")
        print(f"All operations successful: {all(r.status_code == 200 for r in responses)}")

    async def run_all_tests(self):
        """Run all tests in sequence"""
        try:
            await self.test_health()
            await self.test_process_event()

            # Clear events before bulk test
            async with httpx.AsyncClient() as client:
                await client.delete(f"{self.base_url}/events")

            await self.test_submit_multiple_events()
            await self.test_metrics()
            await self.test_dashboard()
            await self.test_anomaly_detection()
            await self.test_filtering()
            await self.test_aggregation()
            await self.test_concurrent_operations()

            print("\n" + "=" * 60)
            print("ALL TESTS COMPLETED SUCCESSFULLY")
            print("=" * 60)

        except httpx.ConnectError:
            print("\n ERROR: Could not connect to API server.")
            print("Make sure the FastAPI server is running:")
            print("  python app.py")
            print("  OR: uvicorn app:app --reload")
        except Exception as e:
            print(f"\n ERROR: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Run the async test client"""
    print("ML FastAPI Analytics Test Client")
    print("Make sure the FastAPI server is running first!")
    print("Command: python app.py")
    print("   OR:   uvicorn app:app --reload")

    input("\nPress Enter to start tests...")

    client = AsyncAPIClient()
    asyncio.run(client.run_all_tests())


if __name__ == "__main__":
    main()
