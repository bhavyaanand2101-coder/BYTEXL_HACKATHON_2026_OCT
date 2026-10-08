import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_college_login_activity_endpoint():
    response = client.get("/api/v1/cohorts/login-activity")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    data = json_data["data"]
    assert data["total_students"] == 469
    assert data["total_batches"] == 7
    assert data["total_branches"] == 1
    assert data["total_educators"] == 2
    assert "inactive_alert" in data
    assert len(data["recent_active_students"]) > 0


def test_college_telemetry_endpoint():
    response = client.get("/api/v1/college/telemetry")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    d = json_data["data"]
    assert "editor" in d
    assert "nimbus" in d
    assert "labs" in d
    assert "assessments" in d
    assert "courses" in d
    assert "leaderboard" in d
    assert "live" in d
    assert "video" in d


def test_project_bank_branding_clean():
    response = client.get("/api/v1/projects/bank")
    assert response.status_code == 200
    json_data = response.json()
    projects = json_data["data"]
    for p in projects:
        assert "byteXL" not in p.get("partner", ""), f"Leftover byteXL in partner: {p}"


def test_admin_department_faculty_hierarchy():
    response = client.get("/api/v1/admin/department-faculty")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    d = json_data["data"]

    # Verify Dean (Superadmin)
    assert "dean" in d
    assert d["dean"]["name"] == "Prof. Rajesh Gupta"
    assert "Superadmin" in d["dean"]["role"]

    # Verify HOD (Admin)
    assert "hod" in d
    assert d["hod"]["name"] == "Dr. S. K. Venkatraman"
    assert "Admin" in d["hod"]["role"]
    assert d["hod"]["total_students"] == 469
    assert d["hod"]["total_faculty"] >= 4

    # Verify Teachers (Faculty) with assigned students under them
    assert "teachers" in d
    assert len(d["teachers"]) >= 4
    ananya = next((t for t in d["teachers"] if "Ananya" in t["name"]), None)
    assert ananya is not None
    assert ananya["assigned_students"] > 0
    assert any("Aarav" in m for m in ananya["key_mentees"])

    # Verify RBAC policies
    assert "rbac_policies" in d
    policies = {p["role"]: p for p in d["rbac_policies"]}
    assert "Full Access" in policies["Dean (Superadmin)"]["admin_portal"]
    assert "Full Access" in policies["HOD (Admin)"]["admin_portal"]
    assert "No Access (Hidden)" in policies["Teacher (Faculty)"]["admin_portal"]
    assert "No Access (Hidden)" in policies["Student"]["admin_portal"]

