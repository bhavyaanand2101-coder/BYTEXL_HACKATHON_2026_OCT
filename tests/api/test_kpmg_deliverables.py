import pytest
from starlette.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_kpmg_deliverables_endpoint():
    response = client.get("/api/v1/kpmg/deliverables")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    d = json_data["data"]
    assert d["organizer"] == "KPMG in India"
    assert "mathematical_formulation_note" in d
    assert "pitch_deck" in d
    assert len(d["pitch_deck"]) == 7
    assert "evaluation_rubric_mapping" in d
    assert "data_integration" in d
    assert len(d["data_integration"]["sources"]) == 7


def test_kpmg_segmentation_matrix_endpoint():
    response = client.get("/api/v1/kpmg/segmentation-matrix")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    d = json_data["data"]
    assert "students" in d
    assert "quadrant_distribution" in d
    assert "Academic Stars with Placement Gap" in d["quadrant_distribution"]
    assert "Hustlers at Academic Risk" in d["quadrant_distribution"]
    assert "Quietly Disengaged" in d["quadrant_distribution"]
    assert "Struggling on All Fronts" in d["quadrant_distribution"]
    assert "Balanced" in d["quadrant_distribution"]


def test_kpmg_rubric_mapping():
    response = client.get("/api/v1/kpmg/deliverables")
    json_data = response.json()
    rubric = json_data["data"]["evaluation_rubric_mapping"]
    
    # 30% Data Integration, 25% Scoring, 25% Dashboard, 10% Problem Understanding, 10% Demo + Bonus
    criteria_names = [r["criterion"] for r in rubric]
    assert "Data Integration & Analysis" in criteria_names
    assert "Success Score & Risk Identification" in criteria_names
    assert "Dashboard & Visualization" in criteria_names
    assert "Problem Understanding" in criteria_names
    assert "Presentation & Demo" in criteria_names
    assert "Bonus: Student Segmentation" in criteria_names
    assert "Bonus: Explainable Score" in criteria_names


def test_health_db_and_ml():
    res_db = client.get("/health/db")
    assert res_db.status_code == 200
    assert res_db.json()["data"]["connected"] is True
    assert "students_count" in res_db.json()["data"]

    res_ml = client.get("/health/ml")
    assert res_ml.status_code == 200
    assert res_ml.json()["data"]["status"] == "healthy"
    assert "features" in res_ml.json()["data"]


def test_ml_layer_endpoints():
    res_models = client.get("/api/v1/ml/models")
    assert res_models.status_code == 200
    models = res_models.json()["data"]
    assert len(models) >= 3
    assert any(m["model_id"] == "model_rf_risk_v5" for m in models)
    assert any(m["model_id"] == "model_gb_risk_v5" for m in models)

    res_fi = client.get("/api/v1/ml/feature-importance")
    assert res_fi.status_code == 200
    features = res_fi.json()["data"]
    assert len(features) == 6
    assert features[0]["feature"] == "academic_index"

    res_eval = client.get("/api/v1/ml/evaluation")
    assert res_eval.status_code == 200
    eval_data = res_eval.json()["data"]
    assert "overall_metrics" in eval_data
    assert eval_data["overall_metrics"]["accuracy"] > 0.90
    assert "fairness_and_bias_audit" in eval_data


def test_ml_predict_and_agreement():
    res_pred = client.post(
        "/api/v1/ml/predict-risk",
        json={"academic": 45.0, "attendance": 55.0, "placement": 40.0, "lms": 30.0, "engagement": 20.0, "skills": 35.0},
    )
    assert res_pred.status_code == 200
    pdata = res_pred.json()["data"]
    assert pdata["risk_level"] in ["HIGH", "MEDIUM", "LOW"]
    assert "risk_probability" in pdata
    assert "top_drivers" in pdata

    res_agr = client.post(
        "/api/v1/ml/agreement-check",
        json={
            "features": {"academic": 85.0, "attendance": 90.0, "placement": 85.0, "lms": 90.0},
            "rules_tier": "on_track",
            "enabled": True,
        },
    )
    assert res_agr.status_code == 200
    adata = res_agr.json()["data"]
    assert adata["agrees"] is True
    assert adata["confidence"] == "High"

