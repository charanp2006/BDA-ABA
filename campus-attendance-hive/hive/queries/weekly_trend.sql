SELECT
  CONCAT(YEAR(attendance_date), '-W', LPAD(CAST(WEEKOFYEAR(attendance_date) AS STRING), 2, '0')) AS week_label,
  COUNT(*) AS total_records,
  SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) AS present_count,
  ROUND(100.0 * SUM(CASE WHEN status = 'PRESENT' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attendance_pct
FROM attendance
GROUP BY YEAR(attendance_date), WEEKOFYEAR(attendance_date)
ORDER BY week_label;
