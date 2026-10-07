"""
Statistical Enrichment Layer.
Computes cohort percentiles, peer z-scores, and historical trend slopes.
Permitted to use seeded RNG with seed sourced strictly from config_hash.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple


def _seed_from_hash(config_hash: str) -> int:
    try:
        return int(config_hash[:8], 16)
    except Exception:
        return 42


def compute_cohort_statistics(
    cohort_values: Dict[str, List[float]],
) -> Dict[str, Dict[str, float]]:
    """
    Computes p25, median (p50), p75, mean, and std for each indicator.
    """
    stats = {}
    for key, vals in cohort_values.items():
        if not vals:
            stats[key] = {"p25": 0.0, "p50": 0.0, "p75": 0.0, "mean": 0.0, "std": 1.0}
            continue
        sorted_vals = sorted(vals)
        n = len(sorted_vals)
        
        def pct(p: float) -> float:
            idx = int(p * (n - 1))
            return sorted_vals[idx]

        mean = sum(vals) / float(n)
        variance = sum((x - mean) ** 2 for x in vals) / float(max(1, n - 1))
        std = math.sqrt(variance) if variance > 0 else 1.0

        stats[key] = {
            "p25": round(pct(0.25), 2),
            "p50": round(pct(0.50), 2),
            "p75": round(pct(0.75), 2),
            "mean": round(mean, 2),
            "std": round(std, 2),
        }
    return stats


def compute_peer_z_scores(
    student_indices: Dict[str, float],
    cohort_stats: Dict[str, Dict[str, float]],
) -> Dict[str, float]:
    """
    Computes z-score = (val - mean) / std for each indicator.
    """
    z_scores = {}
    for key, val in student_indices.items():
        c = cohort_stats.get(key, {"mean": 50.0, "std": 15.0})
        std = c["std"] if c["std"] > 0 else 1.0
        z = (val - c["mean"]) / std
        z_scores[key] = round(z, 2)
    return z_scores


def compute_trend_slope(history_values: List[float]) -> float:
    """
    Simple linear regression slope over historical weekly measurements.
    """
    n = len(history_values)
    if n < 2:
        return 0.0
    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(history_values) / n
    numerator = sum((x[i] - x_mean) * (history_values[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 3)
