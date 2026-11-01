#!/usr/bin/env python3
"""Validate the synthetic attendance dataset before it enters HDFS/Hive.

Checks the schema, row count, value domains, missing data, duplicates and
basic distribution properties. Writes a report to results/validation_report.txt
and exits non-zero if any check fails.
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "attendance.csv"
REPORT_PATH = ROOT / "results" / "validation_report.txt"

EXPECTED_HEADER = [
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
ALLOWED_STATUS = {"PRESENT", "ABSENT"}
DATE_MIN = date(2025, 9, 1)
DATE_MAX = date(2025, 12, 31)

checks: list[tuple[str, bool, str]] = []


def check(name: str, passed: bool, detail: str) -> None:
    checks.append((name, bool(passed), detail))


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def main() -> int:
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found. Run scripts/generate_dataset.py first.")
        return 2

    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
        rows = list(reader)

    check("CSV header matches expected schema", header == EXPECTED_HEADER, f"header={header}")
    check("Row count within 5,000-20,000 target", 5000 <= len(rows) <= 20000, f"rows={len(rows):,}")

    malformed = [i for i, row in enumerate(rows, start=2) if len(row) != len(EXPECTED_HEADER)]
    check("All rows have exactly 9 fields", not malformed, f"malformed_rows={len(malformed)}")

    records = [dict(zip(EXPECTED_HEADER, row)) for row in rows if len(row) == len(EXPECTED_HEADER)]

    missing = [
        (i, key)
        for i, record in enumerate(records, start=2)
        for key in EXPECTED_HEADER
        if str(record.get(key, "")).strip() == ""
    ]
    check("No missing values", not missing, f"missing_cells={len(missing)}")

    statuses = Counter(record.get("status", "") for record in records)
    invalid_status = {value: count for value, count in statuses.items() if value not in ALLOWED_STATUS}
    check("Status domain is PRESENT/ABSENT only", not invalid_status, f"invalid={invalid_status}")

    invalid_dates: list[str] = []
    out_of_range: list[str] = []
    for record in records:
        try:
            parsed = parse_date(record["attendance_date"])
            if not DATE_MIN <= parsed <= DATE_MAX:
                out_of_range.append(record["attendance_date"])
        except (ValueError, KeyError):
            invalid_dates.append(record.get("attendance_date", ""))
    check("All dates are valid YYYY-MM-DD", not invalid_dates, f"invalid_dates={len(invalid_dates)}")
    check("All dates inside 2025-09-01..2025-12-31", not out_of_range, f"out_of_range={len(out_of_range)}")

    invalid_semester = [r for r in records if not r["semester"].isdigit() or not 1 <= int(r["semester"]) <= 8]
    invalid_period = [r for r in records if not r["period_number"].isdigit() or not 1 <= int(r["period_number"]) <= 8]
    check("Semester values are integers in 1..8", not invalid_semester, f"invalid={len(invalid_semester)}")
    check("Period values are integers in 1..8", not invalid_period, f"invalid={len(invalid_period)}")

    keys = [
        (r["student_id"], r["subject_code"], r["attendance_date"], r["period_number"])
        for r in records
    ]
    duplicate_count = len(keys) - len(set(keys))
    check("No duplicate (student, subject, date, period) keys", duplicate_count == 0, f"duplicates={duplicate_count}")

    students = {r["student_id"] for r in records}
    subjects = {(r["department"], r["semester"], r["subject_code"]) for r in records}
    check("At least 100 unique students", len(students) >= 100, f"students={len(students):,}")
    check("At least 20 unique subject offerings", len(subjects) >= 20, f"subjects={len(subjects):,}")

    present = statuses.get("PRESENT", 0)
    percentage = 100.0 * present / len(records) if records else 0.0
    check("Overall attendance percentage between 60 and 95", 60.0 <= percentage <= 95.0, f"pct={percentage:.2f}%")

    # Attendance per student should stay in a plausible range for synthetic data.
    per_student = Counter()
    present_by_student = Counter()
    for record in records:
        per_student[record["student_id"]] += 1
        if record["status"] == "PRESENT":
            present_by_student[record["student_id"]] += 1
    student_pcts = [
        100.0 * present_by_student[sid] / total for sid, total in per_student.items()
    ]
    check(
        "Student attendance percentages within 0..100",
        all(0.0 <= value <= 100.0 for value in student_pcts),
        f"min={min(student_pcts):.2f}% max={max(student_pcts):.2f}%",
    )

    per_group = Counter()
    present_group = Counter()
    for record in records:
        group = (record["student_id"], record["subject_code"], record["subject_name"])
        per_group[group] += 1
        if record["status"] == "PRESENT":
            present_group[group] += 1
    low_groups = [
        group
        for group, total in per_group.items()
        if 100.0 * present_group[group] / total < 75.0
    ]
    check(
        "Dataset contains low-attendance student-subject groups (<75%)",
        len(low_groups) > 0,
        f"low_groups={len(low_groups):,}",
    )

    passed = all(item[1] for item in checks)
    lines = [
        "Campus Attendance Dataset Validation",
        "====================================",
        f"File: {CSV_PATH}",
        f"Rows: {len(records):,}",
        f"Unique students: {len(students):,}",
        f"Unique subject offerings: {len(subjects):,}",
        f"Status counts: PRESENT={statuses.get('PRESENT', 0):,}, ABSENT={statuses.get('ABSENT', 0):,}",
        f"Overall attendance: {percentage:.2f}%",
        f"Low-attendance student-subject groups (<75%): {len(low_groups):,}",
        "",
        "Checks:",
    ]
    for name, ok, detail in checks:
        lines.append(f"  [{'PASS' if ok else 'FAIL'}] {name} ({detail})")
    lines.append("")
    lines.append(f"RESULT: {'PASS' if passed else 'FAIL'}")
    report = "\n".join(lines) + "\n"

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(report)

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
