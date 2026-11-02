Campus Attendance Hive — Simple Explanation, Demo Guide, and Viva Prep

No files changed. This is a read-only explanation of the project we built.

---

## 1. The project in one paragraph

We built a **big-data attendance analytics system**. Attendance records are stored in **HDFS** (Hadoop's distributed file system), and **Apache Hive** is used to answer questions like:

- What is the overall attendance?
- Which subject has the lowest attendance?
- Which students are below 75%?
- Which department/section is doing better?
- Is attendance falling week by week?

The actual analysis is done in **HiveQL**, not in pandas or normal SQL. Python is used only to generate the data, validate it, cross-check Hive's answers, and draw charts.

**Simple analogy:**  
Think of HDFS as a very large warehouse for CSV files. Hive is like a librarian who understands table structure and SQL, so you can ask questions about the warehouse without writing Java/MapReduce programs yourself.

---

## 2. Why this project matters

In a college, attendance is recorded as many small events:

```text
student_id, department, semester, section, subject_code, subject_name,
attendance_date, period_number, status
```

Example row:

```text
4VV23CS001,CSE,3,A,CS301,Data Structures,2025-09-01,1,PRESENT
```

One row means: "Student 4VV23CS001 attended Data Structures on 1 Sep 2025, period 1."

Doing this manually for thousands of rows is slow and error-prone. Our system can answer all the questions consistently from one dataset.

---

## 3. What we actually built

We built a complete pipeline:

1. Generate synthetic attendance data.
2. Validate the data.
3. Upload it to HDFS.
4. Create a Hive external table over the HDFS file.
5. Run 8 HiveQL analytics queries.
6. Save the actual Hive outputs as CSV files.
7. Recompute the same results independently in Python and compare.
8. Draw charts from the Hive results.
9. Write documentation and capture evidence.

**Actual dataset size:** 15,360 records  
**Students:** 480  
**Subject offerings:** 80  
**Departments:** CSE, ISE, ECE, EEE, ME  
**Overall attendance:** 74.95% (11,512 present / 15,360)

---

## 4. Tech stack — what, why, and how

| Technology | Version | Why we used it | How it is used |
|---|---|---|---|
| **HDFS** | Hadoop 2.7.4 | Distributed storage; project must keep Hadoop central | Stores `/bda/attendance/attendance.csv` |
| **Apache Hive** | 2.3.2 | SQL-like analytics over Hadoop data | Database `campus_attendance`, external table `attendance` |
| **HiveQL** | Hive 2.3.2 | Declarative aggregation | All 8 analytics queries |
| **MapReduce** | Hadoop 2.7.4 | Hive executes jobs as MapReduce | Runs in local mode inside the Hive container |
| **Hive Metastore + PostgreSQL** | Hive schema 2.3.0 | Stores table metadata | Remembers database/table definitions |
| **Beeline / HiveServer2** | Hive 2.3.2 | Client interface to Hive | Runs SQL and exports CSV |
| **Docker + Compose** | 29.8.0 / v5.5.1 | Native Hadoop/Hive was not available on Windows | Runs real HDFS + Hive in Linux containers |
| **Python** | 3.14.3 | Data generation and validation | `generate_dataset.py`, `validate_dataset.py` |
| **pandas / numpy** | 3.0.2 / 2.4.4 | Independent result checking | `crosscheck_results.py` |
| **matplotlib** | 3.10.9 | Charts from real Hive results | `make_charts.py` |

**Important point for the professor:**  
Python is **not** replacing Hive. The main analytics are 100% HiveQL. Python only checks and visualises what Hive produced.

---

## 5. How the data flows — step by step

```text
1. Python creates CSV
        ↓
2. CSV uploaded to HDFS: /bda/attendance/attendance.csv
        ↓
3. Hive external table points to that HDFS folder
        ↓
4. HiveQL queries aggregate the data
        ↓
5. Results saved as results/*.csv
        ↓
6. Python recomputes and compares → PASS
        ↓
7. Charts drawn from Hive result files
```

A good sentence to say:

> "HDFS stores the data, Hive gives it a table structure, HiveQL performs the aggregation, and Python independently verifies the output."

---

## 6. What each folder and file does

### Root files

| File | What it does |
|---|---|
| `run.sh` | One-command runner: generates data, starts Docker stack, uploads to HDFS, creates Hive table, runs all queries, cross-checks, and makes charts |
| `README.md` | Full project overview, results, commands |
| `RUNBOOK.md` | Setup, start/stop, troubleshooting, demo sequence |
| `ENVIRONMENT.md` | What tools were detected and why Docker was used |
| `SCREENSHOT_CHECKLIST.md` | Which screenshots to capture and exact commands |

### `data/`

| File | Purpose |
|---|---|
| `attendance.csv` | The 15,360 synthetic attendance records |

### `docker/`

| File | Purpose |
|---|---|
| `docker-compose.yml` | Starts 5 containers: NameNode, DataNode, Hive Metastore, HiveServer2, PostgreSQL |
| `hadoop.env` | Hadoop settings: HDFS address, replication, local MapReduce mode |
| `hive-site.xml` | Tells Hive to use PostgreSQL metastore and HDFS instead of embedded Derby |

This folder is necessary because we could not install Hadoop/Hive natively on this Windows machine.

### `hive/`

| File | Purpose |
|---|---|
| `create_table.sql` | Creates database `campus_attendance` and external table `attendance` |
| `analytics.sql` | All 8 analyses in one file for documentation/manual use |
| `verify_table.sql` | Generated script for `SHOW TABLES`, `DESCRIBE`, `LIMIT`, `COUNT(*)` |
| `queries/overall.sql` | Overall attendance |
| `queries/subject_wise.sql` | Attendance per subject |
| `queries/student_wise.sql` | Attendance per student |
| `queries/low_attendance.sql` | Student-subject groups below 75% |
| `queries/department_wise.sql` | Attendance per department |
| `queries/section_wise.sql` | Attendance per department/semester/section |
| `queries/daily_trend.sql` | Attendance per day |
| `queries/weekly_trend.sql` | Attendance per ISO week |

### `scripts/`

| File | Purpose |
|---|---|
| `generate_dataset.py` | Creates the synthetic CSV using seed 42 |
| `validate_dataset.py` | Checks schema, dates, statuses, missing values, duplicates → 15/15 PASS |
| `crosscheck_results.py` | Recomputes all metrics in Python and compares with Hive CSV outputs → 8/8 PASS |
| `make_charts.py` | Creates 7 charts from the actual Hive result CSVs |
| `summarize_results.py` | Produces `results/key_findings.md` with the main insights |

### `results/`

This is the most important evidence folder.

| File | What it proves |
|---|---|
| `overall.csv` | Hive's overall result: 15360, 11512, 74.95 |
| `subject_wise.csv` | 80 subject rows |
| `student_wise.csv` | 480 student rows |
| `low_attendance.csv` | 650 low-attendance groups |
| `department_wise.csv` | 5 department rows |
| `section_wise.csv` | 40 section rows |
| `daily_trend.csv` | 65 daily rows |
| `weekly_trend.csv` | 13 weekly rows |
| `table_verification.txt` | SHOW TABLES / DESCRIBE / LIMIT / COUNT evidence |
| `hdfs_ls.txt` | HDFS upload evidence |
| `hdfs_sample_rows.txt` | First rows from HDFS |
| `validation_report.txt` | Dataset quality checks |
| `crosscheck_report.txt` | Python-vs-Hive comparison |
| `key_findings.md` | Human-readable summary of actual results |
| `hive_execution.log` | Log of executed Hive queries |

`.err` files only contain harmless SLF4J warning messages. They do not mean the queries failed.

### `charts/`

7 charts, all built from the Hive CSV results:

- subject attendance
- department attendance
- section comparison
- daily trend
- weekly trend
- low-attendance distribution
- student attendance distribution

### `screenshots/`

| File | Content |
|---|---|
| `01_hdfs_namenode_overview.png` | Real HDFS NameNode web UI |
| `02_hdfs_bda_attendance.png` | Real HDFS browse view showing `attendance.csv` |

### `docs/`

| File | Purpose |
|---|---|
| `REPORT_EVIDENCE.md` | Maps the implementation to all 21 report sections |

---

## 7. The 8 Hive analyses — simple explanation

| Analysis | Question answered |
|---|---|
| Overall | What percentage of all records are present? |
| Subject-wise | Which subjects are strong/weak? |
| Student-wise | Which students have low overall attendance? |
| Low attendance | Which student-subject pairs are below 75%? |
| Department-wise | Which department has the best attendance? |
| Section-wise | Does section A or B do better? |
| Daily trend | Which dates have low attendance? |
| Weekly trend | Is attendance improving or falling over the term? |

The core HiveQL pattern is:

```sql
ROUND(100.0 * SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) / COUNT(*), 2)
```

Meaning: count present rows, divide by total rows, multiply by 100, round to 2 decimals.

---

## 8. Actual results — and what they mean

| Result | Value |
|---|---|
| Overall attendance | **74.95%** |
| Present / total | **11,512 / 15,360** |
| Best department | CSE — 75.85% |
| Lowest department | ME — 73.34% |
| Section B vs A | 75.31% vs 74.58% |
| Students below 75% | **199** |
| Low-attendance student-subject groups | **650** |
| Students affected by at least one low group | **343** |
| Mean attendance inside low groups | **55.62%** |
| Best subject | IS302 / IS503 — 83.85% |
| Worst subject | IS601 / ME403 — 67.19% |
| Best week | 2025-W36 — 82.06% |
| Worst week | 2025-W42 — 63.45% |

**Simple interpretation:**

- Overall attendance is just below the 75% rule, so it needs attention.
- ME is the weakest department.
- 199 students are below 75% overall.
- 650 specific student-subject combinations are weak; this is more actionable than only looking at student averages.
- Attendance declines through the term, with a sharp dip in week 42.
- Python independently matched all 8 Hive results, so the numbers are reliable.

---

## 9. How to explain it to your professor — 60–90 second script

Say something like:

> "Our project is a campus attendance analytics system built on the Hadoop ecosystem. We store 15,360 synthetic attendance records in HDFS at `/bda/attendance`. We created an external Hive table called `attendance` in the `campus_attendance` database. All analytics are done in HiveQL: overall attendance, subject-wise, student-wise, low-attendance groups below 75%, department-wise, section-wise, and daily/weekly trends.  
>  
> The dataset is synthetic and reproducible with seed 42, so there is no real student data. We validated it with 15 checks. Hive produced the results, and then we independently recomputed the same metrics in Python; all 8 comparisons passed. Finally, we generated charts only from the Hive result files.  
>  
> The main findings are: overall attendance is 74.95%, ME is the lowest department at 73.34%, 199 students are below 75%, and 650 student-subject groups are below 75%. Weekly attendance drops from 82.06% in week 36 to 63.45% in week 42.  
>  
> The main limitation is that we ran a single-node containerised Hadoop/Hive stack, not a multi-node production cluster, but the HDFS and HiveQL execution is real."

That covers problem, dataset, technology, method, results, validation and limitations.

---

## 10. Likely professor questions and simple answers

**Q: Why Hive and not pandas?**  
Hive is the main analytics engine over HDFS. pandas is only used to independently verify Hive's answers and draw charts. The project keeps Hive central as required.

**Q: Why HDFS?**  
HDFS stores the dataset in a distributed file system and acts as the source of truth. Hive's external table points directly to the HDFS folder.

**Q: What is an external table?**  
It is a Hive table whose data stays in HDFS. Dropping the table does not delete the HDFS file.

**Q: What is the Hive Metastore?**  
It stores metadata: database names, table names, column definitions and the HDFS location. We used PostgreSQL for it.

**Q: What does HiveQL compile into?**  
Hive converts queries into distributed jobs. In our setup, MapReduce runs in local mode inside the HiveServer2 container because we did not start YARN.

**Q: Why Docker?**  
Native Hadoop/Hive was not installed on this Windows machine, and the host has Java 26, which is too new for Hadoop 2.7. Docker gives us a real Linux Hadoop/Hive environment without breaking the host.

**Q: Is the data real?**  
No. It is fully synthetic and anonymised. No real student PII is used.

**Q: How do you know the results are correct?**  
Two ways: the dataset validation has 15/15 PASS, and the independent Python cross-check has 8/8 PASS with matching counts and only 0.01% rounding differences.

**Q: Why is overall attendance 74.95%?**  
Because the raw data has 11,512 present records out of 15,360. It is not forced to exactly 75%.

**Q: Why do some groups show 12.50%?**  
Each student-subject pair has 8 sessions. One present out of eight is 12.5%. Percentages therefore move in 12.5% steps.

**Q: What is the header problem?**  
The CSV has a header row. We handle it with `TBLPROPERTIES ('skip.header.line.count'='1')` so Hive does not treat the header as data.

**Q: What are the limitations?**  
Single-node containerised setup, local MapReduce instead of YARN, synthetic data, one academic term, and older Hadoop/Hive versions.

**Q: What would you improve?**  
Real consented data, partitioned ORC/Parquet tables, YARN/Tez/Spark execution, dashboards, automated alerts, and role-based security.

---

## 11. How to demonstrate — practical sequence

### Before the demo (5 minutes before)

1. Start Docker Desktop.
2. Check containers:

```bash
cd C:/Charan/ABA/BDA-ABA/campus-attendance-hive
docker compose -f docker/docker-compose.yml ps
```

All 5 should be `Up`. If not, run:

```bash
./run.sh
```

3. Open these in advance:
   - Terminal in `campus-attendance-hive`
   - Browser tab: `http://localhost:50070/dfshealth.html#tab-overview`
   - Browser tab: `http://localhost:50070/explorer.html#/bda/attendance`
   - File Explorer: `charts/`
   - File Explorer: `results/`

### Demo step 1 — Show the dataset

```bash
wc -l data/attendance.csv
head data/attendance.csv
```

Say: "This is 15,360 synthetic attendance records plus a header."

### Demo step 2 — Show the Hadoop/Hive stack

```bash
docker compose -f docker/docker-compose.yml ps
```

Say: "HDFS NameNode, DataNode, Hive Metastore, HiveServer2 and PostgreSQL are running."

### Demo step 3 — Show HDFS

```bash
export MSYS_NO_PATHCONV=1
docker compose -f docker/docker-compose.yml exec -T namenode \
  hdfs dfs -ls /bda/attendance
```

Then open the HDFS explorer browser tab and show `attendance.csv`.

### Demo step 4 — Show the Hive table

```bash
docker compose -f docker/docker-compose.yml exec -T hive-server beeline \
  -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive
```

Inside Beeline:

```sql
SHOW TABLES;
DESCRIBE attendance;
SELECT COUNT(*) FROM attendance;
```

Expected: `attendance`, 9 columns, `15360`.

### Demo step 5 — Run the subject query

```sql
SELECT subject_code, subject_name,
       ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct
FROM attendance
GROUP BY subject_code, subject_name
ORDER BY attendance_pct DESC;
```

Say: "Best subjects are IS302 and IS503 at 83.85%; worst are IS601 and ME403 at 67.19%."

### Demo step 6 — Run the low-attendance query

You can run the saved file outside Beeline:

```bash
docker compose -f docker/docker-compose.yml exec -T hive-server beeline \
  -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive \
  --silent=true --outputformat=csv2 \
  -f /workspace/hive/queries/low_attendance.sql
```

Say: "Hive found 650 student-subject groups below 75%, affecting 343 students."

### Demo step 7 — Show validation

```bash
cat results/crosscheck_report.txt
```

Say: "Every Hive result was independently recomputed in Python; 8 out of 8 passed."

### Demo step 8 — Show charts

Open `charts/weekly_trend.png` and `charts/department_attendance.png`.

Say: "These charts are generated from the Hive CSV outputs, not from separate Python calculations."

### Demo step 9 — Explain insights

- Overall 74.95%, just below 75%.
- ME is the weakest department.
- 199 students below 75%.
- 650 weak student-subject groups.
- Attendance declines over the term with a W42 dip.

### Demo step 10 — Limitations and future work

Say: "We used a single-node containerised stack and synthetic data. Future work includes real consented data, partitioned ORC tables, YARN/Spark, and dashboards."

---

## 12. Backup plan if something fails during the demo

Do **not** pretend a failed command succeeded. Instead say:

> "The live stack is not responding right now, but here are the actual outputs saved during the clean run."

Then show:

- `results/*.csv`
- `results/table_verification.txt`
- `results/crosscheck_report.txt`
- `results/key_findings.md`
- `charts/*.png`
- `screenshots/*.png`

This is acceptable because the evidence is real and was produced by actual execution.

---

## 13. Things you must know before the demo

### Do not run this before the demo

```bash
docker compose -f docker/docker-compose.yml down -v
```

`down -v` deletes the HDFS data volumes. `./run.sh` can rebuild everything, but it takes time.

### Safe stop command

```bash
docker compose -f docker/docker-compose.yml stop
```

### Restart later

```bash
docker compose -f docker/docker-compose.yml start
```

### These `.err` files are not failures

Files like `results/overall.err` contain only SLF4J warning messages. The actual CSV outputs are valid.

### First Hive query is slower

The first query may take 20–60 seconds because MapReduce starts local jobs. Later queries are faster.

### Git Bash path issue

If you see `No FileSystem for scheme: C`, run:

```bash
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL='*'
```

`run.sh` sets these automatically.

### Reproducibility

The generator uses seed 42. If you delete and regenerate the dataset, you get the same 15,360 records and the same results.

### Data honesty

Always say the data is synthetic. Do not call it real college attendance data.

### External table point

Because the table is external, the HDFS CSV is the source of truth. This is a strong academic point to mention.

### Hive is not a traditional database

It is a warehouse/query layer over HDFS. It uses schema-on-read and executes distributed jobs.

---

## 14. Suggested team split for the presentation

| Member | Suggested part |
|---|---|
| Bharath Krishna K K | Problem statement, Hadoop ecosystem, HDFS architecture |
| Charan P | Hive table, HiveQL queries, results explanation |
| Abu Safwan | Dataset validation, Python cross-check, charts, limitations, future work |

All three should be able to answer basic questions about the full pipeline, not only their own part.

---

## 15. One-sentence summary to memorise

> "We stored 15,360 synthetic attendance records in HDFS, analysed them with eight HiveQL queries in Apache Hive, independently verified every result in Python with 8/8 matches, and produced charts showing 74.95% overall attendance, 650 low-attendance student-subject groups, and a declining weekly trend."

That sentence alone can anchor the entire presentation.
