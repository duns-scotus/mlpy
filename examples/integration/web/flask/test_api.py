"""
Integration tests for Flask ML API
Tests API endpoints and ML business logic
"""

import sys
import pytest
import json
from pathlib import Path

# Add mlpy to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from examples.integration.web.flask.app import MLFlaskAPI


@pytest.fixture
def app():
    """Create Flask test application"""
    ml_file = Path(__file__).parent / "ml_api.ml"
    api = MLFlaskAPI(ml_file)
    api.app.config['TESTING'] = True
    return api.app


@pytest.fixture
def client(app):
    """Create Flask test client"""
    return app.test_client()


class TestUserValidation:
    """Test user validation endpoint"""

    def test_valid_user(self, client):
        """Test validation with valid user data"""
        valid_user = {
            "username": "johndoe",
            "email": "john@example.com",
            "age": 25
        }

        response = client.post(
            '/api/users/validate',
            data=json.dumps(valid_user),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["valid"] is True

    def test_invalid_username_too_short(self, client):
        """Test validation with too short username"""
        invalid_user = {
            "username": "jo",
            "email": "john@example.com",
            "age": 25
        }

        response = client.post(
            '/api/users/validate',
            data=json.dumps(invalid_user),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["valid"] is False
        assert len(data["errors"]) > 0
        assert any("at least 3 characters" in err for err in data["errors"])

    def test_invalid_email(self, client):
        """Test validation with invalid email"""
        invalid_user = {
            "username": "johndoe",
            "email": "invalid-email",
            "age": 25
        }

        response = client.post(
            '/api/users/validate',
            data=json.dumps(invalid_user),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["valid"] is False
        assert len(data["errors"]) > 0

    def test_invalid_age_too_young(self, client):
        """Test validation with age too young"""
        invalid_user = {
            "username": "johndoe",
            "email": "john@example.com",
            "age": 10
        }

        response = client.post(
            '/api/users/validate',
            data=json.dumps(invalid_user),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["valid"] is False
        assert any("at least 13 years old" in err for err in data["errors"])

    def test_no_data(self, client):
        """Test validation with no data"""
        response = client.post('/api/users/validate')
        assert response.status_code == 400


class TestUserScoring:
    """Test user score calculation endpoint"""

    def test_score_calculation(self, client):
        """Test score calculation with normal activity"""
        activity = {
            "posts": 50,
            "comments": 120,
            "likes_received": 350,
            "reports": 0
        }

        response = client.post(
            '/api/users/score',
            data=json.dumps(activity),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)

        assert "score" in data
        assert "level" in data
        assert "breakdown" in data

        # Check calculation: 50*10 + 120*5 + 350*2 = 1800
        assert data["score"] == 1800
        assert data["level"] == 19  # floor(1800/100) + 1

    def test_score_with_penalties(self, client):
        """Test score calculation with report penalties"""
        activity = {
            "posts": 10,
            "comments": 20,
            "likes_received": 50,
            "reports": 3
        }

        response = client.post(
            '/api/users/score',
            data=json.dumps(activity),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)

        # 10*10 + 20*5 + 50*2 + 3*(-50) = 100 + 100 + 100 - 150 = 150
        assert data["score"] == 150

    def test_score_non_negative(self, client):
        """Test that score cannot go below zero"""
        activity = {
            "posts": 0,
            "comments": 0,
            "likes_received": 0,
            "reports": 10  # Large penalty
        }

        response = client.post(
            '/api/users/score',
            data=json.dumps(activity),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["score"] == 0  # Should be clamped to 0


class TestCohortAnalysis:
    """Test cohort analysis endpoint"""

    def test_cohort_analysis(self, client):
        """Test cohort analysis with sample users"""
        users = [
            {"username": "alice", "age": 24, "score": 450, "active": True},
            {"username": "bob", "age": 19, "score": 280, "active": True},
            {"username": "charlie", "age": 35, "score": 150, "active": False},
            {"username": "diana", "age": 42, "score": 620, "active": True},
        ]

        response = client.post(
            '/api/analytics/cohort',
            data=json.dumps({"users": users}),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data["total_users"] == 4
        assert data["active_users"] == 3
        assert data["activity_rate"] == 75.0
        assert 30 <= data["average_age"] <= 31
        assert 370 <= data["average_score"] <= 380

    def test_cohort_empty_users(self, client):
        """Test cohort analysis with no users"""
        response = client.post(
            '/api/analytics/cohort',
            data=json.dumps({"users": []}),
            content_type='application/json'
        )

        assert response.status_code == 400


class TestUserSearch:
    """Test user search endpoint"""

    def test_search_by_active_status(self, client):
        """Test searching for active users"""
        users = [
            {"username": "alice", "age": 24, "score": 450, "active": True},
            {"username": "bob", "age": 19, "score": 280, "active": True},
            {"username": "charlie", "age": 35, "score": 150, "active": False},
        ]

        response = client.post(
            '/api/users/search',
            data=json.dumps({
                "users": users,
                "criteria": {"active": True}
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["count"] == 2

    def test_search_by_age_range(self, client):
        """Test searching by age range"""
        users = [
            {"username": "alice", "age": 24, "score": 450, "active": True},
            {"username": "bob", "age": 19, "score": 280, "active": True},
            {"username": "charlie", "age": 35, "score": 150, "active": False},
        ]

        response = client.post(
            '/api/users/search',
            data=json.dumps({
                "users": users,
                "criteria": {"min_age": 20, "max_age": 30}
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["count"] == 1
        assert data["results"][0]["username"] == "alice"

    def test_search_by_minimum_score(self, client):
        """Test searching by minimum score"""
        users = [
            {"username": "alice", "age": 24, "score": 450, "active": True},
            {"username": "bob", "age": 19, "score": 280, "active": True},
            {"username": "charlie", "age": 35, "score": 150, "active": False},
        ]

        response = client.post(
            '/api/users/search',
            data=json.dumps({
                "users": users,
                "criteria": {"min_score": 300}
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["count"] == 1
        assert data["results"][0]["username"] == "alice"


class TestReportGeneration:
    """Test analytics report generation"""

    def test_report_generation(self, client):
        """Test generating analytics report"""
        users = [
            {"username": "alice", "age": 24, "score": 450, "active": True},
            {"username": "bob", "age": 19, "score": 280, "active": True},
            {"username": "charlie", "age": 35, "score": 150, "active": False},
            {"username": "diana", "age": 42, "score": 620, "active": True},
        ]

        response = client.post(
            '/api/analytics/report',
            data=json.dumps({
                "users": users,
                "period": "Q1 2025"
            }),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data["success"] is True
        assert data["period"] == "Q1 2025"
        assert "generated_at" in data
        assert "summary" in data
        assert "engagement" in data
        assert "recommendations" in data


class TestHealthCheck:
    """Test health check endpoint"""

    def test_health_endpoint(self, client):
        """Test health check returns correct status"""
        response = client.get('/health')

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data["status"] == "healthy"
        assert "ml_functions_loaded" in data
        assert data["ml_functions_loaded"] >= 6


class TestIndexEndpoint:
    """Test index/root endpoint"""

    def test_index(self, client):
        """Test index endpoint returns API info"""
        response = client.get('/')

        assert response.status_code == 200
        data = json.loads(response.data)

        assert "name" in data
        assert "version" in data
        assert "endpoints" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
