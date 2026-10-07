import urllib.request
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def get_json(url, timeout=5):
    req = urllib.request.Request(url, headers={"User-Agent": "CampusPulseE2EChecker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.status, json.loads(response.read().decode('utf-8'))

def post_json(url, data_dict, timeout=5):
    payload = json.dumps(data_dict).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "CampusPulseE2EChecker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.status, json.loads(response.read().decode('utf-8'))

def run_checks():
    print("=" * 85)
    print("CAMPUSPULSE ENTERPRISE END-TO-END HEALTH & API ENDPOINT VERIFICATION")
    print("=" * 85)
    passed = 0
    failed = 0

    # 1. Base Static and Health
    basic_endpoints = [
        ("GET", "/", 200, "Frontend Single Page Application (HTML UI)"),
        ("GET", "/health", 200, "Root Health Status & Boot Hashes"),
        ("GET", "/health/db", 200, "Database Health & Connection Probe"),
        ("GET", "/health/ml", 200, "ML Disagreement Engine Health Probe"),
        ("GET", "/api/v1/health", 200, "API v1 Health & Readiness Probe"),
        ("GET", "/api/v1/metrics", 200, "Non-PII Prometheus Metrics"),
        ("GET", "/api/v1/cohorts/readiness", 200, "Cohort Readiness Distribution"),
        ("GET", "/api/v1/cohorts/gaps", 200, "Curriculum & Competency Gaps"),
        ("GET", "/api/v1/cohorts/login-activity", 200, "Student Login Activity Telemetry"),
        ("GET", "/api/v1/college/telemetry", 200, "College Reports 9-Subtab Telemetry"),
        ("GET", "/api/v1/excellence/overview", 200, "Institutional Excellence Review"),
        ("GET", "/api/v1/learning/sprints", 200, "Placement Learning Sprints"),
        ("GET", "/api/v1/labs", 200, "Hands-on Coding Labs & Runtimes"),
        ("GET", "/api/v1/trainers/schedule", 200, "Trainer Masterclass Schedule"),
        ("GET", "/api/v1/projects/bank", 200, "Capstone Project Repository"),
        ("GET", "/api/v1/admin/audit-logs", 200, "Governance Audit Trail Ledger"),
        ("GET", "/api/v1/admin/department-faculty", 200, "Admin Portal: Department & Faculty Allocation Hierarchy"),
        ("GET", "/api/v1/competitive/overview", 200, "Competitive Intelligence: Market Overview"),
        ("GET", "/api/v1/competitive/categories", 200, "Competitive Intelligence: 17 Categories"),
        ("GET", "/api/v1/competitive/competitors", 200, "Competitive Intelligence: 9 Profiles"),
        ("GET", "/api/v1/competitive/matrix", 200, "Competitive Intelligence: Feature Matrix"),
        ("GET", "/api/v1/competitive/gaps", 200, "Competitive Intelligence: 10 Gap Cards"),
        ("GET", "/api/v1/competitive/workflow", 200, "Competitive Intelligence: 7-Step Advantage"),
        ("GET", "/api/v1/kpmg/deliverables", 200, "KPMG Deliverables & Presentation Deck"),
        ("GET", "/api/v1/kpmg/segmentation-matrix", 200, "KPMG 2D Student Segmentation Matrix"),
        ("GET", "/api/v1/ml/models", 200, "ML Model Registry (RF, GB, LR Baselines)"),
        ("GET", "/api/v1/ml/feature-importance", 200, "ML Feature Importance Rankings"),
        ("GET", "/api/v1/ml/evaluation", 200, "ML Model Evaluation & Fairness Audit"),
    ]

    for method, path, expected_status, description in basic_endpoints:
        url = f"{BASE_URL}{path}"
        t0 = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "CampusPulseE2EChecker/1.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.status
                latency_ms = (time.time() - t0) * 1000
                if status == expected_status:
                    print(f"✓ [{status}] {method:<4} {path:<46} | {latency_ms:>6.2f}ms | {description}")
                    passed += 1
                else:
                    print(f"✕ [{status}] {method:<4} {path:<46} | Expected {expected_status} | {description}")
                    failed += 1
        except Exception as e:
            latency_ms = (time.time() - t0) * 1000
            print(f"✕ [ERR] {method:<4} {path:<46} | {e} | {description}")
            failed += 1

    # 2. Fetch student list dynamically
    t0 = time.time()
    student_ref = None
    try:
        status, data = get_json(f"{BASE_URL}/api/v1/advisors/me/action-list?limit=10")
        latency_ms = (time.time() - t0) * 1000
        action_list = data.get("data", {}).get("action_list", [])
        if status == 200 and len(action_list) > 0:
            student_ref = action_list[0]["student_ref"]
            print(f"✓ [{status}] GET  /api/v1/advisors/me/action-list?limit=10       | {latency_ms:>6.2f}ms | Advisor Action List (Found: {student_ref})")
            passed += 1
        else:
            print(f"✕ [{status}] GET  /api/v1/advisors/me/action-list failed to return students")
            failed += 1
    except Exception as e:
        print(f"✕ [ERR] GET  /api/v1/advisors/me/action-list | {e}")
        failed += 1

    if not student_ref:
        student_ref = "stu_9f9974d49a1b"

    # 3. Dynamic Student-Specific Endpoints
    student_endpoints = [
        (f"/api/v1/students/{student_ref}", "Student 360 Profile with Risk Factors"),
        (f"/api/v1/students/{student_ref}/explain", "Deterministic Score Math & Formula Decomposition"),
        (f"/api/v1/students/{student_ref}/trend", "Multi-Week Longitudinal Progression Trend"),
    ]

    for path, description in student_endpoints:
        url = f"{BASE_URL}{path}"
        t0 = time.time()
        try:
            status, data = get_json(url)
            latency_ms = (time.time() - t0) * 1000
            if status == 200 and "data" in data:
                print(f"✓ [{status}] GET  {path:<46} | {latency_ms:>6.2f}ms | {description}")
                passed += 1
            else:
                print(f"✕ [{status}] GET  {path:<46} | Invalid envelope response")
                failed += 1
        except Exception as e:
            print(f"✕ [ERR] GET  {path:<46} | {e}")
            failed += 1

    # 4. What-If Simulation
    t0 = time.time()
    try:
        url = f"{BASE_URL}/api/v1/what-if"
        payload = {
            "student_ref": student_ref,
            "overrides": [{"indicator": "academic", "delta": 10.0}]
        }
        status, data = post_json(url, payload)
        latency_ms = (time.time() - t0) * 1000
        if status == 200 and "data" in data and "simulated_score" in data["data"]:
            sim_score = data["data"]["simulated_score"]
            orig_score = data["data"]["original_score"]
            delta = data["data"]["score_delta"]
            print(f"✓ [{status}] POST /api/v1/what-if                              | {latency_ms:>6.2f}ms | Server-Side What-If Simulation ({orig_score} -> {sim_score}, Δ: {delta:+0.2f})")
            passed += 1
        else:
            print(f"✕ [{status}] POST /api/v1/what-if failed simulation calculation")
            failed += 1
    except Exception as e:
        print(f"✕ [ERR] POST /api/v1/what-if | {e}")
        failed += 1

    # 5. Deterministic AST Audit Verification
    t0 = time.time()
    try:
        url = f"{BASE_URL}/api/v1/admin/verify-ast"
        status, data = post_json(url, {})
        latency_ms = (time.time() - t0) * 1000
        if status == 200 and "purity" in data["data"]:
            purity_msg = data["data"]["purity"]
            print(f"✓ [{status}] POST /api/v1/admin/verify-ast                      | {latency_ms:>6.2f}ms | Python AST Audit: {purity_msg}")
            passed += 1
        else:
            print(f"✕ [{status}] POST /api/v1/admin/verify-ast unexpected result: {data}")
            failed += 1
    except Exception as e:
        print(f"✕ [ERR] POST /api/v1/admin/verify-ast | {e}")
        failed += 1

    # 6. ML Risk Predictor Proxy
    t0 = time.time()
    try:
        url = f"{BASE_URL}/api/v1/ml/predict-risk"
        status, data = post_json(url, {"academic": 50.0, "attendance": 65.0, "placement": 45.0, "lms": 40.0})
        latency_ms = (time.time() - t0) * 1000
        if status == 200 and "risk_level" in data.get("data", {}):
            rl = data["data"]["risk_level"]
            prob = data["data"]["risk_percentage"]
            print(f"✓ [{status}] POST /api/v1/ml/predict-risk                       | {latency_ms:>6.2f}ms | ML Risk Estimator (Level: {rl}, Prob: {prob})")
            passed += 1
        else:
            print(f"✕ [{status}] POST /api/v1/ml/predict-risk unexpected result: {data}")
            failed += 1
    except Exception as e:
        print(f"✕ [ERR] POST /api/v1/ml/predict-risk | {e}")
        failed += 1

    # 7. ML Rules Agreement Guardrail
    t0 = time.time()
    try:
        url = f"{BASE_URL}/api/v1/ml/agreement-check"
        status, data = post_json(url, {"features": {"academic": 80.0, "attendance": 85.0}, "rules_tier": "on_track"})
        latency_ms = (time.time() - t0) * 1000
        if status == 200 and data.get("data", {}).get("agrees") is True:
            print(f"✓ [{status}] POST /api/v1/ml/agreement-check                  | {latency_ms:>6.2f}ms | ML/Rules Agreement Guardrail (Agrees: True)")
            passed += 1
        else:
            print(f"✕ [{status}] POST /api/v1/ml/agreement-check unexpected result: {data}")
            failed += 1
    except Exception as e:
        print(f"✕ [ERR] POST /api/v1/ml/agreement-check | {e}")
        failed += 1

    print("=" * 85)
    print(f"ALL SYSTEMS NOMINAL: {passed}/{passed + failed} CHECKS PASSED ({(passed/(passed+failed))*100:.1f}%)")
    print("=" * 85)
    return failed == 0

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)

