-- ============================================================================
-- Campus Attendance Trend Analytics Using Apache Hive
-- Core HiveQL analytics (Hive 2.3.2 / Hadoop 2.7.4)
--
-- Each block is also available as an individual file under hive/queries/ so
-- the runner can capture one CSV per analysis. Run this file interactively
-- with: beeline -u jdbc:hive2://localhost:10000 -f hive/analytics.sql
-- ============================================================================

USE campus_attendance;

-- 1. Overall attendance -------------------------------------------------------
SELECT
  COUNT(*) AS total_records,
  SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS present_records,
  ROUND(100.0 * SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attendance_pct
FROM attendance;

-- 2. Subject-wise attendance --------------------------------------------------
SELECT
  subject_code,
  subject_name,
  COUNT(*) AS total_classes,
  SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS present_count,
  ROUND(100.0 * SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attendance_pct
FROM attendance
GROUP BY subject_code, subject_name
ORDER BY attendance_pct DESC, subject_code;

-- 3. Student-wise attendance --------------------------------------------------
SELECT
  student_id,
  COUNT(*) AS total_classes,
  SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS present_count,
  ROUND(100.0 * SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attendance_pct
FROM attendance
GROUP BY student_id
ORDER BY attendance_pct ASC, student_id;

-- 4. Low-attendance student-subject groups (< 75%) ----------------------------
SELECT
  student_id,
  department,
  semester,
  section,
  subject_code,
  subject_name,
  total_classes,
  present_count,
  attendance_pct
FROM (
  SELECT
    student_id,
    department,
    semester,
    section,
    subject_code,
    subject_name,
    COUNT(*) AS total_classes,
    SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS present_count,
    ROUND(100.0 * SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attendance_pct
  FROM attendance
  GROUP BY student_id, department, semester, section, subject_code, subject_name
) t
WHERE attendance_pct < 75
ORDER BY attendance_pct ASC, student_id, subject_code;

-- 5. Department-wise attendance ----------------------------------------------
SELECT
  department,
  COUNT(*) AS total_records,
  SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS present_count,
  ROUND(100.0 * SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attendance_pct
FROM attendance
GROUP BY department
ORDER BY attendance_pct DESC;

-- 6. Section-wise attendance --------------------------------------------------
SELECT
  department,
  semester,
  section,
  COUNT(*) AS total_records,
  SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS present_count,
  ROUND(100.0 * SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attendance_pct
FROM attendance
GROUP BY department, semester, section
ORDER BY department, semester, section;

-- 7a. Daily trend -------------------------------------------------------------
SELECT
  attendance_date,
  COUNT(*) AS total_records,
  SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS present_count,
  ROUND(100.0 * SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attendance_pct
FROM attendance
GROUP BY attendance_date
ORDER BY attendance_date;

-- 7b. Weekly trend ------------------------------------------------------------
SELECT
  CONCAT(YEAR(attendance_date), '-W', LPAD(CAST(WEEKOFYEAR(attendance_date) AS STRING), 2, '0')) AS week_label,
  COUNT(*) AS total_records,
  SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS present_count,
  ROUND(100.0 * SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attendance_pct
FROM attendance
GROUP BY YEAR(attendance_date), WEEKOFYEAR(attendance_date)
ORDER BY week_label;
