#!/usr/bin/env python3
"""Generate a reproducible synthetic campus attendance dataset.

The data is entirely synthetic and anonymized. It contains no real student
information. Generation is deterministic for a fixed seed.

Output: data/attendance.csv
Schema: student_id,department,semester,section,subject_code,subject_name,
        attendance_date,period_number,status
"""

from __future__ import annotations

import csv
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

SEED = 42
STUDENTS_PER_SECTION = 12
SESSIONS_PER_SUBJECT_SECTION = 8
SEMESTER_START = date(2025, 9, 1)
SEMESTER_END = date(2025, 11, 28)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "attendance.csv"

SUBJECTS = {
    "CSE": {
        3: [("CS301", "Data Structures"), ("CS302", "Digital Logic"), ("CS303", "OOP with Java"), ("CS304", "Discrete Mathematics")],
        4: [("CS401", "Database Management Systems"), ("CS402", "Operating Systems"), ("CS403", "Computer Networks"), ("CS404", "Design and Analysis of Algorithms")],
        5: [("CS501", "Software Engineering"), ("CS502", "Web Technologies"), ("CS503", "Machine Learning"), ("CS504", "Computer Graphics")],
        6: [("CS601", "Compiler Design"), ("CS602", "Cloud Computing"), ("CS603", "Big Data Analytics"), ("CS604", "Cryptography")],
    },
    "ISE": {
        3: [("IS301", "Data Structures"), ("IS302", "Computer Organization"), ("IS303", "Java Programming"), ("IS304", "Probability and Statistics")],
        4: [("IS401", "Database Management Systems"), ("IS402", "Operating Systems"), ("IS403", "Computer Networks"), ("IS404", "Operations Research")],
        5: [("IS501", "Software Engineering"), ("IS502", "Data Mining"), ("IS503", "Big Data Analytics"), ("IS504", "Information Security")],
        6: [("IS601", "Compiler Design"), ("IS602", "Cloud Computing"), ("IS603", "Internet of Things"), ("IS604", "Data Visualization")],
    },
    "ECE": {
        3: [("EC301", "Signals and Systems"), ("EC302", "Digital Electronics"), ("EC303", "Network Theory"), ("EC304", "Electronic Devices")],
        4: [("EC401", "Analog Circuits"), ("EC402", "Communication Systems"), ("EC403", "Microcontrollers"), ("EC404", "Control Systems")],
        5: [("EC501", "Digital Signal Processing"), ("EC502", "VLSI Design"), ("EC503", "Embedded Systems"), ("EC504", "Antenna Theory")],
        6: [("EC601", "Wireless Communication"), ("EC602", "Optical Communication"), ("EC603", "Satellite Communication"), ("EC604", "Robotics")],
    },
    "EEE": {
        3: [("EE301", "Electrical Machines"), ("EE302", "Power Systems"), ("EE303", "Control Systems"), ("EE304", "Circuit Theory")],
        4: [("EE401", "Power Electronics"), ("EE402", "Electrical Measurements"), ("EE403", "Electric Drives"), ("EE404", "Transmission Lines")],
        5: [("EE501", "Renewable Energy Systems"), ("EE502", "Smart Grid"), ("EE503", "High Voltage Engineering"), ("EE504", "Power System Protection")],
        6: [("EE601", "HVDC Transmission"), ("EE602", "FACTS Devices"), ("EE603", "Energy Management"), ("EE604", "Electric Vehicles")],
    },
    "ME": {
        3: [("ME301", "Thermodynamics"), ("ME302", "Fluid Mechanics"), ("ME303", "Strength of Materials"), ("ME304", "Manufacturing Processes")],
        4: [("ME401", "Heat Transfer"), ("ME402", "Machine Design"), ("ME403", "IC Engines"), ("ME404", "Metrology")],
        5: [("ME501", "Refrigeration and Air Conditioning"), ("ME502", "Automobile Engineering"), ("ME503", "CAD/CAM"), ("ME504", "Industrial Engineering")],
        6: [("ME601", "Robotics"), ("ME602", "Mechatronics"), ("ME603", "Finite Element Analysis"), ("ME604", "Additive Manufacturing")],
    },
}

# Short code used in the synthetic student ID (e.g. 4VV23CS001).
DEPT_ID_CODE = {"CSE": "CS", "ISE": "IS", "ECE": "EC", "EEE": "EE", "ME": "ME"}
SEMESTERS = [3, 4, 5, 6]
SECTIONS = ["A", "B"]
DAY_OF_WEEK_FACTOR = {0: 0.92, 1: 1.00, 2: 1.03, 3: 1.00, 4: 0.90}


def weekday_dates(start: date, end: date) -> list[date]:
    days: list[date] = []
    current = start
    while current <= end:
        if current.weekday() < 5:
            days.append(current)
        current += timedelta(days=1)
    return days


def pick_spread_dates(dates: list[date], rng: random.Random, count: int) -> list[date]:
    """Pick one weekday from each of ``count`` equal blocks of the semester."""
    block_size = len(dates) / count
    picked: list[date] = []
    for block in range(count):
        lo = int(block * block_size)
        hi = int((block + 1) * block_size)
        hi = max(hi, lo + 1)
        candidate = dates[rng.randrange(lo, min(hi, len(dates)))]
        while candidate in picked:
            candidate = dates[rng.randrange(lo, min(hi, len(dates)))]
        picked.append(candidate)
    return picked


def build_students(rng: random.Random) -> dict[tuple[str, int, str], list[dict]]:
    groups: dict[tuple[str, int, str], list[dict]] = {}
    for dept, code in DEPT_ID_CODE.items():
        for semester in SEMESTERS:
            for section in SECTIONS:
                students = []
                for index in range(1, STUDENTS_PER_SECTION + 1):
                    number = ((semester - 3) * 2 * STUDENTS_PER_SECTION) + ((0 if section == "A" else STUDENTS_PER_SECTION) + index)
                    student_id = f"4VV23{code}{number:03d}"
                    baseline = min(0.98, max(0.40, rng.gauss(0.84, 0.10)))
                    students.append({"student_id": student_id, "baseline": baseline})
                groups[(dept, semester, section)] = students
    return groups


def date_factor(day: date) -> float:
    week_index = (day - SEMESTER_START).days // 7
    trend = max(0.86, 1.0 - 0.012 * week_index)
    if date(2025, 10, 13) <= day <= date(2025, 10, 17):
        trend *= 0.85
    return trend * DAY_OF_WEEK_FACTOR[day.weekday()]


def generate() -> list[dict]:
    rng = random.Random(SEED)
    dates = weekday_dates(SEMESTER_START, SEMESTER_END)
    students = build_students(rng)
    records: list[dict] = []

    for dept in SUBJECTS:
        for semester in SEMESTERS:
            for section in SECTIONS:
                cohort = students[(dept, semester, section)]
                for subject_code, subject_name in SUBJECTS[dept][semester]:
                    subject_factor = min(1.08, max(0.90, rng.gauss(1.0, 0.04)))
                    session_dates = pick_spread_dates(dates, rng, SESSIONS_PER_SUBJECT_SECTION)
                    for class_date in session_dates:
                        period = rng.randint(1, 8)
                        factor = date_factor(class_date)
                        for student in cohort:
                            probability = student["baseline"] * subject_factor * factor
                            probability = min(0.99, max(0.05, probability))
                            status = "PRESENT" if rng.random() < probability else "ABSENT"
                            records.append(
                                {
                                    "student_id": student["student_id"],
                                    "department": dept,
                                    "semester": semester,
                                    "section": section,
                                    "subject_code": subject_code,
                                    "subject_name": subject_name,
                                    "attendance_date": class_date.isoformat(),
                                    "period_number": period,
                                    "status": status,
                                }
                            )

    records.sort(
        key=lambda r: (
            r["attendance_date"],
            r["period_number"],
            r["department"],
            r["semester"],
            r["section"],
            r["subject_code"],
            r["student_id"],
        )
    )
    return records


def main() -> None:
    records = generate()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "student_id",
        "department",
        "semester",
        "section",
        "subject_code",
        "subject_name",
        "attendance_date",
        "period_number",
        "status",
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    by_students = defaultdict(int)
    for record in records:
        by_students[record["student_id"]] += 1
    present = sum(1 for record in records if record["status"] == "PRESENT")
    print(f"Wrote {len(records):,} records to {OUTPUT}")
    print(f"Students: {len(by_students):,}")
    print(f"Attendance: {present:,}/{len(records):,} = {100.0 * present / len(records):.2f}%")


if __name__ == "__main__":
    main()
