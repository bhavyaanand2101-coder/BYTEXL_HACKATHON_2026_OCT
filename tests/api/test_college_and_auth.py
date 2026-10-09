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


def test_login_and_signin_endpoints():
    res_login = client.get("/login")
    assert res_login.status_code == 200
    assert "CampusPulse" in res_login.text

    res_signin = client.get("/signin")
    assert res_signin.status_code == 200
    assert "CampusPulse" in res_signin.text


def test_firebase_config_endpoint():
    res = client.get("/api/v1/auth/firebase-config")
    assert res.status_code == 200
    json_data = res.json()
    assert "data" in json_data
    d = json_data["data"]
    assert d["firebase_enabled"] is True
    assert "apiKey" in d and len(d["apiKey"]) > 10
    assert "projectId" in d and d["projectId"] == "hackxl"
    assert "authDomain" in d and "firebase" in d["authDomain"]


def test_preset_ingestion_returns_summary_and_records_sample():
    res = client.post("/api/v1/ingest/preset/section_c")
    assert res.status_code == 200
    json_data = res.json()
    assert "data" in json_data
    d = json_data["data"]
    assert d["processed_students"] > 0
    assert "processed_summary" in d
    assert "records_sample" in d
    assert len(d["records_sample"]) > 0
    sample = d["records_sample"][0]
    assert "student_ref" in sample
    assert "success_score" in sample
    assert "tier" in sample
    assert "segment" in sample


def test_custom_sheet_upload_ingestion():
    csv_content = b"Roll No,Student Name,Marks,Branch,Section\n251309901,Test Student One,21.5,CSE,C\n251309902,Test Student Two,14.0,CSE,C\n"
    files = {"file": ("test_upload_roster.csv", csv_content, "text/csv")}
    try:
        res = client.post("/api/v1/ingest/upload", files=files)
        assert res.status_code == 200
        json_data = res.json()
        assert "data" in json_data
        d = json_data["data"]
        assert d["processed_students"] == 2
        assert "records_sample" in d
        assert len(d["records_sample"]) == 2
        assert d["records_sample"][0]["roll_number"] in ["251309901", "251309902"]
    finally:
        from pathlib import Path
        Path("data/raw/test_upload_roster.csv").unlink(missing_ok=True)


