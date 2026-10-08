"""
CampusPulse Demo Seed Script — v5.0
Deterministic, idempotent, re-runnable.

Creates 52 students across:
  - Section C & D, Batch CSE 2029
  - 4 weeks of historical data
  - All 4 tiers: Priority Support, Review Band, Watchlist, On Track
  - Includes VANSHIKA (low score → Priority Support)
  - Includes Aarav Sharma (demo student → On Track / Academic Star)

Run with:
  PYTHONPATH=. python3 scripts/seed_demo.py
"""

import random
from pathlib import Path

import pandas as pd
from adapters.postgres.repository import SessionLocal, init_db
from services.pipeline import execute_pipeline

# Fixed seed for determinism
random.seed(42)

# ── Student roster ────────────────────────────────────────────────────────────
# Format: (roll, name, section, batch, target_tier_hint, scores_w1..w4)
# scores are out of 25 (the test max). Pipeline derives everything else.
STUDENTS = [
    # ── Priority Support (attendance/CGPA floor triggers) ──────────────────
    # Very low test scores → low CGPA proxy → priority_support via score band
    ("2023CSE044", "VANSHIKA",          "C", "CSE 2029", [3.0, 3.5, 4.0, 3.2]),
    ("2023CSE045", "RAHUL .",           "C", "CSE 2029", [4.0, 3.0, 4.5, 4.0]),
    ("2023CSE071", "DHEEREN .",         "D", "CSE 2029", [3.5, 4.0, 3.0, 3.5]),
    ("2023CSE072", "HEMANT .",          "D", "CSE 2029", [2.5, 3.0, 3.5, 2.8]),

    # ── Review Band (borderline CGPA/attendance) ───────────────────────────
    ("2023CSE020", "ANNU SINGH",        "C", "CSE 2029", [4.8, 5.0, 5.2, 4.9]),
    ("2023CSE021", "KARTIK .",          "C", "CSE 2029", [4.6, 4.8, 5.1, 4.7]),
    ("2023CSE073", "PIHU .",            "D", "CSE 2029", [5.0, 5.2, 4.9, 5.1]),
    ("2023CSE074", "SNEHA MOR",         "D", "CSE 2029", [4.7, 5.1, 4.8, 5.0]),

    # ── Watchlist ──────────────────────────────────────────────────────────
    ("2023CSE005", "DAHIYA KRISH",      "C", "CSE 2029", [11.0, 11.5, 12.0, 11.8]),
    ("2023CSE006", "KAVYA MENON",       "C", "CSE 2029", [10.5, 11.0, 10.8, 11.2]),
    ("2023CSE015", "ANGEL TYAGI",       "C", "CSE 2029", [12.0, 11.5, 12.5, 12.0]),
    ("2023CSE016", "PIYUSH GUPTA",      "C", "CSE 2029", [11.5, 12.0, 11.0, 12.5]),
    ("2023CSE017", "HARDIK YADAV",      "C", "CSE 2029", [10.0, 10.5, 11.0, 10.8]),
    ("2023CSE051", "ESHAN VERMA",       "D", "CSE 2029", [12.5, 13.0, 12.0, 13.5]),
    ("2023CSE052", "FATIMA SHEIKH",     "D", "CSE 2029", [11.0, 11.5, 12.0, 11.8]),
    ("2023CSE060", "LAXMI SHARMA",      "D", "CSE 2029", [10.5, 11.0, 11.5, 12.0]),
    ("2023CSE061", "ASHWANI .",         "D", "CSE 2029", [12.0, 11.5, 12.5, 12.0]),

    # ── On Track ───────────────────────────────────────────────────────────
    # Aarav Sharma — Academic Star, demo student
    ("2023CSE001", "Aarav Sharma",      "C", "CSE 2029", [24.5, 23.8, 24.0, 24.2]),
    ("2023CSE002", "Bhavya Gupta",      "C", "CSE 2029", [20.0, 20.5, 21.0, 21.5]),
    ("2023CSE003", "Chirag Patel",      "C", "CSE 2029", [18.5, 19.0, 19.5, 20.0]),
    ("2023CSE004", "Diya Nair",         "C", "CSE 2029", [17.0, 17.5, 18.0, 18.5]),
    ("2023CSE007", "Nikhil Varma",      "C", "CSE 2029", [22.0, 21.5, 22.5, 23.0]),
    ("2023CSE008", "GEETIKA .",         "C", "CSE 2029", [19.0, 19.5, 20.0, 20.5]),
    ("2023CSE009", "PALAK KUMARI",      "C", "CSE 2029", [18.0, 18.5, 19.0, 19.5]),
    ("2023CSE010", "KRISHANT SETHI",    "C", "CSE 2029", [17.5, 18.0, 18.5, 19.0]),
    ("2023CSE011", "HARSHIT JOON",      "C", "CSE 2029", [21.0, 21.5, 22.0, 22.5]),
    ("2023CSE012", "TAMANNA .",         "C", "CSE 2029", [16.5, 17.0, 17.5, 18.0]),
    ("2023CSE013", "ISHIKA .",          "C", "CSE 2029", [20.5, 21.0, 21.5, 22.0]),
    ("2023CSE014", "PUNEET SINGH",      "C", "CSE 2029", [19.5, 20.0, 20.5, 21.0]),
    ("2023CSE018", "ARPAN",             "C", "CSE 2029", [16.0, 16.5, 17.0, 17.5]),
    ("2023CSE019", "SHIVEN S. SINHA",   "C", "CSE 2029", [18.5, 19.0, 19.5, 20.0]),
    ("2023CSE022", "HITESH KUMAR",      "C", "CSE 2029", [17.5, 18.0, 18.5, 19.0]),
    ("2023CSE023", "PRIYA VERMA",       "C", "CSE 2029", [22.5, 23.0, 23.5, 24.0]),
    ("2023CSE024", "MUSKAN SHARMA",     "C", "CSE 2029", [20.0, 20.5, 21.0, 21.5]),
    ("2023CSE025", "AAKASH",            "C", "CSE 2029", [19.0, 19.5, 20.0, 20.5]),
    ("2023CSE053", "GAURAV SEN",        "D", "CSE 2029", [23.5, 24.0, 23.8, 24.5]),
    ("2023CSE054", "HITESH RAO",        "D", "CSE 2029", [21.0, 21.5, 22.0, 22.5]),
    ("2023CSE055", "POOJA REDDY",       "D", "CSE 2029", [20.5, 21.0, 21.5, 22.0]),
    ("2023CSE056", "ROHAN MEHRA",       "D", "CSE 2029", [19.5, 20.0, 20.5, 21.0]),
    ("2023CSE057", "HARSHITA",          "D", "CSE 2029", [22.0, 22.5, 23.0, 23.5]),
    ("2023CSE058", "Sourav Das",        "D", "CSE 2029", [18.5, 19.0, 19.5, 20.0]),
    ("2023CSE059", "ANJALI RAO",        "D", "CSE 2029", [21.5, 22.0, 22.5, 23.0]),
    ("2023CSE062", "JATIN",             "D", "CSE 2029", [17.0, 17.5, 18.0, 18.5]),
    ("2023CSE063", "LOKESH KUMAR",      "D", "CSE 2029", [19.0, 19.5, 20.0, 20.5]),
    ("2023CSE064", "RAUSHAN KUMAR",     "D", "CSE 2029", [18.0, 18.5, 19.0, 19.5]),
    ("2023CSE065", "RIYA VISHWAKARMA",  "D", "CSE 2029", [20.0, 20.5, 21.0, 21.5]),
    ("2023CSE066", "PRANVI SHARMA",     "D", "CSE 2029", [22.5, 23.0, 23.5, 24.0]),
    ("2023CSE067", "PARTH BAJAJ",       "D", "CSE 2029", [16.5, 17.0, 17.5, 18.0]),
    ("2023CSE068", "YASH CHAUHAN",      "D", "CSE 2029", [21.0, 21.5, 22.0, 22.5]),
    ("2023CSE069", "ARYAN MANN",        "D", "CSE 2029", [23.0, 23.5, 24.0, 24.5]),
    ("2023CSE070", "MANU SINGH",        "D", "CSE 2029", [17.5, 18.0, 18.5, 19.0]),
]

PLAG_MAP = {
    # (roll): avg plag across weeks
    "2023CSE044": 45.0,   # VANSHIKA — high plag penalty
    "2023CSE045": 30.0,
    "2023CSE071": 35.0,
    "2023CSE072": 50.0,
    "2023CSE020": 5.0,
    "2023CSE021": 3.0,
    "2023CSE073": 4.0,
    "2023CSE074": 6.0,
}


def build_week_rows(students, week):
    rows = []
    for roll, name, section, batch, scores in students:
        score = scores[week - 1]
        plag = PLAG_MAP.get(roll, random.uniform(0.0, 8.0))
        # Priority students: short time spent (also triggers speed anomaly)
        is_priority = score < 6.0
        time_spent = f"{8.0 + score:.1f}m" if is_priority else f"{22.0 + score:.1f}m"
        rows.append({
            "Roll Number": roll,
            "Name": name,
            "Branch": "CSE",
            "Batch": batch,
            "Section": section,
            "Total Score": score,
            "Tab switches": 4 if is_priority else random.randint(0, 2),
            "Time Spent": time_spent,
            "Submission Date": f"2026-09-{10 + week}T10:30:00",
            "IP Address": "192.168.1.10",
            "Plagiarism %": round(plag, 1),
            "Plagiarism %3": round(max(0, plag - 2.0), 1),
            "Plagiarism %5": round(max(0, plag - 4.0), 1),
        })
    return rows


def run_seed(force: bool = False):
    import sys
    if "--force" in sys.argv or "-f" in sys.argv:
        force = True

    from adapters.postgres.models import Base
    from adapters.postgres.repository import engine

    if force:
        print("[seed_demo] Force mode active: dropping and recreating tables...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    else:
        init_db()

    data_dir = Path("./data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Check if already seeded (idempotent guard)
    if not force:
        db = SessionLocal()
        try:
            from adapters.postgres.models import Student
            existing = db.query(Student).filter(Student.roll_number == "2023CSE001").first()
            if existing:
                from adapters.postgres.models import WeeklyMetric
                wm_count = db.query(WeeklyMetric).filter(
                    WeeklyMetric.student_id == existing.id
                ).count()
                if wm_count >= 4:
                    print(f"[seed_demo] Already seeded (Aarav has {wm_count} weekly metrics). Use --force to re-seed.")
                    return
        finally:
            db.close()

    db = SessionLocal()
    try:
        for week in range(1, 5):
            rows = build_week_rows(STUDENTS, week)
            fname = f"demo_seed_week_{week}.xlsx"
            fpath = data_dir / fname
            pd.DataFrame(rows).to_excel(fpath, index=False)
            print(f"[seed_demo] Ingesting Week {week} ({len(rows)} students)...")
            execute_pipeline(fpath, db, week_number=week)

        print("[seed_demo] ✅ Seed complete!")

        # Report distribution
        from adapters.postgres.models import Student, WeeklyMetric
        from collections import Counter
        total = db.query(Student).count()
        metrics = db.query(WeeklyMetric).filter(WeeklyMetric.week_number == 4).all()
        tier_dist = Counter(m.tier for m in metrics)
        print(f"[seed_demo] Total students in DB: {total}")
        print(f"[seed_demo] Tier distribution (Week 4): {dict(tier_dist)}")

    finally:
        db.close()

    # Export CSV for UI demo upload
    csv_dir = Path("./data")
    csv_dir.mkdir(exist_ok=True)
    all_rows = build_week_rows(STUDENTS, 4)
    pd.DataFrame(all_rows).to_csv(csv_dir / "sample_students.csv", index=False)
    print(f"[seed_demo] Sample CSV exported to data/sample_students.csv")

    # Seed demo interventions for closed-loop triage demonstration
    try:
        from scripts.seed_demo_interventions import seed_demo_interventions
        seed_demo_interventions()
    except Exception as e:
        print(f"[seed_demo] Warning: could not seed interventions: {e}")


if __name__ == "__main__":
    run_seed()
