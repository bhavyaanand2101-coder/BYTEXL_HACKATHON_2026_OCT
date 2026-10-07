"""
Domain flags calculation. Pure computation without I/O.
Detects 6 critical risk patterns and builds structured evidence JSON.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def evaluate_flags(
    cgpa: float,
    week_number: int,
    coding_submissions_last_6w: int,
    coding_score: float,
    cohort_p25_coding: float,
    lms_delta_4w: float,
    attendance_pct: float,
    academic_standing: str,
    attendance_trend: float,
    lms_trend: float,
    engagement_trend: float,
    skills_index: float,
    momentum_str: str,
    plag_avg: float,
    multi_ip: bool,
    speed_anomaly: bool,
    total_score: float,
    tab_switches: int,
    time_spent_min: float,
) -> List[Dict[str, Any]]:
    """
    Evaluates risk flags and returns list of fired flags with evidence.
    Flags:
      1. strong_marks_weak_coding
      2. early_disengagement
      3. passive_attender
      4. hidden_talent
      5. assessment_integrity_review
      6. silent_struggler
    """
    flags = []

    # 1. strong_marks_weak_coding
    if cgpa >= 8.0 and week_number >= 4:
        if coding_submissions_last_6w == 0 or coding_score <= cohort_p25_coding:
            flags.append({
                "flag_code": "strong_marks_weak_coding",
                "title": "High CGPA with Placement Coding Gap",
                "evidence_json": {
                    "cgpa": cgpa,
                    "week_number": week_number,
                    "coding_submissions_last_6w": coding_submissions_last_6w,
                    "coding_score": coding_score,
                    "cohort_p25_coding": cohort_p25_coding,
                },
                "is_advisory": False,
            })

    # 2. early_disengagement
    if week_number >= 4 and lms_delta_4w <= -0.40 and attendance_pct >= 75.0:
        flags.append({
            "flag_code": "early_disengagement",
            "title": "Early Disengagement Signal",
            "evidence_json": {
                "week_number": week_number,
                "lms_delta_4w": lms_delta_4w,
                "attendance_pct": attendance_pct,
            },
            "is_advisory": False,
        })

    # 3. passive_attender
    if (
        academic_standing == "Satisfactory"
        and attendance_trend < 0
        and lms_trend < 0
        and engagement_trend < 0
    ):
        flags.append({
            "flag_code": "passive_attender",
            "title": "Passive Attender Trend",
            "evidence_json": {
                "academic_standing": academic_standing,
                "attendance_trend": attendance_trend,
                "lms_trend": lms_trend,
                "engagement_trend": engagement_trend,
            },
            "is_advisory": False,
        })

    # 4. hidden_talent
    if cgpa < 6.5 and skills_index >= 75.0 and momentum_str == "UP":
        flags.append({
            "flag_code": "hidden_talent",
            "title": "Hidden Technical Talent",
            "evidence_json": {
                "cgpa": cgpa,
                "skills_index": skills_index,
                "momentum": momentum_str,
            },
            "is_advisory": False,
        })

    # 5. assessment_integrity_review (Advisory only)
    if plag_avg >= 90.0 or multi_ip or speed_anomaly:
        flags.append({
            "flag_code": "assessment_integrity_review",
            "title": "Assessment Integrity Review (Confidential)",
            "evidence_json": {
                "plag_avg": plag_avg,
                "multi_ip": multi_ip,
                "speed_anomaly": speed_anomaly,
            },
            "is_advisory": True,
        })

    # 6. silent_struggler
    if total_score <= 10.0 and tab_switches == 0 and time_spent_min >= 30.0:
        flags.append({
            "flag_code": "silent_struggler",
            "title": "Silent Struggler",
            "evidence_json": {
                "total_score": total_score,
                "tab_switches": tab_switches,
                "time_spent_min": time_spent_min,
            },
            "is_advisory": False,
        })

    return flags
