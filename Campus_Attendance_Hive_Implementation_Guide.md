# Campus Attendance Hive — Complete Implementation Guide

## Goal
Build a working BDA project using HDFS + Apache Hive/HiveQL for campus attendance analytics.

## Project structure
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
├── README.md
├── RUNBOOK.md
└── run.sh
```

## Dataset
Schema: `student_id, department, semester, section, subject_code, subject_name, attendance_date, period_number, status`

Use synthetic/anonymized data only. Target 5,000–20,000 rows. Status must be `PRESENT` or `ABSENT`. Dates use `YYYY-MM-DD`. Make generation deterministic with a seed.

## Environment verification
```bash
java -version
hadoop version
hdfs version
hive --version
python3 --version
```
If `hive` is unavailable but `beeline` is available, use the installed Hive/Beeline workflow and document it. Do not claim successful Hadoop/Hive execution unless it actually works.

## Generate and validate data
```bash
python3 scripts/generate_dataset.py
python3 scripts/validate_dataset.py
wc -l data/attendance.csv
head data/attendance.csv
```

## HDFS
```bash
hdfs dfs -mkdir -p /bda/attendance
hdfs dfs -put -f data/attendance.csv /bda/attendance/
hdfs dfs -ls /bda/attendance
hdfs dfs -cat /bda/attendance/attendance.csv | head
```

## Hive database/table
```sql
CREATE DATABASE IF NOT EXISTS campus_attendance;
USE campus_attendance;

DROP TABLE IF EXISTS attendance;

CREATE EXTERNAL TABLE attendance (
  student_id STRING,
  department STRING,
  semester INT,
  section STRING,
  subject_code STRING,
  subject_name STRING,
  attendance_date DATE,
  period_number INT,
  status STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/bda/attendance';
```
Handle CSV headers according to the installed Hive version/configuration. Validate with `SELECT * FROM attendance LIMIT 10`.

## Validation
```sql
SHOW TABLES;
DESCRIBE attendance;
SELECT * FROM attendance LIMIT 10;
SELECT COUNT(*) FROM attendance;
```

## Core HiveQL
### Overall
```sql
SELECT COUNT(*) AS total_records,
SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) AS present_records,
ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct
FROM attendance;
```

### Subject-wise
```sql
SELECT subject_code, subject_name,
COUNT(*) AS total_classes,
SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) AS present_count,
ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct
FROM attendance
GROUP BY subject_code, subject_name
ORDER BY attendance_pct DESC;
```

### Student-wise
```sql
SELECT student_id, COUNT(*) AS total_classes,
SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) AS present_count,
ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct
FROM attendance
GROUP BY student_id
ORDER BY attendance_pct;
```

### Low attendance
```sql
SELECT *
FROM (
  SELECT student_id, subject_code, subject_name,
  COUNT(*) AS total_classes,
  SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) AS present_count,
  ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct
  FROM attendance
  GROUP BY student_id, subject_code, subject_name
) t
WHERE attendance_pct < 75
ORDER BY attendance_pct ASC;
```

### Department
```sql
SELECT department, COUNT(*) AS total_records,
SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) AS present_count,
ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct
FROM attendance
GROUP BY department
ORDER BY attendance_pct DESC;
```

### Daily trend
```sql
SELECT attendance_date, COUNT(*) AS total_records,
ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct
FROM attendance
GROUP BY attendance_date
ORDER BY attendance_date;
```

## Charts
Generate charts only from actual Hive outputs:
1. Subject-wise attendance percentage.
2. Department/section comparison.
3. Daily/weekly trend.
4. Optional low-attendance distribution.

## Evidence
Capture screenshots of:
- project folder and CSV;
- Hadoop/HDFS running;
- HDFS input directory;
- Hive table creation;
- `SELECT COUNT(*)`;
- subject-wise query/output;
- low-attendance query/output;
- charts;
- final output files.

## Demo
1. Explain problem.
2. Show CSV.
3. Show HDFS.
4. Show Hive table.
5. Run subject query.
6. Run low-attendance query.
7. Show chart.
8. Explain an actual insight.
9. Explain limitations/future work.

## Report mapping
Use the supplied sample report as the structural reference. Replace all `[ACTUAL VALUE]` and evidence placeholders with verified implementation output. Never fabricate results.

## Acceptance criteria
The project is complete only when HDFS stores the data, Hive creates the table, core queries execute, outputs are saved, charts are based on actual outputs, screenshots/evidence are available, and README/RUNBOOK explain reproducible execution.
