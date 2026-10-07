"""
Unit Test: Momentum Order-Only Rule.
Asserts that momentum classifier (UP, DOWN, STABLE, UNKNOWN) never changes student tier.
"""

from packages.domain.scores import Momentum, Tier, classify_momentum, determine_tier


def test_momentum_does_not_affect_tier():
    floors = {"attendance_min": 57.0, "cgpa_min": 4.7, "backlog_max": 3}
    review_bands = {"attendance": [57.0, 63.0], "cgpa": [4.7, 5.3]}

    # Student with on_track score (65.0)
    tier, _ = determine_tier(
        attendance=85.0,
        cgpa=7.5,
        backlogs=0,
        success_score=65.0,
        floors=floors,
        review_bands=review_bands,
    )
    assert tier == Tier.ON_TRACK

    # Upward momentum
    mom_up, delta_up = classify_momentum([50.0, 58.0, 65.0])
    assert mom_up == Momentum.UP
    assert tier == Tier.ON_TRACK  # Still on_track

    # Downward momentum
    mom_down, delta_down = classify_momentum([80.0, 72.0, 65.0])
    assert mom_down == Momentum.DOWN
    assert tier == Tier.ON_TRACK  # Still on_track, not downgraded
