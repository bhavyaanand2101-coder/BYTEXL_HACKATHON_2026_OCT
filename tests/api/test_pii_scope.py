"""
API Test: PII Scope Protection.
Asserts that student identifiers (roll_number, name) are never exposed inappropriately.
"""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_metrics_never_contain_pii():
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    text = response.text
    # Verify no student names or student refs in prometheus metrics
    assert "stu_" not in text
    assert "roll_number" not in text
    assert "student_ref" not in text


def test_health_check_non_pii():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["status"] == "healthy"
    assert "roll_number" not in str(data)
