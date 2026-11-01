#!/usr/bin/env python3
"""Independently recompute the analytics in Python and compare with Hive output.

This script never replaces Hive. It reads the same CSV and recalculates the
metrics with the standard library, then verifies that the CSV files produced by
HiveQL agree. It exists to satisfy the independent validation requirement.

Usage: python scripts/crosscheck_results.py [--require-hive]
"""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "attendance.csv"
RESULTS = ROOT / "results"
REPORT = RESULTS / "crosscheck_report.txt"
TOLERANCE = 0.011

REQUIRED_RESULTS = [
    "overall",
    "subject_wise",
    "student_wise",
    "low_attendance",
    "department_wise",
    "section_wise",
    "daily_trend",
    "weekly_trend",
]


def load_hive_csv(name: str) -> list[dict] | None:
    path = RESULTS / f"{name}.csv"
    if not path.exists():
        return None
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.reader(handle) if any(cell.strip() for cell in row)]
    if not rows:
        return []
    header = [cell.strip().strip('"') for cell in rows[0]]
    parsed = []
    for row in rows[1:]:
        values = [cell.strip().strip('"') for cell in row]
        if len(values) != len(header):
            continue
        parsed.append(dict(zip(header, values)))
    return parsed


def independent_metrics(records: list[dict]) -> dict:
    total = len(records)
    present = sum(1 for r in records if r["status"] == "PRESENT")

    def aggregate(key_fields: list[str]) -> dict[tuple, dict]:
        counts: dict[tuple, int] = defaultdict(int)
        presents: dict[tuple, int] = defaultdict(int)
        for record in records:
            key = tuple(record[field] for field in key_fields)
            counts[key] += 1
            if record["status"] == "PRESENT":
                presents[key] += 1
        result = {}
        for key, count in counts.items():
            result[key] = {
                "total": count,
                "present": presents[key],
                "pct": round(100.0 * presents[key] / count, 2),
            }
        return result

    subject = aggregate(["subject_code", "subject_name"])
    student = aggregate(["student_id"])
    department = aggregate(["department"])
    section = aggregate(["department", "semester", "section"])
    daily = aggregate(["attendance_date"])

    # Weekly label must match Hive: YEAR(date)-W<ISO week>.
    for record in records:
        parsed = datetime.strptime(record["attendance_date"], "%Y-%m-%d").date()
        iso = parsed.isocalendar()
        record["week_label"] = f"{iso.year}-W{iso.week:02d}"

    weekly = aggregate(["week_label"])
    low = aggregate(["student_id", "department", "semester", "section", "subject_code", "subject_name"])

    return {
        "overall": {
            "total": total,
            "present": present,
            "pct": round(100.0 * present / total, 2) if total else 0.0,
        },
        "subject": subject,
        "student": student,
        "department": department,
        "section": section,
        "daily": daily,
        "weekly": weekly,
        "low": {key: value for key, value in low.items() if value["pct"] < 75.0},
    }


def compare_counts(
    name: str,
    hive_rows: list[dict] | None,
    python_map: dict[tuple, dict],
    key_fields: list[str],
    result_lines: list[str],
) -> bool:
    if hive_rows is None:
        result_lines.append(f"[SKIP] {name}: results/{name}.csv not found")
        return False

    hive_map = {}
    for row in hive_rows:
        key = tuple(row[field] for field in key_fields)
        hive_map[key] = row

    missing = set(python_map) - set(hive_map)
    extra = set(hive_map) - set(python_map)
    max_diff = 0.0
    count_mismatch = 0
    for key in set(python_map) & set(hive_map):
        py = python_map[key]
        hv = hive_map[key]
        try:
            hv_total = int(hv["total_classes"] if "total_classes" in hv else hv["total_records"])
            hv_present = int(hv["present_count"] if "present_count" in hv else hv["present_records"])
            hv_pct = float(hv["attendance_pct"])
        except (KeyError, ValueError):
            count_mismatch += 1
            continue
        if (hv_total, hv_present) != (py["total"], py["present"]):
            count_mismatch += 1
        max_diff = max(max_diff, abs(hv_pct - py["pct"]))

    ok = (
        not missing
        and not extra
        and count_mismatch == 0
        and max_diff <= TOLERANCE
        and len(hive_rows) == len(python_map)
    )
    result_lines.append(
        f"[{'PASS' if ok else 'FAIL'}] {name}: hive_rows={len(hive_rows)}, "
        f"python_groups={len(python_map)}, missing={len(missing)}, extra={len(extra)}, "
        f"count_mismatch={count_mismatch}, max_pct_diff={max_diff:.4f}"
    )
    return ok


def main() -> int:
    require = "--require-hive" in sys.argv[1:]
    if not DATA.exists():
        print(f"ERROR: {DATA} not found. Generate the dataset first.")
        return 2

    with DATA.open(newline="", encoding="utf-8") as handle:
        records = list(csv.DictReader(handle))

    metrics = independent_metrics(records)
    lines = [
        "Campus Attendance: Independent Hive Result Cross-Check",
        "======================================================",
        f"Dataset: {DATA}",
        f"Dataset rows: {len(records):,}",
        "",
        "Independent Python figures (recomputed from the same CSV):",
        f"  Overall: {metrics['overall']['present']:,}/{metrics['overall']['total']:,} = {metrics['overall']['pct']:.2f}%",
        f"  Subject offerings: {len(metrics['subject'])}",
        f"  Students: {len(metrics['student'])}",
        f"  Departments: {len(metrics['department'])}",
        f"  Department-semester-sections: {len(metrics['section'])}",
        f"  Class dates: {len(metrics['daily'])}",
        f"  ISO weeks: {len(metrics['weekly'])}",
        f"  Low-attendance student-subject groups (<75%): {len(metrics['low'])}",
        "",
        "Comparison with actual Hive output:",
    ]

    all_ok = True
    present = 0

    overall = load_hive_csv("overall")
    if overall is None:
        lines.append("[SKIP] overall: results/overall.csv not found")
        all_ok = False
    elif len(overall) != 1:
        lines.append(f"[FAIL] overall: expected 1 row, got {len(overall)}")
        all_ok = False
    else:
        row = overall[0]
        ok = (
            int(row["total_records"]) == metrics["overall"]["total"]
            and int(row["present_records"]) == metrics["overall"]["present"]
            and abs(float(row["attendance_pct"]) - metrics["overall"]["pct"]) <= TOLERANCE
        )
        lines.append(
            f"[{'PASS' if ok else 'FAIL'}] overall: hive={row['present_records']}/"
            f"{row['total_records']} ({row['attendance_pct']}%), "
            f"python={metrics['overall']['present']}/{metrics['overall']['total']} "
            f"({metrics['overall']['pct']}%)"
        )
        all_ok &= ok

    all_ok &= compare_counts("subject_wise", load_hive_csv("subject_wise"), metrics["subject"], ["subject_code", "subject_name"], lines)
    all_ok &= compare_counts("student_wise", load_hive_csv("student_wise"), metrics["student"], ["student_id"], lines)
    all_ok &= compare_counts("department_wise", load_hive_csv("department_wise"), metrics["department"], ["department"], lines)
    all_ok &= compare_counts("section_wise", load_hive_csv("section_wise"), metrics["section"], ["department", "semester", "section"], lines)
    all_ok &= compare_counts("daily_trend", load_hive_csv("daily_trend"), metrics["daily"], ["attendance_date"], lines)
    all_ok &= compare_counts("weekly_trend", load_hive_csv("weekly_trend"), metrics["weekly"], ["week_label"], lines)
    all_ok &= compare_counts(
        "low_attendance",
        load_hive_csv("low_attendance"),
        metrics["low"],
        ["student_id", "department", "semester", "section", "subject_code", "subject_name"],
        lines,
    )

    lines.append("")
    lines.append(f"RESULT: {'PASS' if all_ok else 'FAIL (or Hive result files missing)'}")
    report = "\n".join(lines) + "\n"
    RESULTS.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    print(report)

    if require and not all_ok:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
