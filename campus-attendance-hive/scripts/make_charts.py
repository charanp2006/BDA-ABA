#!/usr/bin/env python3
"""Create report charts strictly from the CSV files produced by Hive.

Inputs (written by run.sh after actual HiveQL execution):
  results/subject_wise.csv
  results/department_wise.csv
  results/section_wise.csv
  results/daily_trend.csv
  results/weekly_trend.csv
  results/low_attendance.csv
  results/student_wise.csv

Outputs: charts/*.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CHARTS = ROOT / "charts"

THRESHOLD = 75.0
COLOR_OK = "#2A9D8F"
COLOR_LOW = "#E76F51"
PALETTE = ["#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51"]


def read_result(name: str) -> pd.DataFrame:
    path = RESULTS / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run the Hive analytics step before creating charts."
        )
    frame = pd.read_csv(path)
    frame.columns = [column.strip() for column in frame.columns]
    return frame


def save(fig: plt.Figure, filename: str) -> None:
    path = CHARTS / filename
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {path.relative_to(ROOT)}")


def subject_chart() -> None:
    frame = read_result("subject_wise").sort_values("attendance_pct")
    colors = [COLOR_LOW if value < THRESHOLD else COLOR_OK for value in frame["attendance_pct"]]
    labels = frame["subject_code"] + " " + frame["subject_name"]
    fig, ax = plt.subplots(figsize=(12, max(9, 0.24 * len(frame))))
    ax.barh(labels, frame["attendance_pct"], color=colors)
    ax.axvline(THRESHOLD, color="#333333", linestyle="--", linewidth=1, label="75% threshold")
    ax.set_xlim(0, 100)
    ax.set_xlabel("Attendance percentage (%)")
    ax.set_title("Subject-wise attendance percentage (HiveQL output)")
    ax.legend(loc="lower right")
    ax.tick_params(axis="y", labelsize=7)
    ax.grid(axis="x", alpha=0.25)
    save(fig, "subject_attendance.png")


def department_chart() -> None:
    frame = read_result("department_wise").sort_values("attendance_pct", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(frame["department"], frame["attendance_pct"], color=PALETTE)
    ax.axhline(THRESHOLD, color="#333333", linestyle="--", linewidth=1, label="75% threshold")
    for bar, value in zip(bars, frame["attendance_pct"]):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.8, f"{value:.2f}%",
                ha="center", va="bottom", fontsize=9)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Attendance percentage (%)")
    ax.set_title("Department-wise attendance (HiveQL output)")
    ax.legend(loc="lower right")
    ax.grid(axis="y", alpha=0.25)
    save(fig, "department_attendance.png")


def section_chart() -> None:
    frame = read_result("section_wise")
    grouped = (
        frame.groupby(["department", "section"], as_index=False)
        .agg(total_records=("total_records", "sum"), present_count=("present_count", "sum"))
    )
    grouped["attendance_pct"] = 100.0 * grouped["present_count"] / grouped["total_records"]
    pivot = grouped.pivot(index="department", columns="section", values="attendance_pct")
    pivot = pivot.reindex(sorted(pivot.index))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    pivot.plot(kind="bar", ax=ax, color=[PALETTE[0], PALETTE[3]], width=0.75)
    ax.axhline(THRESHOLD, color="#333333", linestyle="--", linewidth=1, label="75% threshold")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Attendance percentage (%)")
    ax.set_xlabel("Department")
    ax.set_title("Section-wise attendance comparison by department (HiveQL output)")
    ax.legend(title="Section", loc="lower right")
    ax.grid(axis="y", alpha=0.25)
    plt.setp(ax.get_xticklabels(), rotation=0)
    save(fig, "section_comparison.png")


def daily_chart() -> None:
    frame = read_result("daily_trend").copy()
    frame["attendance_date"] = pd.to_datetime(frame["attendance_date"])
    frame = frame.sort_values("attendance_date")
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.plot(frame["attendance_date"], frame["attendance_pct"], color=PALETTE[0], linewidth=1.4,
            marker="o", markersize=3)
    ax.axhline(THRESHOLD, color=COLOR_LOW, linestyle="--", linewidth=1, label="75% threshold")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Attendance percentage (%)")
    ax.set_title("Daily attendance trend (HiveQL output)")
    ax.legend(loc="lower left")
    ax.grid(alpha=0.25)
    fig.autofmt_xdate()
    save(fig, "daily_trend.png")


def weekly_chart() -> None:
    frame = read_result("weekly_trend").copy()
    frame = frame.sort_values("week_label")
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(frame["week_label"], frame["attendance_pct"], color=PALETTE[1], linewidth=2,
            marker="o", markersize=6)
    ax.axhline(THRESHOLD, color=COLOR_LOW, linestyle="--", linewidth=1, label="75% threshold")
    for x, value in zip(frame["week_label"], frame["attendance_pct"]):
        ax.annotate(f"{value:.1f}", (x, value), textcoords="offset points", xytext=(0, 7),
                    ha="center", fontsize=8)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Attendance percentage (%)")
    ax.set_xlabel("ISO week")
    ax.set_title("Weekly attendance trend (HiveQL output)")
    ax.legend(loc="lower left")
    ax.grid(alpha=0.25)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    save(fig, "weekly_trend.png")


def low_attendance_chart() -> None:
    frame = read_result("low_attendance")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))
    ax1.hist(frame["attendance_pct"], bins=15, color=COLOR_LOW, edgecolor="white")
    ax1.set_xlabel("Attendance percentage (%)")
    ax1.set_ylabel("Number of student-subject groups")
    ax1.set_title("Distribution of groups below 75%")
    ax1.grid(alpha=0.25)

    counts = frame.groupby("department").size().sort_values(ascending=False)
    ax2.bar(counts.index, counts.values, color=PALETTE)
    ax2.set_xlabel("Department")
    ax2.set_ylabel("Low-attendance groups")
    ax2.set_title("Low-attendance groups by department")
    ax2.grid(axis="y", alpha=0.25)
    fig.suptitle("Low-attendance analysis (HiveQL output)")
    save(fig, "low_attendance_distribution.png")


def student_chart() -> None:
    frame = read_result("student_wise")
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.hist(frame["attendance_pct"], bins=20, color=PALETTE[0], edgecolor="white")
    ax.axvline(THRESHOLD, color=COLOR_LOW, linestyle="--", linewidth=1.5, label="75% threshold")
    ax.set_xlabel("Attendance percentage (%)")
    ax.set_ylabel("Number of students")
    ax.set_title("Distribution of student-wise attendance (HiveQL output)")
    ax.legend()
    ax.grid(alpha=0.25)
    save(fig, "student_attendance_distribution.png")


def main() -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    print("Creating charts from Hive result CSVs...")
    subject_chart()
    department_chart()
    section_chart()
    daily_chart()
    weekly_chart()
    low_attendance_chart()
    student_chart()
    print("Done.")


if __name__ == "__main__":
    main()
