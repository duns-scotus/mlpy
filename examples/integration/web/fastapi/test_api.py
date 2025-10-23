"""
Integration tests for FastAPI ML Analytics
Tests async API endpoints and ML business logic
"""

import sys
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

# Add mlpy to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from examples.integration.web.fastapi.app import create_app


@pytest.fixture
def client():
    """Create FastAPI test client"""
    app = create_app()
    return TestClient(app)


class TestHealthAndInfo:
    """Test health check and info endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert data["name"] == "ML Analytics API"
        assert "endpoints" in data

    def test_health_endpoint(self, client):
        """Test health check"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["ml_functions_loaded"] == 6
        assert data["executor_workers"] == 4


class TestEventProcessing:
    """Test event processing endpoints"""

    def test_process_single_event(self, client):
        """Test processing a single event"""
        event = {
            "id": "evt_001",
            "type": "page_view",
            "user_id": "user_123",
            "data": {"page": "/home", "duration": 45}
        }

        response = client.post("/events/process", json=event)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "event" in data
        assert data["event"]["type"] == "page_view"
        assert data["event"]["category"] == "engagement"
        assert data["event"]["priority"] == 1

    def test_process_purchase_event(self, client):
        """Test processing purchase event gets correct category"""
        event = {
            "id": "evt_002",
            "type": "purchase",
            "user_id": "user_456",
            "data": {"amount": 99.99}
        }

        response = client.post("/events/process", json=event)
        assert response.status_code == 200

        data = response.json()
        assert data["event"]["category"] == "conversion"
        assert data["event"]["priority"] == 3

    def test_process_error_event(self, client):
        """Test processing error event gets high priority"""
        event = {
            "id": "evt_003",
            "type": "error",
            "user_id": "user_789",
            "data": {"error_code": 500}
        }

        response = client.post("/events/process", json=event)
        assert response.status_code == 200

        data = response.json()
        assert data["event"]["category"] == "technical"
        assert data["event"]["priority"] == 5

    def test_process_event_missing_type(self, client):
        """Test processing event without type fails"""
        event = {
            "id": "evt_004",
            "user_id": "user_999"
        }

        response = client.post("/events/process", json=event)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is False
        assert "error" in data

    def test_submit_event_stores_it(self, client):
        """Test submitting event stores it in event store"""
        # Clear events first
        client.delete("/events")

        event = {
            "id": "evt_stored",
            "type": "page_view",
            "user_id": "user_123",
            "data": {}
        }

        response = client.post("/events", json=event)
        assert response.status_code == 200

        # Verify it was stored
        response = client.get("/events")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1


class TestMetricsCalculation:
    """Test metrics calculation endpoint"""

    def test_metrics_empty_events(self, client):
        """Test metrics with no events"""
        # Clear events
        client.delete("/events")

        response = client.post("/metrics")
        assert response.status_code == 200

        data = response.json()
        assert data["total_events"] == 0
        assert data["by_type"] == {}
        assert data["high_priority"] == 0

    def test_metrics_with_events(self, client):
        """Test metrics calculation with sample events"""
        # Clear and populate events
        client.delete("/events")

        events = [
            {"id": "e1", "type": "page_view", "category": "engagement", "priority": 1},
            {"id": "e2", "type": "page_view", "category": "engagement", "priority": 1},
            {"id": "e3", "type": "purchase", "category": "conversion", "priority": 3},
            {"id": "e4", "type": "error", "category": "technical", "priority": 5},
        ]

        # Submit events
        for event in events:
            client.post("/events", json=event)

        # Calculate metrics
        response = client.post("/metrics")
        assert response.status_code == 200

        data = response.json()
        assert data["total_events"] == 4
        assert data["by_type"]["page_view"] == 2
        assert data["by_type"]["purchase"] == 1
        assert data["by_type"]["error"] == 1
        assert data["high_priority"] == 1  # Only error event has priority >= 4


class TestDashboardGeneration:
    """Test dashboard generation endpoint"""

    def test_dashboard_with_sample_events(self, client):
        """Test dashboard generation with sample data"""
        events = [
            {"id": "e1", "type": "page_view", "category": "engagement", "priority": 1, "user_id": "u1"},
            {"id": "e2", "type": "page_view", "category": "engagement", "priority": 1, "user_id": "u2"},
            {"id": "e3", "type": "purchase", "category": "conversion", "priority": 3, "user_id": "u1"},
            {"id": "e4", "type": "error", "category": "technical", "priority": 5, "user_id": "u3"},
        ]

        response = client.post(
            "/dashboard",
            json={"events": events, "time_range": "test_period"}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["time_range"] == "test_period"
        assert data["total_events"] == 4
        assert "health_status" in data
        assert "engagement_score" in data
        assert "conversion_rate" in data
        assert "metrics" in data
        assert "anomalies" in data

    def test_dashboard_no_events_fails(self, client):
        """Test dashboard generation without events fails"""
        response = client.post(
            "/dashboard",
            json={"events": [], "time_range": "empty"}
        )

        assert response.status_code == 400


class TestAnomalyDetection:
    """Test anomaly detection endpoint"""

    def test_anomaly_detection_clean(self, client):
        """Test anomaly detection with clean data"""
        events = [
            {"id": f"e{i}", "type": "page_view", "user_id": f"user_{i}", "priority": 1}
            for i in range(10)
        ]

        response = client.post(
            "/anomalies",
            json=events,
            params={"threshold": 50.0}  # High threshold
        )

        assert response.status_code == 200
        data = response.json()

        # With no errors and different users, should be clean
        assert "anomaly_count" in data
        assert "anomalies" in data
        assert "clean" in data

    def test_anomaly_detection_error_spike(self, client):
        """Test anomaly detection catches error spikes"""
        # Create events with high error rate
        events = [
            {"id": f"e{i}", "type": "error", "user_id": f"user_{i}", "priority": 5}
            for i in range(8)
        ] + [
            {"id": "e8", "type": "page_view", "user_id": "user_8", "priority": 1},
            {"id": "e9", "type": "page_view", "user_id": "user_9", "priority": 1},
        ]

        response = client.post(
            "/anomalies",
            json=events,
            params={"threshold": 10.0}  # Low threshold
        )

        assert response.status_code == 200
        data = response.json()

        # 80% error rate should trigger anomaly
        assert data["clean"] is False
        assert data["anomaly_count"] > 0


class TestEventFiltering:
    """Test event filtering endpoint"""

    def test_filter_by_type(self, client):
        """Test filtering events by type"""
        events = [
            {"id": "e1", "type": "page_view", "category": "engagement", "priority": 1},
            {"id": "e2", "type": "purchase", "category": "conversion", "priority": 3},
            {"id": "e3", "type": "page_view", "category": "engagement", "priority": 1},
        ]

        response = client.post(
            "/filter",
            json={
                "events": events,
                "filters": {"type": "page_view"}
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2

    def test_filter_by_priority(self, client):
        """Test filtering events by minimum priority"""
        events = [
            {"id": "e1", "type": "page_view", "category": "engagement", "priority": 1},
            {"id": "e2", "type": "purchase", "category": "conversion", "priority": 3},
            {"id": "e3", "type": "error", "category": "technical", "priority": 5},
        ]

        response = client.post(
            "/filter",
            json={
                "events": events,
                "filters": {"min_priority": 3}
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2  # purchase and error

    def test_filter_by_category(self, client):
        """Test filtering events by category"""
        events = [
            {"id": "e1", "type": "page_view", "category": "engagement", "priority": 1},
            {"id": "e2", "type": "purchase", "category": "conversion", "priority": 3},
            {"id": "e3", "type": "page_view", "category": "engagement", "priority": 1},
        ]

        response = client.post(
            "/filter",
            json={
                "events": events,
                "filters": {"category": "engagement"}
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2


class TestAggregation:
    """Test time window aggregation endpoint"""

    def test_aggregation_by_window(self, client):
        """Test aggregating events by time window"""
        events = [
            {"id": f"e{i}", "type": "page_view", "category": "engagement", "priority": 1}
            for i in range(15)
        ]

        response = client.post(
            "/aggregate",
            json={
                "events": events,
                "window_size": 5
            }
        )

        assert response.status_code == 200
        data = response.json()

        # 15 events with window size 5 = 3 windows
        assert data["window_count"] == 3
        assert len(data["windows"]) == 3

        for window in data["windows"]:
            assert "window_id" in window
            assert "event_count" in window
            assert "metrics" in window

    def test_aggregation_partial_window(self, client):
        """Test aggregation with partial final window"""
        events = [
            {"id": f"e{i}", "type": "page_view", "category": "engagement", "priority": 1}
            for i in range(12)
        ]

        response = client.post(
            "/aggregate",
            json={
                "events": events,
                "window_size": 5
            }
        )

        assert response.status_code == 200
        data = response.json()

        # 12 events with window size 5 = 2 full windows + 1 partial window = 3 windows
        assert data["window_count"] == 3


class TestEventStore:
    """Test event store management"""

    def test_get_events(self, client):
        """Test retrieving stored events"""
        response = client.get("/events")
        assert response.status_code == 200

        data = response.json()
        assert "total" in data
        assert "events" in data

    def test_clear_events(self, client):
        """Test clearing event store"""
        response = client.delete("/events")
        assert response.status_code == 200

        data = response.json()
        assert data["count"] == 0

        # Verify events are cleared
        response = client.get("/events")
        data = response.json()
        assert data["total"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
