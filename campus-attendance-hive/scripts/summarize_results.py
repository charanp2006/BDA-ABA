#!/usr/bin/env python3
"""Summarize the actual Hive result CSVs into results/key_findings.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def read(name: str) -> pd.DataFrame:
    frame = pd.read_csv(RESULTS / f"{name}.csv")
    frame.columns = [column.strip() for column in frame.columns]
    return frame


def table(frame: pd.DataFrame, columns: list[str], limit: int | None = None, floatfmt: str = "{:.2f}") -> list[str]:
    view = frame[columns].head(limit) if limit else frame[columns]
    header = "| " + " | ".join(columns) + " |"
    separator = "|" + "|".join(["---"] * len(columns)) + "|"
    lines = [header, separator]
    for _, row in view.iterrows():
        cells = []
        for column in columns:
            value = row[column]
            if isinstance(value, float):
                cells.append(floatfmt.format(value))
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def main() -> None:
    overall = read("overall").iloc[0]
    subject = read("subject_wise")
    student = read("student_wise")
    low = read("low_attendance")
    department = read("department_wise")
    section = read("section_wise")
    daily = read("daily_trend")
    weekly = read("weekly_trend")

    dept_section = (
        section.groupby("section", as_index=False)
        .agg(total_records=("total_records", "sum"), present_count=("present_count", "sum"))
    )
    dept_section["attendance_pct"] = 100.0 * dept_section["present_count"] / dept_section["total_records"]

    low_by_dept = low.groupby("department").agg(groups=("student_id", "size"), students=("student_id", "nunique"))
    low_by_dept = low_by_dept.sort_values("groups", ascending=False).reset_index()

    lines = [
        "# Key Findings (generated from actual Hive result files)",
        "",
        f"Source: `results/*.csv` produced by HiveQL on {int(overall['total_records']):,} records.",
        "",
        "## Overall",
        "",
        f"- Total records analysed: **{int(overall['total_records']):,}**",
        f"- Present records: **{int(overall['present_records']):,}**",
        f"- Overall attendance: **{float(overall['attendance_pct']):.2f}%**",
        "",
        "## Top 5 subjects by attendance",
        "",
        *table(subject.sort_values("attendance_pct", ascending=False), ["subject_code", "subject_name", "total_classes", "present_count", "attendance_pct"], 5),
        "",
        "## Bottom 5 subjects by attendance",
        "",
        *table(subject.sort_values("attendance_pct", ascending=True), ["subject_code", "subject_name", "total_classes", "present_count", "attendance_pct"], 5),
        "",
        "## Department-wise attendance",
        "",
        *table(department.sort_values("attendance_pct", ascending=False), ["department", "total_records", "present_count", "attendance_pct"]),
        "",
        "## Section-wise attendance (all departments combined)",
        "",
        *table(dept_section.sort_values("attendance_pct", ascending=False), ["section", "total_records", "present_count", "attendance_pct"]),
        "",
        "## Student-wise attendance",
        "",
        f"- Students analysed: **{len(student):,}**",
        f"- Mean student attendance: **{student['attendance_pct'].mean():.2f}%**",
        f"- Median student attendance: **{student['attendance_pct'].median():.2f}%**",
        f"- Lowest student attendance: **{student['attendance_pct'].min():.2f}%**",
        f"- Highest student attendance: **{student['attendance_pct'].max():.2f}%**",
        f"- Students below 75%: **{int((student['attendance_pct'] < 75).sum()):,}**",
        "",
        "## Low-attendance student-subject groups (<75%)",
        "",
        f"- Groups identified: **{len(low):,}**",
        f"- Distinct students affected: **{low['student_id'].nunique():,}**",
        f"- Distinct subject offerings affected: **{low[['subject_code', 'subject_name']].drop_duplicates().shape[0]:,}**",
        f"- Mean attendance in low groups: **{low['attendance_pct'].mean():.2f}%**",
        "",
        *table(low_by_dept, ["department", "groups", "students"]),
        "",
        "### 10 lowest groups",
        "",
        *table(
            low.sort_values("attendance_pct"),
            ["student_id", "department", "semester", "section", "subject_code", "attendance_pct"],
            10,
        ),
        "",
        "## Trend",
        "",
        f"- Class dates covered: **{len(daily):,}**",
        f"- Highest day: **{daily.loc[daily['attendance_pct'].idxmax(), 'attendance_date']}** at **{daily['attendance_pct'].max():.2f}%**",
        f"- Lowest day: **{daily.loc[daily['attendance_pct'].idxmin(), 'attendance_date']}** at **{daily['attendance_pct'].min():.2f}%**",
        f"- ISO weeks covered: **{len(weekly):,}**",
        f"- Highest week: **{weekly.loc[weekly['attendance_pct'].idxmax(), 'week_label']}** at **{weekly['attendance_pct'].max():.2f}%**",
        f"- Lowest week: **{weekly.loc[weekly['attendance_pct'].idxmin(), 'week_label']}** at **{weekly['attendance_pct'].min():.2f}%**",
        "",
        "### Weekly series",
        "",
        *table(weekly, ["week_label", "total_records", "present_count", "attendance_pct"]),
        "",
    ]

    output = RESULTS / "key_findings.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
