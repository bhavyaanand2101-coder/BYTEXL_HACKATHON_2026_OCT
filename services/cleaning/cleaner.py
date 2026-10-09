"""
Data cleaning and normalization service.
Implements all contract normalizations, quarantine rules, and structured cleaning logs.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import math
import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


STUDENT_ID_SALT = os.getenv("STUDENT_ID_SALT", "CHANGEME_IN_PROD_SECRET_SALT_2026")


def generate_student_ref(roll_number: Optional[str], name: Optional[str]) -> Tuple[str, bool, Optional[str]]:
    """
    Generates canonical or quarantine student ref using SHA256 + salt.
    Returns: (student_ref, is_quarantined, quarantine_reason)
    """
    clean_roll = str(roll_number).strip().upper() if roll_number is not None else ""
    if clean_roll in ("NAN", "NONE", "NULL", ""):
        clean_roll = ""

    clean_name = str(name).strip().upper() if name is not None else ""
    if clean_name in ("NAN", "NONE", "NULL", ""):
        clean_name = ""

    if clean_roll:
        h = hashlib.sha256((clean_roll + STUDENT_ID_SALT).encode("utf-8")).hexdigest()[:12]
        return f"stu_{h}", False, None
    elif clean_name:
        h = hashlib.sha256((clean_name + STUDENT_ID_SALT).encode("utf-8")).hexdigest()[:12]
        return f"stu_quarantine_{h}", False, "Missing roll number (synthesized ref generated)"
    else:
        import uuid
        h = hashlib.sha256(f"unknown_{uuid.uuid4().hex}".encode()).hexdigest()[:12]
        return f"stu_quarantine_{h}", True, "Missing both roll number and name"


def normalize_batch(batch_raw: Any) -> str:
    """
    Trim, uppercase, replace '_' and '-' with space, collapse whitespace -> 'CSE 2029'
    """
    if batch_raw is None or (isinstance(batch_raw, float) and math.isnan(batch_raw)):
        return "CSE 2029"
    s = str(batch_raw).strip().upper()
    if s in ("NAN", "NONE", "NULL", ""):
        return "CSE 2029"
    s = s.replace("_", " ").replace("-", " ")
    s = re.sub(r"\s+", " ", s)
    return s if s else "CSE 2029"


def normalize_section(section_raw: Any) -> str:
    """
    Trim, uppercase, strip leading 'SECTION ', take final token -> 'C' | 'D' | 'UNKNOWN_SECTION'
    """
    if section_raw is None or (isinstance(section_raw, float) and math.isnan(section_raw)):
        return "UNKNOWN_SECTION"
    s = str(section_raw).strip().upper()
    if s in ("NAN", "NONE", "NULL", ""):
        return "UNKNOWN_SECTION"
    s = re.sub(r"^SECTION\s+", "", s)
    tokens = s.split()
    sec = tokens[-1] if tokens else "UNKNOWN_SECTION"
    if sec in ("C", "D", "A", "B", "E"):
        return sec
    return sec if sec else "UNKNOWN_SECTION"


def normalize_time_spent(time_raw: Any) -> Tuple[float, Optional[str]]:
    """
    Parse time into float minutes:
    - '28.6' -> 28.6
    - '28.6m' -> 28.6
    - '1h 20m' -> 80.0
    - '1h' -> 60.0
    Returns: (minutes_float, issue_or_none)
    """
    if time_raw is None or (isinstance(time_raw, float) and math.isnan(time_raw)):
        return 30.0, "missing_time"
    s = str(time_raw).strip().lower()
    if not s or s in ("nan", "none", "null"):
        return 30.0, "missing_time"

    # Numeric / simple float string
    if re.match(r"^[0-9.]+$", s):
        try:
            val = float(s)
            if math.isnan(val) or val <= 0:
                return 30.0, "invalid_time"
            return val, None
        except ValueError:
            return 30.0, "unparseable_time"

    # '28.6m'
    m_match = re.match(r"^([0-9.]+)m$", s)
    if m_match:
        try:
            val = float(m_match.group(1))
            if math.isnan(val) or val <= 0:
                return 30.0, "invalid_time"
            return val, None
        except ValueError:
            return 30.0, "unparseable_time"

    # '1h 20m' or '1h20m' or '1h'
    h_match = re.match(r"^(\d+)h\s*(\d+)?m?$", s)
    if h_match:
        hours = float(h_match.group(1))
        minutes = float(h_match.group(2)) if h_match.group(2) else 0.0
        val = hours * 60.0 + minutes
        return (val if val > 0 else 30.0), None

    return 30.0, "unparseable_time"


def normalize_ip_list(ip_raw: Any) -> List[str]:
    """
    Split on comma, trim each, drop empties.
    """
    if ip_raw is None:
        return []
    s = str(ip_raw).strip()
    if not s or s.lower() in ("nan", "none"):
        return []
    parts = [p.strip() for p in s.split(",")]
    return [p for p in parts if p]


def clean_student_assessment_record(
    raw_row: Dict[str, Any],
    source_file: str,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], bool, Optional[str]]:
    """
    Cleans a single assessment row.
    Returns: (cleaned_dict, cleaning_logs, is_quarantined, quarantine_reason)
    """
    logs = []
    
    # 1. Roll number and Name
    raw_roll = raw_row.get("roll_number")
    clean_roll_str: Optional[str] = None
    if raw_roll is not None:
        cand = re.sub(r"\.0$", "", str(raw_roll).strip())
        if cand and cand.lower() not in ("nan", "none", "null", ""):
            clean_roll_str = cand

    raw_name = raw_row.get("name")
    clean_name_str: Optional[str] = None
    if raw_name is not None:
        cand = str(raw_name).strip()
        if cand and cand.lower() not in ("nan", "none", "null", ""):
            clean_name_str = cand

    student_ref, is_quarantined, quarantine_reason = generate_student_ref(clean_roll_str, clean_name_str)

    if is_quarantined:
        return {}, logs, True, quarantine_reason

    # 2. Batch and Section
    raw_section = raw_row.get("section")
    raw_batch = raw_row.get("batch")
    raw_branch = raw_row.get("branch")

    if raw_section:
        section = normalize_section(raw_section)
        batch = normalize_batch(raw_batch or raw_branch)
    else:
        raw_b = str(raw_batch or "").strip()
        raw_br = str(raw_branch or "").strip()
        if "SECTION" in raw_b.upper():
            batch = normalize_batch(raw_br)
            section = normalize_section(raw_b)
        elif "SECTION" in raw_br.upper():
            batch = normalize_batch(raw_b)
            section = normalize_section(raw_br)
        else:
            batch = normalize_batch(raw_batch)
            section = normalize_section(raw_branch)

    # 3. Total Score (Range [0, 25], flag out-of-range, do NOT clamp)
    raw_score = raw_row.get("total_score")
    flag_score_out_of_range = False
    try:
        if raw_score is None:
            score_val = 0.0
            logs.append({
                "source": "assessment",
                "source_file": source_file,
                "raw_row": raw_row,
                "issue_type": "missing_score",
                "resolution": "defaulted_to_0",
                "logged_at": datetime.datetime.utcnow().isoformat(),
            })
        else:
            score_val = float(raw_score)
            if math.isnan(score_val):
                score_val = 0.0
                logs.append({
                    "source": "assessment",
                    "source_file": source_file,
                    "raw_row": raw_row,
                    "issue_type": "nan_score",
                    "resolution": "defaulted_to_0",
                    "logged_at": datetime.datetime.utcnow().isoformat(),
                })
            elif score_val < 0 or score_val > 25:
                flag_score_out_of_range = True
                logs.append({
                    "source": "assessment",
                    "source_file": source_file,
                    "raw_row": raw_row,
                    "issue_type": "total_score_out_of_range",
                    "resolution": "flagged_not_clamped",
                    "logged_at": datetime.datetime.utcnow().isoformat(),
                })
    except (ValueError, TypeError):
        score_val = 0.0
        logs.append({
            "source": "assessment",
            "source_file": source_file,
            "raw_row": raw_row,
            "issue_type": "non_numeric_score",
            "resolution": "set_to_zero_and_flagged",
            "logged_at": datetime.datetime.utcnow().isoformat(),
        })

    # 4. Tab Switches (int >= 0, negatives set to 0 and flagged)
    raw_tab = raw_row.get("tab_switches")
    try:
        if raw_tab is None or (isinstance(raw_tab, float) and math.isnan(raw_tab)):
            tab_switches = 0
        else:
            tab_switches = int(float(raw_tab))
        if tab_switches < 0:
            tab_switches = 0
            logs.append({
                "source": "assessment",
                "source_file": source_file,
                "raw_row": raw_row,
                "issue_type": "negative_tab_switches",
                "resolution": "set_to_0",
                "logged_at": datetime.datetime.utcnow().isoformat(),
            })
    except (ValueError, TypeError):
        tab_switches = 0

    # 5. Time Spent
    time_spent, time_issue = normalize_time_spent(raw_row.get("time_spent_raw"))
    if time_spent is None or math.isnan(time_spent) or time_spent <= 0:
        time_spent = 30.0
    if time_issue:
        logs.append({
            "source": "assessment",
            "source_file": source_file,
            "raw_row": raw_row,
            "issue_type": time_issue,
            "resolution": "fallback_to_expected_time",
            "logged_at": datetime.datetime.utcnow().isoformat(),
        })

    # 6. IP Address
    ip_list = normalize_ip_list(raw_row.get("ip_address"))
    multi_ip = len(ip_list) > 1

    # 7. Plagiarism percentages
    plag_vals = []
    for p_key in ("plag_1", "plag_2", "plag_3"):
        val = raw_row.get(p_key)
        if val is not None:
            try:
                p_float = float(val)
                if math.isnan(p_float):
                    continue
                if p_float > 100.0:
                    p_float = 100.0
                    logs.append({
                        "source": "assessment",
                        "source_file": source_file,
                        "raw_row": raw_row,
                        "issue_type": "plag_over_100",
                        "resolution": "clipped_to_100",
                        "logged_at": datetime.datetime.utcnow().isoformat(),
                    })
                plag_vals.append(max(0.0, p_float))
            except (ValueError, TypeError):
                pass
    plag_avg = sum(plag_vals) / len(plag_vals) if plag_vals else 0.0
    if math.isnan(plag_avg):
        plag_avg = 0.0

    # 8. Submission Date
    sub_date = raw_row.get("submission_date")
    if sub_date:
        if isinstance(sub_date, datetime.datetime):
            sub_date_iso = sub_date.isoformat()
        else:
            sub_date_iso = str(sub_date)
    else:
        sub_date_iso = datetime.datetime.utcnow().isoformat()

    cleaned = {
        "student_ref": student_ref,
        "roll_number": clean_roll_str,
        "name": clean_name_str or "Student",
        "department": "CSE",
        "batch": batch,
        "section": section,
        "total_score": score_val,
        "tab_switches": tab_switches,
        "time_spent_min": time_spent,
        "ip_list": ip_list,
        "multi_ip": multi_ip,
        "plag_avg": plag_avg,
        "submission_at": sub_date_iso,
        "source_file": source_file,
        "is_quarantined": is_quarantined,
        "quarantine_reason": quarantine_reason,
    }

    return cleaned, logs, False, None
