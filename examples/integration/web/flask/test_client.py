"""
Test client for ML-powered Flask API
Demonstrates how to interact with ML-backed endpoints
"""

import requests
import json
from pprint import pprint


class APIClient:
    """Client for testing the ML Flask API"""

    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url

    def test_validation(self):
        """Test user validation endpoint"""
        print("\n" + "=" * 60)
        print("TEST 1: User Validation")
        print("=" * 60)

        # Test valid user
        valid_user = {
            "username": "johndoe",
            "email": "john@example.com",
            "age": 25
        }

        print("\n1. Testing valid user:")
        print(f"Input: {json.dumps(valid_user, indent=2)}")
        response = requests.post(f"{self.base_url}/api/users/validate", json=valid_user)
        print(f"Status: {response.status_code}")
        pprint(response.json())

        # Test invalid user
        invalid_user = {
            "username": "jo",  # Too short
            "email": "invalid-email",  # Missing @ and .
            "age": 10  # Too young
        }

        print("\n2. Testing invalid user:")
        print(f"Input: {json.dumps(invalid_user, indent=2)}")
        response = requests.post(f"{self.base_url}/api/users/validate", json=invalid_user)
        print(f"Status: {response.status_code}")
        pprint(response.json())

    def test_scoring(self):
        """Test user score calculation endpoint"""
        print("\n" + "=" * 60)
        print("TEST 2: User Score Calculation")
        print("=" * 60)

        activity = {
            "posts": 50,
            "comments": 120,
            "likes_received": 350,
            "reports": 2
        }

        print("\nCalculating score for activity:")
        print(f"Input: {json.dumps(activity, indent=2)}")
        response = requests.post(f"{self.base_url}/api/users/score", json=activity)
        print(f"Status: {response.status_code}")
        pprint(response.json())

    def test_cohort_analysis(self):
        """Test cohort analysis endpoint"""
        print("\n" + "=" * 60)
        print("TEST 3: Cohort Analysis")
        print("=" * 60)

        users = [
            {"username": "alice", "age": 24, "score": 450, "active": True},
            {"username": "bob", "age": 19, "score": 280, "active": True},
            {"username": "charlie", "age": 35, "score": 150, "active": False},
            {"username": "diana", "age": 42, "score": 620, "active": True},
            {"username": "eve", "age": 28, "score": 310, "active": True},
            {"username": "frank", "age": 65, "score": 90, "active": False},
        ]

        print(f"\nAnalyzing cohort of {len(users)} users")
        response = requests.post(f"{self.base_url}/api/analytics/cohort", json={"users": users})
        print(f"Status: {response.status_code}")
        pprint(response.json())

    def test_search(self):
        """Test user search endpoint"""
        print("\n" + "=" * 60)
        print("TEST 4: User Search")
        print("=" * 60)

        users = [
            {"username": "alice_wonder", "age": 24, "score": 450, "active": True},
            {"username": "bob_builder", "age": 19, "score": 280, "active": True},
            {"username": "charlie_brown", "age": 35, "score": 150, "active": False},
            {"username": "diana_prince", "age": 42, "score": 620, "active": True},
            {"username": "eve_online", "age": 28, "score": 310, "active": True},
        ]

        # Search 1: Active users only
        print("\n1. Searching for active users:")
        criteria = {"active": True}
        print(f"Criteria: {json.dumps(criteria, indent=2)}")
        response = requests.post(
            f"{self.base_url}/api/users/search",
            json={"users": users, "criteria": criteria}
        )
        print(f"Status: {response.status_code}")
        results = response.json()
        print(f"Found {results['count']} users:")
        for user in results['results']:
            print(f"  - {user['username']}")

        # Search 2: High-scoring young users
        print("\n2. Searching for users aged 20-30 with score >= 300:")
        criteria = {"min_age": 20, "max_age": 30, "min_score": 300}
        print(f"Criteria: {json.dumps(criteria, indent=2)}")
        response = requests.post(
            f"{self.base_url}/api/users/search",
            json={"users": users, "criteria": criteria}
        )
        print(f"Status: {response.status_code}")
        results = response.json()
        print(f"Found {results['count']} users:")
        for user in results['results']:
            print(f"  - {user['username']} (age: {user['age']}, score: {user['score']})")

    def test_report_generation(self):
        """Test analytics report generation endpoint"""
        print("\n" + "=" * 60)
        print("TEST 5: Analytics Report Generation")
        print("=" * 60)

        users = [
            {"username": "alice", "age": 24, "score": 450, "active": True},
            {"username": "bob", "age": 19, "score": 280, "active": True},
            {"username": "charlie", "age": 35, "score": 150, "active": False},
            {"username": "diana", "age": 42, "score": 620, "active": True},
            {"username": "eve", "age": 28, "score": 310, "active": True},
            {"username": "frank", "age": 65, "score": 90, "active": False},
            {"username": "grace", "age": 31, "score": 520, "active": True},
            {"username": "henry", "age": 18, "score": 40, "active": False},
        ]

        print(f"\nGenerating report for {len(users)} users")
        response = requests.post(
            f"{self.base_url}/api/analytics/report",
            json={"users": users, "period": "Q1 2025"}
        )
        print(f"Status: {response.status_code}")
        pprint(response.json())

    def test_health(self):
        """Test health check endpoint"""
        print("\n" + "=" * 60)
        print("TEST 0: Health Check")
        print("=" * 60)

        response = requests.get(f"{self.base_url}/health")
        print(f"Status: {response.status_code}")
        pprint(response.json())

    def run_all_tests(self):
        """Run all API tests"""
        try:
            self.test_health()
            self.test_validation()
            self.test_scoring()
            self.test_cohort_analysis()
            self.test_search()
            self.test_report_generation()

            print("\n" + "=" * 60)
            print("ALL TESTS COMPLETED SUCCESSFULLY")
            print("=" * 60)

        except requests.exceptions.ConnectionError:
            print("\n ERROR: Could not connect to API server.")
            print("Make sure the Flask server is running: python app.py")
        except Exception as e:
            print(f"\n ERROR: {e}")


def main():
    """Run the test client"""
    print("ML Flask API Test Client")
    print("Make sure the Flask server is running first!")
    print("Command: python app.py")

    input("\nPress Enter to start tests...")

    client = APIClient()
    client.run_all_tests()


if __name__ == "__main__":
    main()
