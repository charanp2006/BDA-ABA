# RUNBOOK

Operational guide for **Campus Attendance Trend Analytics Using Apache Hive on
the Hadoop Ecosystem**.

---

## 1. Prerequisites

| Requirement | Check |
|---|---|
| Python 3.10+ | `python --version` |
| pandas, numpy, matplotlib | `pip install pandas numpy matplotlib` |
| Docker Desktop with Linux containers | `docker version` |
| Docker Compose v2+ | `docker compose version` |
| ~5 GB free disk (first pull) | `docker system df` |

Tested with Docker 29.8.0 / Compose v5.5.1 and Python 3.14.3. See
`ENVIRONMENT.md`.

---

## 2. First-time setup

```bash
cd campus-attendance-hive
chmod +x run.sh

# Start Docker Desktop first, then confirm:
docker version
```

On Windows/Git Bash, `run.sh` already exports:

```bash
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL='*'
```

If you run Docker commands manually in Git Bash, export these yourself.

First run downloads these images (about 4–5 GB total):

- `bde2020/hadoop-namenode:2.0.0-hadoop2.7.4-java8`
- `bde2020/hadoop-datanode:2.0.0-hadoop2.7.4-java8`
- `bde2020/hive:2.3.2-postgresql-metastore`
- `bde2020/hive-metastore-postgresql:2.3.0`

---

## 3. Normal full run

```bash
./run.sh
```

Expected high-level output:

```text
Wrote 15,360 records ...
RESULT: PASS                       # dataset validation
Found 1 items                      # HDFS upload
Running overall ...                # 8 Hive queries
[PASS] overall ...
RESULT: PASS                       # independent cross-check
wrote charts\...
Run complete.
```

Typical runtime after images are cached: 2–5 minutes.

---

## 4. Start / stop / reset

```bash
# Start the stack only
docker compose -f docker/docker-compose.yml up -d

# Status
docker compose -f docker/docker-compose.yml ps

# Stop (keeps HDFS data volumes)
docker compose -f docker/docker-compose.yml stop

# Start again
docker compose -f docker/docker-compose.yml start

# Remove containers and network (keeps named volumes)
docker compose -f docker/docker-compose.yml down

# Full reset (deletes HDFS data volumes too)
docker compose -f docker/docker-compose.yml down -v
```

After a full reset, `./run.sh` recreates the HDFS directory, uploads the CSV and
creates the Hive table again.

---

## 5. Manual operations

```bash
export MSYS_NO_PATHCONV=1

# HDFS
docker compose -f docker/docker-compose.yml exec -T namenode hdfs dfs -ls /bda/attendance
docker compose -f docker/docker-compose.yml exec -T namenode hdfs dfs -cat /bda/attendance/attendance.csv | head

# Hive / Beeline
docker compose -f docker/docker-compose.yml exec -T hive-server beeline \
  -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive \
  --silent=true --showHeader=true --outputformat=csv2
```

Inside Beeline:

```sql
SHOW TABLES;
DESCRIBE attendance;
SELECT COUNT(*) FROM attendance;
SELECT subject_code, subject_name,
       ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct
FROM attendance
GROUP BY subject_code, subject_name
ORDER BY attendance_pct;
```

Run a saved query and capture output:

```bash
docker compose -f docker/docker-compose.yml exec -T hive-server beeline \
  -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive \
  --silent=true --verbose=false --showHeader=true --outputformat=csv2 \
  --hiveconf mapreduce.framework.name=local \
  --hiveconf hive.exec.mode.local.auto=true \
  -f /workspace/hive/queries/subject_wise.sql \
  2>results/subject_wise.err | sed '/^[[:space:]]*$/d' > results/subject_wise.csv
```

---

## 6. Web interfaces

| Service | URL |
|---|---|
| HDFS NameNode | <http://localhost:50070> |
| Browse HDFS | <http://localhost:50070/explorer.html#/bda/attendance> |
| HiveServer2 JDBC | `jdbc:hive2://localhost:10000` |
| Hive Metastore Thrift | `localhost:9083` |

There is no Hive web UI in this stack; use Beeline for Hive evidence.

---

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `failed to connect to the docker API` | Docker Desktop not running | Start Docker Desktop; wait until `docker version` succeeds |
| `No FileSystem for scheme: C` | Git Bash rewrote `/bda/...` | `export MSYS_NO_PATHCONV=1` |
| `hive-metastore` restarting, `Version information not found` | Hive used embedded Derby / wrong metastore | Ensure `docker/hive-site.xml` is mounted (compose does this); then `down` and `up -d` |
| HiveServer2 connection refused | Hive still starting | Wait; `run.sh` polls for up to ~7 minutes. Check `docker logs campus-hive-server` |
| `bde2020/hive-metastore-postgresql` not ready | Startup ordering | `docker compose ... restart hive-metastore hive-server` |
| Query produces empty CSV | SQL error; see `results/<query>.err` | Fix SQL; `weekly_trend.sql` must `ORDER BY week_label` |
| Charts fail with `Missing ...csv` | Analytics not run or failed | Run `./run.sh`, then `python scripts/make_charts.py` |
| `matplotlib` missing | Python dependency | `pip install matplotlib pandas numpy` |
| First query is slow (30–60 s) | MapReduce local job startup | Normal. Later queries are faster |
| Port 50070/10000/9083 already in use | Another service | Stop it or edit `docker/docker-compose.yml` port mappings |

Useful diagnostics:

```bash
docker compose -f docker/docker-compose.yml ps
docker compose -f docker/docker-compose.yml logs --tail=100 namenode
docker compose -f docker/docker-compose.yml logs --tail=100 hive-metastore
docker compose -f docker/docker-compose.yml logs --tail=100 hive-server
docker exec campus-hive-postgres psql -U hive -d metastore -c '\dt'
```

---

## 8. Reproduce from a clean state

```bash
# 1. Remove everything project-specific
docker compose -f docker/docker-compose.yml down -v
rm -f data/attendance.csv
rm -f results/*.csv results/*.txt results/*.log results/*.err results/*.md
rm -f charts/*.png
rm -f hive/verify_table.sql

# 2. Run
./run.sh

# 3. Confirm
cat results/crosscheck_report.txt
ls results charts
```

The generator uses seed 42, so the dataset and every result are reproducible.

---

## 9. Native Hadoop/Hive mode

Use this only when `hdfs` and `beeline` are on `PATH` and the services are
running (for example on a university cluster or a Linux VM):

```bash
export HADOOP_CONF_DIR=/path/to/hadoop/conf
export HIVE_CONF_DIR=/path/to/hive/conf
MODE=native BEELINE_USER=your_user ./run.sh
```

`run.sh` then uses:

```bash
hdfs dfs -mkdir -p /bda/attendance
hdfs dfs -put -f data/attendance.csv /bda/attendance/
beeline -u "jdbc:hive2://localhost:10000/default" -n "$BEELINE_USER" -f hive/create_table.sql
```

If your cluster uses YARN, remove the `--hiveconf mapreduce.framework.name=local`
arguments from the script so Hive submits jobs to YARN.

---

## 10. Demo sequence (8–10 minutes)

1. **Problem** — attendance is recorded per student/subject/period and is hard
   to analyse at scale with spreadsheets.
2. **Show the CSV** — `head data/attendance.csv`, `wc -l data/attendance.csv`
   (15,360 records).
3. **Show HDFS** — `hdfs dfs -ls /bda/attendance` or the NameNode UI
   <http://localhost:50070/explorer.html#/bda/attendance>.
4. **Show the Hive table** — `SHOW TABLES; DESCRIBE attendance;` and
   `SELECT COUNT(*)`.
5. **Run subject query** — show highest/lowest subjects.
6. **Run low-attendance query** — show 650 groups and the 10 lowest.
7. **Show charts** — weekly trend and department comparison.
8. **Insight** — overall 74.95%; ME lowest department; W42 dip to 63.45%;
   199 students below 75%.
9. **Validation** — show `results/crosscheck_report.txt` (8/8 PASS).
10. **Limitations/future work** — containerised Hadoop/Hive, local MapReduce,
    no real PII; future real-time ingestion and dashboards.

---

## 11. After the demo

```bash
docker compose -f docker/docker-compose.yml stop
```

Do **not** run `down -v` unless you intend to delete the HDFS data.
