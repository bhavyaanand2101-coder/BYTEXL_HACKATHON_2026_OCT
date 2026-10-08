"""
CampusPulse — Seed Realistic Demo Interventions
Creates 7 simulated demo intervention records for closed-loop advisor demonstration.
All records are explicitly tagged as [SIMULATED/DEMO] per Rule 05.
"""

import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Ensure root directory is on sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from adapters.postgres.models import Advisor, Intervention, Student
from adapters.postgres.repository import SessionLocal


def seed_demo_interventions():
    db = SessionLocal()
    try:
        advisor = db.query(Advisor).first()
        if not advisor:
            print("[seed_interventions] No advisor found. Creating default advisor...")
            advisor = Advisor(
                id=str(uuid.uuid4()),
                display_name="Dr. Ananya Sharma",
                email="ananya.sharma@campus.edu",
                department_scope="CSE",
            )
            db.add(advisor)
            db.commit()

        # Delete any existing demo interventions to ensure idempotent re-runs
        deleted_count = db.query(Intervention).filter(Intervention.notes.like("%[SIMULATED/DEMO]%")).delete(synchronize_session=False)
        db.commit()
        if deleted_count > 0:
            print(f"[seed_interventions] Removed {deleted_count} previous simulated demo intervention(s).")

        now = datetime.now(timezone.utc)

        # Mapping of targets
        records_to_seed = [
            {
                "roll": "251302312",  # VANSHIKA
                "name": "VANSHIKA",
                "action_code": "PLACEMENT_GAP",
                "notes": "[SIMULATED/DEMO] Coding Clinic: Enrolled in bi-weekly python problem-solving lab and mock coding clinic to address placement aptitude gap.",
                "status": "IN_PROGRESS",
                "days_offset_due": 14,
                "days_offset_created": -3,
            },
            {
                "roll": "251302311",  # Raaghav Madaan
                "name": "Raaghav Madaan",
                "action_code": "LOW_ATTENDANCE",
                "notes": "[SIMULATED/DEMO] Attendance Review: 15-minute faculty check-in conducted. Student cited health barriers; structured attendance recovery plan approved.",
                "status": "COMPLETED",
                "days_offset_due": -2,
                "days_offset_created": -10,
            },
            {
                "roll": "251302330",  # TUSHAR SINGH / or by student_ref fallback
                "student_ref": "stu_a8caec57102b",
                "name": "TUSHAR SINGH",
                "action_code": "CGPA_FLOOR",
                "notes": "[SIMULATED/DEMO] Academic Faculty Review: Referred to academic tutoring cell for remedial tutoring in core subject backlog.",
                "status": "OPEN",
                "days_offset_due": 10,
                "days_offset_created": -1,
            },
            {
                "student_ref": "stu_e445416c629e",
                "name": "Aryan Mann",
                "action_code": "LOW_LMS",
                "notes": "[SIMULATED/DEMO] LMS Engagement Program: Advisor verified LMS portal login credentials and scheduled checkpoint for 3 pending module submissions.",
                "status": "IN_PROGRESS",
                "days_offset_due": 12,
                "days_offset_created": -4,
            },
            {
                "student_ref": "stu_696f9974bad8",
                "name": "JITEN .",
                "action_code": "PLACEMENT_GAP",
                "notes": "[SIMULATED/DEMO] Placement Mentoring: Assigned to senior peer mentor for technical mock interviews and resume ATS optimization.",
                "status": "COMPLETED",
                "days_offset_due": -5,
                "days_offset_created": -14,
            },
            {
                "student_ref": "stu_9f9974d49a1b",
                "name": "SAHIL YADAV",
                "action_code": "LOW_ENGAGEMENT",
                "notes": "[SIMULATED/DEMO] Extracurricular Engagement: Recommended participation in department IoT hackathon and open-source campus club.",
                "status": "OPEN",
                "days_offset_due": 14,
                "days_offset_created": 0,
            },
            {
                "student_ref": "stu_38e1360104d2",
                "name": "ANNU SINGH",
                "action_code": "PLACEMENT_GAP",
                "notes": "[SIMULATED/DEMO] Interview Preparation: Completed preliminary behavioral mock interview session; scheduled technical DSA round.",
                "status": "IN_PROGRESS",
                "days_offset_due": 8,
                "days_offset_created": -2,
            },
        ]

        seeded_count = 0
        for item in records_to_seed:
            student = None
            if "student_ref" in item:
                student = db.query(Student).filter(Student.student_ref == item["student_ref"]).first()
            if not student and "roll" in item:
                student = db.query(Student).filter(Student.roll_number == item["roll"]).first()
            if not student and "name" in item:
                student = db.query(Student).filter(Student.name == item["name"]).first()

            if not student:
                # Fallback to any student in db
                student = db.query(Student).offset(seeded_count).first()

            if not student:
                continue

            created_time = now + timedelta(days=item["days_offset_created"])
            due_time = now + timedelta(days=item["days_offset_due"])

            intervention = Intervention(
                id=str(uuid.uuid4()),
                student_id=student.id,
                advisor_id=advisor.id,
                action_code=item["action_code"],
                notes=item["notes"],
                status=item["status"],
                due_at=due_time.replace(tzinfo=None),
                created_at=created_time.replace(tzinfo=None),
                updated_at=created_time.replace(tzinfo=None),
            )
            db.add(intervention)
            seeded_count += 1

        db.commit()
        print(f"[seed_interventions] Successfully seeded {seeded_count} simulated demo interventions for advisor '{advisor.display_name}'.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_interventions()
