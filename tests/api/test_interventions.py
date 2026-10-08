"""
API Test: Closed-Loop Intervention OS Lifecycle.
Asserts that /api/v1/advisors/me/interventions returns seeded records,
and supports full create and status update lifecycle.
"""

import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_list_interventions_returns_seeded_data():
    response = client.get("/api/v1/advisors/me/interventions")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert "meta" in json_data
    items = json_data["data"]
    # Verify at least the 7 simulated demo interventions exist
    assert len(items) >= 7
    first = items[0]
    assert "id" in first
    assert "student_ref" in first
    assert "action_code" in first
    assert "status" in first
    assert first["status"] in ["OPEN", "IN_PROGRESS", "COMPLETED"]


def test_intervention_crud_lifecycle():
    # 1. Create a new intervention
    create_payload = {
        "student_ref": "stu_2be31afe7f2b",
        "action_code": "LOW_ATTENDANCE",
        "notes": "[SIMULATED/DEMO] Temporary verification check-in",
    }
    create_res = client.post("/api/v1/advisors/me/interventions", json=create_payload)
    assert create_res.status_code == 200
    created = create_res.json()["data"]
    intervention_id = created["id"]
    assert created["action_code"] == "LOW_ATTENDANCE"

    # 2. Update status to IN_PROGRESS
    patch_res1 = client.patch(
        f"/api/v1/advisors/me/interventions/{intervention_id}",
        json={"status": "IN_PROGRESS", "notes": "[SIMULATED/DEMO] Student contacted"},
    )
    assert patch_res1.status_code == 200
    assert patch_res1.json()["data"]["status"] == "IN_PROGRESS"

    # 3. Update status to COMPLETED
    patch_res2 = client.patch(
        f"/api/v1/advisors/me/interventions/{intervention_id}",
        json={"status": "COMPLETED"},
    )
    assert patch_res2.status_code == 200
    assert patch_res2.json()["data"]["status"] == "COMPLETED"

    # 4. Cleanup temporary intervention from local test DB
    from adapters.postgres.repository import SessionLocal
    from adapters.postgres.models import Intervention
    db = SessionLocal()
    try:
        db.query(Intervention).filter(Intervention.id == intervention_id).delete()
        db.commit()
    finally:
        db.close()


def test_update_nonexistent_intervention_returns_404():
    patch_res = client.patch(
        "/api/v1/advisors/me/interventions/non-existent-uuid-9999",
        json={"status": "COMPLETED"},
    )
    assert patch_res.status_code == 404
    body = patch_res.json()
    assert "error" in body
    assert body["error"]["code"] == "HTTP_404"
