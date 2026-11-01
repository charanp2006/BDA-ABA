-- Campus Attendance Trend Analytics: database and external table
-- Target: Apache Hive 2.3.2 on Hadoop 2.7.4 (container) or compatible.
-- The CSV header is skipped with skip.header.line.count because the external
-- table is backed directly by the header-bearing CSV stored in HDFS.

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
LOCATION '/bda/attendance'
TBLPROPERTIES ('skip.header.line.count'='1');

SHOW TABLES;
DESCRIBE attendance;
SELECT * FROM attendance LIMIT 10;
SELECT COUNT(*) AS total_records FROM attendance;
