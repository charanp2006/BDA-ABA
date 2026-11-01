# Copilot / AI Agent Prompt

I will attach:
1. `Campus_Attendance_Hive_Implementation_Guide.md` — authoritative implementation guide.
2. `BDA_Campus_Attendance_Sample_Report.pdf` — report structure/style reference.
3. `BDA_Campus_Attendance_Analytics_Final_Presentation.pptx` — PPT reference.

Build a COMPLETE, WORKING, DEMONSTRABLE project named **Campus Attendance Trend Analytics Using Apache Hive on the Hadoop Ecosystem**.

Team:
- Bharath Krishna K K — 4VV23CS033
- Charan P — 4VV23CS042
- Abu Safwan — 4VV23CS006

## Non-negotiable rules
- Read the implementation guide first.
- Follow the sample report's organization and academic level.
- Keep HDFS + Apache Hive/HiveQL central.
- Do not replace Hive with pandas or ordinary SQL.
- Python may be used for synthetic data generation, validation, export and charts.
- Never fabricate results, screenshots, record counts, percentages or execution claims.
- Use synthetic/anonymized attendance data; never introduce real student PII.
- Detect the environment before making version-specific assumptions.
- If Hadoop/Hive cannot run in the current environment, build everything possible and document the exact remaining manual steps.

## Phase 1 — inspect
Check OS/shell, Java, Hadoop, HDFS, Hive/Beeline, Python and workspace. Create `ENVIRONMENT.md`.

## Phase 2 — create
Create:
```text
campus-attendance-hive/
├── data/attendance.csv
├── hive/create_table.sql
├── hive/analytics.sql
├── scripts/generate_dataset.py
├── scripts/validate_dataset.py
├── scripts/make_charts.py
├── results/
├── charts/
├── screenshots/
├── docs/
├── README.md
├── RUNBOOK.md
└── run.sh
```

## Phase 3 — data
Generate 5,000–20,000 reproducible synthetic records with:
`student_id, department, semester, section, subject_code, subject_name, attendance_date, period_number, status`

Validate schema, dates, status values and missing data.

## Phase 4 — HDFS
Create `/bda/attendance`, upload the CSV, verify it and show sample rows.

## Phase 5 — Hive
Create database `campus_attendance` and external table `attendance` using the guide's schema. Handle CSV headers correctly for the installed Hive version. Verify with SHOW TABLES, DESCRIBE, LIMIT and COUNT.

## Phase 6 — analytics
Actually execute:
1. overall attendance;
2. subject-wise attendance;
3. student-wise attendance;
4. low-attendance student-subject groups below 75%;
5. department-wise attendance;
6. section-wise attendance;
7. daily/weekly trend.

Save real outputs in `results/`.

## Phase 7 — charts
Create charts only from actual Hive results:
- subject attendance;
- department/section comparison;
- daily/weekly trend;
- optional low-attendance distribution.

## Phase 8 — validation
Cross-check selected results independently with Python. Document row counts, percentage range, invalid statuses and consistency.

## Phase 9 — documentation
Create README and RUNBOOK with exact setup, commands, outputs, troubleshooting and demo sequence.

## Phase 10 — evidence
Capture real screenshots if possible. Otherwise create a `SCREENSHOT_CHECKLIST.md` with exact captures required.

## Phase 11 — report support
Create `docs/REPORT_EVIDENCE.md` mapping the actual implementation to these report sections:
1 Introduction
2 Problem Statement
3 Significance
4 Objectives
5 Scope
6 Existing System
7 Proposed System
8 Hadoop Ecosystem and Tool Selection
9 Requirements
10 Dataset
11 Architecture
12 Methodology
13 Implementation
14 Hive Analytics/Data Flow
15 Demonstration
16 Results and Analysis
17 Advantages
18 Limitations
19 Future Enhancements
20 Conclusion
21 References

## Final verification
Run the documented workflow from a clean state as far as the environment permits.

Final response must list:
- project tree;
- exact run commands;
- actual dataset size;
- actual Hive result summary;
- files created;
- screenshots/evidence;
- environment limitations;
- remaining manual steps.

Academic integrity is more important than appearance. Never invent execution evidence.
