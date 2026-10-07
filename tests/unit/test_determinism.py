"""
Unit Test: Determinism & Byte-Identical Output.
Asserts that given the same inputs and config_hash, rules_layer and stat_layer
produce byte-identical dictionary and serialized JSON outputs across multiple invocations.
"""

import json
from services.enrichment.rules_layer import enrich_student_rules
from services.enrichment.stat_layer import compute_cohort_statistics, compute_peer_z_scores


def test_rules_layer_determinism():
    student_raw = {
        "cgpa": 8.4,
        "backlogs": 0,
        "attendance_pct": 88.5,
        "subjects_att_below_60": 0,
        "aptitude": 75.0,
        "coding": 82.0,
        "mock": 80.0,
        "assignment_completion_pct": 90.0,
        "scaled_logins": 85.0,
        "events": 2,
        "clubs": 1,
        "hackathons": 1,
        "certs": 1,
        "technical_score": 85.0,
        "soft_score": 75.0,
    }
    cohort_p25 = {
        "academic": 50.0,
        "attendance": 65.0,
        "placement": 45.0,
        "lms": 40.0,
        "engagement": 20.0,
        "skills": 45.0,
    }
    weights = {"academic": 0.25, "attendance": 0.20, "placement": 0.20, "lms": 0.15, "engagement": 0.10, "skills": 0.10}
    floors = {"attendance_min": 57.0, "cgpa_min": 4.7, "backlog_max": 3}
    review_bands = {"attendance": [57.0, 63.0], "cgpa": [4.7, 5.3]}

    run1 = enrich_student_rules(student_raw, cohort_p25, weights, floors, review_bands)
    run2 = enrich_student_rules(student_raw, cohort_p25, weights, floors, review_bands)

    json1 = json.dumps(run1, sort_keys=True, default=str)
    json2 = json.dumps(run2, sort_keys=True, default=str)

    assert json1 == json2
    assert run1["success_score"] == run2["success_score"]
    assert run1["tier"] == run2["tier"]
    assert run1["segment"] == run2["segment"]


def test_stat_layer_determinism():
    cohort_data = {
        "academic": [45.0, 60.0, 75.0, 85.0, 92.0],
        "attendance": [55.0, 70.0, 82.0, 88.0, 95.0],
    }
    stats1 = compute_cohort_statistics(cohort_data)
    stats2 = compute_cohort_statistics(cohort_data)

    assert json.dumps(stats1, sort_keys=True) == json.dumps(stats2, sort_keys=True)
