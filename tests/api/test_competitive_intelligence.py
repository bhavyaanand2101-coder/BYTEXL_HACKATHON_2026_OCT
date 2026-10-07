"""
API test suite for Competitive Feature Intelligence Module.
Validates overview, competitor profiles, categories, feature matrix, gap analysis,
advantage comparison, and closed-loop workflow endpoints.
"""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_competitive_overview():
    res = client.get("/api/v1/competitive/overview")
    assert res.status_code == 200
    body = res.json()
    assert "data" in body
    assert "meta" in body
    data = body["data"]
    assert "hero" in data
    assert "stat_cards" in data
    assert len(data["stat_cards"]) == 4
    assert data["stat_cards"][0]["value"] == "9"  # 9 competitors


def test_list_competitors():
    res = client.get("/api/v1/competitive/competitors")
    assert res.status_code == 200
    body = res.json()
    competitors = body["data"]["competitors"]
    assert len(competitors) == 9
    comp_names = [c["name"] for c in competitors]
    assert "CodeTantra" in comp_names
    assert "iamneo" in comp_names
    assert "AccioJob" in comp_names
    assert "SixPhrase" in comp_names
    assert "Talentely" in comp_names
    assert "Hitbullseye" in comp_names
    assert "FACE Prep" in comp_names
    assert "EduGorilla" in comp_names
    assert "Edunet Foundation" in comp_names


def test_single_competitor_detail():
    res = client.get("/api/v1/competitive/competitors/codetantra")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["name"] == "CodeTantra"
    assert "relationship_to_campuspulse" in data
    assert "strongest_capabilities" in data

    res404 = client.get("/api/v1/competitive/competitors/non_existent_id")
    assert res404.status_code == 404
    assert "error" in res404.json()


def test_categories_and_matrix():
    res_cats = client.get("/api/v1/competitive/categories")
    assert res_cats.status_code == 200
    cats = res_cats.json()["data"]["categories"]
    assert len(cats) == 17

    res_matrix = client.get("/api/v1/competitive/matrix?category_id=coding")
    assert res_matrix.status_code == 200
    matrix_items = res_matrix.json()["data"]["matrix"]
    assert len(matrix_items) > 0
    # Every item should have competitor_name, feature_name, and status
    assert "status" in matrix_items[0]
    assert "evidence" in matrix_items[0]


def test_gap_analysis_and_advantage():
    res_gaps = client.get("/api/v1/competitive/gaps")
    assert res_gaps.status_code == 200
    gaps = res_gaps.json()["data"]["core_gaps"]
    assert len(gaps) == 10
    assert any(g["name"] == "Universal Student Intelligence Layer" for g in gaps)
    assert any(g["name"] == "Closed-Loop Student Support Cycle" for g in gaps)

    res_adv = client.get("/api/v1/competitive/advantage")
    assert res_adv.status_code == 200
    data = res_adv.json()["data"]
    assert "comparison" in data
    assert len(data["comparison"]["campuspulse"]) == 8
    assert len(data["workflow_steps"]) == 7


def test_closed_loop_workflow():
    res = client.get("/api/v1/competitive/workflow")
    assert res.status_code == 200
    steps = res.json()["data"]["steps"]
    assert len(steps) == 7
    step_names = [s["name"] for s in steps]
    assert step_names == ["Detect", "Explain", "Recommend", "Assign", "Intervene", "Measure", "Learn"]
