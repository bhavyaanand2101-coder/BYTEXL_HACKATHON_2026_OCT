"""
Sample dataset generator and multi-week seeder for CampusPulse demo.
Populates realistic student records covering Section C, Section D across Weeks 1 to 4.
"""

from pathlib import Path
import pandas as pd
from adapters.postgres.repository import init_db, SessionLocal
from services.pipeline import execute_pipeline


def generate_and_seed_data():
    init_db()
    data_dir = Path("./data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)

    # 1. Base Section C student roster
    # Aarav Sharma: High score on test (24.5), High CGPA (9.1), Great Attendance (92%),
    # but low placement coding submission history -> Academic Stars with Placement Gap
    students_c = [
        {"Roll Number": "2023CSE001", "Name": "Aarav Sharma", "Branch": "CSE", "Batch": "CSE 2029", "Plag": 4.0},
        {"Roll Number": "2023CSE002", "Name": "Bhavya Gupta", "Branch": "CSE", "Batch": "CSE_2029", "Plag": 10.0},
        {"Roll Number": "2023CSE003", "Name": "Chirag Patel", "Branch": "Section C", "Batch": "CSE-2029", "Plag": 1.0},
        {"Roll Number": "2023CSE004", "Name": "Diya Nair", "Branch": "CSE", "Batch": "cse  2029", "Plag": 92.0},
        {"Roll Number": "2023CSE005", "Name": "Dahiya Krish", "Branch": "Section C", "Batch": "CSE 2029", "Plag": 8.0},
        {"Roll Number": "2023CSE006", "Name": "Kavya Menon", "Branch": "CSE", "Batch": "CSE 2029", "Plag": 2.0},
        {"Roll Number": "2023CSE007", "Name": "Nikhil Varma", "Branch": "CSE", "Batch": "CSE 2029", "Plag": 0.0},
    ]

    # 2. Base Section D student roster
    students_d = [
        {"Roll Number": "2023CSE051", "Name": "Eshan Verma", "Branch": "Section D", "Batch": "CSE 2029", "Plag": 2.0},
        {"Roll Number": "2023CSE052", "Name": "Fatima Sheikh", "Branch": "Section D", "Batch": "CSE 2029", "Plag": 12.0},
        {"Roll Number": "2023CSE053", "Name": "Gaurav Sen", "Branch": "Section D", "Batch": "CSE 2029", "Plag": 0.0},
        {"Roll Number": "2023CSE054", "Name": "Hitesh Rao", "Branch": "Section D", "Batch": "CSE 2029", "Plag": 6.0},
        {"Roll Number": "2023CSE055", "Name": "Pooja Reddy", "Branch": "Section D", "Batch": "CSE 2029", "Plag": 5.0},
        {"Roll Number": "2023CSE056", "Name": "Rohan Mehra", "Branch": "Section D", "Batch": "CSE 2029", "Plag": 3.0},
    ]

    db = SessionLocal()
    try:
        # Seed Weeks 1 to 4
        for week in range(1, 5):
            sec_c_rows = []
            for s in students_c:
                score_mod = (week - 1) * 0.8
                time_val = f"{28.0 + week * 0.5:.1f}m" if s["Roll Number"] != "2023CSE004" else "12.0m"
                sec_c_rows.append({
                    "Roll Number": s["Roll Number"],
                    "Name": s["Name"],
                    "Branch": s["Branch"],
                    "Batch": s["Batch"],
                    "Total Score": min(25.0, (21.5 if s["Roll Number"] == "2023CSE001" else 15.0) + score_mod),
                    "Tab switches": 1 if s["Roll Number"] != "2023CSE004" else 4,
                    "Time Spent": time_val,
                    "Submission Date": f"2026-09-{10 + week}T10:30:00",
                    "IP Address": "192.168.1.10" if s["Roll Number"] != "2023CSE004" else "192.168.1.14, 10.0.0.5",
                    "Plagiarism %": s["Plag"],
                    "Plagiarism %3": max(0.0, s["Plag"] - 1.0),
                    "Plagiarism %5": max(0.0, s["Plag"] - 2.0),
                })

            sec_d_rows = []
            for s in students_d:
                score_mod = (week - 1) * 0.5
                sec_d_rows.append({
                    "Roll Number": s["Roll Number"],
                    "Name": s["Name"],
                    "Branch": s["Branch"],
                    "Batch": s["Batch"],
                    "Total Score": min(25.0, (18.0 if s["Roll Number"] == "2023CSE051" else 10.0) + score_mod),
                    "Tab switches": 0,
                    "Time Spent": f"{25.0 + week * 0.8:.1f}m",
                    "Submission Date": f"2026-09-{11 + week}T11:00:00",
                    "IP Address": "192.168.2.20",
                    "Plagiarism %": s["Plag"],
                    "Plagiarism %3": max(0.0, s["Plag"] - 1.0),
                    "Plagiarism %5": max(0.0, s["Plag"] - 2.0),
                })

            file_c = data_dir / f"Section_C_Week_{week}.xlsx"
            file_d = data_dir / f"Section_D_Week_{week}.xlsx"

            pd.DataFrame(sec_c_rows).to_excel(file_c, index=False)
            pd.DataFrame(sec_d_rows).to_excel(file_d, index=False)

            print(f"Ingesting Week {week} Section C...")
            execute_pipeline(file_c, db, week_number=week)

            print(f"Ingesting Week {week} Section D...")
            execute_pipeline(file_d, db, week_number=week)

        print("Multi-week database seeding complete across Weeks 1 to 4!")
    finally:
        db.close()


if __name__ == "__main__":
    generate_and_seed_data()
