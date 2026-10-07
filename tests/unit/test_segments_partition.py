"""
Unit Test: Segmentation Partition.
Asserts that every student permutation maps to exactly one exclusive segment.
"""

from packages.domain.scores import Segment, Tier
from packages.domain.segments import SEGMENT_PRECEDENCE, assign_segment


def test_segment_partition_is_exclusive():
    cohort_p25 = {
        "academic": 45.0,
        "attendance": 60.0,
        "placement": 40.0,
        "lms": 35.0,
        "engagement": 20.0,
        "skills": 40.0,
    }

    # Case 1: Struggling on All Fronts
    s1 = assign_segment(
        tier=Tier.PRIORITY_SUPPORT,
        sub_indices={"academic": 30.0, "attendance": 40.0, "placement": 20.0, "lms": 25.0, "engagement": 10.0, "skills": 20.0},
        cohort_p25=cohort_p25,
    )
    assert s1 == Segment.STRUGGLING

    # Case 2: Academic Stars with Placement Gap
    s2 = assign_segment(
        tier=Tier.ON_TRACK,
        sub_indices={"academic": 85.0, "attendance": 80.0, "placement": 30.0, "lms": 70.0, "engagement": 40.0, "skills": 50.0},
        cohort_p25=cohort_p25,
    )
    assert s2 == Segment.ACADEMIC_STARS_PLACEMENT_GAP

    # Case 3: Hustlers at Academic Risk
    s3 = assign_segment(
        tier=Tier.WATCHLIST,
        sub_indices={"academic": 35.0, "attendance": 70.0, "placement": 50.0, "lms": 60.0, "engagement": 80.0, "skills": 60.0},
        cohort_p25=cohort_p25,
    )
    assert s3 == Segment.HUSTLERS_ACADEMIC_RISK

    # Case 4: Quietly Disengaged
    s4 = assign_segment(
        tier=Tier.WATCHLIST,
        sub_indices={"academic": 60.0, "attendance": 75.0, "placement": 50.0, "lms": 25.0, "engagement": 15.0, "skills": 50.0},
        cohort_p25=cohort_p25,
    )
    assert s4 == Segment.QUIETLY_DISENGAGED

    # Case 5: Balanced Fallback
    s5 = assign_segment(
        tier=Tier.ON_TRACK,
        sub_indices={"academic": 70.0, "attendance": 80.0, "placement": 65.0, "lms": 60.0, "engagement": 50.0, "skills": 60.0},
        cohort_p25=cohort_p25,
    )
    assert s5 == Segment.BALANCED

    for s in [s1, s2, s3, s4, s5]:
        assert s in SEGMENT_PRECEDENCE
