"""
Deterministic Rules Enrichment Layer.
Executes pure domain mathematical models, indices, tiers, momentum, and priority scores.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from packages.domain.scores import (
    Momentum,
    Tier,
    classify_momentum,
    compute_academic_index,
    compute_attendance_index,
    compute_engagement_index,
    compute_lms_index,
    compute_placement_index,
    compute_priority_score,
    compute_skills_index,
    compute_success_score,
    determine_tier,
)
from packages.domain.segments import assign_segment


def enrich_student_rules(
    student_raw: Dict[str, Any],
    cohort_p25: Dict[str, float],
    config_weights: Dict[str, float],
    floors: Dict[str, float],
    review_bands: Dict[str, List[float]],
    history_scores: Optional[List[float]] = None,
) -> Dict[str, Any]:
    """
    Pure deterministic scoring rule execution.
    Outputs: sub_indices, success_score, momentum, tier, segment, priority_score, reason_codes, evidence_json.
    """
    cgpa = float(student_raw.get("cgpa", 7.0))
    backlogs = int(student_raw.get("backlogs", 0))
    mean_attendance = float(student_raw.get("attendance_pct", 80.0))
    subjects_below_60 = int(student_raw.get("subjects_att_below_60", 0))
    
    aptitude = float(student_raw.get("aptitude", 60.0))
    coding = float(student_raw.get("coding", student_raw.get("assessment_sub_score", 50.0)))
    mock = float(student_raw.get("mock", 60.0))

    assignment_completion_pct = float(student_raw.get("assignment_completion_pct", 75.0))
    scaled_logins = float(student_raw.get("scaled_logins", 70.0))

    events = int(student_raw.get("events", 1))
    clubs = int(student_raw.get("clubs", 1))
    hackathons = int(student_raw.get("hackathons", 0))
    certs = int(student_raw.get("certs", 1))

    technical = float(student_raw.get("technical_score", 65.0))
    soft = float(student_raw.get("soft_score", 70.0))

    # 1. Compute Sub-indices
    academic_idx = compute_academic_index(cgpa, backlogs)
    attendance_idx = compute_attendance_index(mean_attendance, subjects_below_60)
    placement_idx = compute_placement_index(aptitude, coding, mock)
    lms_idx = compute_lms_index(assignment_completion_pct, scaled_logins)
    engagement_idx = compute_engagement_index(events, clubs, hackathons, certs)
    skills_idx = compute_skills_index(technical, soft)

    sub_indices = {
        "academic": round(academic_idx, 2),
        "attendance": round(attendance_idx, 2),
        "placement": round(placement_idx, 2),
        "lms": round(lms_idx, 2),
        "engagement": round(engagement_idx, 2),
        "skills": round(skills_idx, 2),
    }

    # 2. Compute Success Score
    success_score = compute_success_score(
        academic=academic_idx,
        attendance=attendance_idx,
        placement=placement_idx,
        lms=lms_idx,
        engagement=engagement_idx,
        skills=skills_idx,
        weights=config_weights,
    )
    success_score = round(success_score, 2)

    # 3. Determine Tier & Hard Floor
    tier, hard_floor_triggered = determine_tier(
        attendance=mean_attendance,
        cgpa=cgpa,
        backlogs=backlogs,
        success_score=success_score,
        floors=floors,
        review_bands=review_bands,
    )

    # 4. Momentum (3-week EWMA)
    scores_hist = (history_scores or []) + [success_score]
    momentum, momentum_delta = classify_momentum(scores_hist)

    # 5. Segment Assignment
    segment = assign_segment(
        tier=tier,
        sub_indices=sub_indices,
        cohort_p25=cohort_p25,
    )

    # 6. Priority Score
    priority_score = compute_priority_score(
        success_score=success_score,
        tier=tier,
        hard_floor_triggered=hard_floor_triggered,
        momentum=momentum,
        sub_indices=sub_indices,
        cohort_p25=cohort_p25,
    )

    marks_10th = float(student_raw.get("marks_10th", 85.0))
    marks_12th = float(student_raw.get("marks_12th", 82.0))
    lms_time_spent = float(student_raw.get("lms_time_spent", 45.5))

    # 7. Reason Codes & Evidence JSON
    reason_codes = []
    evidence_json: Dict[str, Any] = {
        "cgpa": cgpa,
        "marks_10th": marks_10th,
        "marks_12th": marks_12th,
        "lms_time_spent": lms_time_spent,
        "backlogs": backlogs,
        "attendance_pct": mean_attendance,
        "coding_score": coding,
        "sub_indices": sub_indices,
        "hard_floor_triggered": hard_floor_triggered,
    }

    if hard_floor_triggered:
        if mean_attendance < floors.get("attendance_min", 57.0):
            reason_codes.append("HARD_FLOOR_ATTENDANCE")
        if cgpa < floors.get("cgpa_min", 4.7):
            reason_codes.append("HARD_FLOOR_CGPA")
        if backlogs >= floors.get("backlog_max", 3):
            reason_codes.append("HARD_FLOOR_BACKLOGS")

    if mean_attendance < cohort_p25.get("attendance", 70.0):
        reason_codes.append("LOW_ATTENDANCE")
    if lms_idx < cohort_p25.get("lms", 50.0):
        reason_codes.append("LOW_LMS")
    if engagement_idx < cohort_p25.get("engagement", 30.0):
        reason_codes.append("LOW_ENGAGEMENT")
    if academic_idx >= 75.0 and placement_idx < cohort_p25.get("placement", 50.0):
        reason_codes.append("PLACEMENT_GAP")

    return {
        "sub_indices": sub_indices,
        "success_score": success_score,
        "momentum": momentum.value,
        "momentum_delta": momentum_delta,
        "tier": tier.value,
        "hard_floor_triggered": hard_floor_triggered,
        "segment": segment.value,
        "priority_score": priority_score,
        "reason_codes": reason_codes,
        "evidence_json": evidence_json,
    }
