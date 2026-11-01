#!/usr/bin/env bash
# End-to-end runner for the Campus Attendance Hive project.
#
# Modes:
#   MODE=docker (default) - starts the bundled HDFS + Hive stack with Docker
#   MODE=native           - uses hadoop/hdfs/beeline already installed on PATH
#
# Usage:
#   ./run.sh
#   MODE=native ./run.sh
#   PYTHON=python ./run.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# Git Bash/MSYS would otherwise rewrite container-side paths such as
# /bda/attendance into Windows paths before they reach docker exec.
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL='*'

MODE="${MODE:-docker}"
COMPOSE_FILE="docker/docker-compose.yml"
BEELINE_USER="${BEELINE_USER:-hive}"
RESULTS="$ROOT/results"
CHARTS="$ROOT/charts"

step() { printf '\n=== %s ===\n' "$*"; }
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

if [[ -z "${PYTHON:-}" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
  elif command -v python >/dev/null 2>&1; then
    PYTHON=python
  else
    fail "Python 3 is required but was not found on PATH."
  fi
fi

mkdir -p "$RESULTS" "$CHARTS" "$ROOT/data"

step "Python environment"
"$PYTHON" --version

step "Phase 3: generate dataset"
"$PYTHON" scripts/generate_dataset.py

step "Phase 3: validate dataset"
"$PYTHON" scripts/validate_dataset.py

QUERY_ORDER=(overall subject_wise student_wise low_attendance department_wise section_wise daily_trend weekly_trend)

if [[ "$MODE" == "docker" ]]; then
  command -v docker >/dev/null 2>&1 || fail "docker not found. Use MODE=native or install Docker."
  docker info >/dev/null 2>&1 || fail "Docker daemon is not running. Start Docker Desktop and retry."

  step "Phase 4: starting HDFS + Hive containers"
  docker compose -f "$COMPOSE_FILE" up -d

  step "Waiting for HDFS NameNode"
  hdfs_ready=0
  for _ in $(seq 1 60); do
    if docker compose -f "$COMPOSE_FILE" exec -T namenode hdfs dfs -ls / >/dev/null 2>&1; then
      hdfs_ready=1
      break
    fi
    sleep 5
  done
  [[ "$hdfs_ready" -eq 1 ]] || fail "HDFS did not become ready. Check: docker compose -f docker/docker-compose.yml logs"

  step "Phase 4: creating /bda/attendance and uploading CSV"
  docker compose -f "$COMPOSE_FILE" exec -T namenode hdfs dfs -mkdir -p /bda/attendance
  docker compose -f "$COMPOSE_FILE" exec -T namenode hdfs dfs -put -f /workspace-data/attendance.csv /bda/attendance/attendance.csv
  docker compose -f "$COMPOSE_FILE" exec -T namenode hdfs dfs -ls /bda/attendance | tee results/hdfs_ls.txt
  docker compose -f "$COMPOSE_FILE" exec -T namenode hdfs dfs -cat /bda/attendance/attendance.csv > results/hdfs_cat.tmp
  head -n 5 results/hdfs_cat.tmp > results/hdfs_sample_rows.txt
  rm -f results/hdfs_cat.tmp

  step "Waiting for HiveServer2"
  hive_ready=0
  for _ in $(seq 1 90); do
    if docker compose -f "$COMPOSE_FILE" exec -T hive-server beeline \
      -u "jdbc:hive2://localhost:10000/default" -n "$BEELINE_USER" \
      --silent=true --verbose=false -e "SHOW DATABASES;" >/dev/null 2>&1; then
      hive_ready=1
      break
    fi
    sleep 5
  done
  [[ "$hive_ready" -eq 1 ]] || fail "HiveServer2 did not become ready. Check: docker compose -f docker/docker-compose.yml logs hive-server"

  step "Phase 5: create database and external table"
  docker compose -f "$COMPOSE_FILE" exec -T hive-server beeline \
    -u "jdbc:hive2://localhost:10000/default" -n "$BEELINE_USER" \
    --silent=true --verbose=false --showHeader=true --outputformat=csv2 \
    -f /workspace/hive/create_table.sql > results/hive_setup_output.txt 2> results/hive_setup_error.txt

  step "Phase 5: verify with SHOW TABLES, DESCRIBE, LIMIT, COUNT"
  {
    echo "SHOW TABLES;"
    echo "DESCRIBE attendance;"
    echo "SELECT * FROM attendance LIMIT 10;"
    echo "SELECT COUNT(*) AS total_records FROM attendance;"
  } > "$ROOT/hive/verify_table.sql"
  docker compose -f "$COMPOSE_FILE" exec -T hive-server beeline \
    -u "jdbc:hive2://localhost:10000/campus_attendance" -n "$BEELINE_USER" \
    --silent=true --verbose=false --showHeader=true --outputformat=csv2 \
    --hiveconf mapreduce.framework.name=local --hiveconf hive.exec.mode.local.auto=true \
    -f /workspace/hive/verify_table.sql > results/table_verification.txt 2> results/table_verification_error.txt

  step "Phase 6: executing HiveQL analytics"
  : > results/hive_execution.log
  for query in "${QUERY_ORDER[@]}"; do
    echo "Running $query ..."
    docker compose -f "$COMPOSE_FILE" exec -T hive-server beeline \
      -u "jdbc:hive2://localhost:10000/campus_attendance" -n "$BEELINE_USER" \
      --silent=true --verbose=false --showHeader=true --outputformat=csv2 \
      --hiveconf mapreduce.framework.name=local --hiveconf hive.exec.mode.local.auto=true \
      -f "/workspace/hive/queries/$query.sql" 2> "results/$query.err" | sed '/^[[:space:]]*$/d' > "results/$query.csv"
    if [[ $(wc -l < "results/$query.csv") -lt 2 ]]; then
      fail "Hive query '$query' produced no data. See results/$query.err"
    fi
    printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$query" >> results/hive_execution.log
    wc -l < "results/$query.csv" | tr -d ' ' | xargs -I{} echo "  $query.csv rows (including header): {}"
  done
else
  command -v hdfs >/dev/null 2>&1 || fail "hdfs not found on PATH for MODE=native."
  command -v beeline >/dev/null 2>&1 || fail "beeline not found on PATH for MODE=native."

  step "Phase 4: HDFS upload (native)"
  hdfs dfs -mkdir -p /bda/attendance
  hdfs dfs -put -f data/attendance.csv /bda/attendance/
  hdfs dfs -ls /bda/attendance | tee results/hdfs_ls.txt
  hdfs dfs -cat /bda/attendance/attendance.csv > results/hdfs_cat.tmp
  head -n 5 results/hdfs_cat.tmp > results/hdfs_sample_rows.txt
  rm -f results/hdfs_cat.tmp

  step "Phase 5: create database and external table (native)"
  beeline -u "jdbc:hive2://localhost:10000/default" -n "$BEELINE_USER" \
    --silent=true --verbose=false --showHeader=true --outputformat=csv2 \
    -f hive/create_table.sql > results/hive_setup_output.txt 2> results/hive_setup_error.txt

  step "Phase 6: executing HiveQL analytics (native)"
  : > results/hive_execution.log
  for query in "${QUERY_ORDER[@]}"; do
    echo "Running $query ..."
    beeline -u "jdbc:hive2://localhost:10000/campus_attendance" -n "$BEELINE_USER" \
      --silent=true --verbose=false --showHeader=true --outputformat=csv2 \
      --hiveconf mapreduce.framework.name=local --hiveconf hive.exec.mode.local.auto=true \
      -f "hive/queries/$query.sql" 2> "results/$query.err" | sed '/^[[:space:]]*$/d' > "results/$query.csv"
    [[ $(wc -l < "results/$query.csv") -ge 2 ]] || fail "Hive query '$query' produced no data. See results/$query.err"
    printf '%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$query" >> results/hive_execution.log
  done
fi

step "Phase 8: independent Python cross-check"
"$PYTHON" scripts/crosscheck_results.py --require-hive | tee results/crosscheck_stdout.txt

step "Phase 7: charts from Hive results"
"$PYTHON" scripts/make_charts.py

step "Phase 8: summarize actual results for the report"
"$PYTHON" scripts/summarize_results.py > results/key_findings_console.txt
echo "Wrote results/key_findings.md"

step "Summary"
"$PYTHON" - <<'PY'
import csv
from pathlib import Path

root = Path.cwd()
with (root / "results" / "overall.csv").open(newline="", encoding="utf-8") as handle:
    row = next(csv.DictReader(handle))
print(f"Total records : {int(row['total_records']):,}")
print(f"Present       : {int(row['present_records']):,}")
print(f"Attendance    : {row['attendance_pct']}%")

low_path = root / "results" / "low_attendance.csv"
with low_path.open(newline="", encoding="utf-8") as handle:
    low_rows = list(csv.DictReader(handle))
print(f"Low-attendance student-subject groups (<75%): {len(low_rows):,}")
print(f"Results       : {root / 'results'}")
print(f"Charts        : {root / 'charts'}")
PY

printf '\nRun complete.\n'
