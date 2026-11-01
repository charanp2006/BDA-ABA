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
