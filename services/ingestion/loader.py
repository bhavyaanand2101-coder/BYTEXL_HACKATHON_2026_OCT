"""
Ingestion Service.
Reads Excel and CSV files, maps canonical columns, attaches SHA256 snapshots,
invokes cleaner and produces structured cleaning reports.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import openpyxl
import pandas as pd
from services.cleaning.cleaner import clean_student_assessment_record


CANONICAL_COLUMN_MAP = {
    "roll_number": ["Roll Number", "Roll Num", "roll_number", "roll number", "Roll No", "Roll"],
    "name": ["Name", "Student Name", "name", "student_name"],
    "branch": ["Branch", "Department", "branch", "dept"],
    "batch": ["Batch", "batch", "Year"],
    "section": ["Section", "section", "Sec"],
    "total_score": ["Total Score", "Score Num", "Score", "total_score", "Total"],
    "tab_switches": ["Tab switches", "Tab Switches", "tab_switches", "Tabs"],
    "time_spent_raw": ["Time Spent", "Time Spent (raw)", "Time (min)", "time_spent", "Duration"],
    "submission_date": ["Submission Date", "Timestamp", "submission_date", "Date"],
    "ip_address": ["IP Address", "ip_address", "IP"],
    "plag_1": ["Plagiarism %", "Plag 1%", "plag_1", "Plagiarism 1"],
    "plag_2": ["Plagiarism %3", "Plag 2%", "plag_2", "Plagiarism 2"],
    "plag_3": ["Plagiarism %5", "Plag 3%", "plag_3", "Plagiarism 3"],
}


def compute_file_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def map_row_to_canonical(raw_dict: Dict[str, Any]) -> Dict[str, Any]:
    mapped: Dict[str, Any] = {}
    normalized_keys = {str(k).strip().lower(): k for k in raw_dict}

    for canonical_field, aliases in CANONICAL_COLUMN_MAP.items():
        found = False
        for alias in aliases:
            low_alias = alias.strip().lower()
            if low_alias in normalized_keys:
                orig_key = normalized_keys[low_alias]
                mapped[canonical_field] = raw_dict[orig_key]
                found = True
                break
        if not found:
            mapped[canonical_field] = None

    return mapped


def read_file_rows(file_path: Path) -> List[Dict[str, Any]]:
    """
    Reads file using openpyxl (with fallback) or pandas.
    """
    suffix = file_path.suffix.lower()
    if suffix in (".xlsx", ".xlsm", ".xltx"):
        try:
            # First attempt with openpyxl data_only=True
            wb = openpyxl.load_workbook(file_path, data_only=True)
            sheet = wb.active
            rows = list(sheet.iter_rows(values_only=True))
            if not rows or len(rows) < 2:
                return []
            header = [str(c).strip() if c is not None else f"col_{i}" for i, c in enumerate(rows[0])]
            result = []
            for row_idx, r in enumerate(rows[1:], start=2):
                if not any(r):
                    continue
                row_dict = {}
                for i, col_name in enumerate(header):
                    val = r[i] if i < len(r) else None
                    row_dict[col_name] = val
                result.append(row_dict)
            return result
        except Exception:
            df = pd.read_excel(file_path)
            return df.to_dict(orient="records")
    elif suffix in (".csv", ".txt"):
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def process_ingestion_file(
    file_path: Path,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    """
    Executes full ingestion & cleaning pipeline on a raw file.
    Returns: (cleaned_records, quarantine_records, cleaning_report)
    """
    sha256_hash = compute_file_sha256(file_path)
    raw_rows = read_file_rows(file_path)
    file_name = file_path.name

    cleaned_records = []
    quarantine_records = []
    all_logs = []
    quarantine_reasons = {}

    seen_rolls = {}
    duplicates_count = 0
    repaired_count = 0

    for idx, raw in enumerate(raw_rows):
        canonical_raw = map_row_to_canonical(raw)
        row_sha = hashlib.sha256(json.dumps(canonical_raw, sort_keys=True, default=str).encode()).hexdigest()

        cleaned, logs, is_quarantined, q_reason = clean_student_assessment_record(
            canonical_raw,
            source_file=file_name,
        )

        all_logs.extend(logs)
        if logs:
            repaired_count += 1

        if is_quarantined:
            quarantine_records.append({
                "source_file": file_name,
                "raw_payload": canonical_raw,
                "quarantine_reason": q_reason,
                "row_sha256": row_sha,
                "ingested_at": datetime.datetime.utcnow().isoformat(),
            })
            quarantine_reasons[q_reason] = quarantine_reasons.get(q_reason, 0) + 1
        else:
            # Check duplicate roll numbers (keep latest or update)
            r_num = cleaned.get("roll_number")
            if r_num and r_num in seen_rolls:
                duplicates_count += 1
                # Replace with latest record
                cleaned_records[seen_rolls[r_num]] = cleaned
            else:
                if r_num:
                    seen_rolls[r_num] = len(cleaned_records)
                cleaned_records.append(cleaned)

    # Sort cleaned records by (source_file, student_ref) to guarantee stable idempotent row order
    cleaned_records.sort(key=lambda r: (r.get("source_file", ""), r.get("student_ref", "")))

    total_received = len(raw_rows)
    report = {
        "received": total_received,
        "repaired": repaired_count,
        "dropped": len(quarantine_records),
        "ambiguous": len(quarantine_records),
        "duplicates": duplicates_count,
        "missing_rate": round(len(quarantine_records) / max(1, total_received), 4),
        "per_source": {
            file_name: {
                "received": total_received,
                "cleaned": len(cleaned_records),
                "quarantined": len(quarantine_records),
                "sha256": sha256_hash,
            }
        },
        "quarantined": len(quarantine_records),
        "quarantine_reasons": quarantine_reasons,
        "cleaning_logs": all_logs,
    }

    return cleaned_records, quarantine_records, report
