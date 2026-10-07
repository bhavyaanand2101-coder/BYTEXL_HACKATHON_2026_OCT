#!/usr/bin/env python3
"""
scripts/boot_check.py
─────────────────────
Pre-flight validation run at two points:
  1. apps/api/main.py startup event
  2. .github/workflows/ci.yml (standalone)

Exit codes:
  0 — all checks passed
  2 — fatal config error (weights, missing key, etc.)
  1 — unexpected / unhandled error

Contract requirements enforced:
  ✓ weights sum to 1.00 (±1e-9 tolerance)
  ✓ review_band floors are ordered correctly per dimension (not cross-compared)
  ✓ config.assessment.expected_time_min present
  ✓ config_hash = sha256(canonical_json(parsed config + rules))[:16]
  ✓ targets_hash = sha256(canonical_json(parsed TARGETS))[:16]
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import yaml

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
CONFIG_YAML   = ROOT / "config" / "config.yaml"
RULES_YAML    = ROOT / "config" / "rules.yaml"
TARGETS_YAML  = ROOT / "config" / "TARGETS.yaml"

WEIGHT_KEYS = ["academic", "attendance", "placement", "lms", "engagement", "skills"]


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _canonical_json(obj: object) -> str:
    """Deterministic JSON (sorted keys, no whitespace variance)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _sha256_prefix(s: str, length: int = 16) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:length]


# ── Individual checks ─────────────────────────────────────────────────────────

def check_weights(config: dict) -> None:
    weights = config.get("weights", {})
    total = sum(weights.get(k, 0.0) for k in WEIGHT_KEYS)
    if abs(total - 1.0) > 1e-9:
        print(
            f"[BOOT_CHECK FATAL] weights do not sum to 1.00 "
            f"(got {total:.10f}). Fix config/config.yaml.",
            file=sys.stderr,
        )
        sys.exit(2)
    print(f"[BOOT_CHECK OK] weights sum = {total:.10f}")


def check_floors_ordered(config: dict) -> None:
    """
    For each dimension independently:
      review_band.min == floor.value <= review_band.max
    Attendance and CGPA checked separately (not cross-compared).
    """
    rb = config.get("review_band", {})
    floors = config.get("floors", {})

    checks = [
        ("attendance", floors.get("attendance_min"), rb.get("attendance")),
        ("cgpa",       floors.get("cgpa_min"),       rb.get("cgpa")),
    ]

    errors = []
    for dim, floor_val, band in checks:
        if floor_val is None:
            errors.append(f"  floors.{dim}_min missing")
            continue
        if band is None or len(band) != 2:
            errors.append(f"  review_band.{dim} missing or not a 2-element list")
            continue
        band_min, band_max = band
        if not (band_min <= floor_val <= band_max):
            errors.append(
                f"  {dim}: floor={floor_val} not in [{band_min}, {band_max}]"
            )

    if errors:
        print("[BOOT_CHECK FATAL] Floor/review_band ordering violated:", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        sys.exit(2)

    print("[BOOT_CHECK OK] Floor/review_band ordering valid for all dimensions")


def check_expected_time_min(config: dict) -> None:
    assessment = config.get("assessment", {})
    if assessment.get("expected_time_min") is None:
        print(
            "[BOOT_CHECK FATAL] config.assessment.expected_time_min is missing. "
            "Refusing to boot. (See data_contract → assessment_sub_score → missing_config_guard)",
            file=sys.stderr,
        )
        sys.exit(2)
    print(
        f"[BOOT_CHECK OK] expected_time_min = {assessment['expected_time_min']} min"
    )


# ── Hash computation ──────────────────────────────────────────────────────────

def compute_hashes(config: dict, rules: dict, targets: dict) -> tuple[str, str]:
    config_hash = _sha256_prefix(_canonical_json({**config, **rules}))
    targets_hash = _sha256_prefix(_canonical_json(targets))
    return config_hash, targets_hash


# ── Entry point ───────────────────────────────────────────────────────────────

def run_boot_check() -> tuple[str, str]:
    """
    Run all boot checks. Returns (config_hash, targets_hash) on success.
    Exits with code 2 on any fatal failure.
    """
    print("[BOOT_CHECK] Loading config files …")
    try:
        config  = _load_yaml(CONFIG_YAML)
        rules   = _load_yaml(RULES_YAML)
        targets = _load_yaml(TARGETS_YAML)
    except FileNotFoundError as exc:
        print(f"[BOOT_CHECK FATAL] Missing config file: {exc}", file=sys.stderr)
        sys.exit(2)
    except yaml.YAMLError as exc:
        print(f"[BOOT_CHECK FATAL] YAML parse error: {exc}", file=sys.stderr)
        sys.exit(2)

    check_weights(config)
    check_floors_ordered(config)
    check_expected_time_min(config)

    config_hash, targets_hash = compute_hashes(config, rules, targets)
    print(f"[BOOT_CHECK OK] config_hash  = {config_hash}")
    print(f"[BOOT_CHECK OK] targets_hash = {targets_hash}")
    print("[BOOT_CHECK] All checks passed. System ready to boot.")

    return config_hash, targets_hash


if __name__ == "__main__":
    run_boot_check()
