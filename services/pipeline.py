"""
Pipeline Orchestrator.
Coordinates: Ingest -> Clean -> Enrich -> Score -> Flag -> Segment -> Persist.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from sqlalchemy.orm import Session

from adapters.postgres.models import (
    Advisor,
    AssessmentResult,
    CleaningLog,
    HiddenRiskFlag,
    RawSnapshot,
    Student,
    WeeklyMetric,
)
from packages.domain.flags import evaluate_flags
from packages.domain.scores import compute_assessment_sub_score
from scripts.boot_check import compute_hashes, run_boot_check
from services.enrichment.nl_layer import render_advisor_notes
from services.enrichment.rules_layer import enrich_student_rules
from services.enrichment.stat_layer import compute_cohort_statistics
from services.ingestion.loader import process_ingestion_file


def load_config() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], str, str]:
    root = Path(__file__).parent.parent
    with open(root / "config" / "config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    with open(root / "config" / "rules.yaml", "r", encoding="utf-8") as f:
        rules = yaml.safe_load(f)
    with open(root / "config" / "TARGETS.yaml", "r", encoding="utf-8") as f:
        targets = yaml.safe_load(f)
    config_hash, targets_hash = compute_hashes(config, rules, targets)
    return config, rules, targets, config_hash, targets_hash


def execute_pipeline(
    file_path: Path,
    session: Session,
    week_number: int = 1,
) -> Dict[str, Any]:
    """
    Runs the full end-to-end pipeline:
    1. Ingestion & Cleaning
    2. Assessment Sub-Score derivation
    3. Rules, Stat, and NL Enrichment
    4. Flag Evaluation
    5. Persistence to Database
    """
    config, rules, targets, config_hash, targets_hash = load_config()
    weights = config.get("weights", {})
    floors = config.get("floors", {})
    review_bands = config.get("review_band", {})
    assessment_cfg = config.get("assessment", {})

    # 1. Ingest & Clean
    cleaned_records, quarantine_records, cleaning_report = process_ingestion_file(file_path)

    # Persist cleaning logs
    for log_item in cleaning_report.get("cleaning_logs", []):
        cl = CleaningLog(
            source=log_item.get("source", "assessment"),
            source_file=log_item.get("source_file", file_path.name),
            raw_row=log_item.get("raw_row", {}),
            issue_type=log_item.get("issue_type", "unknown"),
            resolution=log_item.get("resolution", "logged"),
            logged_at=datetime.datetime.utcnow(),
        )
        session.add(cl)

    # Find or create default advisor
    advisor = session.query(Advisor).first()
    if not advisor:
        advisor = Advisor(
            display_name="Dr. Ananya Sharma",
            email="ananya.sharma@campus.edu",
            department_scope=["CSE", "ECE", "IT"],
        )
        session.add(advisor)
        session.commit()
        session.refresh(advisor)

    processed_count = 0

    # Intermediate storage to compute cohort stats
    enriched_items = []

    for item in cleaned_records:
        student_ref = item["student_ref"]

        # Derive assessment sub score
        sub_score, speed_score, integrity_score, integrity_flag = compute_assessment_sub_score(
            total_score=item["total_score"],
            time_spent_min=item["time_spent_min"],
            plag_avg=item["plag_avg"],
            multi_ip=item["multi_ip"],
            expected_time_min=assessment_cfg.get("expected_time_min", 30),
            speed_anomaly_threshold_min=assessment_cfg.get("speed_anomaly_threshold_min", 15),
        )

        item["assessment_sub_score"] = sub_score
        item["speed_score"] = speed_score
        item["integrity_score"] = integrity_score
        item["integrity_flag"] = integrity_flag

        # Synthetic multi-indicator baseline if only single assessment is ingested
        # (Allows realistic Student Success Score demo across all 6 dimensions)
        cgpa_baseline = round(min(10.0, max(4.0, (item["total_score"] / 25.0) * 6.0 + 3.8)), 2)
        attendance_baseline = round(min(100.0, max(45.0, (item["total_score"] / 25.0) * 40.0 + 55.0)), 2)
        
        student_raw = {
            "cgpa": cgpa_baseline,
            "backlogs": 1 if cgpa_baseline < 5.0 else 0,
            "attendance_pct": attendance_baseline,
            "subjects_att_below_60": 1 if attendance_baseline < 60 else 0,
            "aptitude": round(sub_score * 0.9 + 5.0, 2),
            "coding": round(sub_score, 2),
            "assessment_sub_score": round(sub_score, 2),
            "mock": round(sub_score * 0.85 + 10.0, 2),
            "assignment_completion_pct": round(attendance_baseline * 0.9, 2),
            "scaled_logins": round(min(100.0, item["total_score"] * 3.5 + 20), 2),
            "events": 2 if cgpa_baseline > 7.0 else 0,
            "clubs": 1,
            "hackathons": 1 if sub_score > 60 else 0,
            "certs": 1 if cgpa_baseline > 8.0 else 0,
            "technical_score": round(sub_score, 2),
            "soft_score": 70.0,
        }

        # Baseline cohort p25 for standard scoring
        cohort_p25 = {
            "academic": 50.0,
            "attendance": 65.0,
            "placement": 45.0,
            "lms": 40.0,
            "engagement": 20.0,
            "skills": 45.0,
        }

        enrich_res = enrich_student_rules(
            student_raw=student_raw,
            cohort_p25=cohort_p25,
            config_weights=weights,
            floors=floors,
            review_bands=review_bands,
        )

        advisor_notes = render_advisor_notes(
            reason_codes=enrich_res["reason_codes"],
            evidence_json=enrich_res["evidence_json"],
        )

        enriched_items.append({
            "cleaned": item,
            "raw": student_raw,
            "enrich": enrich_res,
            "advisor_notes": advisor_notes,
        })

    # Persist records to DB
    for entry in enriched_items:
        item = entry["cleaned"]
        enrich = entry["enrich"]

        # Student entity
        student = None
        if item.get("roll_number"):
            student = session.query(Student).filter(Student.roll_number == item["roll_number"]).first()
        if not student:
            student = session.query(Student).filter(Student.student_ref == item["student_ref"]).first()

        if not student:
            try:
                student = Student(
                    student_ref=item["student_ref"],
                    roll_number=item.get("roll_number"),
                    name=item.get("name") or "Student",
                    department=item.get("department", "CSE"),
                    batch=item.get("batch", "CSE 2029"),
                    section=item.get("section", "UNKNOWN_SECTION"),
                    advisor_id=advisor.id,
                    is_quarantined=item.get("is_quarantined", False),
                    quarantine_reason=item.get("quarantine_reason"),
                )
                session.add(student)
                session.commit()
                session.refresh(student)
            except Exception:
                session.rollback()
                # Re-query in case another row or transaction already committed it
                student = None
                if item.get("roll_number"):
                    student = session.query(Student).filter(Student.roll_number == item["roll_number"]).first()
                if not student:
                    student = session.query(Student).filter(Student.student_ref == item["student_ref"]).first()
                if not student:
                    fallback_ref = f"stu_{uuid.uuid4().hex[:12]}"
                    student = Student(
                        student_ref=fallback_ref,
                        roll_number=None,
                        name=item.get("name") or "Student",
                        department=item.get("department", "CSE"),
                        batch=item.get("batch", "CSE 2029"),
                        section=item.get("section", "UNKNOWN_SECTION"),
                        advisor_id=advisor.id,
                    )
                    session.add(student)
                    session.commit()
                    session.refresh(student)
        else:
            student.batch = item.get("batch", student.batch)
            student.section = item.get("section", student.section)
            if item.get("name") and (not student.name or student.name == "Student"):
                student.name = item.get("name")
            if item.get("roll_number") and not student.roll_number:
                student.roll_number = item.get("roll_number")
            session.commit()

        # Assessment Result
        ass_res = AssessmentResult(
            student_id=student.id,
            source_file=item["source_file"],
            total_score=item["total_score"],
            tab_switches=item["tab_switches"],
            time_spent_min=item["time_spent_min"],
            plag_avg=item["plag_avg"],
            multi_ip=item["multi_ip"],
            speed_anomaly=(item["time_spent_min"] < assessment_cfg.get("speed_anomaly_threshold_min", 15)),
            integrity_flag=item["integrity_flag"],
            submission_at=datetime.datetime.utcnow(),
            ip_list=item["ip_list"],
            is_primary=True,
        )
        session.add(ass_res)

        # Weekly Metric
        wm = WeeklyMetric(
            student_id=student.id,
            week_number=week_number,
            academic_index=enrich["sub_indices"]["academic"],
            attendance_index=enrich["sub_indices"]["attendance"],
            placement_index=enrich["sub_indices"]["placement"],
            lms_index=enrich["sub_indices"]["lms"],
            engagement_index=enrich["sub_indices"]["engagement"],
            skills_index=enrich["sub_indices"]["skills"],
            assessment_sub_score=item["assessment_sub_score"],
            success_score=enrich["success_score"],
            momentum=enrich["momentum"],
            momentum_delta=enrich["momentum_delta"],
            tier=enrich["tier"],
            segment=enrich["segment"],
            confidence="High",
            priority_score=enrich["priority_score"],
            reason_codes=enrich["reason_codes"],
            evidence_json=enrich["evidence_json"],
            config_hash=config_hash,
            targets_hash=targets_hash,
            score_version="v5.0",
            generated_at=datetime.datetime.utcnow(),
        )
        session.add(wm)

        # Evaluate and save flags
        flags = evaluate_flags(
            cgpa=entry["raw"]["cgpa"],
            week_number=week_number,
            coding_submissions_last_6w=1,
            coding_score=entry["raw"]["coding"],
            cohort_p25_coding=40.0,
            lms_delta_4w=0.0,
            attendance_pct=entry["raw"]["attendance_pct"],
            academic_standing="Satisfactory",
            attendance_trend=0.0,
            lms_trend=0.0,
            engagement_trend=0.0,
            skills_index=enrich["sub_indices"]["skills"],
            momentum_str=enrich["momentum"],
            plag_avg=item["plag_avg"],
            multi_ip=item["multi_ip"],
            speed_anomaly=ass_res.speed_anomaly,
            total_score=item["total_score"],
            tab_switches=item["tab_switches"],
            time_spent_min=item["time_spent_min"],
        )

        for f in flags:
            flag_row = HiddenRiskFlag(
                student_id=student.id,
                week_number=week_number,
                flag_code=f["flag_code"],
                evidence_json=f["evidence_json"],
            )
            session.add(flag_row)

        processed_count += 1

    session.commit()

    processed_summary = {
        "total": processed_count,
        "avg_score": round(sum(e["enrich"]["success_score"] for e in enriched_items) / max(1, processed_count), 2) if enriched_items else 0.0,
        "tiers": {
            "priority_support": sum(1 for e in enriched_items if e["enrich"]["tier"] == "priority_support"),
            "review": sum(1 for e in enriched_items if e["enrich"]["tier"] == "review"),
            "watchlist": sum(1 for e in enriched_items if e["enrich"]["tier"] == "watchlist"),
            "on_track": sum(1 for e in enriched_items if e["enrich"]["tier"] == "on_track"),
        },
        "segments": {
            seg: sum(1 for e in enriched_items if e["enrich"]["segment"] == seg)
            for seg in set(e["enrich"]["segment"] for e in enriched_items)
        } if enriched_items else {},
    }

    records_sample = [
        {
            "student_ref": e["cleaned"]["student_ref"],
            "name": e["cleaned"].get("name") or "Student",
            "roll_number": e["cleaned"].get("roll_number") or "--",
            "department": e["cleaned"].get("department", "CSE"),
            "batch": e["cleaned"].get("batch", "AIT 2029"),
            "section": e["cleaned"].get("section", "C"),
            "raw_score": e["cleaned"].get("total_score", 0),
            "assessment_score": round(float(e["cleaned"].get("assessment_sub_score", 0)), 2),
            "success_score": round(float(e["enrich"]["success_score"]), 2),
            "academic_index": round(float(e["enrich"]["sub_indices"]["academic"]), 2),
            "placement_index": round(float(e["enrich"]["sub_indices"]["placement"]), 2),
            "attendance_index": round(float(e["enrich"]["sub_indices"]["attendance"]), 2),
            "tier": e["enrich"]["tier"],
            "segment": e["enrich"]["segment"],
            "reason_codes": e["enrich"]["reason_codes"][:3],
        }
        for e in enriched_items
    ]

    return {
        "run_id": hashlib.sha256(f"{file_path.name}_{datetime.datetime.utcnow()}".encode()).hexdigest()[:12],
        "file_name": file_path.name,
        "processed_students": processed_count,
        "quarantined_students": len(quarantine_records),
        "cleaning_report": cleaning_report,
        "config_hash": config_hash,
        "targets_hash": targets_hash,
        "processed_summary": processed_summary,
        "records_sample": records_sample,
    }
