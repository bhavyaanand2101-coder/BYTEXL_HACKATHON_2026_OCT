"""
Natural Language Enrichment Layer (Frozen Templates Only).
Turns reason_codes + evidence_json into plain-language advisor copy.
CRITICAL: Pure function of (reason_codes, evidence_json). No network / LLM calls.
"""

from __future__ import annotations

from typing import Any, Dict, List


FROZEN_TEMPLATES: Dict[str, Dict[str, str]] = {
    "HARD_FLOOR_ATTENDANCE": {
        "title": "Attendance below institutional threshold",
        "body": "Attendance is {attendance_pct:.0f}%, which is below the minimum mandatory requirement. Immediate advisor reach-out is required.",
    },
    "HARD_FLOOR_CGPA": {
        "title": "Academic standing risk (CGPA < 4.7)",
        "body": "Current CGPA of {cgpa:.2f} is in the critical academic standing band. Remedial tutoring recommended.",
    },
    "HARD_FLOOR_BACKLOGS": {
        "title": "Critical backlog accumulation",
        "body": "Student has {backlogs} active backlogs exceeding the threshold. Clear credit backlog roadmap needed.",
    },
    "LOW_ATTENDANCE": {
        "title": "Schedule attendance conversation",
        "body": "Attendance is {attendance_pct:.0f}%. A 15-minute check-in may surface personal or transit barriers.",
    },
    "LOW_LMS": {
        "title": "Check LMS access & assignment backlog",
        "body": "LMS activity is below cohort p25. Recommend verifying portal login and reviewing pending assignment submissions.",
    },
    "LOW_ENGAGEMENT": {
        "title": "Recommend a club or hackathon",
        "body": "Extracurricular engagement index is in the bottom quartile. Participation in 1-2 campus events will boost profile.",
    },
    "PLACEMENT_GAP": {
        "title": "Enrol in coding / aptitude prep",
        "body": "Strong academic record but coding and placement readiness signals are lagging. Enrolment in mock practice recommended.",
    },
}


def render_advisor_notes(
    reason_codes: List[str],
    evidence_json: Dict[str, Any],
) -> List[Dict[str, str]]:
    """
    Renders human-readable advisor action recommendations.
    Deterministic, pure function of (reason_codes, evidence_json).
    """
    rendered = []
    
    # Defaults for template formatting to ensure stability
    context = {
        "attendance_pct": float(evidence_json.get("attendance_pct", 75.0)),
        "cgpa": float(evidence_json.get("cgpa", 7.0)),
        "backlogs": int(evidence_json.get("backlogs", 0)),
        "coding_score": float(evidence_json.get("coding_score", 50.0)),
    }

    # Sort reason codes to guarantee deterministic ordering
    sorted_codes = sorted(list(set(reason_codes)))

    for code in sorted_codes:
        if code in FROZEN_TEMPLATES:
            tmpl = FROZEN_TEMPLATES[code]
            title = tmpl["title"]
            try:
                body = tmpl["body"].format(**context)
            except Exception:
                body = tmpl["body"]
            rendered.append({
                "code": code,
                "title": title,
                "body": body,
            })

    if not rendered:
        rendered.append({
            "code": "ON_TRACK_GENERAL",
            "title": "Routine Progress Review",
            "body": "Student is progressing within expected performance parameters across major indicators.",
        })

    return rendered
