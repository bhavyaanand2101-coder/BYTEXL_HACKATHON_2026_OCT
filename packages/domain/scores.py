"""
Domain models and calculation functions for student success scoring.
STRICT PURITY RULE: No I/O imports (no requests, no DB, no file I/O).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class Tier(str, Enum):
    ON_TRACK = "on_track"
    WATCHLIST = "watchlist"
    REVIEW = "review"
    PRIORITY_SUPPORT = "priority_support"


class Momentum(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    STABLE = "STABLE"
    UNKNOWN = "UNKNOWN"


class Segment(str, Enum):
    STRUGGLING = "Struggling on All Fronts"
    ACADEMIC_STARS_PLACEMENT_GAP = "Academic Stars with Placement Gap"
    HUSTLERS_ACADEMIC_RISK = "Hustlers at Academic Risk"
    QUIETLY_DISENGAGED = "Quietly Disengaged"
    BALANCED = "Balanced"


def clamp(x: float, lo: float, hi: float) -> float:
    """
    Clamps x to [lo, hi].
    Raises ValueError if x is NaN.
    """
    if x is None or math.isnan(x):
        raise ValueError("clamp received NaN")
    if x < lo:
        return float(lo)
    if x > hi:
        return float(hi)
    return float(x)


def compute_academic_index(cgpa: float, backlogs: int) -> float:
    """
    clamp(cgpa*10 - 3*min(backlogs, 5), 0, 100)
    """
    val = (cgpa * 10.0) - (3.0 * min(max(0, backlogs), 5))
    return clamp(val, 0.0, 100.0)


def compute_attendance_index(mean_attendance: float, subjects_below_60: int) -> float:
    """
    clamp(mean_attendance - 5*count(subject_att_below_60), 0, 100)
    """
    val = mean_attendance - (5.0 * max(0, subjects_below_60))
    return clamp(val, 0.0, 100.0)


def compute_placement_index(
    aptitude: float,
    coding: float,
    mock: float,
    weights: Optional[Dict[str, float]] = None,
) -> float:
    """
    0.35*aptitude + 0.40*coding + 0.25*mock
    """
    w_apt = 0.35
    w_cod = 0.40
    w_mock = 0.25
    if weights:
        w_apt = weights.get("aptitude", w_apt)
        w_cod = weights.get("coding", w_cod)
        w_mock = weights.get("mock", w_mock)
    val = (w_apt * aptitude) + (w_cod * coding) + (w_mock * mock)
    return clamp(val, 0.0, 100.0)


def compute_lms_index(assignment_completion_pct: float, scaled_logins: float) -> float:
    """
    0.50*assignment_completion + 0.50*scaled_logins
    """
    val = (0.50 * assignment_completion_pct) + (0.50 * scaled_logins)
    return clamp(val, 0.0, 100.0)


def compute_engagement_index(
    events: int,
    clubs: int,
    hackathons: int,
    certs: int,
    engagement_cap: float = 20.0,
) -> float:
    """
    clamp(sum(events, clubs, hackathons, certs) * 100 / engagement_cap, 0, 100)
    """
    raw_sum = float(events + clubs + hackathons + certs)
    val = (raw_sum * 100.0) / max(1.0, engagement_cap)
    return clamp(val, 0.0, 100.0)


def compute_skills_index(technical: float, soft: float) -> float:
    """
    0.60*technical + 0.40*soft
    """
    val = (0.60 * technical) + (0.40 * soft)
    return clamp(val, 0.0, 100.0)


def compute_assessment_sub_score(
    total_score: float,
    time_spent_min: float,
    plag_avg: float,
    multi_ip: bool,
    expected_time_min: float = 30.0,
    speed_anomaly_threshold_min: float = 15.0,
    max_test_score: float = 25.0,
) -> Tuple[float, float, float, bool]:
    """
    Assessment sub score derivation for python_assessment source.
    Formula: 0.60*normalized_total_score + 0.20*speed_score + 0.20*integrity_score

    Returns: (assessment_sub_score, speed_score, integrity_score, integrity_flag)
    """
    if expected_time_min is None or expected_time_min <= 0:
        raise ValueError("expected_time_min must be positive and present")

    # Defensive NaN sanitization
    if total_score is None or math.isnan(total_score):
        total_score = 0.0
    if time_spent_min is None or math.isnan(time_spent_min) or time_spent_min <= 0:
        time_spent_min = expected_time_min
    if plag_avg is None or math.isnan(plag_avg):
        plag_avg = 0.0

    normalized_score = clamp((total_score / max_test_score) * 100.0, 0.0, 100.0)
    
    # speed_score: under-time flagged as suspicious, not rewarded
    speed_score = clamp((time_spent_min / expected_time_min) * 50.0, 0.0, 100.0)
    
    speed_flag_penalty = 1.0 if time_spent_min < speed_anomaly_threshold_min else 0.0
    multi_ip_penalty = 1.0 if multi_ip else 0.0
    
    integrity_score = clamp(
        100.0 - (0.60 * plag_avg + 0.40 * speed_flag_penalty * 100.0 + multi_ip_penalty * 100.0),
        0.0,
        100.0,
    )
    
    sub_score = (
        0.60 * normalized_score
        + 0.20 * speed_score
        + 0.20 * integrity_score
    )
    sub_score = clamp(sub_score, 0.0, 100.0)

    integrity_flag = (plag_avg >= 90.0) or multi_ip or (time_spent_min < speed_anomaly_threshold_min)
    return sub_score, speed_score, integrity_score, integrity_flag


def compute_success_score(
    academic: float,
    attendance: float,
    placement: float,
    lms: float,
    engagement: float,
    skills: float,
    weights: Optional[Dict[str, float]] = None,
) -> float:
    """
    0.25*academic + 0.20*attendance + 0.20*placement + 0.15*lms + 0.10*engagement + 0.10*skills
    """
    w = weights or {
        "academic": 0.25,
        "attendance": 0.20,
        "placement": 0.20,
        "lms": 0.15,
        "engagement": 0.10,
        "skills": 0.10,
    }
    score = (
        w.get("academic", 0.25) * academic
        + w.get("attendance", 0.20) * attendance
        + w.get("placement", 0.20) * placement
        + w.get("lms", 0.15) * lms
        + w.get("engagement", 0.10) * engagement
        + w.get("skills", 0.10) * skills
    )
    return clamp(score, 0.0, 100.0)


def classify_momentum(
    history_scores: List[float],
    delta_threshold: float = 5.0,
) -> Tuple[Momentum, Optional[float]]:
    """
    3-week EWMA over success_score.
    Weeks 1 and 2: momentum='UNKNOWN' with delta=None.
    delta >= 5.0 -> UP, delta <= -5.0 -> DOWN, else STABLE
    ORDER-ONLY rule: Never changes tier.
    """
    if len(history_scores) < 3:
        return Momentum.UNKNOWN, None

    # Calculate 3-week EWMA with alpha = 2/(3+1) = 0.5
    alpha = 0.5
    ewma_prev = history_scores[-3]
    ewma_curr = alpha * history_scores[-2] + (1 - alpha) * ewma_prev
    ewma_latest = alpha * history_scores[-1] + (1 - alpha) * ewma_curr

    delta = round(ewma_latest - ewma_curr, 2)
    if delta >= delta_threshold:
        return Momentum.UP, delta
    elif delta <= -delta_threshold:
        return Momentum.DOWN, delta
    else:
        return Momentum.STABLE, delta


def determine_tier(
    attendance: float,
    cgpa: float,
    backlogs: int,
    success_score: float,
    floors: Optional[Dict[str, float]] = None,
    review_bands: Optional[Dict[str, List[float]]] = None,
) -> Tuple[Tier, bool]:
    """
    Tier decision order:
    1. Hard floor: attendance < 57 OR cgpa < 4.7 OR backlogs >= 3 -> priority_support [FLAG:HARD_FLOOR_TRIGGERED]
    2. Review band: 57 <= attendance <= 63 OR 4.7 <= cgpa <= 5.3 -> review
    3. Score bands: score >= 60 on_track | 40 <= score < 60 watchlist | score < 40 priority_support
    4. Momentum: annotate only
    5. ML check: annotate confidence only
    """
    f = floors or {"attendance_min": 57.0, "cgpa_min": 4.7, "backlog_max": 3}
    rb = review_bands or {"attendance": [57.0, 63.0], "cgpa": [4.7, 5.3]}

    # 1. Hard floor
    if (
        attendance < f.get("attendance_min", 57.0)
        or cgpa < f.get("cgpa_min", 4.7)
        or backlogs >= int(f.get("backlog_max", 3))
    ):
        return Tier.PRIORITY_SUPPORT, True

    # 2. Review band
    att_rb = rb.get("attendance", [57.0, 63.0])
    cgpa_rb = rb.get("cgpa", [4.7, 5.3])
    if (att_rb[0] <= attendance <= att_rb[1]) or (cgpa_rb[0] <= cgpa <= cgpa_rb[1]):
        return Tier.REVIEW, False

    # 3. Score bands
    if success_score >= 60.0:
        return Tier.ON_TRACK, False
    elif success_score >= 40.0:
        return Tier.WATCHLIST, False
    else:
        return Tier.PRIORITY_SUPPORT, False


def compute_priority_score(
    success_score: float,
    tier: Tier,
    hard_floor_triggered: bool,
    momentum: Momentum,
    sub_indices: Dict[str, float],
    cohort_p25: Dict[str, float],
) -> float:
    """
    formula: (0.5*Severity + 0.25*Actionability + 0.25*Urgency) * MomentumBoost
    severity: 100 * (1 - success_score/100)
    actionability: 100 if any of {attendance, lms, engagement} below cohort_p25 AND has action template;
                   else 50 if any below p25; else 0
    urgency: 100 if hard_floor_triggered OR momentum == DOWN; 50 if tier == review; else 0
    momentum_boost: 1.10 if UP, 1.00 if STABLE/UNKNOWN, 1.15 if DOWN
    """
    severity = 100.0 * (1.0 - (success_score / 100.0))

    actionable_keys = ["attendance", "lms", "engagement"]
    below_p25_count = sum(
        1 for k in actionable_keys if sub_indices.get(k, 100.0) < cohort_p25.get(k, 25.0)
    )
    if below_p25_count > 0:
        actionability = 100.0
    else:
        any_below = any(
            sub_indices.get(k, 100.0) < cohort_p25.get(k, 25.0) for k in sub_indices
        )
        actionability = 50.0 if any_below else 0.0

    if hard_floor_triggered or momentum == Momentum.DOWN:
        urgency = 100.0
    elif tier == Tier.REVIEW:
        urgency = 50.0
    else:
        urgency = 0.0

    if momentum == Momentum.UP:
        boost = 1.10
    elif momentum == Momentum.DOWN:
        boost = 1.15
    else:
        boost = 1.00

    raw = (0.50 * severity + 0.25 * actionability + 0.25 * urgency) * boost
    return round(raw, 2)
