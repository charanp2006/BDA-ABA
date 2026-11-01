# Report Evidence Map

This document maps the **actual implementation** to the 21 sections of the
supplied sample report. Use the real figures and file references below; do not
replace them with invented values.

Project: **Campus Attendance Trend Analytics Using Apache Hive on the Hadoop
Ecosystem**

| Name | USN |
|---|---|
| Bharath Krishna K K | 4VV23CS033 |
| Charan P | 4VV23CS042 |
| Abu Safwan | 4VV23CS006 |

Primary evidence:

| Evidence | File |
|---|---|
| Environment detection | `ENVIRONMENT.md` |
| Dataset | `data/attendance.csv` |
| Dataset validation | `results/validation_report.txt` |
| HDFS listing / sample | `results/hdfs_ls.txt`, `results/hdfs_sample_rows.txt` |
| Hive DDL | `hive/create_table.sql` |
| Hive verification | `results/table_verification.txt` |
| HiveQL | `hive/analytics.sql`, `hive/queries/*.sql` |
| Hive results | `results/*.csv` |
| Independent verification | `results/crosscheck_report.txt` |
| Generated findings | `results/key_findings.md` |
| Charts | `charts/*.png` |
| Real screenshots | `screenshots/01_*.png`, `screenshots/02_*.png` |

---

## 1. Introduction

Campus attendance is generated every day as a stream of
(student, subject, date, period, status) events. When these events remain in
registers or isolated spreadsheets, producing institution-level insight requires
manual effort and does not scale. This project stores attendance events in the
Hadoop Distributed File System and analyses them with Apache Hive, so that
aggregation is expressed declaratively in HiveQL and executed over a distributed
data store.

The implementation uses **15,360 synthetic attendance records** covering
**480 students**, **80 subject offerings**, five departments, semesters 3–6 and
sections A/B for the academic term 2025-09-01 to 2025-11-28. It executes eight
HiveQL analyses and verifies every result independently in Python.

Evidence: `README.md`, `ENVIRONMENT.md`, `results/key_findings.md`.

## 2. Problem Statement

Manual and spreadsheet-based attendance analysis has four concrete problems:

1. **Volume** — thousands of period-level records per term are slow to aggregate
   by hand.
2. **Repetition** — the same percentages must be recomputed for each subject,
   student, department and section.
3. **Inconsistency** — different formulas in different sheets produce different
   numbers for the same question.
4. **Late detection** — students below the 75% requirement are identified only
   after reports are prepared, not while intervention is still possible.

The project addresses these problems with one HDFS-resident dataset, one Hive
table and a fixed set of HiveQL queries whose outputs are saved and cross-checked.

## 3. Significance

- Moves attendance analysis from manual aggregation to a scalable HDFS + Hive
  pipeline.
- Produces repeatable department, section, subject and student comparisons from
  a single source of truth.
- Identifies low-attendance student-subject groups early: the executed query
  found **650 groups** involving **343 students**.
- Creates an auditable evidence chain: raw CSV → HDFS → Hive table → CSV results
  → independent Python verification → charts.
- Demonstrates a realistic BDA workflow using HiveQL rather than replacing Hive
  with pandas or ordinary SQL.

## 4. Objectives

| # | Objective | Actual evidence |
|---|---|---|
| 1 | Generate reproducible synthetic attendance data | `scripts/generate_dataset.py`, seed 42, 15,360 rows |
| 2 | Validate data quality before analysis | `results/validation_report.txt`, 15/15 PASS |
| 3 | Store the dataset in HDFS | `/bda/attendance/attendance.csv`, 999,647 bytes |
| 4 | Create a Hive external table | `campus_attendance.attendance`, 9 columns |
| 5 | Compute overall, subject, student, department and section attendance | 5 Hive result files |
| 6 | Detect student-subject groups below 75% | 650 rows in `results/low_attendance.csv` |
| 7 | Analyse daily and weekly trends | 65 daily rows, 13 weekly rows |
| 8 | Independently verify Hive output | 8/8 comparisons PASS |
| 9 | Produce charts from actual Hive results | 7 PNG files in `charts/` |

## 5. Scope

**Included**

- Synthetic attendance for five departments (CSE, ISE, ECE, EEE, ME).
- Semesters 3–6, sections A/B, 16 subject offerings per department.
- 65 class dates in one academic term, periods 1–8.
- Attendance status restricted to `PRESENT` and `ABSENT`.
- Batch analytics with HiveQL over HDFS.

**Excluded**

- Real student identity or any PII.
- Real-time streaming ingestion.
- Biometric/RFID capture hardware.
- Timetable optimisation, payroll or exam eligibility workflows.
- Multi-node fault-tolerance experiments and YARN scheduling studies.

## 6. Existing System

A typical existing system is a register or spreadsheet per class, with attendance
percentages calculated manually or by ad-hoc formulas at the end of a term.
Characteristics and limitations:

- Data is fragmented across files owned by different faculty members.
- Aggregation across departments or sections requires copying and re-keying.
- There is no single schema, so date formats and status values can differ.
- Historical trend analysis is rarely produced because it is labour-intensive.
- The 75% threshold is applied late and inconsistently.
- Scalability is limited by spreadsheet row limits and manual effort.

No claim is made about a specific institution's software; this is the general
baseline the proposed system replaces.

## 7. Proposed System

The proposed system is a batch analytics pipeline:

1. Python generates a deterministic synthetic dataset with a fixed schema.
2. The CSV is uploaded to HDFS under `/bda/attendance`.
3. Hive exposes the CSV through an EXTERNAL table, preserving HDFS as the system
   of record.
4. HiveQL computes all required aggregations.
5. Beeline writes each result set to `results/*.csv`.
6. An independent Python script recomputes the same metrics and compares them.
7. Python/matplotlib renders charts from the Hive result files only.

This keeps HDFS + Hive central and uses Python only for generation, validation,
export and visualisation, as required.

## 8. Hadoop Ecosystem and Tool Selection

| Layer | Tool | Version used | Reason |
|---|---|---|---|
| Distributed storage | HDFS | Hadoop 2.7.4 | Stores the CSV as a replicated HDFS file and is the table LOCATION |
| Table abstraction | Apache Hive | 2.3.2 | SQL-like HiveQL, schema-on-read, external tables |
| Execution | MapReduce (local mode) | Hadoop 2.7.4 | Executes Hive jobs inside the HiveServer2 container without YARN |
| Metastore | Hive Metastore + PostgreSQL | Hive 2.3.2 / PostgreSQL image | Persistent table metadata outside the Hive process |
| Interface | Beeline / HiveServer2 | 2.3.2 | JDBC access and CSV export |
| Runtime packaging | Docker / Docker Compose | 29.8.0 / v5.5.1 | Provides a real Hadoop/Hive stack on a Windows host without native install |
| Data generation | Python | 3.14.3 | Deterministic synthetic data, no PII |
| Validation / charts | pandas, numpy, matplotlib | 3.0.2 / 2.4.4 / 3.10.9 | Independent checks and report figures |

Hive was not replaced with pandas or ordinary SQL: pandas only re-checks the
Hive output and draws charts.

## 9. Requirements

### Functional

- Generate 5,000–20,000 synthetic records with the required nine columns.
- Validate schema, dates, status values, missing data and duplicates.
- Upload the dataset to HDFS and verify it.
- Create the Hive database and external table.
- Execute overall, subject, student, low-attendance, department, section, daily
  and weekly analyses.
- Save real outputs and generate charts from them.

### Non-functional

- **Reproducibility** — fixed seed 42; the same CSV is regenerated.
- **Integrity** — no fabricated results; every number traceable to a file.
- **Portability** — `MODE=native` supports a real cluster; Docker is the default.
- **Auditability** — validation and cross-check reports are saved.

### Actual environment

- Windows 11 + Git Bash, Python 3.14.3, Docker 29.8.0.
- No native Hadoop/Hive; containerised Hadoop 2.7.4 + Hive 2.3.2.
- See `ENVIRONMENT.md` for command outputs and limitations.

## 10. Dataset

File: `data/attendance.csv` (header + 15,360 rows, 999,647 bytes).

```text
student_id,department,semester,section,subject_code,subject_name,
attendance_date,period_number,status
```

Actual statistics:

| Metric | Value |
|---|---|
| Records | 15,360 |
| Present | 11,512 |
| Absent | 3,848 |
| Overall attendance | 74.95% |
| Students | 480 |
| Subject offerings | 80 |
| Departments | 5 |
| Department-semester-sections | 40 |
| Distinct class dates | 65 |
| ISO weeks | 13 |
| Low-attendance groups (<75%) | 650 |

Generation model: each student has a baseline attendance probability; each
subject-section has a small difficulty factor; the date factor includes weekday
effects, a gradual decline and a mid-semester dip (2025-10-13 to 2025-10-17).
Status is therefore not uniformly random, which makes the trend analysis
meaningful. The dataset is entirely synthetic and contains no real identifiers.

Validation: `results/validation_report.txt` records 15 checks, all PASS, including
header, row count, 9-field rows, no missing values, status domain, date validity,
semester/period ranges, duplicate keys and low-group presence.

## 11. Architecture

```text
Python generator (seed 42)
        |
        v
data/attendance.csv  --hdfs dfs -put-->  HDFS /bda/attendance/attendance.csv
                                                |
                                                | LOCATION
                                                v
                                   Hive EXTERNAL table attendance
                                   database: campus_attendance
                                                |
                          HiveQL via Beeline (jdbc:hive2://localhost:10000)
                                                |
                                                v
                              results/overall.csv, subject_wise.csv, ...
                                   |                       |
                                   v                       v
                       Python cross-check          matplotlib charts
                       crosscheck_report.txt       charts/*.png
```

Component responsibilities:

- **NameNode/DataNode** — HDFS namespace and block storage.
- **Hive Metastore (PostgreSQL)** — stores database/table metadata.
- **HiveServer2** — accepts JDBC/Beeline queries and runs MapReduce jobs.
- **Beeline** — executes HiveQL and exports CSV.
- **Python** — generation, validation, independent verification and charts.

## 12. Methodology

1. **Environment inspection** — detect OS, Java, Hadoop, HDFS, Hive, Beeline,
   Python and Docker; record results in `ENVIRONMENT.md`.
2. **Data generation** — deterministic synthesis with seed 42.
3. **Data validation** — schema, domains, duplicates and distribution checks.
4. **HDFS ingestion** — create `/bda/attendance`, upload and verify.
5. **Hive modelling** — create `campus_attendance` and an EXTERNAL table with
   `skip.header.line.count=1`.
6. **Analytics** — execute eight HiveQL queries; save one CSV per query.
7. **Independent validation** — recompute in Python and compare group-by-group.
8. **Visualisation** — build charts only from the saved Hive CSVs.
9. **Documentation and evidence** — README, RUNBOOK, report mapping, screenshots.

## 13. Implementation

Key commands (full sequence in `RUNBOOK.md`):

```bash
python scripts/generate_dataset.py
python scripts/validate_dataset.py

docker compose -f docker/docker-compose.yml up -d

docker compose -f docker/docker-compose.yml exec -T namenode \
  hdfs dfs -mkdir -p /bda/attendance
docker compose -f docker/docker-compose.yml exec -T namenode \
  hdfs dfs -put -f /workspace-data/attendance.csv /bda/attendance/attendance.csv

docker compose -f docker/docker-compose.yml exec -T hive-server beeline \
  -u "jdbc:hive2://localhost:10000/default" -n hive \
  --silent=true --outputformat=csv2 -f /workspace/hive/create_table.sql
```

External table DDL (`hive/create_table.sql`):

```sql
CREATE EXTERNAL TABLE attendance (
  student_id STRING, department STRING, semester INT, section STRING,
  subject_code STRING, subject_name STRING, attendance_date DATE,
  period_number INT, status STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/bda/attendance'
TBLPROPERTIES ('skip.header.line.count'='1');
```

Runtime notes:

- Hive uses the PostgreSQL metastore through `docker/hive-site.xml`; the default
  embedded Derby is bypassed.
- `mapreduce.framework.name=local` lets Hive run jobs without YARN.
- Git Bash requires `MSYS_NO_PATHCONV=1` so container paths are not rewritten.

## 14. Hive Analytics / Data Flow

The table is **external**, so dropping the table does not delete the HDFS file.
Every query reads the same HDFS CSV and writes a result set to a CSV file.

| # | Query file | Purpose | Hive output rows |
|---|---|---|---|
| 1 | `overall.sql` | Overall attendance | 1 |
| 2 | `subject_wise.sql` | Attendance by subject code/name | 80 |
| 3 | `student_wise.sql` | Attendance by student | 480 |
| 4 | `low_attendance.sql` | Student-subject groups below 75% | 650 |
| 5 | `department_wise.sql` | Attendance by department | 5 |
| 6 | `section_wise.sql` | Attendance by department/semester/section | 40 |
| 7 | `daily_trend.sql` | Attendance by date | 65 |
| 8 | `weekly_trend.sql` | Attendance by ISO week | 13 |

Representative HiveQL (overall):

```sql
SELECT COUNT(*) AS total_records,
       SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) AS present_records,
       ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct
FROM attendance;
```

Actual verification (`results/table_verification.txt`):

```text
SHOW TABLES  -> attendance
DESCRIBE     -> 9 columns
LIMIT 10     -> 10 rows beginning 4VV23EE025,EEE,4,A,EE402,...
COUNT(*)     -> 15360
```

## 15. Demonstration

Use the sequence in `RUNBOOK.md` §10. Actual outputs to show:

| Step | Command | Actual output |
|---|---|---|
| Dataset | `wc -l data/attendance.csv` | 15,361 lines (header + 15,360) |
| HDFS | `hdfs dfs -ls /bda/attendance` | one 999,647-byte CSV |
| Table | `SHOW TABLES; DESCRIBE attendance;` | `attendance`; 9 columns |
| Count | `SELECT COUNT(*) FROM attendance;` | 15360 |
| Subject | `subject_wise.sql` | 80 rows; best 83.85%, worst 67.19% |
| Low attendance | `low_attendance.sql` | 650 rows; lowest 12.50% |
| Validation | `crosscheck_report.txt` | 8/8 PASS |
| Chart | `charts/weekly_trend.png` | W36 82.06% to W48 69.33% |

## 16. Results and Analysis

### Overall

11,512 of 15,360 records are present: **74.95%**, just below the 75% policy line.
In a real institution this would trigger an immediate review because the overall
figure is borderline.

### Department

| department | total | present | attendance_pct |
|---|---|---|---|
| CSE | 3,072 | 2,330 | 75.85 |
| ISE | 3,072 | 2,329 | 75.81 |
| ECE | 3,072 | 2,303 | 74.97 |
| EEE | 3,072 | 2,297 | 74.77 |
| ME | 3,072 | 2,253 | 73.34 |

CSE and ISE are above 75%; ECE, EEE and ME are below. ME is the lowest at 73.34%.

### Section

| section | total | present | attendance_pct |
|---|---|---|---|
| B | 7,680 | 5,784 | 75.31 |
| A | 7,680 | 5,728 | 74.58 |

The gap is only 0.73 percentage points, so section alone is not a strong driver
of attendance in this dataset.

### Subjects

- Highest: IS302 Computer Organization and IS503 Big Data Analytics, both 83.85%.
- Lowest: IS601 Compiler Design and ME403 IC Engines, both 67.19%.
- All 80 offerings are below 90%; the spread is 16.66 percentage points.

### Students and low attendance

- 480 students; mean 74.95%, median 75.00%, range 40.63%–100.00%.
- 199 students are below 75%.
- 650 student-subject groups are below 75%, involving 343 distinct students.
- Mean attendance inside low groups is 55.62%.
- Low groups by department: ME 146, EEE 137, ISE 127, ECE 124, CSE 116.

The fact that 343 of 480 students (71.5%) have at least one weak subject is the
most actionable result: intervention should target subject-level gaps, not only
overall student averages.

### Trend

- Best day: 2025-09-10, 88.49%.
- Worst day: 2025-10-15, 60.12%.
- Best week: 2025-W36, 82.06%.
- Worst week: 2025-W42, 63.45%.

Weekly attendance declines over the term, with a sharp W42 dip corresponding to
the synthetic mid-semester period. This supports a practical recommendation:
attendance monitoring and reminders should intensify after the mid-semester break.

### Validation

`results/crosscheck_report.txt` shows 8/8 comparisons PASS. Counts match exactly;
the maximum percentage difference is 0.01 due to rounding. This rules out
formula drift between Hive and the independent recomputation.

## 17. Advantages

- **Scalable storage** — HDFS holds the raw CSV outside any single machine's
  spreadsheet limit.
- **Declarative analytics** — HiveQL expresses aggregations compactly and
  consistently.
- **External table** — the HDFS file remains the source of truth; dropping the
  table does not destroy data.
- **Reproducible** — seed 42 and saved outputs make the study repeatable.
- **Auditable** — every result has a CSV, a cross-check and a chart.
- **Low PII risk** — synthetic IDs only; no real student data.
- **Portable** — the same SQL files run on a native cluster with `MODE=native`.

## 18. Limitations

- The runtime is a **single-node containerised** Hadoop/Hive stack, not a
  multi-node production cluster.
- Hive executes MapReduce in **local mode**; YARN scheduling is not exercised.
- The dataset is **synthetic**; absolute percentages describe the generator, not
  a real institution.
- The data covers one 2025 academic term and 65 class dates.
- Each student-subject combination has **8 sessions**, so percentages move in
  12.5% steps; this limits fine-grained statistical inference.
- Hive 2.3.2 / Hadoop 2.7.4 are older versions; newer Hive supports additional
  optimisations and ACID features.
- No real-time ingestion, authentication, row-level security or dashboards.
- Screenshots for terminal/Hive sessions still need to be captured manually
  (`SCREENSHOT_CHECKLIST.md`).

## 19. Future Enhancements

1. Replace the synthetic feed with a real, consented attendance source and add
   privacy controls.
2. Ingest incrementally with Kafka/Flume and partitioned Hive tables (by
   department/date) stored as ORC/Parquet.
3. Move execution to YARN or Tez/Spark for larger volumes.
4. Add semester-wise and subject-difficulty modelling.
5. Build a dashboard (Superset/Grafana) on top of the Hive results.
6. Automate alerts when a student-subject group falls below 75%.
7. Add role-based access control and audit logging.
8. Add unit tests for the SQL pipeline using a small fixture dataset.

## 20. Conclusion

The project implements a complete HDFS + Apache Hive attendance analytics
pipeline. A reproducible synthetic dataset of 15,360 records was stored in HDFS,
exposed through an external Hive table, and analysed with eight HiveQL queries.
The executed results show 74.95% overall attendance, ME as the lowest department
(73.34%), 199 students below 75%, 650 low-attendance student-subject groups, and
a declining weekly trend with a W42 dip to 63.45%. Every result was independently
recomputed in Python and matched exactly (8/8 PASS). Charts and report evidence
are generated from those actual Hive outputs.

## 21. References

1. Apache Hadoop 2.7.4 documentation — <https://hadoop.apache.org/docs/r2.7.4/>
2. Apache Hive — <https://hive.apache.org/>
3. Apache Hive Language Manual — <https://cwiki.apache.org/confluence/display/Hive/LanguageManual>
4. Apache Hive external tables and `skip.header.line.count` — Hive Language Manual, DDL section.
5. Docker documentation — <https://docs.docker.com/>
6. Docker Compose documentation — <https://docs.docker.com/compose/>
7. PostgreSQL documentation — <https://www.postgresql.org/docs/>
8. pandas documentation — <https://pandas.pydata.org/docs/>
9. Matplotlib documentation — <https://matplotlib.org/stable/>
10. Big Data Europe Hadoop Docker images — <https://github.com/big-data-europe/docker-hadoop>
11. Big Data Europe Hive Docker images — <https://github.com/big-data-europe/docker-hive>
12. Supplied sample report `BDA_Campus_Attendance_Sample_Report.pdf` (structure reference only).
