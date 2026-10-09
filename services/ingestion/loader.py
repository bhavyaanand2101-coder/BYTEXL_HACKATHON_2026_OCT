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
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import openpyxl
import pandas as pd
from services.cleaning.cleaner import clean_student_assessment_record


CANONICAL_COLUMN_MAP = {
    "roll_number": ["Roll Number", "Roll Num", "roll_number", "roll number", "Roll No", "Roll", "roll", "Enrollment No", "Enrollment", "Enrolment No", "Reg No", "Registration No", "URN", "Student ID", "StudentID", "ID", "RollNo", "Roll_No", "SRN", "Hall Ticket No", "student_ref"],
    "name": ["Name", "Student Name", "name", "student_name", "Full Name", "Candidate Name", "Student", "Learner Name", "Participant Name", "first_name"],
    "branch": ["Branch", "Department", "branch", "dept", "Dept", "Stream", "Course", "Discipline", "Program"],
    "batch": ["Batch", "batch", "Year", "Class", "Cohort", "Academic Year"],
    "section": ["Section", "section", "Sec", "sec", "Division", "Div", "Group"],
    "total_score": ["Total Score", "Score Num", "Score", "total_score", "Total", "score", "Marks", "Marks Obtained", "Total Marks", "Assessment Score", "Test Score", "Quiz Score", "Exam Score", "Percentage", "Score %", "Grade", "CGPA", "success_score", "academic_index"],
    "tab_switches": ["Tab switches", "Tab Switches", "tab_switches", "Tabs", "Tab Switch", "Tab Switch Count"],
    "time_spent_raw": ["Time Spent", "Time Spent (raw)", "Time (min)", "time_spent", "Duration", "Time", "Time Taken", "Duration (min)"],
    "submission_date": ["Submission Date", "Timestamp", "submission_date", "Date", "Submitted At", "Submitted Date"],
    "ip_address": ["IP Address", "ip_address", "IP", "IPs", "Client IP"],
    "plag_1": ["Plagiarism %", "Plag 1%", "plag_1", "Plagiarism 1", "Plag 1"],
    "plag_2": ["Plagiarism %3", "Plag 2%", "plag_2", "Plagiarism 2", "Plag 2"],
    "plag_3": ["Plagiarism %5", "Plag 3%", "plag_3", "Plagiarism 3", "Plag 3"],
}


def compute_file_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def map_row_to_canonical(raw_dict: Dict[str, Any]) -> Dict[str, Any]:
    mapped: Dict[str, Any] = {}
    # Map alphanumeric cleaned key -> original key
    normalized_keys = {re.sub(r"[^a-z0-9]", "", str(k).strip().lower()): k for k in raw_dict}

    for canonical_field, aliases in CANONICAL_COLUMN_MAP.items():
        found = False
        for alias in aliases:
            norm_alias = re.sub(r"[^a-z0-9]", "", alias.strip().lower())
            if norm_alias in normalized_keys:
                orig_key = normalized_keys[norm_alias]
                mapped[canonical_field] = raw_dict[orig_key]
                found = True
                break
        if not found:
            mapped[canonical_field] = None

    # Fallback heuristics for non-standard or custom column headers
    if mapped.get("roll_number") is None:
        for k, v in raw_dict.items():
            k_low = str(k).lower()
            if any(term in k_low for term in ["roll", "reg", "enrol", "urn", "prn", "usn", "id", "seat", "admit"]) and v is not None and str(v).strip():
                mapped["roll_number"] = str(v).strip()
                break

    if mapped.get("name") is None:
        for k, v in raw_dict.items():
            k_low = str(k).lower()
            if any(term in k_low for term in ["name", "student", "cand", "learner", "person"]) and v is not None and str(v).strip():
                mapped["name"] = str(v).strip()
                break

    if mapped.get("total_score") is None:
        for k, v in raw_dict.items():
            k_low = str(k).lower()
            if any(term in k_low for term in ["score", "mark", "point", "grade", "total", "val", "result", "pct"]):
                try:
                    mapped["total_score"] = float(v)
                    break
                except (ValueError, TypeError):
                    pass

    return mapped


def read_file_rows(file_path: Path) -> List[Dict[str, Any]]:
    """
    Reads file using openpyxl (with dynamic header detection) or pandas.
    """
    suffix = file_path.suffix.lower()
    if suffix in (".xlsx", ".xlsm", ".xltx"):
        try:
            wb = openpyxl.load_workbook(file_path, data_only=True)
            sheet = wb.active
            rows = list(sheet.iter_rows(values_only=True))
            if not rows or len(rows) < 2:
                return []

            # Scan first 10 rows to detect the true header row
            header_row_idx = 0
            best_match_score = -1
            known_tokens = {
                "roll", "number", "name", "student", "score", "marks", "total",
                "batch", "dept", "branch", "sec", "cgpa", "time", "date", "plag"
            }
            for candidate_idx, candidate_row in enumerate(rows[:10]):
                if not candidate_row:
                    continue
                non_empty = [str(c).strip().lower() for c in candidate_row if c is not None and str(c).strip()]
                if not non_empty:
                    continue
                match_count = sum(1 for cell in non_empty if any(tok in cell for tok in known_tokens))
                candidate_score = match_count * 10 + len(non_empty)
                if candidate_score > best_match_score:
                    best_match_score = candidate_score
                    header_row_idx = candidate_idx

            header = [str(c).strip() if c is not None else f"col_{i}" for i, c in enumerate(rows[header_row_idx])]
            result = []
            for row_idx, r in enumerate(rows[header_row_idx + 1:], start=header_row_idx + 2):
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
        try:
            df = pd.read_csv(file_path)
            return df.to_dict(orient="records")
        except Exception:
            df = pd.read_csv(file_path, encoding="latin1")
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
