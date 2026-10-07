"""
API Test: Error Envelope Shape.
Asserts that all error responses (404, 422, etc.) return the mandatory { error: { code, message, hint } } envelope.
"""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_404_error_envelope():
    response = client.get("/api/v1/students/non_existent_ref_12345")
    assert response.status_code == 404
    body = response.json()
    assert "error" in body
    assert "code" in body["error"]
    assert "message" in body["error"]
    assert "hint" in body["error"]
    assert body["error"]["code"] == "HTTP_404"


def test_422_validation_error_envelope():
    # Sending invalid payload to what-if simulation endpoint
    response = client.post("/api/v1/what-if", json={"invalid_field": "test"})
    assert response.status_code == 422
    body = response.json()
    assert "error" in body
    assert "code" in body["error"]
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert "hint" in body["error"]


def test_success_envelope_shape():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert "meta" in body
    assert "config_hash" in body["meta"]
    assert "targets_hash" in body["meta"]
    assert "generated_at" in body["meta"]
