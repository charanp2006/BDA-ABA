# Screenshot / Evidence Checklist

Two **real** UI screenshots were captured with headless Chrome from the running
HDFS NameNode. The remaining captures are terminal/Hive views that require the
interactive session; exact commands and expected content are listed below.

## Captured automatically (DONE)

| # | File | Source | Expected content |
|---|---|---|---|
| 01 | `screenshots/01_hdfs_namenode_overview.png` | <http://localhost:50070/dfshealth.html#tab-overview> | Live HDFS NameNode overview page |
| 02 | `screenshots/02_hdfs_bda_attendance.png` | <http://localhost:50070/explorer.html#/bda/attendance> | HDFS browse view showing `/bda/attendance/attendance.csv` |

Capture command used:

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" \
  --headless=new --disable-gpu --hide-scrollbars \
  --virtual-time-budget=6000 --window-size=1440,1000 \
  --screenshot="C:/Charan/ABA/BDA-ABA/campus-attendance-hive/screenshots/02_hdfs_bda_attendance.png" \
  "http://localhost:50070/explorer.html#/bda/attendance"
```

## Still required (terminal / Beeline)

Take these after `./run.sh` (or with the stack running). Redact nothing; the data
is synthetic.

| # | File to save as | Command | What must be visible |
|---|---|---|---|
| 03 | `screenshots/03_project_and_csv.png` | `pwd; ls -R data hive scripts; head data/attendance.csv; wc -l data/attendance.csv` | Project tree, CSV header, **15360 data/attendance.csv** |
| 04 | `screenshots/04_docker_stack.png` | `docker compose -f docker/docker-compose.yml ps` | 5 containers Up: namenode, datanode, hive-metastore, hive-postgres, hive-server |
| 05 | `screenshots/05_hdfs_upload.png` | see RUNBOOK §5: `hdfs dfs -mkdir -p`, `hdfs dfs -put -f`, `hdfs dfs -ls /bda/attendance` | `Found 1 items`, `999647 ... /bda/attendance/attendance.csv` |
| 06 | `screenshots/06_hive_create_table.png` | Beeline `-f /workspace/hive/create_table.sql` | `CREATE DATABASE`, `CREATE EXTERNAL TABLE` completing without error |
| 07 | `screenshots/07_hive_count.png` | Beeline `SELECT COUNT(*) FROM attendance;` | `15360` |
| 08 | `screenshots/08_subject_wise.png` | Beeline `-f /workspace/hive/queries/subject_wise.sql` | 80 subject rows; highest IS302/IS503 (83.85), lowest IS601/ME403 (67.19) |
| 09 | `screenshots/09_low_attendance.png` | Beeline `-f /workspace/hive/queries/low_attendance.sql` | 650 rows starting with 12.50% groups |
| 10 | `screenshots/10_weekly_trend.png` | Beeline `-f /workspace/hive/queries/weekly_trend.sql` | 2025-W36 ... 2025-W48 with W42 = 63.45 |
| 11 | `screenshots/11_validation.png` | `cat results/crosscheck_report.txt` | 8 `[PASS]` lines and `RESULT: PASS` |
| 12 | `screenshots/12_charts.png` | Open `charts/` in File Explorer (or the slide deck) | All 7 chart PNGs |
| 13 | `screenshots/13_results_folder.png` | `ls -lh results charts` | Result CSVs, validation reports, chart files |

## How to open Beeline interactively

```bash
export MSYS_NO_PATHCONV=1
docker compose -f docker/docker-compose.yml exec hive-server beeline \
  -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive
```

Then run the SQL shown above. Use `!q` to exit.

## Rules

- Capture the actual terminal, not reconstructed output.
- Keep the prompt visible where practical.
- Do not edit the PNG files afterwards.
- If a command fails, fix the environment and recapture; do not keep a failed
  screenshot as successful evidence.
