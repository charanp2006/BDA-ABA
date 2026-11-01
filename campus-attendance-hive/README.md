# Campus Attendance Trend Analytics Using Apache Hive on the Hadoop Ecosystem

A complete Big Data Analytics project that stores synthetic campus attendance data
in **HDFS** and analyses it with **Apache Hive / HiveQL**. Python is used only for
deterministic data generation, validation, result verification and charts.

**Team**

| Name | USN |
|---|---|
| Bharath Krishna K K | 4VV23CS033 |
| Charan P | 4VV23CS042 |
| Abu Safwan | 4VV23CS006 |

> All data is **synthetic and anonymised**. No real student information is used.

---

## 1. What this project demonstrates

- A reproducible synthetic attendance dataset of **15,360 records**.
- Upload of that CSV into **HDFS at `/bda/attendance`**.
- An **EXTERNAL Hive table** `campus_attendance.attendance` over the HDFS file.
- Eight HiveQL analyses: overall, subject, student, low-attendance, department,
  section, daily trend and weekly trend.
- Hive results saved as real CSV files in `results/`.
- An **independent Python cross-check** of every Hive result.
- Charts generated only from the Hive result CSVs.
- Report-ready evidence, documentation and screenshot checklist.

---

## 2. Architecture

```text
+---------------------+        +------------------------------+
|  Python generator   |        |        Apache Hive           |
|  (seed = 42)        |        |  database: campus_attendance |
|  data/attendance.csv|        |  external table: attendance  |
+----------+----------+        +---------------+--------------+
           |                                   |
           | hdfs dfs -put                     | HiveQL / Beeline JDBC
           v                                   |
+---------------------+        +---------------v--------------+
|       HDFS          |        |     HiveServer2 :10000       |
| /bda/attendance/    |<-------+     Hive Metastore :9083     |
|   attendance.csv    |        |     PostgreSQL metastore     |
+---------------------+        +------------------------------+
                                           |
                                           v
                              +--------------------------+
                              | results/*.csv            |
                              | charts/*.png             |
                              | crosscheck_report.txt    |
                              +--------------------------+
```

The Hadoop/Hive services run in Docker on this Windows host because no native
Hadoop/Hive installation is available. Details: `ENVIRONMENT.md`.

---

## 3. Dataset

| Property | Actual value |
|---|---|
| File | `data/attendance.csv` |
| Records (excluding header) | **15,360** |
| Unique students | **480** |
| Subject offerings | **80** (16 subjects in each of 5 departments) |
| Departments | CSE, ISE, ECE, EEE, ME |
| Semesters | 3, 4, 5, 6 |
| Sections | A, B |
| Class dates | 2025-09-01 to 2025-11-28 (65 weekdays) |
| Periods | 1 to 8 |
| Status values | `PRESENT`, `ABSENT` only |
| Overall attendance | **74.95%** (11,512 present / 15,360) |
| Low-attendance student-subject groups (<75%) | **650** |
| Random seed | 42 (deterministic; re-running reproduces the same file) |

Schema:

```text
student_id, department, semester, section, subject_code, subject_name,
attendance_date, period_number, status
```

The generator intentionally models per-student ability, subject-level variation,
weekday effects and a mid-semester dip so the trend analysis is meaningful.

---

## 4. Project structure

```text
campus-attendance-hive/
├── data/
│   └── attendance.csv                 # 15,360 synthetic records
├── docker/
│   ├── docker-compose.yml             # HDFS + Hive + PostgreSQL metastore
│   ├── hadoop.env                     # Hadoop/HDFS/MapReduce configuration
│   └── hive-site.xml                  # Hive -> PostgreSQL + HDFS configuration
├── hive/
│   ├── create_table.sql               # database + EXTERNAL table
│   ├── analytics.sql                  # all HiveQL analyses in one file
│   ├── verify_table.sql               # generated verification script
│   └── queries/                       # one HiveQL file per analysis
├── scripts/
│   ├── generate_dataset.py
│   ├── validate_dataset.py
│   ├── crosscheck_results.py          # independent Python verification
│   ├── make_charts.py
│   └── summarize_results.py
├── results/                           # actual Hive output + validation reports
├── charts/                            # charts built from Hive output
├── screenshots/                       # real HDFS UI captures
├── docs/
│   └── REPORT_EVIDENCE.md
├── ENVIRONMENT.md
├── README.md
├── RUNBOOK.md
├── SCREENSHOT_CHECKLIST.md
└── run.sh
```

---

## 5. Prerequisites

- Python 3.10+ with `pandas`, `numpy`, `matplotlib`
- Docker Desktop with the Linux container engine running
- ~5 GB free disk for the first image pull
- Internet access on first run

The tested environment is documented in `ENVIRONMENT.md`.

---

## 6. Quick start (one command)

```bash
cd campus-attendance-hive
chmod +x run.sh
./run.sh
```

`run.sh` performs the complete workflow:

1. generate + validate the dataset;
2. start HDFS/Hive containers;
3. create `/bda/attendance` and upload the CSV;
4. create `campus_attendance.attendance`;
5. verify with `SHOW TABLES`, `DESCRIBE`, `LIMIT`, `COUNT(*)`;
6. execute the eight HiveQL analyses;
7. cross-check every result with Python;
8. generate charts;
9. write the key-findings summary.

If Hadoop/Hive are installed natively, use:

```bash
MODE=native ./run.sh
```

---

## 7. Step-by-step commands (equivalent to run.sh)

### 7.1 Generate and validate

```bash
python scripts/generate_dataset.py
python scripts/validate_dataset.py
wc -l data/attendance.csv
head data/attendance.csv
```

### 7.2 Start the Hadoop/Hive stack

```bash
docker compose -f docker/docker-compose.yml up -d
docker compose -f docker/docker-compose.yml ps
```

### 7.3 HDFS upload

```bash
export MSYS_NO_PATHCONV=1          # Git Bash only
docker compose -f docker/docker-compose.yml exec -T namenode \
  hdfs dfs -mkdir -p /bda/attendance
docker compose -f docker/docker-compose.yml exec -T namenode \
  hdfs dfs -put -f /workspace-data/attendance.csv /bda/attendance/attendance.csv
docker compose -f docker/docker-compose.yml exec -T namenode \
  hdfs dfs -ls /bda/attendance
```

### 7.4 Create and verify the Hive table

```bash
docker compose -f docker/docker-compose.yml exec -T hive-server beeline \
  -u "jdbc:hive2://localhost:10000/default" -n hive --silent=true \
  --outputformat=csv2 -f /workspace/hive/create_table.sql

docker compose -f docker/docker-compose.yml exec -T hive-server beeline \
  -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive --silent=true \
  --outputformat=csv2 -f /workspace/hive/verify_table.sql
```

Actual verification result:

```text
SHOW TABLES      -> attendance
DESCRIBE         -> 9 columns (student_id ... status)
LIMIT 10         -> 10 real attendance rows
COUNT(*)         -> 15360
```

### 7.5 Run all analytics

Use `./run.sh`, or run each file in `hive/queries/` through Beeline and save the
stdout as `results/<name>.csv`. `hive/analytics.sql` contains the same queries
for interactive use.

---

## 8. Actual results

All figures below were produced by Hive and independently recomputed from the
same CSV. Full detail: `results/key_findings.md`,
`results/crosscheck_report.txt`.

### Overall

| total_records | present_records | attendance_pct |
|---|---|---|
| 15,360 | 11,512 | 74.95 |

### Department-wise

| department | total_records | present_count | attendance_pct |
|---|---|---|---|
| CSE | 3,072 | 2,330 | 75.85 |
| ISE | 3,072 | 2,329 | 75.81 |
| ECE | 3,072 | 2,303 | 74.97 |
| EEE | 3,072 | 2,297 | 74.77 |
| ME | 3,072 | 2,253 | 73.34 |

### Section-wise (all departments combined)

| section | total_records | present_count | attendance_pct |
|---|---|---|---|
| B | 7,680 | 5,784 | 75.31 |
| A | 7,680 | 5,728 | 74.58 |

### Highest and lowest subjects

| Direction | subject_code | subject_name | attendance_pct |
|---|---|---|---|
| Highest | IS302 | Computer Organization | 83.85 |
| Highest | IS503 | Big Data Analytics | 83.85 |
| Lowest | IS601 | Compiler Design | 67.19 |
| Lowest | ME403 | IC Engines | 67.19 |

### Student-wise

- 480 students analysed
- Mean attendance: **74.95%**
- Median: **75.00%**
- Range: **40.63% – 100.00%**
- Students below 75%: **199**

### Low attendance

- **650** student-subject groups below 75%
- **343** distinct students affected
- All 80 subject offerings contain at least one low group
- Mean attendance inside low groups: **55.62%**
- Most affected department: **ME** (146 groups, 72 students)

### Trend

| Metric | Actual value |
|---|---|
| Highest day | 2025-09-10 — 88.49% |
| Lowest day | 2025-10-15 — 60.12% |
| Highest week | 2025-W36 — 82.06% |
| Lowest week | 2025-W42 — 63.45% |

The weekly series declines from 82.06% in W36 to 69.33% in W48, with a sharp
mid-semester dip in W42. This is a genuine property of the generated data, not a
hard-coded conclusion.

---

## 9. Charts (from Hive output only)

| File | Content |
|---|---|
| `charts/subject_attendance.png` | All 80 subject offerings with 75% threshold |
| `charts/department_attendance.png` | Department comparison |
| `charts/section_comparison.png` | Section A vs B by department |
| `charts/daily_trend.png` | Daily attendance trend |
| `charts/weekly_trend.png` | Weekly trend |
| `charts/low_attendance_distribution.png` | Low-group distribution and department counts |
| `charts/student_attendance_distribution.png` | Distribution of student attendance |

---

## 10. Validation

`scripts/validate_dataset.py` checks header, row count, field count, missing
values, status domain, date validity/range, semester/period ranges, duplicate
keys, student/subject counts and the presence of low-attendance groups. Current
result: **15/15 checks PASS**.

`scripts/crosscheck_results.py` recomputes all metrics independently from
`data/attendance.csv` and compares them with the Hive CSV outputs. Current
result: **8/8 comparisons PASS**, with a maximum percentage difference of 0.01
(caused only by rounding). See `results/crosscheck_report.txt`.

---

## 11. Evidence

| Evidence | Location |
|---|---|
| Dataset validation report | `results/validation_report.txt` |
| HDFS directory listing | `results/hdfs_ls.txt` |
| HDFS sample rows | `results/hdfs_sample_rows.txt` |
| Table creation + `SHOW/DESCRIBE/LIMIT/COUNT` | `results/table_verification.txt` |
| Hive setup output | `results/hive_setup_output.txt` |
| Eight Hive result CSVs | `results/*.csv` |
| Hive execution log | `results/hive_execution.log` |
| Independent cross-check | `results/crosscheck_report.txt` |
| Real HDFS web UI screenshots | `screenshots/01_*.png`, `screenshots/02_*.png` |
| Remaining captures to take manually | `SCREENSHOT_CHECKLIST.md` |

---

## 12. Environment limitations and remaining manual steps

- Hadoop/Hive were **not available natively** on this Windows machine. A real
  Hadoop 2.7.4 + Hive 2.3.2 stack was executed in Docker instead.
- No YARN cluster is used. Hive runs MapReduce in local mode; all HiveQL and
  HDFS operations are still genuine.
- If the evaluator requires a native or university cluster:
  1. install a compatible JDK (Java 8 for Hadoop 2.7 / Java 8 or 11 for
     Hadoop 3.x and Hive 3.x);
  2. start HDFS (`start-dfs.sh`) and Hive (`hiveserver2` / `metastore`);
  3. export `HADOOP_CONF_DIR`/`HIVE_CONF_DIR` and add `hdfs`/`beeline` to `PATH`;
  4. run `MODE=native ./run.sh`.
- The provided 2025 dates are the synthetic academic term; they are not the
  current calendar date.
- Manual screenshots still required for terminal/Hive outputs; exact commands
  are listed in `SCREENSHOT_CHECKLIST.md`.

---

## 13. Documentation map

- `ENVIRONMENT.md` — detected tools and runtime decision
- `RUNBOOK.md` — setup, operation, troubleshooting, demo sequence
- `docs/REPORT_EVIDENCE.md` — mapping to the 21 report sections
- `SCREENSHOT_CHECKLIST.md` — evidence capture plan
- `results/key_findings.md` — generated actual findings

---

## 14. Academic integrity

Every number in this README is taken from files produced by the executed Hive
queries or from the independent Python cross-check of those files. No execution
claims, screenshots or results were invented.
