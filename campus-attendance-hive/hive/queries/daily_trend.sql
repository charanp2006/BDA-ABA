SELECT
  attendance_date,
  COUNT(*) AS total_records,
  SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS present_count,
  ROUND(100.0 * SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attendance_pct
FROM attendance
GROUP BY attendance_date
ORDER BY attendance_date;
