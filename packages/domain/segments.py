"""
Student segmentation assignment based on deterministic rules and precedence order.
Rule: EXCLUSIVE. Each student belongs to exactly one segment per week.
"""

from __future__ import annotations

from typing import Dict, List
from packages.domain.scores import Segment, Tier


SEGMENT_PRECEDENCE: List[Segment] = [
    Segment.STRUGGLING,
    Segment.ACADEMIC_STARS_PLACEMENT_GAP,
    Segment.HUSTLERS_ACADEMIC_RISK,
    Segment.QUIETLY_DISENGAGED,
    Segment.BALANCED,
]


def assign_segment(
    tier: Tier,
    sub_indices: Dict[str, float],
    cohort_p25: Dict[str, float],
) -> Segment:
    """
    Evaluates segment membership in strict precedence order:
    1. Struggling on All Fronts: tier == 'priority_support' AND >= 4 sub-indices below cohort_p25
    2. Academic Stars with Placement Gap: academic_index >= 75 AND placement_index <= cohort_p25['placement']
    3. Hustlers at Academic Risk: engagement_index >= 75 AND academic_index < cohort_p25['academic']
    4. Quietly Disengaged: lms_index < cohort_p25['lms'] AND engagement_index < cohort_p25['engagement'] AND attendance_index >= 60
    5. Balanced: fallback
    """
    academic = sub_indices.get("academic", 0.0)
    attendance = sub_indices.get("attendance", 0.0)
    placement = sub_indices.get("placement", 0.0)
    lms = sub_indices.get("lms", 0.0)
    engagement = sub_indices.get("engagement", 0.0)
    skills = sub_indices.get("skills", 0.0)

    # Count sub indices below cohort p25
    keys = ["academic", "attendance", "placement", "lms", "engagement", "skills"]
    below_p25_count = sum(
        1 for k in keys if sub_indices.get(k, 0.0) < cohort_p25.get(k, 25.0)
    )

    # 1. Struggling on All Fronts
    if tier == Tier.PRIORITY_SUPPORT and below_p25_count >= 4:
        return Segment.STRUGGLING

    # 2. Academic Stars with Placement Gap
    if academic >= 75.0 and placement <= cohort_p25.get("placement", 35.0):
        return Segment.ACADEMIC_STARS_PLACEMENT_GAP

    # 3. Hustlers at Academic Risk
    if engagement >= 75.0 and academic < cohort_p25.get("academic", 45.0):
        return Segment.HUSTLERS_ACADEMIC_RISK

    # 4. Quietly Disengaged
    if (
        lms < cohort_p25.get("lms", 40.0)
        and engagement < cohort_p25.get("engagement", 20.0)
        and attendance >= 60.0
    ):
        return Segment.QUIETLY_DISENGAGED

    # 5. Balanced
    return Segment.BALANCED
